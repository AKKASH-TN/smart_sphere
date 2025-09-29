import 'package:flutter/material.dart';
import '../widgets/device_control_card.dart';

class DevicesScreen extends StatefulWidget {
  const DevicesScreen({super.key});

  @override
  State<DevicesScreen> createState() => _DevicesScreenState();
}

class _DevicesScreenState extends State<DevicesScreen>
    with TickerProviderStateMixin {
  Map<String, bool> deviceStates = {
    'Living Room Fan': true,
    'Bedroom Light': false,
    'Kitchen Light': true,
    'Air Conditioner': false,
    'Water Heater': false,
    'Smart TV': true,
    'WiFi Router': true,
    'Security Camera': true,
  };

  Map<String, IconData> deviceIcons = {
    'Living Room Fan': Icons.air,
    'Bedroom Light': Icons.lightbulb_outline,
    'Kitchen Light': Icons.lightbulb,
    'Air Conditioner': Icons.ac_unit,
    'Water Heater': Icons.hot_tub,
    'Smart TV': Icons.tv,
    'WiFi Router': Icons.router,
    'Security Camera': Icons.security,
  };

  Map<String, String> deviceSubtitles = {
    'Living Room Fan': 'Speed: Medium',
    'Bedroom Light': 'Dimmed',
    'Kitchen Light': 'Brightness: 90%',
    'Air Conditioner': 'Set to 24°C',
    'Water Heater': 'Scheduled for 6:00 AM',
    'Smart TV': 'Netflix - Living Room',
    'WiFi Router': '5GHz - 25 devices',
    'Security Camera': 'Recording - Front Door',
  };

  late AnimationController _staggerController;

  @override
  void initState() {
    super.initState();
    _staggerController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );
    _staggerController.forward();
  }

  @override
  void dispose() {
    _staggerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'All Devices',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.add_circle_outline),
            onPressed: _showAddDeviceDialog,
          ),
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildStatusOverview(),
              const SizedBox(height: 24),
              const Text(
                'Connected Devices',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: GridView.builder(
                  padding: const EdgeInsets.only(bottom: 20),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    childAspectRatio: 0.75,
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                  ),
                  itemCount: deviceStates.length,
                  itemBuilder: (context, index) {
                    final deviceName = deviceStates.keys.elementAt(index);
                    final isOn = deviceStates[deviceName]!;

                    return AnimatedBuilder(
                      animation: _staggerController,
                      builder: (context, child) {
                        final delayedValue =
                            (_staggerController.value - (index * 0.1)).clamp(
                              0.0,
                              1.0,
                            );
                        final animationValue = Curves.easeOutBack.transform(
                          delayedValue,
                        );

                        return Transform.scale(
                          scale: animationValue.clamp(0.0, 1.0),
                          child: Opacity(
                            opacity: animationValue.clamp(0.0, 1.0),
                            child: DeviceControlCard(
                              deviceName: deviceName,
                              icon: deviceIcons[deviceName]!,
                              status: isOn,
                              subtitle: isOn
                                  ? deviceSubtitles[deviceName]
                                  : 'Offline',
                              onToggle: (value) {
                                setState(() {
                                  deviceStates[deviceName] = value;
                                });
                              },
                            ),
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatusOverview() {
    int activeDevices = deviceStates.values.where((status) => status).length;
    int totalDevices = deviceStates.length;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF4CAF50), Color(0xFF45A049)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.green.withOpacity(0.3),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.devices, color: Colors.white, size: 28),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '$activeDevices of $totalDevices devices active',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  'System Status: ${activeDevices > 0 ? "Online" : "All devices offline"}',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.9),
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              '${((activeDevices / totalDevices) * 100).round()}%',
              style: const TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showAddDeviceDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: const Color(0xFF1A1F2E),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          title: const Text(
            'Add New Device',
            style: TextStyle(color: Colors.white),
          ),
          content: const Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'Device discovery feature coming soon!',
                style: TextStyle(color: Colors.grey),
              ),
              SizedBox(height: 16),
              Text(
                '• Scan for nearby IoT devices\n• Automatic configuration\n• Voice control setup',
                style: TextStyle(color: Colors.grey, fontSize: 14),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Got it', style: TextStyle(color: Colors.blue)),
            ),
          ],
        );
      },
    );
  }
}
