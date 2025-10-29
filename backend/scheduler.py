import asyncio
from datetime import datetime
from typing import Dict, Callable, List

class DeviceScheduler:
    """Manages automated device scheduling"""
    
    def __init__(self):
        # Default schedules for demo
        self.schedules = {
            'fan': {
                'time': '19:00',
                'action': 'ON',
                'enabled': True,
                'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            },
            'light': {
                'time': '18:30',
                'action': 'ON',
                'enabled': True,
                'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            }
        }
    
    async def check_schedules(self, control_callback: Callable):
        """Check and execute schedules every minute"""
        print("[SCHEDULER] Started automatic scheduling service")
        while True:
            try:
                current_time = datetime.now().strftime('%H:%M')
                current_day = datetime.now().strftime('%A').lower()
                
                for device, schedule in self.schedules.items():
                    if (schedule['enabled'] and 
                        schedule['time'] == current_time and
                        current_day in schedule['days']):
                        await control_callback(device, schedule['action'])
                        print(f"[SCHEDULER] Auto {schedule['action']}: {device} at {current_time}")
                
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"[SCHEDULER] Error: {e}")
                await asyncio.sleep(60)
    
    def add_schedule(self, device: str, time: str, action: str, enabled: bool = True, days: List[str] = None):
        """Add or update a device schedule"""
        if days is None:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        self.schedules[device] = {
            'time': time,
            'action': action,
            'enabled': enabled,
            'days': days
        }
        return self.schedules[device]
    
    def remove_schedule(self, device: str):
        """Remove a device schedule"""
        if device in self.schedules:
            del self.schedules[device]
            return True
        return False
    
    def toggle_schedule(self, device: str, enabled: bool):
        """Enable or disable a schedule"""
        if device in self.schedules:
            self.schedules[device]['enabled'] = enabled
            return True
        return False
    
    def get_schedules(self):
        """Get all schedules"""
        return self.schedules
    
    def get_schedule(self, device: str):
        """Get schedule for a specific device"""
        return self.schedules.get(device)