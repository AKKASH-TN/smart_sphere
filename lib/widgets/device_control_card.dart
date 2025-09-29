import 'package:flutter/material.dart';
import 'package:flutter_switch/flutter_switch.dart';

class DeviceControlCard extends StatefulWidget {
  final String deviceName;
  final IconData icon;
  final bool status;
  final Function(bool) onToggle;
  final String? subtitle;
  final List<String>? modes;

  const DeviceControlCard({
    super.key,
    required this.deviceName,
    required this.icon,
    required this.status,
    required this.onToggle,
    this.subtitle,
    this.modes,
  });

  @override
  State<DeviceControlCard> createState() => _DeviceControlCardState();
}

class _DeviceControlCardState extends State<DeviceControlCard>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late AnimationController _rotationController;
  late AnimationController _scaleController;
  late AnimationController _glowController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _rotationAnimation;
  late Animation<double> _scaleAnimation;
  late Animation<double> _glowAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );
    _rotationController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    );
    _scaleController = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );
    _glowController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );

    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.1).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );

    _rotationAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _rotationController, curve: Curves.linear),
    );

    _scaleAnimation = Tween<double>(begin: 1.0, end: 0.95).animate(
      CurvedAnimation(parent: _scaleController, curve: Curves.easeInOut),
    );

    _glowAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _glowController, curve: Curves.easeInOut),
    );

    if (widget.status) {
      _pulseController.repeat(reverse: true);
      _glowController.repeat(reverse: true);
      if (widget.deviceName.toLowerCase().contains('fan')) {
        _rotationController.repeat();
      }
    }
  }

  @override
  void didUpdateWidget(DeviceControlCard oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.status != oldWidget.status) {
      if (widget.status) {
        _pulseController.repeat(reverse: true);
        _glowController.repeat(reverse: true);
        if (widget.deviceName.toLowerCase().contains('fan')) {
          _rotationController.repeat();
        }
      } else {
        _pulseController.stop();
        _rotationController.stop();
        _glowController.stop();
      }
    }
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _rotationController.dispose();
    _scaleController.dispose();
    _glowController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) {
        _scaleController.forward();
      },
      onTapUp: (_) {
        _scaleController.reverse();
      },
      onTapCancel: () {
        _scaleController.reverse();
      },
      child: AnimatedBuilder(
        animation: Listenable.merge([_scaleAnimation, _glowAnimation]),
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              curve: Curves.easeInOut,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: widget.status
                    ? const Color(0xFF1A1F2E)
                    : const Color(0xFF12171E),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: widget.status
                      ? Colors.blue
                      : Colors.grey.withOpacity(0.3),
                  width: 2,
                ),
                boxShadow: [
                  if (widget.status)
                    BoxShadow(
                      color: Colors.blue.withOpacity(
                        0.3 + (_glowAnimation.value * 0.2),
                      ),
                      blurRadius: 8 + (_glowAnimation.value * 4),
                      offset: const Offset(0, 4),
                    ),
                  BoxShadow(
                    color: Colors.black.withOpacity(0.2),
                    blurRadius: 4,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Animated Icon
                  AnimatedBuilder(
                    animation: widget.deviceName.toLowerCase().contains('fan')
                        ? _rotationAnimation
                        : _pulseAnimation,
                    builder: (context, child) {
                      return Transform.rotate(
                        angle:
                            widget.deviceName.toLowerCase().contains('fan') &&
                                widget.status
                            ? _rotationAnimation.value * 2 * 3.14159
                            : 0,
                        child: Transform.scale(
                          scale: widget.status ? _pulseAnimation.value : 1.0,
                          child: Container(
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: widget.status
                                  ? Colors.blue.withOpacity(0.2)
                                  : Colors.grey.withOpacity(0.1),
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: widget.status
                                    ? Colors.blue
                                    : Colors.grey,
                                width: 2,
                              ),
                            ),
                            child: Icon(
                              widget.icon,
                              color: widget.status ? Colors.blue : Colors.grey,
                              size: 32,
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 16),

                  // Device Name
                  Text(
                    widget.deviceName,
                    style: TextStyle(
                      color: widget.status ? Colors.white : Colors.grey,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 8),

                  // Subtitle
                  if (widget.subtitle != null)
                    Text(
                      widget.subtitle!,
                      style: TextStyle(
                        color: Colors.grey.withOpacity(0.8),
                        fontSize: 12,
                      ),
                      textAlign: TextAlign.center,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  const SizedBox(height: 16),

                  // Switch
                  FlutterSwitch(
                    width: 50.0,
                    height: 25.0,
                    valueFontSize: 10.0,
                    toggleSize: 18.0,
                    value: widget.status,
                    borderRadius: 15.0,
                    padding: 2.0,
                    showOnOff: false,
                    activeColor: Colors.blue,
                    inactiveColor: Colors.grey,
                    onToggle: widget.onToggle,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
