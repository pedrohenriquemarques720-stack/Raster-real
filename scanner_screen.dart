// scanner_screen.dart - Exemplo de uso no Flutter

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';

class ScannerScreen extends StatefulWidget {
  @override
  _ScannerScreenState createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  static const platform = MethodChannel('com.autelpro/audio');
  
  @override
  void initState() {
    super.initState();
    _setupAudioHandlers();
  }
  
  Future<void> _setupAudioHandlers() async {
    // Configura handlers para áudio/vibração
    try {
      await platform.invokeMethod('initialize');
    } on PlatformException catch (e) {
      print("Erro ao inicializar áudio: ${e.message}");
    }
  }
  
  Future<void> _triggerCriticalFault() async {
    try {
      await platform.invokeMethod('triggerCriticalFault');
    } on PlatformException catch (e) {
      print("Erro: ${e.message}");
    }
  }
  
  Future<void> _triggerSGWUnlocked() async {
    try {
      await platform.invokeMethod('triggerSGWUnlocked');
    } on PlatformException catch (e) {
      print("Erro: ${e.message}");
    }
  }
  
  Future<void> _triggerScanComplete() async {
    try {
      await platform.invokeMethod('triggerScanComplete');
    } on PlatformException catch (e) {
      print("Erro: ${e.message}");
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Scanner Pro'),
        backgroundColor: Colors.black,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _triggerCriticalFault,
              child: Text('Simular Falha Grave'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _triggerSGWUnlocked,
              child: Text('Simular Desbloqueio SGW'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.cyan,
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _triggerScanComplete,
              child: Text('Simular Scan Completo'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
