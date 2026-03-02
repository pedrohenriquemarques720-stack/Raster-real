# orcamento_automatico.py - Versão simplificada

import random
from datetime import datetime
from typing import Dict, List, Optional

class OrcamentoAutomatico:
    """
    Módulo de orçamento automático e consulta de peças
    Versão simplificada
    """
    
    def __init__(self):
        self.tabela_precos = {
            'COIL': {'peca': 'Bobina de Ignição', 'codigo': '06K905110', 'preco': 450.00},
            'O2_SENSOR': {'peca': 'Sonda Lambda', 'codigo': '55236131', 'preco': 380.00},
            'MAF_SENSOR': {'peca': 'Sensor MAF', 'codigo': '0281006322', 'preco': 520.00},
            'CKP_SENSOR': {'peca': 'Sensor de Rotação', 'codigo': '06A906433A', 'preco': 290.00},
            'SPARK_PLUG': {'peca': 'Vela de Ignição', 'codigo': '04C905616', 'preco': 85.00}
        }
        
        self.mao_obra = {
            'COIL': 1.5,
            'O2_SENSOR': 1.2,
            'MAF_SENSOR': 0.5,
            'CKP_SENSOR': 1.0,
            'SPARK_PLUG': 1.0
        }
    
    def consultar_peca(self, vin: str, component: str, part_number: str = '') -> Dict:
        """
        Simula consulta de peça em fornecedores
        """
        preco_base = self.tabela_precos.get(component, {'preco': 300.00})['preco']
        codigo = self.tabela_precos.get(component, {'codigo': part_number})['codigo']
        
        # Simula múltiplos fornecedores
        suppliers = [
            {
                'name': 'AutoPeças Brasil',
                'price': preco_base * 0.95,
                'shipping': 25.00,
                'total_price': preco_base * 0.95 + 25.00,
                'availability': 'Em estoque',
                'warranty': '3 meses'
            },
            {
                'name': 'Mercado Livre',
                'price': preco_base,
                'shipping': 30.00,
                'total_price': preco_base + 30.00,
                'availability': 'Em estoque',
                'warranty': '3 meses'
            },
            {
                'name': 'Distribuidora Local',
                'price': preco_base * 1.05,
                'shipping': 0.00,
                'total_price': preco_base * 1.05,
                'availability': 'Sob consulta',
                'warranty': '6 meses'
            }
        ]
        
        # Ordena por preço
        suppliers.sort(key=lambda x: x['total_price'])
        
        return {
            'component': component,
            'part_number': codigo,
            'suppliers': suppliers,
            'best_price': suppliers[0]['total_price'],
            'recommended_supplier': suppliers[0]
        }
    
    def gerar_orcamento(self, vin: str, vehicle_info: Dict,
                         diagnostic_result: Dict, part_info: Dict,
                         labor_hour_rate: float = 120.0) -> Dict:
        """
        Gera orçamento completo
        """
        componente = diagnostic_result['probabilities'][0]['component'] if diagnostic_result.get('probabilities') else 'COIL'
        tempo_mao_obra = self.mao_obra.get(componente, 1.0)
        
        total_pecas = part_info['best_price']
        total_mao_obra = tempo_mao_obra * labor_hour_rate
        
        return {
            'numero': f"ORC-{random.randint(1000, 9999)}",
            'data': datetime.now().strftime('%d/%m/%Y'),
            'validade': '7 dias',
            'veiculo': vehicle_info,
            'itens': [
                {
                    'tipo': 'Peça',
                    'descricao': self.tabela_precos.get(componente, {}).get('peca', componente),
                    'quantidade': 1,
                    'valor_unitario': part_info['best_price'],
                    'total': part_info['best_price']
                },
                {
                    'tipo': 'Mão de Obra',
                    'descricao': f"Substituição de {componente}",
                    'quantidade': tempo_mao_obra,
                    'valor_unitario': labor_hour_rate,
                    'total': total_mao_obra
                }
            ],
            'resumo': {
                'total_pecas': total_pecas,
                'total_mao_obra': total_mao_obra,
                'total': total_pecas + total_mao_obra
            }
        }
