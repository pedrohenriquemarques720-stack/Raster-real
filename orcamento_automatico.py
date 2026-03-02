# orcamento_automatico.py - Sistema Profissional de Orçamentos

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from dataclasses import dataclass

@dataclass
class PartInfo:
    code: str
    name: str
    price: float
    supplier: str
    availability: str
    warranty: str
    shipping: float

@dataclass
class LaborInfo:
    hours: float
    rate: float
    difficulty: str
    special_tools: List[str]

class OrcamentoAutomatico:
    """
    Sistema profissional de orçamento automático e consulta de peças
    """
    
    def __init__(self):
        self.parts_catalog = self._load_parts_catalog()
        self.labor_catalog = self._load_labor_catalog()
        self.suppliers = self._load_suppliers()
        
    def _load_parts_catalog(self) -> Dict:
        """Carrega catálogo profissional de peças"""
        return {
            'COIL': {
                'name': 'Bobina de Ignição',
                'oem': {'VW': '06K905110', 'Fiat': '55211234', 'Ford': 'CM5G-12A366-BA'},
                'aftermarket': [
                    {'brand': 'Bosch', 'code': '0221504024', 'price': 450.00},
                    {'brand': 'NGK', 'code': '48005', 'price': 380.00},
                    {'brand': 'Valeo', 'code': '245025', 'price': 420.00}
                ],
                'specs': {
                    'type': 'Indutiva',
                    'voltage': '12V',
                    'resistance': '0.5-1.5Ω'
                }
            },
            'O2_SENSOR': {
                'name': 'Sonda Lambda',
                'oem': {'VW': '06K906262', 'Fiat': '55236131', 'Ford': 'F1EB-9F472-AA'},
                'aftermarket': [
                    {'brand': 'Bosch', 'code': '0258007033', 'price': 380.00},
                    {'brand': 'NGK', 'code': '91005', 'price': 420.00},
                    {'brand': 'Denso', 'code': 'DOX-0101', 'price': 395.00}
                ],
                'specs': {
                    'type': 'Largo banda',
                    'heater_resistance': '3-5Ω',
                    'wires': 4
                }
            },
            'MAF_SENSOR': {
                'name': 'Sensor MAF',
                'oem': {'VW': '06K906461', 'Fiat': '55228734', 'Ford': 'CM5G-12B579-AA'},
                'aftermarket': [
                    {'brand': 'Bosch', 'code': '0281006322', 'price': 520.00},
                    {'brand': 'Pierburg', 'code': '7.22684.06.0', 'price': 580.00},
                    {'brand': 'VDO', 'code': 'A2C59513828', 'price': 490.00}
                ],
                'specs': {
                    'type': 'Hot film',
                    'output': '0.5-4.5V',
                    'connector': '5 pinos'
                }
            },
            'CKP_SENSOR': {
                'name': 'Sensor de Rotação',
                'oem': {'VW': '06A906433A', 'Fiat': '55211982', 'Ford': 'F6DZ-6C315-AA'},
                'aftermarket': [
                    {'brand': 'Bosch', 'code': '0261210224', 'price': 290.00},
                    {'brand': 'Facet', 'code': '904115', 'price': 210.00},
                    {'brand': 'Febi', 'code': '176059', 'price': 250.00}
                ],
                'specs': {
                    'type': 'Indutivo',
                    'resistance': '500-900Ω',
                    'connector': '3 pinos'
                }
            },
            'SPARK_PLUG': {
                'name': 'Vela de Ignição',
                'oem': {'VW': '04C905616', 'Fiat': '55222456', 'Ford': 'CM5G-12405-AA'},
                'aftermarket': [
                    {'brand': 'NGK', 'code': 'BKR6E-11', 'price': 85.00},
                    {'brand': 'Bosch', 'code': 'FR7DPX', 'price': 95.00},
                    {'brand': 'Denso', 'code': 'K20PR-U11', 'price': 88.00}
                ],
                'specs': {
                    'type': 'Iridio',
                    'gap': '0.8-1.1mm',
                    'torque': '25-30 Nm'
                }
            }
        }
        
    def _load_labor_catalog(self) -> Dict:
        """Carrega tabela de mão de obra profissional"""
        return {
            'COIL': {
                'hours': 1.5,
                'difficulty': 'Médio',
                'special_tools': ['Chave de vela', 'Torquímetro'],
                'procedure': [
                    'Remover conector elétrico',
                    'Remover parafuso de fixação',
                    'Puxar bobina para cima',
                    'Instalar nova bobina',
                    'Torquear parafuso (8-10 Nm)',
                    'Reconectar elétrica'
                ]
            },
            'O2_SENSOR': {
                'hours': 1.2,
                'difficulty': 'Médio',
                'special_tools': ['Chave para sonda lambda', 'Anti-aderente'],
                'procedure': [
                    'Desconectar conector',
                    'Remover sonda com chave específica',
                    'Aplicar anti-aderente na rosca',
                    'Instalar nova sonda',
                    'Torquear (40-50 Nm)',
                    'Reconectar elétrica'
                ]
            },
            'MAF_SENSOR': {
                'hours': 0.5,
                'difficulty': 'Fácil',
                'special_tools': ['Chave Torx'],
                'procedure': [
                    'Desconectar conector',
                    'Remover parafusos',
                    'Retirar sensor do duto',
                    'Limpar área de instalação',
                    'Instalar novo sensor',
                    'Reconectar elétrica'
                ]
            },
            'CKP_SENSOR': {
                'hours': 1.0,
                'difficulty': 'Médio',
                'special_tools': ['Multímetro', 'Chave combinada'],
                'procedure': [
                    'Localizar sensor próximo ao volante',
                    'Desconectar conector',
                    'Remover parafuso',
                    'Remover sensor',
                    'Verificar anel fônico',
                    'Instalar novo sensor',
                    'Ajustar folga (0.5-1.5mm)'
                ]
            },
            'SPARK_PLUG': {
                'hours': 0.8,
                'difficulty': 'Fácil',
                'special_tools': ['Chave de vela', 'Torquímetro', 'Calibrador de folga'],
                'procedure': [
                    'Remover bobina',
                    'Remover vela com chave específica',
                    'Verificar e ajustar folga',
                    'Aplicar anti-aderente',
                    'Instalar vela',
                    'Torquear (25-30 Nm)'
                ]
            }
        }
        
    def _load_suppliers(self) -> List[Dict]:
        """Carrega lista de fornecedores profissionais"""
        return [
            {
                'name': 'AutoPeças Brasil',
                'type': 'Distribuidor Nacional',
                'shipping_time': '1-2 dias',
                'shipping_cost': 25.00,
                'trust_factor': 0.95
            },
            {
                'name': 'Mercado Livre',
                'type': 'Marketplace',
                'shipping_time': '2-3 dias',
                'shipping_cost': 30.00,
                'trust_factor': 0.85
            },
            {
                'name': 'Distribuidora Oficina',
                'type': 'Atacadista',
                'shipping_time': '1 dia',
                'shipping_cost': 0.00,
                'trust_factor': 0.98,
                'min_purchase': 500.00
            },
            {
                'name': 'AutoPeças Express',
                'type': 'Varejista',
                'shipping_time': '1-2 dias',
                'shipping_cost': 20.00,
                'trust_factor': 0.92
            }
        ]
        
    def consultar_peca(self, vin: str, component: str, part_number: str = '') -> Dict:
        """
        Consulta profissional de peças
        """
        comp_info = self.parts_catalog.get(component, {
            'name': component,
            'oem': {'Generic': 'PART001'},
            'aftermarket': [{'brand': 'Genérico', 'code': 'GEN001', 'price': 300.00}]
        })
        
        # Determina fabricante pelo VIN
        manufacturer = 'VW' if '9BW' in vin else 'Fiat' if '935' in vin else 'Generic'
        oem_code = comp_info.get('oem', {}).get(manufacturer, 'OEM001')
        
        suppliers_list = []
        
        # Gera ofertas dos fornecedores
        for supplier in self.suppliers:
            # Preço baseado na confiança do fornecedor
            base_price = comp_info['aftermarket'][0]['price']
            price_factor = 1.0 + (1 - supplier['trust_factor']) * 0.2
            price = base_price * price_factor
            
            # Verifica disponibilidade
            availability = random.choices(
                ['Em estoque', 'Sob consulta', 'Prazo 3 dias', 'Indisponível'],
                weights=[0.6, 0.2, 0.15, 0.05]
            )[0]
            
            if availability != 'Indisponível':
                suppliers_list.append({
                    'name': supplier['name'],
                    'type': supplier['type'],
                    'brand': comp_info['aftermarket'][0]['brand'],
                    'code': comp_info['aftermarket'][0]['code'],
                    'oem_code': oem_code,
                    'price': round(price, 2),
                    'shipping': supplier['shipping_cost'] if 'min_purchase' not in supplier or price > supplier.get('min_purchase', 0) else 0,
                    'total_price': round(price + (supplier['shipping_cost'] if 'min_purchase' not in supplier or price > supplier.get('min_purchase', 0) else 0), 2),
                    'availability': availability,
                    'warranty': '6 meses' if supplier['trust_factor'] > 0.9 else '3 meses',
                    'shipping_time': supplier['shipping_time']
                })
        
        # Ordena por preço total
        suppliers_list.sort(key=lambda x: x['total_price'])
        
        return {
            'component': component,
            'part_name': comp_info['name'],
            'oem_code': oem_code,
            'suppliers': suppliers_list,
            'best_price': suppliers_list[0]['total_price'] if suppliers_list else None,
            'recommended_supplier': suppliers_list[0] if suppliers_list else None,
            'specifications': comp_info.get('specs', {})
        }
        
    def gerar_orcamento(self, vin: str, vehicle_info: Dict,
                         diagnostic_result: Dict, part_info: Dict,
                         labor_hour_rate: float = 120.0) -> Dict:
        """
        Gera orçamento profissional completo
        """
        componente = diagnostic_result.get('probabilities', [{}])[0].get('component', 'COIL')
        
        # Obtém informações de mão de obra
        labor_info = self.labor_catalog.get(componente, {
            'hours': 1.0,
            'difficulty': 'Médio',
            'special_tools': [],
            'procedure': []
        })
        
        # Cálculos
        total_pecas = part_info['best_price'] if part_info['best_price'] else 0
        total_mao_obra = labor_info['hours'] * labor_hour_rate
        subtotal = total_pecas + total_mao_obra
        
        # Gera número do orçamento
        orcamento_num = f"ORC-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        return {
            'numero': orcamento_num,
            'data': datetime.now().strftime('%d/%m/%Y'),
            'validade': (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y'),
            'cliente': {
                'nome': 'Cliente',
                'veiculo': f"{vehicle_info.get('manufacturer', '')} {vehicle_info.get('model', '')} {vehicle_info.get('year', '')}",
                'placa': 'ABC-1234',
                'km': vehicle_info.get('km', '0')
            },
            'itens': [
                {
                    'codigo': part_info.get('oem_code', 'N/A'),
                    'descricao': part_info.get('part_name', componente),
                    'quantidade': 1,
                    'valor_unitario': total_pecas,
                    'total': total_pecas
                },
                {
                    'codigo': 'MAO_OBRA',
                    'descricao': f"Mão de obra - {componente}",
                    'quantidade': labor_info['hours'],
                    'valor_unitario': labor_hour_rate,
                    'total': total_mao_obra
                }
            ],
            'resumo': {
                'subtotal': round(subtotal, 2),
                'desconto': 0,
                'total': round(subtotal, 2),
                'forma_pagamento': 'À vista, cartão ou parcelado',
                'observacoes': labor_info.get('procedure', [])
            },
            'labor_details': {
                'horas': labor_info['hours'],
                'dificuldade': labor_info['difficulty'],
                'ferramentas': labor_info.get('special_tools', [])
            }
        }
        
    def gerar_pdf_html(self, orcamento: Dict) -> str:
        """Gera HTML para visualização do orçamento"""
        html = """
        <div style="background:#1a1d24; padding:20px; border-radius:10px; color:white; font-family: 'Roboto Mono', monospace;">
            <h2 style="color:#00ffff; text-align:center;">ORÇAMENTO DE SERVIÇOS</h2>
            <hr style="border:1px solid #00ffff;">
        """
        
        html += f"<p><strong>Nº:</strong> {orcamento['numero']}</p>"
        html += f"<p><strong>Data:</strong> {orcamento['data']}</p>"
        html += f"<p><strong>Válido até:</strong> {orcamento['validade']}</p>"
        
        html += "<h3 style='color:#00ffff;'>Veículo</h3>"
        html += f"<p>{orcamento['cliente']['veiculo']} - KM: {orcamento['cliente']['km']}</p>"
        
        html += "<h3 style='color:#00ffff;'>Itens</h3>"
        html += "<table style='width:100%; border-collapse:collapse;'>"
        html += "<tr><th>Descrição</th><th>Qtd</th><th>Valor Unit.</th><th>Total</th></tr>"
        
        for item in orcamento['itens']:
            html += f"<tr>"
            html += f"<td style='border:1px solid #333; padding:5px;'>{item['descricao']}</td>"
            html += f"<td style='border:1px solid #333; padding:5px;'>{item['quantidade']}</td>"
            html += f"<td style='border:1px solid #333; padding:5px;'>R$ {item['valor_unitario']:.2f}</td>"
            html += f"<td style='border:1px solid #333; padding:5px;'>R$ {item['total']:.2f}</td>"
            html += f"</tr>"
            
        html += "</table>"
        
        html += "<h3 style='color:#00ffff;'>Resumo</h3>"
        html += f"<p><strong>Subtotal:</strong> R$ {orcamento['resumo']['subtotal']:.2f}</p>"
        html += f"<p><strong>Total:</strong> R$ {orcamento['resumo']['total']:.2f}</p>"
        
        if orcamento['labor_details']['ferramentas']:
            html += "<p><strong>Ferramentas especiais:</strong> " + ", ".join(orcamento['labor_details']['ferramentas']) + "</p>"
            
        html += """
            <hr style="border:1px solid #00ffff;">
            <p style="text-align:center; color:#888;">Este orçamento é válido por 7 dias</p>
        </div>
        """
        
        return html
