from datetime import datetime
from typing import Dict, List
import random

class AIPredictor:
    """AI-powered predictions and recommendations for smart home automation"""
    
    def __init__(self):
        self.usage_patterns = {}
        self.learning_data = []
    
    def analyze_pattern(self, device_logs: List[Dict]) -> Dict:
        """Analyze usage patterns and provide AI-driven recommendations"""
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime('%A')
        
        # Simulated AI pattern analysis based on time and usage
        predictions = {
            "fan": {
                "prediction": self._predict_fan(current_hour),
                "confidence": self._calculate_confidence(current_hour, 19, 3),
                "next_action": self._predict_next_action("fan", current_hour),
                "estimated_time": self._estimate_next_usage("fan", current_hour)
            },
            "light": {
                "prediction": self._predict_light(current_hour),
                "confidence": self._calculate_confidence(current_hour, 18, 2),
                "next_action": self._predict_next_action("light", current_hour),
                "estimated_time": self._estimate_next_usage("light", current_hour)
            },
            "energy": {
                "prediction": self._predict_energy(current_hour),
                "peak_hours": "7:00 PM - 10:00 PM",
                "optimization": self._get_energy_optimization(current_hour),
                "savings_potential": f"{random.randint(15, 35)}%"
            },
            "summary": {
                "day": current_day,
                "time": datetime.now().strftime('%I:%M %p'),
                "overall_efficiency": f"{random.randint(70, 95)}%",
                "devices_active": random.randint(1, 3)
            }
        }
        
        return predictions
    
    def _predict_fan(self, hour: int) -> str:
        """Predict fan usage based on time patterns"""
        if 19 <= hour <= 23:
            return "High probability of fan usage detected. Auto-ON recommended at 7 PM to maintain comfort."
        elif 12 <= hour <= 15:
            return "Afternoon peak hours. Fan usage recommended for cooling. Consider auto-scheduling."
        elif 0 <= hour <= 6:
            return "Night hours. Moderate fan speed recommended for sleep comfort."
        return "Fan usage unlikely during morning hours. Auto-OFF recommended to conserve energy."
    
    def _predict_light(self, hour: int) -> str:
        """Predict light usage based on time patterns"""
        if 18 <= hour <= 22:
            return "Evening hours detected. Lights auto-scheduled at 6:30 PM for optimal visibility."
        elif 22 <= hour <= 6:
            return "Night hours. All lights should be OFF except security lights to save energy."
        elif 6 <= hour <= 8:
            return "Morning hours. Minimal lighting needed. Natural light available."
        return "Daylight hours. All lights OFF recommended to maximize energy savings."
    
    def _predict_energy(self, hour: int) -> str:
        """Predict energy consumption patterns"""
        if 19 <= hour <= 22:
            return "Peak usage time (7-10 PM). Expected consumption: 2.5-3.0 kW. Solar battery can offset 40% load."
        elif 12 <= hour <= 15:
            return "Afternoon usage moderate (1.5 kW). Solar panels generating peak power. Battery charging active."
        elif 0 <= hour <= 6:
            return "Night usage low (0.5 kW). Running on battery power. Minimal grid dependency."
        return "Morning usage moderate (1.2 kW). Solar panels starting generation. Grid power active."
    
    def _calculate_confidence(self, current_hour: int, target_hour: int, window: int) -> str:
        """Calculate prediction confidence based on time proximity"""
        diff = abs(current_hour - target_hour)
        if diff <= window:
            return f"{random.randint(85, 98)}%"
        elif diff <= window * 2:
            return f"{random.randint(70, 84)}%"
        return f"{random.randint(50, 69)}%"
    
    def _predict_next_action(self, device: str, hour: int) -> str:
        """Predict the next action for a device"""
        if device == "fan":
            if hour < 19:
                return "ON"
            elif hour >= 23:
                return "OFF"
            return "MAINTAIN"
        elif device == "light":
            if hour < 18:
                return "ON"
            elif hour >= 22:
                return "OFF"
            return "MAINTAIN"
        return "UNKNOWN"
    
    def _estimate_next_usage(self, device: str, hour: int) -> str:
        """Estimate time until next usage"""
        if device == "fan":
            if hour < 19:
                hours_until = 19 - hour
                return f"in {hours_until} hour{'s' if hours_until > 1 else ''}"
            return "currently active period"
        elif device == "light":
            if hour < 18:
                hours_until = 18 - hour
                return f"in {hours_until} hour{'s' if hours_until > 1 else ''}"
            return "currently active period"
        return "unknown"
    
    def _get_energy_optimization(self, hour: int) -> str:
        """Get energy optimization recommendation"""
        if 19 <= hour <= 22:
            return "Use battery power during peak hours. Reduce AC usage by 2°C."
        elif 12 <= hour <= 16:
            return "Solar peak hours. Charge batteries. Run heavy appliances now."
        elif 0 <= hour <= 6:
            return "Off-peak hours. Schedule washing machine, dishwasher for maximum savings."
        return "Standard operations. Monitor consumption patterns."
    
    def get_energy_saving_tips(self) -> List[Dict]:
        """Provide actionable energy saving recommendations"""
        tips = [
            {
                "title": "Smart Lighting",
                "description": "Turn OFF lights when not in room",
                "savings": "15-20%",
                "priority": "HIGH",
                "icon": "💡"
            },
            {
                "title": "Fan vs AC",
                "description": "Use fan instead of AC during mild weather",
                "savings": "60-70%",
                "priority": "HIGH",
                "icon": "🌀"
            },
            {
                "title": "Off-Peak Scheduling",
                "description": "Schedule heavy appliances during off-peak hours (11 PM - 6 AM)",
                "savings": "25-30%",
                "priority": "MEDIUM",
                "icon": "⏰"
            },
            {
                "title": "AC Optimization",
                "description": "Maintain AC temperature at 24-26°C for optimal efficiency",
                "savings": "30-40%",
                "priority": "HIGH",
                "icon": "❄️"
            },
            {
                "title": "Solar Utilization",
                "description": "Run appliances during solar peak hours (12 PM - 3 PM)",
                "savings": "50-60%",
                "priority": "MEDIUM",
                "icon": "☀️"
            },
            {
                "title": "Standby Power",
                "description": "Unplug devices when not in use to eliminate phantom power",
                "savings": "5-10%",
                "priority": "LOW",
                "icon": "🔌"
            }
        ]
        return tips
    
    def get_device_insights(self, device: str) -> Dict:
        """Get detailed insights for a specific device"""
        insights = {
            "fan": {
                "avg_daily_usage": "6.5 hours",
                "peak_usage_time": "7:00 PM - 11:00 PM",
                "energy_consumption": "0.45 kWh/day",
                "cost_per_month": "₹135",
                "optimization_potential": "20%",
                "recommendation": "Schedule auto-OFF at 11 PM to save energy"
            },
            "light": {
                "avg_daily_usage": "4.2 hours",
                "peak_usage_time": "6:30 PM - 10:30 PM",
                "energy_consumption": "0.28 kWh/day",
                "cost_per_month": "₹84",
                "optimization_potential": "15%",
                "recommendation": "Use motion sensors to auto-OFF when room is empty"
            }
        }
        return insights.get(device, {})
    
    def get_weekly_summary(self) -> Dict:
        """Get weekly energy and usage summary"""
        return {
            "total_energy_used": f"{random.uniform(45, 65):.1f} kWh",
            "avg_daily_usage": f"{random.uniform(6, 9):.1f} kWh",
            "cost_this_week": f"₹{random.randint(180, 280)}",
            "savings_vs_last_week": f"{random.randint(5, 25)}%",
            "carbon_footprint": f"{random.uniform(15, 25):.1f} kg CO2",
            "solar_contribution": f"{random.randint(35, 55)}%",
            "peak_usage_day": random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
            "most_used_device": random.choice(["Fan", "Light", "AC"])
        }