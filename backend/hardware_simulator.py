import asyncio
import random
from typing import Dict, Callable
from datetime import datetime

class HardwareSimulator:
    """
    Simulates real IoT hardware devices (LED, Fan, Sensors)
    This replaces the need for Raspberry Pi GPIO during development/demo
    """
    
    def __init__(self):
        # Start with devices OFF - they'll be controlled by UI
        self.devices = {
            'light': {'state': 'OFF', 'power_watts': 0.0, 'gpio_pin': 17},
            'fan': {'state': 'OFF', 'power_watts': 0.0, 'gpio_pin': 27}
        }
        
        self.sensors = {
            'temperature': 25.0,  # Celsius
            'humidity': 60.0,     # Percentage
            'motion': False,
            'door': 'CLOSED'
        }
        
        self.running = False
        print("[HARDWARE SIM] Initialized - all devices OFF, waiting for UI commands")
        
    def control_device(self, device: str, action: str) -> Dict:
        """Simulate GPIO control of device"""
        if device not in self.devices:
            return {'error': f'Device {device} not found'}
        
        action = action.upper()
        self.devices[device]['state'] = action
        
        # Simulate power consumption
        if action == 'ON':
            if device == 'light':
                self.devices[device]['power_watts'] = random.uniform(10, 15)  # LED bulb
            elif device == 'fan':
                self.devices[device]['power_watts'] = random.uniform(50, 75)  # Ceiling fan
        else:
            self.devices[device]['power_watts'] = 0
        
        print(f"[HARDWARE SIM] {device.upper()} GPIO Pin {self.devices[device]['gpio_pin']}: {action}")
        print(f"[HARDWARE SIM] Power consumption: {self.devices[device]['power_watts']:.2f}W")
        
        return {
            'device': device,
            'state': action,
            'power_watts': self.devices[device]['power_watts'],
            'gpio_pin': self.devices[device]['gpio_pin'],
            'timestamp': datetime.now().isoformat()
        }
    
    def get_device_state(self, device: str) -> Dict:
        """Get current device state"""
        if device not in self.devices:
            return {'error': f'Device {device} not found'}
        
        return {
            'device': device,
            'state': self.devices[device]['state'],
            'power_watts': self.devices[device]['power_watts'],
            'gpio_pin': self.devices[device]['gpio_pin']
        }
    
    def get_all_devices(self) -> Dict:
        """Get all device states"""
        return {
            device: {
                'state': info['state'],
                'power_watts': info['power_watts'],
                'gpio_pin': info['gpio_pin']
            }
            for device, info in self.devices.items()
        }
    
    async def simulate_sensors(self, callback: Callable = None):
        """Simulate sensor readings (temperature, humidity, motion)"""
        self.running = True
        print("[HARDWARE SIM] Sensor simulation started")
        
        while self.running:
            # Simulate temperature fluctuation
            self.sensors['temperature'] += random.uniform(-0.5, 0.5)
            self.sensors['temperature'] = max(20, min(35, self.sensors['temperature']))
            
            # Simulate humidity fluctuation
            self.sensors['humidity'] += random.uniform(-2, 2)
            self.sensors['humidity'] = max(40, min(80, self.sensors['humidity']))
            
            # Random motion detection (5% chance)
            self.sensors['motion'] = random.random() < 0.05
            
            # Random door state change (2% chance)
            if random.random() < 0.02:
                self.sensors['door'] = 'OPENED' if self.sensors['door'] == 'CLOSED' else 'CLOSED'
            
            sensor_data = {
                'temperature': round(self.sensors['temperature'], 1),
                'humidity': round(self.sensors['humidity'], 1),
                'motion': self.sensors['motion'],
                'door': self.sensors['door'],
                'timestamp': datetime.now().isoformat()
            }
            
            if self.sensors['motion']:
                print(f"[SENSOR SIM] 🚨 Motion detected!")
            
            if self.sensors['door'] == 'OPENED':
                print(f"[SENSOR SIM] 🚪 Door opened!")
            
            if callback:
                await callback(sensor_data)
            
            await asyncio.sleep(5)  # Update every 5 seconds
    
    def get_sensor_data(self) -> Dict:
        """Get current sensor readings"""
        return {
            'temperature': round(self.sensors['temperature'], 1),
            'humidity': round(self.sensors['humidity'], 1),
            'motion': self.sensors['motion'],
            'door': self.sensors['door'],
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_total_power(self) -> float:
        """Calculate total power consumption of all devices"""
        return sum(device['power_watts'] for device in self.devices.values())
    
    def stop(self):
        """Stop sensor simulation"""
        self.running = False
        print("[HARDWARE SIM] Stopped")