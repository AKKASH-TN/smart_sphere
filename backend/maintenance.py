from datetime import datetime, timedelta
from typing import List, Dict
import random

class MaintenanceMonitor:
    """Proactive maintenance monitoring and alert system"""
    
    def __init__(self):
        # Simulated device usage data
        self.device_usage = {
            "fan": {
                "total_hours": random.randint(650, 750),
                "last_maintenance": "2024-08-15",
                "maintenance_interval": 720,  # hours
                "filter_life": 85,  # percentage
                "motor_health": 92,
                "noise_level": "Normal",
                "vibration": "Low"
            },
            "light": {
                "total_hours": random.randint(800, 900),
                "last_maintenance": "2024-09-01",
                "maintenance_interval": 1000,  # hours
                "bulb_life": 78,  # percentage
                "brightness_degradation": 5,
                "flicker_count": 0
            },
            "ac": {
                "total_hours": random.randint(400, 500),
                "last_maintenance": "2024-07-20",
                "maintenance_interval": 500,  # hours
                "filter_life": 45,
                "coolant_level": 88,
                "compressor_health": 95,
                "noise_level": "Normal"
            },
            "water_heater": {
                "total_hours": random.randint(300, 400),
                "last_maintenance": "2024-06-10",
                "maintenance_interval": 720,
                "element_health": 70,
                "tank_condition": "Good",
                "temperature_consistency": 95
            }
        }
    
    def get_maintenance_alerts(self) -> List[Dict]:
        """Generate proactive maintenance alerts"""
        alerts = []
        
        for device, data in self.device_usage.items():
            # Check if maintenance is due
            hours_until_maintenance = data['maintenance_interval'] - data['total_hours']
            
            if hours_until_maintenance <= 0:
                alerts.append({
                    "device": device.replace("_", " ").title(),
                    "message": f"Maintenance overdue by {abs(hours_until_maintenance)} hours",
                    "priority": "CRITICAL",
                    "type": "OVERDUE",
                    "action_required": "Schedule maintenance immediately",
                    "estimated_cost": f"₹{random.randint(300, 800)}"
                })
            elif hours_until_maintenance <= 50:
                alerts.append({
                    "device": device.replace("_", " ").title(),
                    "message": f"Maintenance due in {hours_until_maintenance} hours of operation",
                    "priority": "HIGH",
                    "type": "DUE_SOON",
                    "action_required": "Schedule maintenance within 7 days",
                    "estimated_cost": f"₹{random.randint(200, 600)}"
                })
            elif hours_until_maintenance <= 100:
                alerts.append({
                    "device": device.replace("_", " ").title(),
                    "message": f"Maintenance recommended in {hours_until_maintenance} hours",
                    "priority": "MEDIUM",
                    "type": "UPCOMING",
                    "action_required": "Plan maintenance in next 2 weeks",
                    "estimated_cost": f"₹{random.randint(150, 500)}"
                })
            
            # Check component-specific alerts
            if device == "fan":
                if data['filter_life'] < 20:
                    alerts.append({
                        "device": "Fan",
                        "message": f"Filter replacement required (life remaining: {data['filter_life']}%)",
                        "priority": "HIGH",
                        "type": "COMPONENT",
                        "action_required": "Replace filter",
                        "estimated_cost": "₹150"
                    })
                elif data['filter_life'] < 50:
                    alerts.append({
                        "device": "Fan",
                        "message": f"Filter cleaning recommended (life: {data['filter_life']}%)",
                        "priority": "MEDIUM",
                        "type": "COMPONENT",
                        "action_required": "Clean filter",
                        "estimated_cost": "₹0 (DIY)"
                    })
            
            elif device == "light":
                if data['bulb_life'] < 20:
                    alerts.append({
                        "device": "Light",
                        "message": f"Bulb replacement needed soon (life: {data['bulb_life']}%)",
                        "priority": "MEDIUM",
                        "type": "COMPONENT",
                        "action_required": "Replace bulb",
                        "estimated_cost": "₹200"
                    })
            
            elif device == "ac":
                if data['filter_life'] < 30:
                    alerts.append({
                        "device": "AC",
                        "message": f"AC filter critically dirty (life: {data['filter_life']}%)",
                        "priority": "HIGH",
                        "type": "COMPONENT",
                        "action_required": "Clean/replace AC filter immediately",
                        "estimated_cost": "₹300"
                    })
        
        # Sort by priority
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        alerts.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return alerts
    
    def get_device_health(self, device: str) -> Dict:
        """Get detailed health information for a specific device"""
        if device not in self.device_usage:
            return {"error": "Device not found"}
        
        data = self.device_usage[device]
        hours_until_maintenance = data['maintenance_interval'] - data['total_hours']
        
        # Calculate overall health score
        health_factors = []
        if 'filter_life' in data:
            health_factors.append(data['filter_life'])
        if 'motor_health' in data:
            health_factors.append(data['motor_health'])
        if 'bulb_life' in data:
            health_factors.append(data['bulb_life'])
        if 'compressor_health' in data:
            health_factors.append(data['compressor_health'])
        
        overall_health = sum(health_factors) / len(health_factors) if health_factors else 85
        
        return {
            "device": device.replace("_", " ").title(),
            "overall_health": f"{overall_health:.0f}%",
            "status": self._get_health_status(overall_health),
            "total_operating_hours": data['total_hours'],
            "hours_until_maintenance": max(0, hours_until_maintenance),
            "last_maintenance_date": data['last_maintenance'],
            "next_maintenance_date": self._calculate_next_maintenance(data),
            "components": self._get_component_status(device, data),
            "recommendations": self._get_recommendations(device, data)
        }
    
    def _get_health_status(self, health: float) -> str:
        """Determine health status based on score"""
        if health >= 90:
            return "EXCELLENT"
        elif health >= 75:
            return "GOOD"
        elif health >= 60:
            return "FAIR"
        elif health >= 40:
            return "POOR"
        return "CRITICAL"
    
    def _calculate_next_maintenance(self, data: Dict) -> str:
        """Calculate estimated next maintenance date"""
        last_maintenance = datetime.strptime(data['last_maintenance'], "%Y-%m-%d")
        # Assume 8 hours usage per day
        days_until = (data['maintenance_interval'] - data['total_hours']) / 8
        next_date = datetime.now() + timedelta(days=max(0, days_until))
        return next_date.strftime("%Y-%m-%d")
    
    def _get_component_status(self, device: str, data: Dict) -> List[Dict]:
        """Get status of individual components"""
        components = []
        
        if device == "fan":
            components = [
                {"name": "Filter", "health": f"{data['filter_life']}%", "status": "OK" if data['filter_life'] > 50 else "REPLACE"},
                {"name": "Motor", "health": f"{data['motor_health']}%", "status": "EXCELLENT"},
                {"name": "Blades", "health": "95%", "status": "GOOD"}
            ]
        elif device == "light":
            components = [
                {"name": "Bulb", "health": f"{data['bulb_life']}%", "status": "OK" if data['bulb_life'] > 30 else "REPLACE"},
                {"name": "Socket", "health": "98%", "status": "EXCELLENT"},
                {"name": "Switch", "health": "92%", "status": "GOOD"}
            ]
        elif device == "ac":
            components = [
                {"name": "Filter", "health": f"{data['filter_life']}%", "status": "REPLACE" if data['filter_life'] < 30 else "CLEAN"},
                {"name": "Compressor", "health": f"{data['compressor_health']}%", "status": "EXCELLENT"},
                {"name": "Coolant", "health": f"{data['coolant_level']}%", "status": "GOOD"}
            ]
        elif device == "water_heater":
            components = [
                {"name": "Heating Element", "health": f"{data['element_health']}%", "status": "GOOD"},
                {"name": "Tank", "health": "88%", "status": data['tank_condition'].upper()},
                {"name": "Thermostat", "health": f"{data['temperature_consistency']}%", "status": "EXCELLENT"}
            ]
        
        return components
    
    def _get_recommendations(self, device: str, data: Dict) -> List[str]:
        """Get maintenance recommendations for device"""
        recommendations = []
        
        if device == "fan":
            if data['filter_life'] < 50:
                recommendations.append("Clean or replace filter to improve air quality and efficiency")
            if data['total_hours'] > 600:
                recommendations.append("Lubricate motor bearings to reduce noise and wear")
            recommendations.append("Clean blades to maintain optimal airflow")
        
        elif device == "light":
            if data['bulb_life'] < 30:
                recommendations.append("Consider upgrading to LED bulbs for better energy efficiency")
            if data['brightness_degradation'] > 3:
                recommendations.append("Check electrical connections for voltage consistency")
        
        elif device == "ac":
            if data['filter_life'] < 50:
                recommendations.append("Clean AC filter monthly for optimal cooling and efficiency")
            recommendations.append("Service condenser coils every 6 months")
            recommendations.append("Check coolant levels and refill if necessary")
        
        elif device == "water_heater":
            recommendations.append("Drain and flush tank annually to remove sediment")
            recommendations.append("Check pressure relief valve every 6 months")
            if data['element_health'] < 80:
                recommendations.append("Inspect heating element for scaling and corrosion")
        
        return recommendations
    
    def get_maintenance_history(self, device: str) -> List[Dict]:
        """Get maintenance history for a device"""
        # Simulated maintenance history
        history = [
            {
                "date": "2024-09-15",
                "type": "Routine Maintenance",
                "description": "Filter cleaning and general inspection",
                "cost": "₹200",
                "technician": "Service Team A"
            },
            {
                "date": "2024-06-10",
                "type": "Component Replacement",
                "description": "Replaced worn bearings",
                "cost": "₹500",
                "technician": "Service Team B"
            },
            {
                "date": "2024-03-05",
                "type": "Routine Maintenance",
                "description": "Complete service and lubrication",
                "cost": "₹300",
                "technician": "Service Team A"
            }
        ]
        return history[:3]  # Return last 3 entries
    
    def schedule_maintenance(self, device: str, date: str, notes: str = "") -> Dict:
        """Schedule maintenance for a device"""
        return {
            "status": "success",
            "message": f"Maintenance scheduled for {device.replace('_', ' ').title()}",
            "scheduled_date": date,
            "confirmation_id": f"MNT{random.randint(10000, 99999)}",
            "estimated_duration": "1-2 hours",
            "notes": notes
        }