// motor_3d_viewer.dart - Visualizador 3D de Motor com Diagnóstico

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'dart:math';
import 'dart:ui' as ui;
import 'dart:async';

class Motor3DViewer extends StatefulWidget {
  final String dtcCode;
  final String component;
  final int cylinder;

  Motor3DViewer({
    required this.dtcCode,
    required this.component,
    this.cylinder = 1,
  });

  @override
  _Motor3DViewerState createState() => _Motor3DViewerState();
}

class _Motor3DViewerState extends State<Motor3DViewer>
    with SingleTickerProviderStateMixin {
  late TransformationController _transformationController;
  late AnimationController _blinkController;
  Offset _startPan = Offset.zero;
  double _rotationX = 0.0;
  double _rotationY = 0.0;
  double _scale = 1.0;
  bool _showInfo = true;
  bool _focusOnComponent = false;

  @override
  void initState() {
    super.initState();
    _transformationController = TransformationController();
    _blinkController = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 500),
    )..repeat(reverse: true);

    // Foca automaticamente no componente após 1 segundo
    Timer(Duration(seconds: 1), () {
      setState(() {
        _focusOnComponent = true;
      });
    });
  }

  @override
  void dispose() {
    _transformationController.dispose();
    _blinkController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Visualizador 3D
          GestureDetector(
            onPanStart: (details) {
              _startPan = details.localPosition;
            },
            onPanUpdate: (details) {
              setState(() {
                _rotationY += (details.localPosition.dx - _startPan.dx) * 0.01;
                _rotationX += (details.localPosition.dy - _startPan.dy) * 0.01;
                _startPan = details.localPosition;
              });
            },
            onScaleUpdate: (details) {
              setState(() {
                _scale *= details.scale;
                if (_scale < 0.5) _scale = 0.5;
                if (_scale > 3.0) _scale = 3.0;
              });
            },
            child: CustomPaint(
              size: Size.infinite,
              painter: Motor3DPainter(
                rotationX: _rotationX,
                rotationY: _rotationY,
                scale: _scale,
                highlightComponent: widget.component,
                cylinder: widget.cylinder,
                blinkValue: _blinkController.value,
                focusOnComponent: _focusOnComponent,
              ),
            ),
          ),

          // Balão de informações lateral
          if (_showInfo)
            Positioned(
              left: 20,
              top: 100,
              bottom: 100,
              child: Container(
                width: 280,
                decoration: BoxDecoration(
                  color: Colors.grey[900]!.withOpacity(0.95),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.cyan, width: 2),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.cyan.withOpacity(0.3),
                      blurRadius: 20,
                      spreadRadius: 5,
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Cabeçalho
                    Container(
                      padding: EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        border: Border(
                          bottom: BorderSide(color: Colors.cyan, width: 1),
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.error_outline, color: Colors.red, size: 24),
                          SizedBox(width: 8),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  widget.dtcCode,
                                  style: TextStyle(
                                    color: Colors.red,
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    fontFamily: 'RobotoMono',
                                  ),
                                ),
                                Text(
                                  _getComponentName(widget.component),
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 14,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),

                    // Localização
                    _buildInfoSection(
                      'LOCALIZAÇÃO',
                      Icons.location_on,
                      _getComponentLocation(widget.component, widget.cylinder),
                    ),

                    // Esquema elétrico
                    _buildPinoutSection(widget.component),

                    // Valores de referência
                    _buildInfoSection(
                      'VALORES DE REFERÊNCIA',
                      Icons.science,
                      _getReferenceValues(widget.component),
                    ),

                    Spacer(),

                    // Instrução de rotação
                    Padding(
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.touch_app, color: Colors.cyan, size: 20),
                          SizedBox(width: 8),
                          Text(
                            'Gire com o dedo para ver a peça',
                            style: TextStyle(
                              color: Colors.grey[400],
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),

          // Botão para fechar balão
          Positioned(
            left: 20,
            top: 50,
            child: IconButton(
              icon: Icon(
                _showInfo ? Icons.chevron_left : Icons.chevron_right,
                color: Colors.cyan,
                size: 32,
              ),
              onPressed: () {
                setState(() {
                  _showInfo = !_showInfo;
                });
              },
            ),
          ),

          // Controles de zoom
          Positioned(
            right: 20,
            bottom: 50,
            child: Column(
              children: [
                FloatingActionButton(
                  heroTag: 'zoom_in',
                  mini: true,
                  backgroundColor: Colors.grey[900],
                  child: Icon(Icons.add, color: Colors.cyan),
                  onPressed: () {
                    setState(() {
                      _scale += 0.2;
                      if (_scale > 3.0) _scale = 3.0;
                    });
                  },
                ),
                SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'zoom_out',
                  mini: true,
                  backgroundColor: Colors.grey[900],
                  child: Icon(Icons.remove, color: Colors.cyan),
                  onPressed: () {
                    setState(() {
                      _scale -= 0.2;
                      if (_scale < 0.5) _scale = 0.5;
                    });
                  },
                ),
                SizedBox(height: 8),
                FloatingActionButton(
                  heroTag: 'reset',
                  mini: true,
                  backgroundColor: Colors.grey[900],
                  child: Icon(Icons.refresh, color: Colors.cyan),
                  onPressed: () {
                    setState(() {
                      _rotationX = 0;
                      _rotationY = 0;
                      _scale = 1.0;
                    });
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoSection(String title, IconData icon, String content) {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Colors.grey[800]!, width: 1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: Colors.cyan, size: 18),
              SizedBox(width: 8),
              Text(
                title,
                style: TextStyle(
                  color: Colors.cyan,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'RobotoMono',
                ),
              ),
            ],
          ),
          SizedBox(height: 8),
          Text(
            content,
            style: TextStyle(
              color: Colors.white,
              fontSize: 13,
              height: 1.4,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPinoutSection(String component) {
    Map<String, dynamic> pinout = _getPinout(component);
    
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Colors.grey[800]!, width: 1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.electrical_services, color: Colors.cyan, size: 18),
              SizedBox(width: 8),
              Text(
                'ESQUEMA ELÉTRICO',
                style: TextStyle(
                  color: Colors.cyan,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'RobotoMono',
                ),
              ),
            ],
          ),
          SizedBox(height: 8),
          Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.grey[850],
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: pinout.entries.map((entry) {
                return Column(
                  children: [
                    Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.grey[900],
                        border: Border.all(color: Colors.cyan, width: 1),
                      ),
                      child: Center(
                        child: Text(
                          entry.key,
                          style: TextStyle(
                            color: Colors.cyan,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      entry.value['function'],
                      style: TextStyle(
                        color: Colors.grey[400],
                        fontSize: 10,
                      ),
                    ),
                    Text(
                      entry.value['wire'],
                      style: TextStyle(
                        color: Colors.orange,
                        fontSize: 9,
                        fontFamily: 'RobotoMono',
                      ),
                    ),
                  ],
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  String _getComponentName(String component) {
    switch (component) {
      case 'COIL':
        return 'Bobina de Ignição';
      case 'INJECTOR':
        return 'Injetor de Combustível';
      case 'CKP_SENSOR':
        return 'Sensor de Rotação';
      case 'O2_SENSOR':
        return 'Sonda Lambda';
      default:
        return 'Componente';
    }
  }

  String _getComponentLocation(String component, int cylinder) {
    switch (component) {
      case 'COIL':
        return 'Cabeçote do motor, lado direito.\nCilindro $cylinder - próximo à válvula borboleta.';
      case 'INJECTOR':
        return 'Trilho de combustível.\nCilindro $cylinder - parte superior do motor.';
      case 'CKP_SENSOR':
        return 'Bloco do motor, próximo ao volante do motor.';
      case 'O2_SENSOR':
        return 'Escapamento, antes do catalisador.';
      default:
        return 'Localização não disponível';
    }
  }

  String _getReferenceValues(String component) {
    switch (component) {
      case 'COIL':
        return '• Resistência primária: 0.5-1.5Ω\n• Resistência secundária: 5-10kΩ\n• Alimentação: 12V\n• Forma de onda: Quadrada 0-5V';
      case 'INJECTOR':
        return '• Resistência: 12-17Ω\n• Vazão: 180-220 ml/min\n• Ângulo de spray: 30°';
      case 'CKP_SENSOR':
        return '• Resistência: 500-900Ω\n• Folga do anel: 0.5-1.5mm\n• Forma de onda: Senoidal';
      case 'O2_SENSOR':
        return '• Tensão: 0.1-0.9V\n• Resistência aquecimento: 3-5Ω\n• Frequência: 1-5Hz';
      default:
        return 'Valores não disponíveis';
    }
  }

  Map<String, dynamic> _getPinout(String component) {
    switch (component) {
      case 'COIL':
        return {
          '1': {'function': '12V', 'wire': 'Vermelho'},
          '2': {'function': 'GND', 'wire': 'Preto'},
          '3': {'function': 'Sinal', 'wire': 'Verde'},
        };
      case 'INJECTOR':
        return {
          '1': {'function': '12V', 'wire': 'Azul'},
          '2': {'function': 'Sinal', 'wire': 'Marrom'},
        };
      case 'CKP_SENSOR':
        return {
          '1': {'function': 'Sinal', 'wire': 'Branco'},
          '2': {'function': 'GND', 'wire': 'Preto'},
          '3': {'function': 'Shield', 'wire': 'Cinza'},
        };
      case 'O2_SENSOR':
        return {
          '1': {'function': 'Sinal', 'wire': 'Preto'},
          '2': {'function': 'GND', 'wire': 'Cinza'},
          '3': {'function': '12V', 'wire': 'Vermelho'},
          '4': {'function': 'GND', 'wire': 'Marrom'},
        };
      default:
        return {};
    }
  }
}

class Motor3DPainter extends CustomPainter {
  final double rotationX;
  final double rotationY;
  final double scale;
  final String highlightComponent;
  final int cylinder;
  final double blinkValue;
  final bool focusOnComponent;

  Motor3DPainter({
    required this.rotationX,
    required this.rotationY,
    required this.scale,
    required this.highlightComponent,
    required this.cylinder,
    required this.blinkValue,
    required this.focusOnComponent,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    
    canvas.translate(center.dx, center.dy);
    canvas.scale(scale);
    canvas.rotate(rotationY);
    canvas.rotate(rotationX);
    
    // Desenha bloco do motor
    _drawEngineBlock(canvas);
    
    // Desenha cabeçote
    _drawCylinderHead(canvas);
    
    // Desenha componentes
    _drawComponents(canvas);
  }

  void _drawEngineBlock(Canvas canvas) {
    final paint = Paint()
      ..color = Colors.grey[700]!
      ..style = PaintingStyle.fill;
    
    // Bloco principal
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(0, 0),
        width: 300,
        height: 200,
      ),
      paint,
    );
    
    // Detalhes do bloco
    paint.color = Colors.grey[600]!;
    for (int i = 0; i < 4; i++) {
      canvas.drawRect(
        Rect.fromCenter(
          center: Offset(-100 + i * 50, -30),
          width: 20,
          height: 80,
        ),
        paint,
      );
    }
  }

  void _drawCylinderHead(Canvas canvas) {
    final paint = Paint()
      ..color = Colors.grey[500]!
      ..style = PaintingStyle.fill;
    
    // Cabeçote
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(0, -120),
        width: 280,
        height: 40,
      ),
      paint,
    );
  }

  void _drawComponents(Canvas canvas) {
    for (int i = 0; i < 4; i++) {
      double x = -100 + i * 50;
      
      // Desenha bobinas
      if (highlightComponent == 'COIL' && i == cylinder - 1) {
        _drawHighlightedCoil(canvas, x, -100, i);
      } else {
        _drawCoil(canvas, x, -100, i);
      }
      
      // Desenha injetores
      if (highlightComponent == 'INJECTOR' && i == cylinder - 1) {
        _drawHighlightedInjector(canvas, x, 20);
      } else {
        _drawInjector(canvas, x, 20);
      }
    }
  }

  void _drawCoil(Canvas canvas, double x, double y, int index) {
    final paint = Paint()
      ..color = Colors.grey[400]!
      ..style = PaintingStyle.fill;
    
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(x, y),
        width: 30,
        height: 40,
      ),
      paint,
    );
    
    // Conector
    paint.color = Colors.grey[600]!;
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(x, y - 25),
        width: 15,
        height: 10,
      ),
      paint,
    );
  }

  void _drawHighlightedCoil(Canvas canvas, double x, double y, int index) {
    final paint = Paint()
      ..color = Colors.orange.withOpacity(blinkValue)
      ..style = PaintingStyle.fill;
    
    // Corpo da bobina com brilho
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(x, y),
        width: 35,
        height: 45,
      ),
      paint,
    );
    
    // Contorno brilhante
    paint
      ..color = Colors.yellow
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;
    
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(x, y),
        width: 35,
        height: 45,
      ),
      paint,
    );
    
    // Brilho extra
    paint
      ..color = Colors.yellow.withOpacity(0.3 * blinkValue)
      ..style = PaintingStyle.fill;
    
    canvas.drawCircle(
      Offset(x, y),
      30,
      paint,
    );
  }

  void _drawInjector(Canvas canvas, double x, double y) {
    final paint = Paint()
      ..color = Colors.grey[500]!
      ..style = PaintingStyle.fill;
    
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(x, y),
        width: 20,
        height: 40,
      ),
      paint,
    );
  }

  void _drawHighlightedInjector(Canvas canvas, double x, double y) {
    final paint = Paint()
      ..color = Colors.orange.withOpacity(blinkValue)
      ..style = PaintingStyle.fill;
    
    canvas.drawRect(
      Rect.fromCenter(
        center: Offset(x, y),
        width: 25,
        height: 45,
      ),
      paint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}
