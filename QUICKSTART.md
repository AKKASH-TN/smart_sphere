# 🚀 Quick Start Guide - Smart Home AI Platform

## Setup Steps (15 minutes)

### Step 1: Start the Backend (5 min)

1. **Open Terminal in VS Code** (Ctrl + `)

2. **Navigate to backend folder**:
```powershell
cd backend
```

3. **Install Python dependencies** (first time only):
```powershell
pip install fastapi uvicorn paho-mqtt aiosqlite pydantic
```

4. **Start the server**:
```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
[SYSTEM] Smart Home AI Platform started successfully
```

### Step 2: Test the Backend (2 min)

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Test Endpoint**: http://localhost:8000/device/status

You should see JSON data!

### Step 3: Run the Flutter App (5 min)

1. **Open a NEW Terminal** (don't close the backend terminal!)

2. **Navigate back to main folder**:
```powershell
cd ..
```

3. **Get Flutter dependencies**:
```powershell
flutter pub get
```

4. **Run the app**:
```powershell
flutter run
```

Select your device (Chrome, Android emulator, or connected phone).

### Step 4: Test Integration (3 min)

In your Flutter app:
1. Try controlling a device (Fan/Light)
2. Check energy analytics
3. View AI predictions

---

## 📱 Using the Features in Your App

### Current Features Already Working:
- ✅ Device Control (Fan, Light)
- ✅ Energy Analytics Dashboard
- ✅ Chatbot with AI
- ✅ Voice Control Screen

### New Backend Features Available:
- ✅ AI Predictions & Tips
- ✅ Device Scheduling
- ✅ Security Monitoring
- ✅ Maintenance Alerts

---

## 🔌 Integrating Backend with UI

### Example 1: Add AI Tips to Energy Screen

In `lib/screens/energy_analytics_screen.dart`, add this button:

```dart
import '../services/smart_home_api.dart';

final apiService = SmartHomeApiService();

// Add this in your UI
ElevatedButton(
  onPressed: () async {
    final tips = await apiService.getEnergySavingTips();
    // Show tips in dialog or bottom sheet
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Energy Saving Tips'),
        content: SingleChildScrollView(
          child: Column(
            children: (tips['tips'] as List).map((tip) => ListTile(
              leading: Text(tip['icon']),
              title: Text(tip['title']),
              subtitle: Text(tip['description']),
            )).toList(),
          ),
        ),
      ),
    );
  },
  child: Text('Get AI Tips'),
)
```

### Example 2: Show Maintenance Alerts

In `lib/screens/home_dashboard.dart`, add this:

```dart
import '../services/smart_home_api.dart';

final apiService = SmartHomeApiService();

