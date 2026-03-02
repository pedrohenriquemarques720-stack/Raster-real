# co_piloto_oficina.py - Versão simplificada

import random
from typing import Dict, List, Optional
from datetime import datetime

class CoPilotoOficina:
    """
    Assistente inteligente para diagnóstico automotivo
    Versão simplificada
    """
    
    def __init__(self):
        self.diagnostic_history = []
        self.base_conhecimento = {
            'P0301': {
                'componentes': ['COIL', 'SPARK_PLUG', 'INJECTOR'],
                'probabilidades': {'COIL': 0.7, 'SPARK_PLUG': 0.2, 'INJECTOR': 0.1},
                'testes': {
                    'COIL': 'Medir resistência entre pinos 1 e 2: 0.5-1.5Ω',
                    'SPARK_PLUG': 'Verificar folga do eletrodo: 0.8-1.1mm',
                    'INJECTOR': 'Medir resistência: 12-17Ω'
                }
            },
            'P0420': {
                'componentes': ['O2_SENSOR', 'CATALYST'],
                'probabilidades': {'O2_SENSOR': 0.6, 'CATALYST': 0.4},
                'testes': {
                    'O2_SENSOR': 'Verificar tensão: deve variar 0.1-0.9V',
                    'CATALYST': 'Medir temperatura entrada/saída: diferença > 100°C'
                }
            },
            'P0171': {
                'componentes': ['MAF_SENSOR', 'VACUUM_LEAK', 'FUEL_PRESSURE'],
                'probabilidades': {'MAF_SENSOR': 0.5, 'VACUUM_LEAK': 0.3, 'FUEL_PRESSURE': 0.2},
                'testes': {
                    'MAF_SENSOR': 'Verificar valor em marcha lenta: 2.5-4.5 g/s',
                    'VACUUM_LEAK': 'Usar spray de carburador nas mangueiras',
                    'FUEL_PRESSURE': 'Instalar manômetro: 3.0-4.0 bar'
                }
            }
        }
    
    def diagnose(self, dtc: str, live_data: Dict, history: List[Dict],
                 vehicle_info: Dict) -> Dict:
        """
        Diagnóstico baseado em IA
        """
        info = self.base_conhecimento.get(dtc, {
            'componentes': ['COMPONENTE_GENERICO'],
            'probabilidades': {'COMPONENTE_GENERICO': 1.0},
            'testes': {'COMPONENTE_GENERICO': 'Consulte o manual do veículo'}
        })
        
        probabilities = []
        for comp, prob in info['probabilidades'].items():
            # Simula variação baseada nos dados ao vivo
            if comp == 'COIL' and live_data.get('rpm', 0) > 3000:
                prob *= 1.2
            elif comp == 'MAF_SENSOR' and live_data.get('maf', 0) < 2.5:
                prob *= 1.3
            
            probabilities.append({
                'component': comp,
                'probability': round(min(prob * 100, 99), 1),
                'confidence': round(prob * 100, 1),
                'part_number': self._get_part_number(comp),
                'recommended_test': info['testes'].get(comp, 'Teste não disponível')
            })
        
        probabilities.sort(key=lambda x: x['probability'], reverse=True)
        
        result = {
            'dtc': dtc,
            'timestamp': datetime.now().isoformat(),
            'vehicle': vehicle_info,
            'probabilities': probabilities,
            'knowledge_base': {},
            'recommended_tests': [],
            'final_recommendation': {
                'priority': 'ALTA' if probabilities[0]['probability'] > 70 else 'MÉDIA',
                'primary_suspect': probabilities[0],
                'action_plan': [
                    f"1. {probabilities[0]['recommended_test']}",
                    "2. Verificar conectores e cabos",
                    "3. Se necessário, substituir componente"
                ]
            },
            'confidence_score': probabilities[0]['confidence']
        }
        
        self.diagnostic_history.append(result)
        return result
    
    def _get_part_number(self, component: str) -> str:
        parts = {
            'COIL': '06K905110',
            'SPARK_PLUG': '04C905616',
            'INJECTOR': '0261500298',
            'O2_SENSOR': '55236131',
            'MAF_SENSOR': '0281006322',
            'CKP_SENSOR': '06A906433A'
        }
        return parts.get(component, 'CONSULTAR_CATALOGO')
