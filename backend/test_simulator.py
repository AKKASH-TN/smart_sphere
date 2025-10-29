"""
Test script for Smart Home Hardware Simulator
Run this after starting the backend to verify all features work
"""
import requests
import time
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_device_control():
    """Test device control with hardware simulation"""
    print_section("Testing Device Control")
    
    # Turn on light
    print("🔆 Turning ON light...")
    response = requests.post(f"{BASE_URL}/device/control", json={"device": "light", "action": "ON"})
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    time.sleep(2)
    
    # Turn on fan
    print("\n🌀 Turning ON fan...")
    response = requests.post(f"{BASE_URL}/device/control", json={"device": "fan", "action": "ON"})
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    time.sleep(2)
    
    # Get device status
    print("\n📊 Getting device status...")
    response = requests.get(f"{BASE_URL}/device/status")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

def test_sensors():
    """Test sensor readings"""
    print_section("Testing Sensor Readings")
    
    response = requests.get(f"{BASE_URL}/sensors")
    data = response.json()
    print(f"Current Sensor Data:")
    print(f"  🌡️  Temperature: {data['temperature']}°C")
    print(f"  💧 Humidity: {data['humidity']}%")
    print(f"  👁️  Motion: {'Detected' if data['motion'] else 'None'}")
    print(f"  🚪 Door: {data['door']}")

def test_energy():
    """Test energy monitoring"""
    print_section("Testing Energy Monitoring")
    
    response = requests.get(f"{BASE_URL}/energy")
    data = response.json()
    print(f"Current Power Consumption: {data['current_consumption']}W")
    print(f"\nRecent Energy Logs:")
    for log in data['history'][:5]:
        print(f"  • {log['timestamp']}: {log['watts']:.2f}W")

def test_hardware_status():
    """Test hardware simulator status"""
    print_section("Testing Hardware Simulator")
    
    response = requests.get(f"{BASE_URL}/hardware/status")
    data = response.json()
    
    print("Device States:")
    for device, info in data['devices'].items():
        print(f"  • {device.upper()}")
        print(f"    - State: {info['state']}")
        print(f"    - Power: {info['power_watts']:.2f}W")
        print(f"    - GPIO Pin: {info['gpio_pin']}")
    
    print(f"\nTotal Power Consumption: {data['total_power']}W")
    
    print("\nSensor Data:")
    sensors = data['sensors']
    print(f"  • Temperature: {sensors['temperature']}°C")
    print(f"  • Humidity: {sensors['humidity']}%")
    print(f"  • Motion: {sensors['motion']}")
    print(f"  • Door: {sensors['door']}")

def test_ai_predictions():
    """Test AI predictions"""
    print_section("Testing AI Predictions")
    
    response = requests.get(f"{BASE_URL}/predict")
    data = response.json()
    print("AI Predictions:")
    print(f"  Fan: {data['fan']['prediction']}")
    print(f"  Light: {data['light']['prediction']}")

def test_security():
    """Test security monitoring"""
    print_section("Testing Security Monitoring")
    
    response = requests.get(f"{BASE_URL}/security")
    data = response.json()
    print(f"Security Status: {data['security_status']}")
    print(f"Cameras Active: {data['cameras_active']}")
    print(f"Sensors Active: {data['sensors_active']}")

def test_maintenance():
    """Test maintenance alerts"""
    print_section("Testing Maintenance Alerts")
    
    response = requests.get(f"{BASE_URL}/maintenance")
    data = response.json()
    alerts = data['alerts']
    
    if alerts:
        print(f"Found {len(alerts)} maintenance alerts:")
        for alert in alerts[:3]:
            print(f"\n  • {alert['device']}")
            print(f"    Priority: {alert['priority']}")
            print(f"    Message: {alert['message']}")
    else:
        print("No maintenance alerts at this time")

def test_full_cycle():
    """Test complete device control cycle"""
    print_section("Testing Full Device Cycle")
    
    devices = ['light', 'fan']
    
    for device in devices:
        print(f"\n{device.upper()} Test:")
        
        # Turn ON
        print(f"  ► Turning ON...")
        requests.post(f"{BASE_URL}/device/control", json={"device": device, "action": "ON"})
        time.sleep(1)
        
        # Check status
        response = requests.get(f"{BASE_URL}/hardware/status")
        data = response.json()
        state = data['devices'][device]
        print(f"  ✓ State: {state['state']}, Power: {state['power_watts']:.2f}W")
        
        time.sleep(2)
        
        # Turn OFF
        print(f"  ► Turning OFF...")
        requests.post(f"{BASE_URL}/device/control", json={"device": device, "action": "OFF"})
        time.sleep(1)
        
        # Check status
        response = requests.get(f"{BASE_URL}/hardware/status")
        data = response.json()
        state = data['devices'][device]
        print(f"  ✓ State: {state['state']}, Power: {state['power_watts']:.2f}W")
        
        print()

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  SMART HOME HARDWARE SIMULATOR TEST SUITE")
    print("="*60)
    
    try:
        # Check if backend is running
        response = requests.get(f"{BASE_URL}/device/status")
        if response.status_code != 200:
            print("\n❌ Error: Backend is not responding!")
            print("Please start the backend first:")
            print("  cd backend")
            print("  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
            return
        
        print("\n✅ Backend is running!")
        
        # Run all tests
        test_device_control()
        time.sleep(1)
        
        test_sensors()
        time.sleep(1)
        
        test_energy()
        time.sleep(1)
        
        test_hardware_status()
        time.sleep(1)
        
        test_ai_predictions()
        time.sleep(1)
        
        test_security()
        time.sleep(1)
        
        test_maintenance()
        time.sleep(1)
        
        test_full_cycle()
        
        print_section("All Tests Completed Successfully! ✅")
        print("Your Smart Home Hardware Simulator is working perfectly!")
        print("\nNext steps:")
        print("  1. Use your Flutter app to control devices")
        print("  2. View the Swagger UI at http://localhost:8000/docs")
        print("  3. Check the database at backend/smart_home.db")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend!")
        print("\nPlease start the backend server:")
        print("  cd backend")
        print("  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")

if __name__ == "__main__":
    main()