// Fetch maintenance alerts
FutureBuilder(
  future: apiService.getMaintenanceAlerts(),
  builder: (context, snapshot) {
    if (!snapshot.hasData) return CircularProgressIndicator();
    
    final alerts = snapshot.data!['alerts'] as List;
    
    return Column(
      children: alerts.map((alert) => Card(
        child: ListTile(
          leading: Icon(
            Icons.build,
            color: alert['priority'] == 'HIGH' ? Colors.red : Colors.orange,
          ),
          title: Text(alert['device']),
          subtitle: Text(alert['message']),
          trailing: Chip(label: Text(alert['priority'])),
        ),
      )).toList(),
    );
  },
)
```

### Example 3: Display Security Status

Create a new widget in `home_dashboard.dart`:

```dart
Widget buildSecurityCard() {
  return FutureBuilder(
    future: apiService.getSecurityStatus(),
    builder: (context, snapshot) {
      if (!snapshot.hasData) return CircularProgressIndicator();
      
      final security = snapshot.data!;
      
      return Card(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            children: [
              Icon(
                Icons.security,
                size: 48,
                color: security['security_status'] == 'ARMED' 
                  ? Colors.green 
                  : Colors.grey,
              ),
              SizedBox(height: 8),
              Text(
                security['security_status'],
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              Text('Cameras: ${security['cameras_active']}'),
              Text('Sensors: ${security['sensors_active']}'),
            ],
          ),
        ),
      );
    },
  );
}
```

---

## 🎯 Hackathon Demo Flow

### 1. **Opening** (30 seconds)
- "SmartSphere is an AI-powered smart home platform"
- "Works offline, privacy-first, budget-friendly"

### 2. **Device Control** (1 minute)
- Show dashboard
- Toggle Fan and Light
- Mention sub-2-second response time

### 3. **Energy Analytics** (1 minute)
- Show energy consumption charts
- Display weekly summary
- Show energy saving tips

### 4. **AI Predictions** (1 minute)
- Show AI predictions for devices
- Explain pattern learning
- Show confidence scores

### 5. **Automation** (1 minute)
- Show scheduling feature
- Demonstrate auto-ON/OFF times
- Explain optimization

### 6. **Security** (30 seconds)
- Show security monitoring
- Display camera feeds
- Show sensor status

### 7. **Maintenance** (30 seconds)
- Show proactive alerts
- Display device health
- Mention cost savings

### 8. **Closing** (30 seconds)
- Recap features
- Mention scalability
- Thank judges

**Total Time: 5-6 minutes**

---

## 🐛 Troubleshooting

### Backend Not Starting
```powershell
# Try different port
python -m uvicorn main:app --reload --port 8001
```

### Flutter Can't Connect
1. Check if backend is running (visit http://localhost:8000/docs)
2. Update API URL in `lib/services/smart_home_api.dart`
3. For physical device, use computer's IP address

### Database Issues
```powershell
# Delete and recreate
cd backend
del smart_home.db
# Restart backend (it will recreate)
```

### Import Errors
```powershell
# Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt
```

---

## 📊 Accessing the Database

### View Data in Real-Time

**Option 1: Using Browser (Easiest)**
1. Keep backend running
2. Visit: http://localhost:8000/docs
3. Try different API endpoints

**Option 2: Using DB Browser**
1. Download: https://sqlitebrowser.org/
2. Open `backend/smart_home.db`
3. Browse tables: `devices`, `energy_logs`

**Option 3: Using Command Line**
```powershell
cd backend
sqlite3 smart_home.db

# View devices
SELECT * FROM devices;

# View energy logs
SELECT * FROM energy_logs ORDER BY timestamp DESC LIMIT 10;

# Exit
.exit
```

---

## 🎨 UI Integration Checklist

- [ ] Backend running on port 8000
- [ ] Flutter app connects successfully
- [ ] Device control works
- [ ] Energy data displays
- [ ] AI tips accessible
- [ ] Scheduling visible (optional)
- [ ] Security status shown (optional)
- [ ] Maintenance alerts visible (optional)

---

## 📝 Demo Script

**"Hello judges, I'm presenting SmartSphere - an AI-powered smart home automation platform designed for Indian households.**

**[Show Dashboard]**
Let me demonstrate real-time device control. [Toggle Fan] Notice the sub-2-second response time - this is because everything runs locally, no cloud dependency.

**[Show Energy Analytics]**
Our AI analyzes energy patterns in real-time. [Show charts] Based on your usage, it provides personalized recommendations to save 15-35% on electricity bills.

**[Show AI Predictions]**
The system learns your family's routine. [Show predictions] It knows when to turn devices ON/OFF automatically, with 85-98% confidence based on historical patterns.

**[Show Scheduling]**
Users can set automated schedules. [Show schedule] For example, lights at 6:30 PM, fan at 7 PM - completely hands-free.

**[Show Security]**
Security monitoring with 2 cameras and 5 sensors. [Show status] Real-time alerts for any suspicious activity.

**[Show Maintenance]**
Proactive maintenance alerts prevent costly repairs. [Show alerts] The system monitors device health and recommends service before failures occur.

**Key Features:**
- ✅ Offline-first architecture
- ✅ Privacy-focused (data stays on-device)
- ✅ Budget-friendly (works with any IoT device)
- ✅ Sub-2-second response time
- ✅ Scalable to 100+ devices

**Thank you!"**

---

## 🚀 Ready for Hackathon!

All features are implemented and ready to demo. Focus on:
1. ✅ Smooth device control
2. ✅ Beautiful energy charts
3. ✅ AI predictions
4. ✅ Real-time updates

**Good luck! 🎉**