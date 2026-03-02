// dashboard_scanner.dart - Dashboard Principal com Círculo de Saúde

import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:math';
import 'package:flutter/services.dart';

void main() {
  runApp(ScannerApp());
}

class ScannerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Scanner Pro',
      theme: ThemeData.dark().copyWith(
        primaryColor: Colors.blue,
        scaffoldBackgroundColor: Colors.black,
        textTheme: TextTheme(
          bodyText1: TextStyle(fontFamily: 'RobotoMono', color: Colors.white),
          bodyText2: TextStyle(fontFamily: 'RobotoMono', color: Colors.grey),
        ),
      ),
      home: DashboardScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;
  
  List<SystemIcon> systems = [
    SystemIcon(name: 'MOTOR', icon: Icons.engineering, color: Colors.grey),
    SystemIcon(name: 'ABS', icon: Icons.car_repair, color: Colors.grey),
    SystemIcon(name: 'AIRBAG', icon: Icons.airbag, color: Colors.grey),
    SystemIcon(name: 'TRANSMISSÃO', icon: Icons.settings, color: Colors.grey),
    SystemIcon(name: 'SRS', icon: Icons.warning, color: Colors.grey),
    SystemIcon(name: 'BATERIA', icon: Icons.battery_charging_full, color: Colors.grey),
    SystemIcon(name: 'SUSPENSÃO', icon: Icons.miscellaneous_services, color: Colors.grey),
    SystemIcon(name: 'AR COND.', icon: Icons.ac_unit, color: Colors.grey),
  ];

  int ecusDetected = 0;
  int falhasEncontradas = 0;
  bool scanning = false;
  Timer? _scanTimer;
  double scanProgress = 0.0;

  @override
  void initState() {
    super.initState();
    
    _pulseController = AnimationController(
      duration: Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);
    
    _pulseAnimation = Tween<double>(begin: 0.8, end: 1.2).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
    
    startScan();
  }

  void startScan() {
    setState(() {
      scanning = true;
      ecusDetected = 0;
      falhasEncontradas = 0;
    });

    _scanTimer = Timer.periodic(Duration(milliseconds: 300), (timer) {
      setState(() {
        if (ecusDetected < 45) {
          ecusDetected += Random().nextInt(3) + 1;
          if (ecusDetected > 45) ecusDetected = 45;
        }

        // Simula descoberta de falhas
        if (Random().nextDouble() > 0.7 && falhasEncontradas < 12) {
          falhasEncontradas++;
          
          // Atualiza cores dos sistemas baseado em falhas
          int randomIndex = Random().nextInt(systems.length);
          systems[randomIndex] = systems[randomIndex].copyWith(
            color: Random().nextBool() ? Colors.orange : Colors.red,
          );
        }

        // Atualiza progresso
        scanProgress = ecusDetected / 45;
      });

      if (ecusDetected >= 45) {
        timer.cancel();
        setState(() {
          scanning = false;
        });
      }
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _scanTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.black, Color(0xFF001a33)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              _buildHeader(),
              Expanded(
                child: _buildMainDashboard(),
              ),
              _buildFooter(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'SCANNER PRO',
                style: TextStyle(
                  color: Colors.cyan,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2,
                  fontFamily: 'RobotoMono',
                ),
              ),
              Text(
                'SISTEMA DE DIAGNÓSTICO',
                style: TextStyle(
                  color: Colors.grey[600],
                  fontSize: 12,
                  fontFamily: 'RobotoMono',
                ),
              ),
            ],
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              border: Border.all(color: Colors.cyan, width: 1),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: scanning ? Colors.green : Colors.cyan,
                    shape: BoxShape.circle,
                  ),
                ),
                SizedBox(width: 8),
                Text(
                  scanning ? 'SCAN ATIVO' : 'PRONTO',
                  style: TextStyle(
                    color: scanning ? Colors.green : Colors.cyan,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    fontFamily: 'RobotoMono',
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMainDashboard() {
    return LayoutBuilder(
      builder: (context, constraints) {
        double size = min(constraints.maxWidth, constraints.maxHeight) * 0.6;
        
        return Stack(
          alignment: Alignment.center,
          children: [
            // Círculo de saúde central pulsante
            AnimatedBuilder(
              animation: _pulseAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _pulseAnimation.value,
                  child: Container(
                    width: size,
                    height: size,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: RadialGradient(
                        colors: [
                          Colors.cyan.withOpacity(0.3),
                          Colors.cyan.withOpacity(0.1),
                          Colors.transparent,
                        ],
                        stops: [0.2, 0.5, 1.0],
                      ),
                      border: Border.all(
                        color: Colors.cyan.withOpacity(0.5),
                        width: 2,
                      ),
                    ),
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            'SAÚDE',
                            style: TextStyle(
                              color: Colors.cyan,
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                              fontFamily: 'RobotoMono',
                            ),
                          ),
                          Text(
                            '${((1 - (falhasEncontradas / 45)) * 100).toInt()}%',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 28,
                              fontWeight: FontWeight.bold,
                              fontFamily: 'RobotoMono',
                            ),
                          ),
                          SizedBox(height: 8),
                          _buildProgressRing(),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
            
            // Ícones orbitais
            ..._buildOrbitingIcons(size),
          ],
        );
      },
    );
  }

  Widget _buildProgressRing() {
    return SizedBox(
      width: 80,
      height: 80,
      child: Stack(
        fit: StackFit.expand,
        children: [
          CircularProgressIndicator(
            value: scanProgress,
            valueColor: AlwaysStoppedAnimation<Color>(Colors.cyan),
            backgroundColor: Colors.grey[800]!,
            strokeWidth: 4,
          ),
          Center(
            child: Text(
              '${(scanProgress * 100).toInt()}%',
              style: TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
                fontFamily: 'RobotoMono',
              ),
            ),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildOrbitingIcons(double centerSize) {
    List<Widget> icons = [];
    double radius = centerSize * 0.7;
    
    for (int i = 0; i < systems.length; i++) {
      double angle = (i / systems.length) * 2 * pi;
      
      // Animação orbital sutil
      if (scanning) {
        angle += DateTime.now().millisecondsSinceEpoch / 5000;
      }
      
      double x = cos(angle) * radius;
      double y = sin(angle) * radius;
      
      icons.add(
        Positioned(
          left: centerSize / 2 + x - 25,
          top: centerSize / 2 + y - 25,
          child: TweenAnimationBuilder(
            duration: Duration(milliseconds: 300),
            tween: ColorTween(
              begin: systems[i].color,
              end: systems[i].color,
            ),
            builder: (context, color, child) {
              return Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  color: Colors.grey[900],
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: color ?? Colors.grey,
                    width: 2,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: (color ?? Colors.grey).withOpacity(0.3),
                      blurRadius: 8,
                      spreadRadius: 2,
                    ),
                  ],
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      systems[i].icon,
                      color: color ?? Colors.grey,
                      size: 20,
                    ),
                    SizedBox(height: 2),
                    Text(
                      systems[i].name,
                      style: TextStyle(
                        color: color ?? Colors.grey,
                        fontSize: 8,
                        fontFamily: 'RobotoMono',
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      );
    }
    
    return icons;
  }

  Widget _buildFooter() {
    return Container(
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        border: Border(
          top: BorderSide(color: Colors.cyan.withOpacity(0.3), width: 1),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatCounter('ECUs DETECTADAS', ecusDetected, 45, Colors.cyan),
          Container(
            height: 40,
            width: 1,
            color: Colors.grey[800],
          ),
          _buildStatCounter('FALHAS', falhasEncontradas, null, 
              falhasEncontradas > 0 ? Colors.red : Colors.green),
        ],
      ),
    );
  }

  Widget _buildStatCounter(String label, int value, int? max, Color color) {
    return Column(
      children: [
        Text(
          label,
          style: TextStyle(
            color: Colors.grey[600],
            fontSize: 12,
            fontFamily: 'RobotoMono',
          ),
        ),
        SizedBox(height: 4),
        Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              value.toString(),
              style: TextStyle(
                color: color,
                fontSize: 32,
                fontWeight: FontWeight.bold,
                fontFamily: 'RobotoMono',
              ),
            ),
            if (max != null)
              Text(
                ' / $max',
                style: TextStyle(
                  color: Colors.grey[600],
                  fontSize: 16,
                  fontFamily: 'RobotoMono',
                ),
              ),
          ],
        ),
      ],
    );
  }
}

class SystemIcon {
  final String name;
  final IconData icon;
  final Color color;

  SystemIcon({
    required this.name,
    required this.icon,
    required this.color,
  });

  SystemIcon copyWith({Color? color}) {
    return SystemIcon(
      name: name,
      icon: icon,
      color: color ?? this.color,
    );
  }
}
