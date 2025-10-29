import 'dart:convert';
import 'package:http/http.dart' as http;

class SmartHomeApiService {
  // Update this to your computer's IP address when testing on physical device
  // Find your IP: Run 'ipconfig' in cmd and look for IPv4 Address
  static const String baseUrl = 'http://localhost:8000';

  // Alternative: Use your computer's IP for physical device testing
  // static const String baseUrl = 'http://192.168.x.x:8000';

  // Device Control APIs
  Future<Map<String, dynamic>> controlDevice(
    String device,
    String action,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/device/control'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'device': device, 'action': action}),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to control device: ${response.statusCode}');
      }
    } catch (e) {
      print('Error controlling device: $e');
      rethrow;
    }
  }

  Future<List<dynamic>> getDeviceStatus() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/device/status'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as List;
      } else {
        throw Exception('Failed to get device status');
      }
    } catch (e) {
      print('Error getting device status: $e');
      return [];
    }
  }

  // Energy APIs
  Future<List<dynamic>> getEnergyData() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/energy'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as List;
      } else {
        throw Exception('Failed to get energy data');
      }
    } catch (e) {
      print('Error getting energy data: $e');
      return [];
    }
  }

  // AI Prediction APIs
  Future<Map<String, dynamic>> getAIPredictions() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/predict'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get predictions');
      }
    } catch (e) {
      print('Error getting predictions: $e');
      return {};
    }
  }

  Future<Map<String, dynamic>> getEnergySavingTips() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/ai/tips'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get tips');
      }
    } catch (e) {
      print('Error getting tips: $e');
      return {'tips': []};
    }
  }

  Future<Map<String, dynamic>> getDeviceInsights(String device) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/ai/insights/$device'),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get device insights');
      }
    } catch (e) {
      print('Error getting device insights: $e');
      return {};
    }
  }

  Future<Map<String, dynamic>> getWeeklySummary() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/ai/summary'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get weekly summary');
      }
    } catch (e) {
      print('Error getting weekly summary: $e');
      return {};
    }
  }

  // Scheduling APIs
  Future<Map<String, dynamic>> getSchedules() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/schedule'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get schedules');
      }
    } catch (e) {
      print('Error getting schedules: $e');
      return {'schedules': {}};
    }
  }

  Future<Map<String, dynamic>> addSchedule(
    String device,
    String time,
    String action, {
    bool enabled = true,
    List<String>? days,
  }) async {
    try {
      final body = {
        'device': device,
        'time': time,
        'action': action,
        'enabled': enabled,
      };

      if (days != null) {
        body['days'] = days;
      }

      final response = await http.post(
        Uri.parse('$baseUrl/schedule'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to add schedule');
      }
    } catch (e) {
      print('Error adding schedule: $e');
      rethrow;
    }
  }

  Future<bool> removeSchedule(String device) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/schedule/$device'),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error removing schedule: $e');
      return false;
    }
  }

  Future<bool> toggleSchedule(String device, bool enabled) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/schedule/$device/toggle?enabled=$enabled'),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error toggling schedule: $e');
      return false;
    }
  }

  // Security APIs
  Future<Map<String, dynamic>> getSecurityStatus() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/security'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get security status');
      }
    } catch (e) {
      print('Error getting security status: $e');
      return {};
    }
  }

  Future<Map<String, dynamic>> getSecurityAlerts() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/security/alerts'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get security alerts');
      }
    } catch (e) {
      print('Error getting security alerts: $e');
      return {'alerts': []};
    }
  }

  Future<Map<String, dynamic>> getSecurityStats() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/security/stats'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get security stats');
      }
    } catch (e) {
      print('Error getting security stats: $e');
      return {};
    }
  }

  Future<Map<String, dynamic>> getCameraFeeds() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/security/cameras'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get camera feeds');
      }
    } catch (e) {
      print('Error getting camera feeds: $e');
      return {'cameras': []};
    }
  }

  Future<Map<String, dynamic>> getSensorStatus() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/security/sensors'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get sensor status');
      }
    } catch (e) {
      print('Error getting sensor status: $e');
      return {'sensors': []};
    }
  }

  Future<bool> setSecurityMode(String mode) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/security/mode'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'mode': mode}),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error setting security mode: $e');
      return false;
    }
  }

  Future<bool> acknowledgeAlert(int alertId) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/security/alert/$alertId/acknowledge'),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error acknowledging alert: $e');
      return false;
    }
  }

  Future<bool> clearAcknowledgedAlerts() async {
    try {
      final response = await http.delete(Uri.parse('$baseUrl/security/alerts'));

      return response.statusCode == 200;
    } catch (e) {
      print('Error clearing alerts: $e');
      return false;
    }
  }

  // Maintenance APIs
  Future<Map<String, dynamic>> getMaintenanceAlerts() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/maintenance'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get maintenance alerts');
      }
    } catch (e) {
      print('Error getting maintenance alerts: $e');
      return {'alerts': []};
    }
  }

  Future<Map<String, dynamic>> getDeviceHealth(String device) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/maintenance/$device/health'),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get device health');
      }
    } catch (e) {
      print('Error getting device health: $e');
      return {};
    }
  }

  Future<Map<String, dynamic>> getMaintenanceHistory(String device) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/maintenance/$device/history'),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get maintenance history');
      }
    } catch (e) {
      print('Error getting maintenance history: $e');
      return {'history': []};
    }
  }

  Future<Map<String, dynamic>> scheduleMaintenance(
    String device,
    String date, {
    String notes = '',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/maintenance/schedule'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'device': device, 'date': date, 'notes': notes}),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to schedule maintenance');
      }
    } catch (e) {
      print('Error scheduling maintenance: $e');
      rethrow;
    }
  }

  // Health check
  Future<bool> isBackendRunning() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/device/status'));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  // Sensor & Hardware Simulator APIs
  Future<Map<String, dynamic>> getSensorData() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/sensors'));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get sensor data');
      }
    } catch (e) {
      print('Error getting sensor data: $e');
      return {};
    }
  }

  Future<Map<String, dynamic>> getSensorHistory({int limit = 20}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/sensors/history?limit=$limit'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get sensor history');
      }
    } catch (e) {
      print('Error getting sensor history: $e');
      return {'history': []};
    }
  }

  Future<Map<String, dynamic>> getHardwareStatus() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/hardware/status'));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get hardware status');
      }
    } catch (e) {
      print('Error getting hardware status: $e');
      return {};
    }
  }
}
