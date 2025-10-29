from datetime import datetime
from typing import List, Dict
import random

class SecurityMonitor:
    """Security monitoring and alert management system"""
    
    def __init__(self):
        self.alerts = []
        self.security_status = "ARMED"
        self.last_check = datetime.now()
    
    def check_security(self) -> Dict:
        """Perform security checks and return current status"""
        events = []
        
        # Simulate various security events for demo
        current_hour = datetime.now().hour
        
        # Door sensor simulation
        if random.random() > 0.92:
            events.append({
                "type": "DOOR",
                "status": "OPENED" if random.random() > 0.5 else "CLOSED",
                "location": random.choice(["Main Door", "Back Door", "Garage Door"]),
                "timestamp": datetime.now().isoformat(),
                "severity": "INFO"
            })
        
        # Motion detection simulation
        if random.random() > 0.88:
            events.append({
                "type": "MOTION",
                "status": "DETECTED",
                "location": random.choice(["Living Room", "Kitchen", "Bedroom", "Hallway"]),
                "timestamp": datetime.now().isoformat(),
                "severity": "INFO"
            })
        
        # Window sensor simulation
        if random.random() > 0.95:
            events.append({
                "type": "WINDOW",
                "status": "OPENED",
                "location": random.choice(["Living Room Window", "Bedroom Window", "Kitchen Window"]),
                "timestamp": datetime.now().isoformat(),
                "severity": "WARNING"
            })
        
        # Suspicious activity during night hours
        if 22 <= current_hour or current_hour <= 6:
            if random.random() > 0.96:
                events.append({
                    "type": "SUSPICIOUS",
                    "status": "DETECTED",
                    "location": "Backyard",
                    "timestamp": datetime.now().isoformat(),
                    "severity": "CRITICAL"
                })
        
        # Add events to alerts if they are warnings or critical
        for event in events:
            if event['severity'] in ['WARNING', 'CRITICAL']:
                self.add_alert(event)
        
        self.last_check = datetime.now()
        
        return {
            "security_status": self.security_status,
            "recent_events": events,
            "cameras_active": 2,
            "sensors_active": 5,
            "doors_locked": 3,
            "windows_closed": 6,
            "alarm_status": "READY" if self.security_status == "ARMED" else "STANDBY",
            "last_check": self.last_check.isoformat()
        }
    
    def get_alerts(self) -> List[Dict]:
        """Get all security alerts"""
        return self.alerts
    
    def add_alert(self, alert: Dict):
        """Add a security alert"""
        alert['id'] = len(self.alerts) + 1
        alert['timestamp'] = datetime.now().isoformat()
        alert['acknowledged'] = False
        self.alerts.insert(0, alert)  # Add to beginning
        
        # Keep only last 50 alerts
        if len(self.alerts) > 50:
            self.alerts = self.alerts[:50]
    
    def acknowledge_alert(self, alert_id: int):
        """Acknowledge a security alert"""
        for alert in self.alerts:
            if alert.get('id') == alert_id:
                alert['acknowledged'] = True
                return True
        return False
    
    def clear_alerts(self):
        """Clear all acknowledged alerts"""
        self.alerts = [alert for alert in self.alerts if not alert.get('acknowledged', False)]
    
    def set_security_mode(self, mode: str):
        """Set security system mode (ARMED, DISARMED, STAY, AWAY)"""
        valid_modes = ["ARMED", "DISARMED", "STAY", "AWAY"]
        if mode.upper() in valid_modes:
            self.security_status = mode.upper()
            self.add_alert({
                "type": "SYSTEM",
                "status": f"Security mode changed to {mode.upper()}",
                "location": "System",
                "severity": "INFO"
            })
            return True
        return False
    
    def get_security_stats(self) -> Dict:
        """Get security system statistics"""
        total_alerts = len(self.alerts)
        critical_alerts = len([a for a in self.alerts if a.get('severity') == 'CRITICAL'])
        warning_alerts = len([a for a in self.alerts if a.get('severity') == 'WARNING'])
        
        return {
            "total_alerts": total_alerts,
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
            "info_alerts": total_alerts - critical_alerts - warning_alerts,
            "acknowledged_alerts": len([a for a in self.alerts if a.get('acknowledged', False)]),
            "uptime": "99.8%",
            "last_incident": self.alerts[0]['timestamp'] if self.alerts else None
        }
    
    def get_camera_feeds(self) -> List[Dict]:
        """Get simulated camera feed information"""
        return [
            {
                "id": 1,
                "name": "Front Door Camera",
                "status": "ONLINE",
                "resolution": "1080p",
                "recording": True,
                "motion_detection": True,
                "last_motion": "2 minutes ago"
            },
            {
                "id": 2,
                "name": "Backyard Camera",
                "status": "ONLINE",
                "resolution": "1080p",
                "recording": True,
                "motion_detection": True,
                "last_motion": "15 minutes ago"
            }
        ]
    
    def get_sensor_status(self) -> List[Dict]:
        """Get status of all sensors"""
        return [
            {"name": "Main Door Sensor", "type": "DOOR", "status": "CLOSED", "battery": "95%"},
            {"name": "Back Door Sensor", "type": "DOOR", "status": "CLOSED", "battery": "88%"},
            {"name": "Garage Door Sensor", "type": "DOOR", "status": "CLOSED", "battery": "92%"},
            {"name": "Living Room Motion", "type": "MOTION", "status": "IDLE", "battery": "78%"},
            {"name": "Hallway Motion", "type": "MOTION", "status": "IDLE", "battery": "85%"}
        ]