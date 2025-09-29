import 'package:flutter/material.dart';

class SmartSphereLogo extends StatelessWidget {
  final double size;
  final Color color;

  const SmartSphereLogo({Key? key, this.size = 32.0, this.color = Colors.white})
    : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      child: Stack(
        children: [
          // Outer sphere ring
          Container(
            width: size,
            height: size,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(color: color, width: 2.5),
            ),
          ),
          // Inner sphere with gradient
          Center(
            child: Container(
              width: size * 0.6,
              height: size * 0.6,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: [color, color.withOpacity(0.6)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
            ),
          ),
          // Smart connection lines
          Positioned(
            top: size * 0.15,
            left: size * 0.5,
            child: Container(width: 2, height: size * 0.2, color: color),
          ),
          Positioned(
            top: size * 0.65,
            left: size * 0.5,
            child: Container(width: 2, height: size * 0.2, color: color),
          ),
          Positioned(
            top: size * 0.5,
            left: size * 0.15,
            child: Container(width: size * 0.2, height: 2, color: color),
          ),
          Positioned(
            top: size * 0.5,
            left: size * 0.65,
            child: Container(width: size * 0.2, height: 2, color: color),
          ),
        ],
      ),
    );
  }
}
