from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio

from database import Database
from mqtt_client import MQTTClient
from scheduler import DeviceScheduler
from ai_predictor import AIPredictor
from security import SecurityMonitor
from maintenance import MaintenanceMonitor
from hardware_simulator import HardwareSimulator

# Initialize FastAPI app
app = FastAPI(title="Smart Home AI Platform")

# Add CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize all components
db = Database()
mqtt_client = None
scheduler = DeviceScheduler()
ai_predictor = AIPredictor()
security_monitor = SecurityMonitor()
maintenance_monitor = MaintenanceMonitor()
hardware_sim = HardwareSimulator()  # Hardware simulator

class DeviceControl(BaseModel):
    device: str
    action: str

class Schedule(BaseModel):
    device: str
    time: str
    action: str
    enabled: Optional[bool] = True
    days: Optional[List[str]] = None

class SecurityMode(BaseModel):
    mode: str

class MaintenanceSchedule(BaseModel):
    device: str
    date: str
    notes: Optional[str] = ""

@app.on_event("startup")
async def startup_event():
    # Initialize database
    await db.init_db()
    
    # Sync hardware simulator with database state
    device_states = await db.get_device_states()
    for device in device_states:
        hardware_sim.control_device(device['name'], device['state'])
    print("[HARDWARE SIM] Synced with database - devices initialized")
    
    # Initialize MQTT client
    global mqtt_client
    mqtt_client = MQTTClient(callback=handle_mqtt_message)
    mqtt_client.start()
    
    # Start energy data simulation
    asyncio.create_task(simulate_energy_data())
    
    # Start scheduler
    asyncio.create_task(scheduler.check_schedules(execute_scheduled_action))
    
    # Start hardware sensor simulation
    asyncio.create_task(hardware_sim.simulate_sensors(log_sensor_data))
    
    print("[SYSTEM] Smart Home AI Platform started successfully")
    print("[SYSTEM] All services initialized: MQTT, Database, Scheduler, AI, Security, Maintenance, Hardware Simulator")

@app.on_event("shutdown")
def shutdown_event():
    if mqtt_client:
        mqtt_client.stop()
    hardware_sim.stop()
    print("[SYSTEM] Smart Home AI Platform shutdown complete")

async def simulate_energy_data():
    """Simulate energy consumption based on device states"""
    while True:
        # Get total power from hardware simulator
        total_watts = hardware_sim.calculate_total_power()
        
        # Add base consumption (always-on devices like router, modem)
        base_consumption = 20  # 20W
        total_watts += base_consumption
        
        # Log to database
        await db.log_energy_usage(total_watts)
        
        await asyncio.sleep(5)

async def log_sensor_data(sensor_data: dict):
    """Log sensor data to database"""
    await db.log_sensor_data(sensor_data)

async def handle_mqtt_message(topic: str, payload: Dict):
    device = topic.split('/')[-1]  # Extract device name from topic
    if 'state' in payload:
        await db.update_device_state(device, payload['state'])
        # Update hardware simulator
        hardware_sim.control_device(device, payload['state'])
        print(f"[MQTT] {device.capitalize()} turned {payload['state']}")

async def execute_scheduled_action(device: str, action: str):
    """Execute scheduled device action"""
    await db.update_device_state(device, action)
    
    # Control simulated hardware
    hardware_sim.control_device(device, action)
    
    # Publish to MQTT
    mqtt_client.publish_device_state(device, action)
    print(f"[SCHEDULER] Executed: {device} -> {action}")

@app.post("/device/control")
async def control_device(control: DeviceControl):
    valid_devices = ['fan', 'light']
    valid_actions = ['ON', 'OFF']
    
    if control.device not in valid_devices:
        raise HTTPException(status_code=400, detail="Invalid device")
    if control.action.upper() not in valid_actions:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    # Update device state in database
    state = control.action.upper()
    await db.update_device_state(control.device, state)
    
    # Control simulated hardware
    result = hardware_sim.control_device(control.device, state)
    
    # Publish to MQTT
    mqtt_client.publish_device_state(control.device, state)
    
    return {
        "status": "success",
        "message": f"{control.device} set to {state}",
        "hardware_response": result
    }

@app.get("/device/status")
async def get_device_status():
    db_states = await db.get_device_states()
    hardware_states = hardware_sim.get_all_devices()
    
    # Combine database and hardware simulator states
    combined = []
    for device in db_states:
        device['hardware'] = hardware_states.get(device['name'], {})
        combined.append(device)
    
    return combined

@app.get("/energy")
async def get_energy_data():
    logs = await db.get_latest_energy_logs(10)
    total_power = hardware_sim.calculate_total_power()
    
    return {
        "current_consumption": round(total_power, 2),
        "history": logs
    }

@app.get("/predict")
async def get_prediction():
    """AI-powered predictions and recommendations"""
    device_logs = await db.get_latest_energy_logs(50)
    predictions = ai_predictor.analyze_pattern(device_logs)
    return predictions

