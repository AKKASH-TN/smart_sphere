import paho.mqtt.client as mqtt
import json
import random
import asyncio
from datetime import datetime
from typing import Callable

class MQTTClient:
    def __init__(self, broker="localhost", port=1883, callback: Callable = None):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.callback = callback
        
        # Set up MQTT callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        # Subscribe to device topics
        self.client.subscribe("home/fan")
        self.client.subscribe("home/light")

    def _on_message(self, client, userdata, msg):
        if self.callback:
            # Parse message and call the callback
            try:
                payload = json.loads(msg.payload.decode())
                asyncio.create_task(self.callback(msg.topic, payload))
            except json.JSONDecodeError:
                print(f"Invalid JSON payload received on topic {msg.topic}")

    def start(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            print(f"[MQTT] Connected to broker at {self.broker}:{self.port}")
        except Exception as e:
            print(f"[MQTT] Warning: Could not connect to MQTT broker at {self.broker}:{self.port}")
            print(f"[MQTT] Running in simulation mode without MQTT broker")
            print(f"[MQTT] Error: {e}")

    def stop(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except:
            pass

    def publish_device_state(self, device: str, state: str):
        try:
            topic = f"home/{device}"
            payload = json.dumps({"state": state})
            self.client.publish(topic, payload)
            print(f"[MQTT] Published: {topic} -> {state}")
        except Exception as e:
            print(f"[MQTT] Could not publish (broker not connected): {e}")

    async def simulate_energy_data(self, energy_callback: Callable):
        """Simulates periodic energy usage data"""
        while True:
            # Generate random energy usage between 100W and 500W
            watts = random.uniform(100, 500)
            
            # Publish to MQTT
            try:
                self.client.publish(
                    "home/energy",
                    json.dumps({
                        "timestamp": datetime.now().isoformat(),
                        "watts": watts
                    })
                )
            except Exception as e:
                # Silently continue if MQTT is not connected
                pass
            
            # Call the callback to log the data
            if energy_callback:
                await energy_callback(watts)
            
            await asyncio.sleep(5)  # Wait 5 seconds before next update