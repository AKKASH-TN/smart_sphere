# Smart Home AI Backend

This backend provides AI-powered smart home automation with MQTT, scheduling, security monitoring, and maintenance alerts.

## Features

✅ **Device Control**: Control smart devices (Fan, Light) via MQTT
✅ **AI Predictions**: Pattern-based usage predictions and energy optimization
✅ **Scheduling**: Automated device scheduling based on time
✅ **Security Monitoring**: Real-time security alerts and camera feeds
✅ **Maintenance Alerts**: Proactive device maintenance recommendations
✅ **Energy Analytics**: Track and analyze energy consumption

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

## Running the Backend

### Option 1: Without MQTT Broker (Recommended for Demo)
The backend works standalone without needing an external MQTT broker for basic testing:

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: With MQTT Broker (Full Features)
1. **Install Mosquitto MQTT Broker**:
   - Windows: Download from https://mosquitto.org/download/
   - Or use `choco install mosquitto`

2. **Start Mosquitto**:
```bash
mosquitto -v
```

3. **Start the backend** (in another terminal):
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Device Control
- `POST /device/control` - Control devices
- `GET /device/status` - Get all device states

### Energy & AI
- `GET /energy` - Get energy consumption data
- `GET /predict` - Get AI predictions
- `GET /ai/tips` - Get energy saving tips
- `GET /ai/insights/{device}` - Get device insights
- `GET /ai/summary` - Get weekly summary

### Scheduling
- `GET /schedule` - Get all schedules
- `POST /schedule` - Add/update schedule
- `GET /schedule/{device}` - Get device schedule
- `DELETE /schedule/{device}` - Remove schedule
- `PUT /schedule/{device}/toggle` - Enable/disable schedule

### Security
- `GET /security` - Get security status
- `GET /security/alerts` - Get security alerts
- `GET /security/stats` - Get security statistics
- `GET /security/cameras` - Get camera feeds
- `GET /security/sensors` - Get sensor status
- `POST /security/mode` - Set security mode
- `PUT /security/alert/{id}/acknowledge` - Acknowledge alert
- `DELETE /security/alerts` - Clear acknowledged alerts

### Maintenance
- `GET /maintenance` - Get maintenance alerts
- `GET /maintenance/{device}/health` - Get device health
- `GET /maintenance/{device}/history` - Get maintenance history
- `POST /maintenance/schedule` - Schedule maintenance

## Testing the API

### Using Browser
Open: http://localhost:8000/docs (Swagger UI)

### Using curl
```bash
# Get device status
curl http://localhost:8000/device/status

# Control a device
curl -X POST http://localhost:8000/device/control \
  -H "Content-Type: application/json" \
  -d '{"device":"fan","action":"ON"}'

# Get AI predictions
curl http://localhost:8000/predict

# Get security status
curl http://localhost:8000/security

# Get maintenance alerts
curl http://localhost:8000/maintenance
```

## Connecting Flutter App

In your Flutter app, update the API base URL to:
```dart
const String apiBaseUrl = "http://localhost:8000";
// or use your computer's IP address for physical device
// const String apiBaseUrl = "http://192.168.x.x:8000";
```

## Database

The backend uses SQLite for local storage:
- **Location**: `backend/smart_home.db`
- **Tables**: 
  - `devices` - Device states
  - `energy_logs` - Energy consumption data

### Viewing the Database

#### Option 1: Using DB Browser (GUI)
1. Download DB Browser for SQLite: https://sqlitebrowser.org/
2. Open `backend/smart_home.db`
3. Browse tables and data

#### Option 2: Using Command Line
```bash
cd backend
sqlite3 smart_home.db

# View tables
.tables

# View devices
SELECT * FROM devices;

# View energy logs
SELECT * FROM energy_logs ORDER BY timestamp DESC LIMIT 10;

# Exit
.exit
```

#### Option 3: Using Python
```python
import sqlite3

conn = sqlite3.connect('smart_home.db')
cursor = conn.cursor()

# Get all devices
cursor.execute('SELECT * FROM devices')
print(cursor.fetchall())

# Get latest energy logs
cursor.execute('SELECT * FROM energy_logs ORDER BY timestamp DESC LIMIT 10')
print(cursor.fetchall())

conn.close()
```

## Troubleshooting

### Port Already in Use
If port 8000 is busy, use a different port:
```bash
uvicorn main:app --reload --port 8001
```

### MQTT Connection Failed
The app will work without MQTT but with limited real-time features. To fix:
1. Install Mosquitto MQTT broker
2. Start it with `mosquitto -v`
3. Restart the backend

### Database Locked
If you get "database is locked" error:
1. Close any database viewer applications
2. Delete `smart_home.db` (it will be recreated)
3. Restart the backend

## Demo Mode

For hackathon demos, the backend simulates:
- Energy consumption (random data every 5 seconds)
- Security events (random alerts)
- Device usage patterns
- Maintenance schedules

All features work without real hardware!

## Architecture

```
┌─────────────┐
│ Flutter App │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐     ┌──────────┐
│  FastAPI    │────▶│  SQLite  │
│  Backend    │     │    DB    │
└──────┬──────┘     └──────────┘
       │
       ▼
┌─────────────┐
│    MQTT     │
│   Broker    │
└─────────────┘
```

## Next Steps

1. ✅ Start the backend
2. ✅ Test API endpoints using Swagger UI
3. ✅ Connect Flutter app
4. ✅ Demo all features

## Support

For hackathon support:
- Check logs in terminal
- Use Swagger UI for API testing: http://localhost:8000/docs
- View database using DB Browser
- All features work in simulation mode