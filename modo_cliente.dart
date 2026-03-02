// modo_cliente.dart - Tela para Cliente Final

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:math';
import 'dart:ui';

void main() {
  runApp(ClienteApp());
}

class ClienteApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Diagnóstico - Modo Cliente',
      theme: ThemeData.dark().copyWith(
        primaryColor: Colors.blue,
        scaffoldBackgroundColor: Color(0xFF0A0C10),
      ),
      home: ModoClienteScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class ModoClienteScreen extends StatefulWidget {
  @override
  _ModoClienteScreenState createState() => _ModoClienteScreenState();
}

class _ModoClienteScreenState extends State<ModoClienteScreen> {
  bool _assinaturaCompleta = false;
  final _signatureController = TextEditingController();
  List<Map<String, dynamic>> _diagnosticos = [
    {
      'tecnico': 'P0420 - Baixa eficiência do catalisador',
      'cliente': 'Sistema de filtragem de poluição comprometido',
      'severidade': 0.8, // 0-1
      'custo': 1850.00,
      'tempo': 3.0,
      'recomendacao': 'Substituir catalisador e sensores lambda'
    },
    {
      'tecnico': 'P0301 - Falha de ignição no cilindro 1',
      'cliente': 'Problema na queima de combustível do motor',
      'severidade': 0.6,
      'custo': 450.00,
      'tempo': 1.5,
      'recomendacao': 'Substituir bobina de ignição'
    },
  ];

  String _getSeveridadeText(double severidade) {
    if (severidade < 0.4) return 'Baixa';
    if (severidade < 0.7) return 'Média';
    return 'Alta';
  }