# ============ NEW ENDPOINTS ============

@app.get("/ai/tips")
async def get_energy_tips():
    """Get AI-powered energy saving tips"""
    return {"tips": ai_predictor.get_energy_saving_tips()}

@app.get("/ai/insights/{device}")
async def get_device_insights(device: str):
    """Get detailed AI insights for specific device"""
    return ai_predictor.get_device_insights(device)

@app.get("/ai/summary")
async def get_weekly_summary():
    """Get weekly energy and usage summary"""
    return ai_predictor.get_weekly_summary()

# Scheduling Endpoints
@app.post("/schedule")
async def add_schedule(schedule: Schedule):
    """Add or update device schedule"""
    result = scheduler.add_schedule(
        schedule.device,
        schedule.time,
        schedule.action,
        schedule.enabled if schedule.enabled is not None else True,
        schedule.days
    )
    return {"status": "success", "schedule": result}

@app.get("/schedule")
async def get_schedules():
    """Get all device schedules"""
    return {"schedules": scheduler.get_schedules()}

@app.get("/schedule/{device}")
async def get_device_schedule(device: str):
    """Get schedule for specific device"""
    schedule = scheduler.get_schedule(device)
    if schedule:
        return {"device": device, "schedule": schedule}
    raise HTTPException(status_code=404, detail="Schedule not found")

@app.delete("/schedule/{device}")
async def remove_schedule(device: str):
    """Remove device schedule"""
    if scheduler.remove_schedule(device):
        return {"status": "success", "message": f"Schedule removed for {device}"}
    raise HTTPException(status_code=404, detail="Schedule not found")

@app.put("/schedule/{device}/toggle")
async def toggle_schedule(device: str, enabled: bool):
    """Enable or disable schedule for device"""
    if scheduler.toggle_schedule(device, enabled):
        return {"status": "success", "enabled": enabled}
    raise HTTPException(status_code=404, detail="Schedule not found")

# Security Endpoints
@app.get("/security")
async def get_security_status():
    """Get current security monitoring status"""
    return security_monitor.check_security()

@app.get("/security/alerts")
async def get_security_alerts():
    """Get all security alerts"""
    return {"alerts": security_monitor.get_alerts()}

@app.get("/security/stats")
async def get_security_stats():
    """Get security system statistics"""
    return security_monitor.get_security_stats()

@app.get("/security/cameras")
async def get_camera_feeds():
    """Get camera feed information"""
    return {"cameras": security_monitor.get_camera_feeds()}

@app.get("/security/sensors")
async def get_sensor_status():
    """Get status of all sensors"""
    return {"sensors": security_monitor.get_sensor_status()}

@app.post("/security/mode")
async def set_security_mode(mode: SecurityMode):
    """Set security system mode (ARMED, DISARMED, STAY, AWAY)"""
    if security_monitor.set_security_mode(mode.mode):
        return {"status": "success", "mode": mode.mode.upper()}
    raise HTTPException(status_code=400, detail="Invalid security mode")

@app.put("/security/alert/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int):
    """Acknowledge a security alert"""
    if security_monitor.acknowledge_alert(alert_id):
        return {"status": "success", "message": "Alert acknowledged"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.delete("/security/alerts")
async def clear_acknowledged_alerts():
    """Clear all acknowledged alerts"""
    security_monitor.clear_alerts()
    return {"status": "success", "message": "Acknowledged alerts cleared"}

# Maintenance Endpoints
@app.get("/maintenance")
async def get_maintenance_alerts():
    """Get all proactive maintenance alerts"""
    alerts = maintenance_monitor.get_maintenance_alerts()
    return {"alerts": alerts}

@app.get("/maintenance/{device}/health")
async def get_device_health(device: str):
    """Get detailed health information for device"""
    return maintenance_monitor.get_device_health(device)

@app.get("/maintenance/{device}/history")
async def get_maintenance_history(device: str):
    """Get maintenance history for device"""
    return {"history": maintenance_monitor.get_maintenance_history(device)}

@app.post("/maintenance/schedule")
async def schedule_maintenance(schedule: MaintenanceSchedule):
    """Schedule maintenance for a device"""
    result = maintenance_monitor.schedule_maintenance(
        schedule.device,
        schedule.date,
        schedule.notes
    )
    return result

# Hardware Simulator & Sensor Endpoints
@app.get("/sensors")
async def get_sensor_data():
    """Get current sensor readings"""
    return hardware_sim.get_sensor_data()

@app.get("/sensors/history")
async def get_sensor_history(limit: int = 20):
    """Get sensor data history"""
    logs = await db.get_latest_sensor_logs(limit)
    return {"history": logs}

@app.get("/hardware/status")
async def get_hardware_status():
    """Get hardware simulator status"""
    return {
        "devices": hardware_sim.get_all_devices(),
        "sensors": hardware_sim.get_sensor_data(),
        "total_power": round(hardware_sim.calculate_total_power(), 2)
    }