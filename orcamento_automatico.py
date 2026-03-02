# orcamento_automatico.py - Módulo de orçamento automático

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import hashlib
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import os

class OrcamentoAutomatico:
    """
    Módulo de orçamento automático e consulta de peças
    Integração com APIs de autopeças
    """
    
    def __init__(self):
        self.part_suppliers = self._load_suppliers()
        self.labor_database = self._load_labor_times()
        self.price_cache = {}
        
    def _load_suppliers(self) -> Dict:
        """Carrega informações de fornecedores"""
        return {
            'auto_pecas_brasil': {
                'api_url': 'https://api.autopecasbrasil.com.br/v1',
                'api_key': '${AUTO_PECAS_API_KEY}',
                'shipping_time': '24h',
                'discount_tier': 0.15
            },
            'mercadolivre': {
                'api_url': 'https://api.mercadolibre.com',
                'api_key': '${ML_API_KEY}',
                'shipping_time': '48h',
                'discount_tier': 0.1
            },
            'distribuidora_local': {
                'api_url': 'http://localhost:8000/api',
                'api_key': 'local_key',
                'shipping_time': '2h',
                'discount_tier': 0.2
            }
        }
    
    def _load_labor_times(self) -> Dict:
        """Carrega tabela de tempos de mão de obra"""
        return {
            'COIL': {
                'time_hours': 1.5,
                'difficulty': 'Médio',
                'special_tools': ['Chave de vela', 'Torquímetro']
            },
            'SPARK_PLUG': {
                'time_hours': 1.0,
                'difficulty': 'Fácil',
                'special_tools': ['Chave de vela', 'Torquímetro']
            },
            'O2_SENSOR': {
                'time_hours': 1.2,
                'difficulty': 'Médio',
                'special_tools': ['Chave para sonda lambda']
            },
            'MAF_SENSOR': {
                'time_hours': 0.5,
                'difficulty': 'Fácil',
                'special_tools': ['Chave Torx']
            },
            'CKP_SENSOR': {
                'time_hours': 1.0,
                'difficulty': 'Médio',
                'special_tools': ['Multímetro']
            },
            'INJECTOR': {
                'time_hours': 2.5,
                'difficulty': 'Difícil',
                'special_tools': ['Bancada de teste', 'Chaves especiais']
            },
            'CATALYST': {
                'time_hours': 3.0,
                'difficulty': 'Difícil',
                'special_tools': ['Maçarico', 'Chaves combinadas']
            }
        }
    
    def consultar_peca(self, vin: str, component: str, 
                        part_number: str) -> Dict:
        """
        Consulta peça em múltiplos fornecedores
        """
        results = {
            'component': component,
            'part_number': part_number,
            'suppliers': [],
            'best_price': None,
            'recommended_supplier': None,
            'compatibility': self._check_compatibility(vin, part_number)
        }
        
        for supplier_name, supplier in self.part_suppliers.items():
            try:
                # Consulta preço no fornecedor
                price_info = self._query_supplier(supplier, part_number)
                
                if price_info:
                    supplier_result = {
                        'name': supplier_name,
                        'price': price_info['price'],
                        'shipping': price_info['shipping'],
                        'total_price': price_info['price'] + price_info['shipping'],
                        'availability': price_info['availability'],
                        'shipping_time': supplier['shipping_time'],
                        'warranty': price_info.get('warranty', '3 meses')
                    }
                    
                    results['suppliers'].append(supplier_result)
                    
                    # Atualiza melhor preço
                    if (results['best_price'] is None or 
                        supplier_result['total_price'] < results['best_price']):
                        results['best_price'] = supplier_result['total_price']
                        results['recommended_supplier'] = supplier_result
                        
            except Exception as e:
                print(f"Erro ao consultar {supplier_name}: {e}")
        
        # Ordena por preço
        results['suppliers'].sort(key=lambda x: x['total_price'])
        
        return results
    
    def _query_supplier(self, supplier: Dict, part_number: str) -> Optional[Dict]:
        """Consulta preço em fornecedor específico"""
        # Simula consulta à API
        import random
        
        return {
            'price': round(random.uniform(150, 800), 2),
            'shipping': round(random.uniform(15, 50), 2),
            'availability': random.choice(['Em estoque', 'Sob consulta', 'Prazo de 3 dias']),
            'warranty': '3 meses'
        }
    
    def _check_compatibility(self, vin: str, part_number: str) -> Dict:
        """Verifica compatibilidade da peça com o veículo"""
        # Simula verificação
        return {
            'compatible': True,
            'notes': 'Peça original equivalente',
            'confidence': 0.95
        }
    
    def gerar_orcamento(self, vin: str, vehicle_info: Dict,
                         diagnostic_result: Dict, part_info: Dict,
                         labor_hour_rate: float = 120.0) -> Dict:
        """
        Gera orçamento completo para o cliente
        """
        orcamento = {
            'numero': self._generate_orcamento_number(),
            'data': datetime.now().strftime('%d/%m/%Y'),
            'validade': '7 dias',
            'cliente': None,  # A ser preenchido pelo mecânico
            'veiculo': vehicle_info,
            'itens': [],
            'resumo': {}
        }
        
        total_pecas = 0
        total_mao_obra = 0
        
        # Adiciona peça principal
        if part_info['recommended_supplier']:
            item_peca = {
                'tipo': 'Peça',
                'descricao': f"{diagnostic_result['primary_suspect']['component']} - {diagnostic_result['primary_suspect']['part_number']}",
                'quantidade': 1,
                'valor_unitario': part_info['recommended_supplier']['price'],
                'total': part_info['recommended_supplier']['price']
            }
            orcamento['itens'].append(item_peca)
            total_pecas += item_peca['total']
        
        # Adiciona mão de obra
        labor_info = self.labor_database.get(
            diagnostic_result['primary_suspect']['component'], 
            {'time_hours': 1.0, 'difficulty': 'Médio', 'special_tools': []}
        )
        
        valor_mao_obra = labor_info['time_hours'] * labor_hour_rate
        
        item_mao_obra = {
            'tipo': 'Mão de Obra',
            'descricao': f"Substituição de {diagnostic_result['primary_suspect']['component']}",
            'detalhes': f"Tempo estimado: {labor_info['time_hours']}h - Dificuldade: {labor_info['difficulty']}",
            'quantidade': labor_info['time_hours'],
            'valor_unitario': labor_hour_rate,
            'total': valor_mao_obra
        }
        orcamento['itens'].append(item_mao_obra)
        total_mao_obra += valor_mao_obra
        
        # Adiciona materiais auxiliares
        if labor_info['special_tools']:
            orcamento['observacoes'] = f"Ferramentas especiais necessárias: {', '.join(labor_info['special_tools'])}"
        
        # Resumo
        orcamento['resumo'] = {
            'total_pecas': round(total_pecas, 2),
            'total_mao_obra': round(total_mao_obra, 2),
            'subtotal': round(total_pecas + total_mao_obra, 2),
            'desconto': 0,
            'total': round(total_pecas + total_mao_obra, 2),
            'forma_pagamento': 'À vista, cartão ou parcelado'
        }
        
        return orcamento
    
    def _generate_orcamento_number(self) -> str:
        """Gera número único de orçamento"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        hash_obj = hashlib.md5(timestamp.encode())
        return f"ORC-{hash_obj.hexdigest()[:8].upper()}"
    
    def exportar_pdf(self, orcamento: Dict, filename: str = None) -> str:
        """
        Exporta orçamento para PDF
        """
        if not filename:
            filename = f"orcamento_{orcamento['numero']}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#ff6600'),
            alignment=1
        )
        elements.append(Paragraph("ORÇAMENTO DE SERVIÇOS", title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Informações do orçamento
        info_data = [
            ['Nº:', orcamento['numero'], 'Data:', orcamento['data']],
            ['Válido até:', orcamento['validade'], '', '']
        ]
        info_table = Table(info_data, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Informações do veículo
        elements.append(Paragraph("DADOS DO VEÍCULO", styles['Heading2']))
        vehicle_data = [
            ['Modelo:', f"{orcamento['veiculo'].get('manufacturer', '')} {orcamento['veiculo'].get('model', '')}"],
            ['Ano:', str(orcamento['veiculo'].get('year', '')), 'Motor:', orcamento['veiculo'].get('engine', '')],
            ['VIN:', orcamento['veiculo'].get('vin', '')]
        ]
        vehicle_table = Table(vehicle_data, colWidths=[4*cm, 8*cm])
        vehicle_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(vehicle_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Tabela de itens
        elements.append(Paragraph("ITENS DO ORÇAMENTO", styles['Heading2']))
        
        item_data = [['Item', 'Descrição', 'Qtd', 'Valor Unit.', 'Total']]
        for i, item in enumerate(orcamento['itens'], 1):
            item_data.append([
                str(i),
                item['descricao'],
                str(item['quantidade']),
                f"R$ {item['valor_unitario']:.2f}",
                f"R$ {item['total']:.2f}"
            ])
        
        item_table = Table(item_data, colWidths=[2*cm, 8*cm, 2*cm, 3*cm, 3*cm])
        item_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6600')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(item_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Resumo
        resumo_data = [
            ['Subtotal:', f"R$ {orcamento['resumo']['subtotal']:.2f}"],
            ['Desconto:', f"R$ {orcamento['resumo']['desconto']:.2f}"],
            ['TOTAL:', f"R$ {orcamento['resumo']['total']:.2f}"]
        ]
        resumo_table = Table(resumo_data, colWidths=[8*cm, 5*cm])
        resumo_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.black)
        ]))
        elements.append(resumo_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Observações
        if 'observacoes' in orcamento:
            elements.append(Paragraph(f"Observações: {orcamento['observacoes']}", styles['Normal']))
        
        # Rodapé
        elements.append(Spacer(1, 2*cm))
        elements.append(Paragraph("Este orçamento é válido por 7 dias.", styles['Italic']))
        
        # Gera PDF
        doc.build(elements)
        
        return filename
    
    def enviar_whatsapp(self, orcamento: Dict, telefone: str) -> bool:
        """
        Envia orçamento via WhatsApp
        """
        # Gera PDF temporário
        pdf_file = self.exportar_pdf(orcamento, f"temp_{orcamento['numero']}.pdf")
        
        # Simula envio
        print(f"Enviando orçamento {orcamento['numero']} para {telefone}")
        print(f"Total: R$ {orcamento['resumo']['total']:.2f}")
        
        # Limpa arquivo temporário
        if os.path.exists(pdf_file):
            os.remove(pdf_file)
        
        return True


# API de integração com WhatsApp
"""
# whatsapp_integration.py

import requests
import base64

class WhatsAppAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.whatsapp.com/v1"
    
    def send_document(self, phone_number, document_path, caption):
        with open(document_path, "rb") as f:
            document_base64 = base64.b64encode(f.read()).decode()
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "document",
            "document": {
                "filename": "orcamento.pdf",
                "caption": caption,
                "data": document_base64
            }
        }
        
        response = requests.post(
            f"{self.base_url}/messages",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        return response.json()
"""
