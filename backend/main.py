from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import asyncio

from database import Database
from mqtt_client import MQTTClient

# Initialize FastAPI app
app = FastAPI(title="Smart Home API")

# Initialize database and MQTT client
db = Database()
mqtt_client = None

class DeviceControl(BaseModel):
    device: str
    action: str

@app.on_event("startup")
async def startup_event():
    # Initialize database
    await db.init_db()
    
    # Initialize MQTT client
    global mqtt_client
    mqtt_client = MQTTClient(callback=handle_mqtt_message)
    mqtt_client.start()
    
    # Start energy data simulation
    asyncio.create_task(mqtt_client.simulate_energy_data(db.log_energy_usage))

@app.on_event("shutdown")
def shutdown_event():
    if mqtt_client:
        mqtt_client.stop()

async def handle_mqtt_message(topic: str, payload: Dict):
    device = topic.split('/')[-1]  # Extract device name from topic
    if 'state' in payload:
        await db.update_device_state(device, payload['state'])
        print(f"{device.capitalize()} turned {payload['state']}")

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
    
    # Publish to MQTT
    mqtt_client.publish_device_state(control.device, state)
    
    return {"status": "success", "message": f"{control.device} set to {state}"}

@app.get("/device/status")
async def get_device_status():
    return await db.get_device_states()

@app.get("/energy")
async def get_energy_data():
    return await db.get_latest_energy_logs(10)

@app.get("/predict")
async def get_prediction():
    # Simulated AI prediction (hardcoded)
    predictions = {
        "fan": "Fan is usually ON at 7 PM on warm days",
        "light": "Light usage peaks between 6 PM and 10 PM",
        "energy": "Expected peak usage in 2 hours based on historical patterns"
    }
    return predictions