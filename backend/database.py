import aiosqlite
import asyncio
from datetime import datetime

# Database initialization and operations
class Database:
    def __init__(self, db_path="smart_home.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Create devices table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    state TEXT NOT NULL
                )
            ''')

            # Create energy logs table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS energy_logs (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME NOT NULL,
                    watts REAL NOT NULL
                )
            ''')

            # Initialize default devices if not exists
            await db.execute('SELECT COUNT(*) FROM devices')
            count = await db.fetchone()
            if count[0] == 0:
                await db.executemany(
                    'INSERT INTO devices (name, state) VALUES (?, ?)',
                    [('fan', 'OFF'), ('light', 'OFF')]
                )
            
            await db.commit()

    async def update_device_state(self, device_name: str, new_state: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE devices SET state = ? WHERE name = ?',
                (new_state, device_name)
            )
            await db.commit()

    async def get_device_states(self):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM devices') as cursor:
                return [dict(row) for row in await cursor.fetchall()]

    async def log_energy_usage(self, watts: float):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT INTO energy_logs (timestamp, watts) VALUES (?, ?)',
                (datetime.now().isoformat(), watts)
            )
            await db.commit()

    async def get_latest_energy_logs(self, limit: int = 10):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                'SELECT * FROM energy_logs ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            ) as cursor:
                return [dict(row) for row in await cursor.fetchall()]