  Color _getSeveridadeColor(double severidade) {
    if (severidade < 0.4) return Colors.green;
    if (severidade < 0.7) return Colors.orange;
    return Colors.red;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0A0C10), Color(0xFF1A1D24)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              _buildHeader(),
              Expanded(
                child: SingleChildScrollView(
                  padding: EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildVehicleInfo(),
                      SizedBox(height: 24),
                      _buildUrgencyBar(),
                      SizedBox(height: 24),
                      _buildDiagnosticsList(),
                      SizedBox(height: 24),
                      _buildSignatureSection(),
                      SizedBox(height: 24),
                      _buildBudgetButton(),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Colors.cyan.withOpacity(0.3), width: 1),
        ),
      ),
      child: Row(
        children: [
          Icon(Icons.visibility, color: Colors.cyan, size: 28),
          SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'MODO CLIENTE',
                  style: TextStyle(
                    color: Colors.cyan,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2,
                  ),
                ),
                Text(
                  'Termos técnicos traduzidos',
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.cyan.withOpacity(0.1),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: Colors.cyan, width: 1),
            ),
            child: Text(
              'OFICINA PARCEIRA',
              style: TextStyle(
                color: Colors.cyan,
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildVehicleInfo() {
    return Container(
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Color(0xFF1A1D24),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.cyan.withOpacity(0.3), width: 1),
      ),
      child: Row(
        children: [
          Icon(Icons.directions_car, color: Colors.cyan, size: 40),
          SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'VW GOL 1.6 MSI 2024',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  'Placa: ABC-1234 • KM: 15.234 km',
                  style: TextStyle(
                    color: Colors.grey[400],
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildUrgencyBar() {
    // Calcula urgência máxima
    double maxSeveridade = _diagnosticos
        .map((d) => d['severidade'] as double)
        .fold(0.0, max);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'URGÊNCIA DE REPARO',
          style: TextStyle(
            color: Colors.grey[400],
            fontSize: 14,
            fontWeight: FontWeight.bold,
          ),
        ),
        SizedBox(height: 8),
        Container(
          height: 40,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            color: Color(0xFF1A1D24),
          ),
          child: Stack(
            children: [
              // Fundo
              Row(
                children: [
                  Expanded(
                    flex: 4,
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.green.withOpacity(0.3),
                        borderRadius: BorderRadius.horizontal(
                          left: Radius.circular(20),
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: Container(
                      color: Colors.orange.withOpacity(0.3),
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.red.withOpacity(0.3),
                        borderRadius: BorderRadius.horizontal(
                          right: Radius.circular(20),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              // Indicador
              AnimatedContainer(
                duration: Duration(milliseconds: 500),
                width: (MediaQuery.of(context).size.width - 80) * maxSeveridade,
                height: 40,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  gradient: LinearGradient(
                    colors: [
                      Colors.green,
                      Colors.orange,
                      Colors.red,
                    ],
                    stops: [0.0, 0.5, 1.0],
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: _getSeveridadeColor(maxSeveridade).withOpacity(0.5),
                      blurRadius: 10,
                      spreadRadius: 2,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        SizedBox(height: 8),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('Seguro', style: TextStyle(color: Colors.green, fontSize: 12)),
            Text('Atenção', style: TextStyle(color: Colors.orange, fontSize: 12)),
            Text('Crítico', style: TextStyle(color: Colors.red, fontSize: 12)),
          ],
        ),
      ],
    );
  }

  Widget _buildDiagnosticsList() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'PROBLEMAS DETECTADOS',
          style: TextStyle(
            color: Colors.grey[400],
            fontSize: 14,
            fontWeight: FontWeight.bold,
          ),
        ),
        SizedBox(height: 12),
        ..._diagnosticos.asMap().entries.map((entry) {
          int index = entry.key;
          var diag = entry.value;
          return _buildDiagnosticCard(index, diag);
        }),
      ],
    );
  }

  Widget _buildDiagnosticCard(int index, Map<String, dynamic> diag) {
    double severidade = diag['severidade'];
    Color severityColor = _getSeveridadeColor(severidade);
    
    return Container(
      margin: EdgeInsets.only(bottom: 12),
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Color(0xFF1A1D24),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: severityColor.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 4,
                height: 40,
                decoration: BoxDecoration(
                  color: severityColor,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
              SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'DIAGNÓSTICO #${index + 1}',
                      style: TextStyle(
                        color: severityColor,
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 2),
                    Text(
                      diag['cliente'],
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: severityColor.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${(severidade * 100).toInt()}%',
                  style: TextStyle(
                    color: severityColor,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          SizedBox(height: 12),
          Container(
            padding: EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.3),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                Icon(Icons.info_outline, color: severityColor, size: 18),
                SizedBox(width: 8),
                Expanded(
                  child: Text(
                    diag['recomendacao'],
                    style: TextStyle(
                      color: Colors.grey[300],
                      fontSize: 13,
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.access_time, color: Colors.cyan, size: 16),
                  SizedBox(width: 4),
                  Text(
                    '${diag['tempo']}h de serviço',
                    style: TextStyle(
                      color: Colors.grey[400],
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
              Text(
                'R\$ ${diag['custo'].toStringAsFixed(2)}',
                style: TextStyle(
                  color: Colors.cyan,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSignatureSection() {
    return Container(
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Color(0xFF1A1D24),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.cyan.withOpacity(0.3), width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.draw, color: Colors.cyan, size: 24),
              SizedBox(width: 8),
              Text(
                'ASSINATURA DIGITAL',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          SizedBox(height: 16),
          Container(
            height: 120,
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.5),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: _assinaturaCompleta ? Colors.green : Colors.grey[700]!,
                width: 1,
              ),
            ),
            child: _assinaturaCompleta
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.check_circle, color: Colors.green, size: 32),
                        SizedBox(height: 4),
                        Text(
                          'Assinatura registrada',
                          style: TextStyle(color: Colors.green),
                        ),
                      ],
                    ),
                  )
                : GestureDetector(
                    onPanUpdate: (details) {
                      // Simula desenho da assinatura
                      if (!_assinaturaCompleta) {
                        setState(() {
                          _assinaturaCompleta = true;
                        });
                      }
                    },
                    child: Center(
                      child: Text(
                        'Deslize o dedo para assinar',
                        style: TextStyle(
                          color: Colors.grey[600],
                          fontSize: 14,
                        ),
                      ),
                    ),
                  ),
          ),
          if (_assinaturaCompleta)
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Text(
                'Ao assinar, você autoriza o reparo e concorda com o orçamento apresentado.',
                style: TextStyle(
                  color: Colors.grey[500],
                  fontSize: 11,
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildBudgetButton() {
    return Container(
      width: double.infinity,
      height: 60,
      child: ElevatedButton(
        onPressed: _assinaturaCompleta ? _gerarOrcamento : null,
        style: ElevatedButton.styleFrom(
          backgroundColor: _assinaturaCompleta ? Colors.cyan : Colors.grey[800],
          foregroundColor: Colors.black,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(30),
          ),
          elevation: _assinaturaCompleta ? 8 : 0,
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.description, size: 24),
            SizedBox(width: 8),
            Text(
              'AUTORIZAR REPARO E GERAR ORÇAMENTO',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                letterSpacing: 1,
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _gerarOrcamento() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Color(0xFF1A1D24),
        title: Text(
          'ORÇAMENTO GERADO!',
          style: TextStyle(color: Colors.cyan),
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Total: R\$ 2.300,00',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Enviaremos o orçamento detalhado via WhatsApp para sua aprovação final.',
              style: TextStyle(color: Colors.grey[400]),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('OK', style: TextStyle(color: Colors.cyan)),
          ),
        ],
      ),
    );
  }
}
