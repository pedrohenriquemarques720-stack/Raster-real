# co_piloto_oficina.py - Sistema Profissional de Diagnóstico com IA

import random
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class DiagnosticResult:
    dtc: str
    confidence: float
    components: List[Dict]
    recommendations: List[str]
    estimated_repair_time: float
    estimated_cost: float
    severity: str

class CoPilotoOficina:
    """
    Assistente profissional de diagnóstico com IA
    """
    
    def __init__(self):
        self.diagnostic_history = []
        self.knowledge_base = self._load_knowledge_base()
        self.correlation_matrix = self._load_correlation_matrix()
        
    def _load_knowledge_base(self) -> Dict:
        """Carrega base de conhecimento profissional"""
        return {
            'P0171': {
                'description': 'Mistura pobre (banco 1)',
                'severity': 'ALTA',
                'typical_causes': [
                    'Sensor MAF contaminado (35%)',
                    'Vazamento de vácuo (25%)',
                    'Pressão de combustível baixa (20%)',
                    'Injetores sujos (15%)',
                    'Sensor O2 com defeito (5%)'
                ],
                'diagnostic_steps': [
                    'Verificar Short Term Fuel Trim com scanner',
                    'Inspecionar mangueiras de vácuo com spray',
                    'Testar sensor MAF com multímetro',
                    'Medir pressão de combustível',
                    'Analisar forma de onda do O2'
                ],
                'live_data_correlation': {
                    'stft': {'>10': 'Vazamento ou MAF', '>20': 'Injetor ou pressão'},
                    'ltft': {'>15': 'Adaptação fora do limite'},
                    'maf': {'<2.5': 'MAF sujo', '>6.0': 'MAF com defeito'},
                    'o2': {'<0.45': 'Mistura pobre confirmada'}
                }
            },
            'P0300': {
                'description': 'Falha de ignição aleatória',
                'severity': 'CRÍTICA',
                'typical_causes': [
                    'Bobinas com defeito (40%)',
                    'Velas desgastadas (30%)',
                    'Injetores obstruídos (15%)',
                    'Compressão baixa (10%)',
                    'Sensor CKP com defeito (5%)'
                ],
                'diagnostic_steps': [
                    'Verificar contagem de falhas por cilindro',
                    'Trocar bobinas entre cilindros',
                    'Testar velas com multímetro',
                    'Realizar teste de compressão',
                    'Verificar sinal do CKP com osciloscópio'
                ],
                'live_data_correlation': {
                    'rpm': {'erratic': 'Falha confirmada'},
                    'stft': {'fluctuating': 'Injetor ou vela'},
                    'load': {'fluctuating': 'Bobina ou compressão'}
                }
            },
            'P0420': {
                'description': 'Catalisador ineficiente',
                'severity': 'MÉDIA',
                'typical_causes': [
                    'Catalisador danificado (50%)',
                    'Sonda O2 pós defeituosa (30%)',
                    'Vazamento no escapamento (15%)',
                    'Mistura rica prolongada (5%)'
                ],
                'diagnostic_steps': [
                    'Comparar leitura O2 pré e pós',
                    'Medir temperatura do catalisador',
                    'Verificar vazamentos no escapamento',
                    'Testar aquecimento da sonda pós',
                    'Analisar forma de onda do O2'
                ],
                'live_data_correlation': {
                    'o2_pre': {'oscillating': 'Normal'},
                    'o2_pos': {'<0.1': 'Sonda com defeito', '>0.8': 'Catalisador ineficiente'}
                }
            }
        }
        
    def _load_correlation_matrix(self) -> Dict:
        """Carrega matriz de correlação para análise de dados"""
        return {
            'fuel_trim_analysis': {
                'thresholds': [5, 10, 15, 20],
                'interpretations': [
                    'Normal',
                    'Atenção - verificar admissão',
                    'Crítico - vazamento ou MAF',
                    'Emergência - injetores ou pressão'
                ]
            },
            'o2_analysis': {
                'cross_count': {
                    'good': '>5 em 10s',
                    'fair': '3-5 em 10s',
                    'poor': '<3 em 10s'
                },
                'voltage_range': {
                    'normal': '0.1-0.9V',
                    'lean': '<0.45V constante',
                    'rich': '>0.8V constante'
                }
            }
        }
        
    def diagnose(self, dtc: str, live_data: Dict, history: List[Dict],
                 vehicle_info: Dict) -> Dict:
        """
        Diagnóstico profissional completo
        """
        base_info = self.knowledge_base.get(dtc, {
            'description': 'Código não encontrado',
            'severity': 'MÉDIA',
            'typical_causes': ['Consultar documentação técnica'],
            'diagnostic_steps': ['Diagnóstico manual necessário']
        })
        
        # Análise de correlação com dados ao vivo
        correlations = self._analyze_correlations(dtc, live_data, history)
        
        # Cálculo de probabilidades
        probabilities = self._calculate_probabilities(dtc, live_data, correlations)
        
        # Gera recomendações personalizadas
        recommendations = self._generate_recommendations(dtc, probabilities, live_data)
        
        # Estimativa de tempo e custo
        est_time, est_cost = self._estimate_repair(dtc, probabilities)
        
        result = {
            'dtc': dtc,
            'description': base_info['description'],
            'severity': base_info['severity'],
            'timestamp': datetime.now().isoformat(),
            'vehicle': vehicle_info,
            'live_data_analyzed': live_data,
            'correlations': correlations,
            'probabilities': probabilities,
            'recommendations': recommendations,
            'estimated_repair_time': est_time,
            'estimated_cost': est_cost,
            'confidence': self._calculate_confidence(probabilities),
            'diagnostic_steps': base_info['diagnostic_steps']
        }
        
        self.diagnostic_history.append(result)
        return result
    
    def _analyze_correlations(self, dtc: str, live_data: Dict, history: List[Dict]) -> Dict:
        """Analisa correlações entre DTC e dados ao vivo"""
        correlations = {}
        
        # Análise de STFT/LTFT
        stft = live_data.get('short_term_fuel_trim', 0)
        ltft = live_data.get('long_term_fuel_trim', 0)
        
        if stft > 10 or ltft > 15:
            correlations['fuel_trim'] = {
                'status': 'CRÍTICO' if stft > 20 or ltft > 25 else 'ATENÇÃO',
                'stft': stft,
                'ltft': ltft,
                'interpretation': self.correlation_matrix['fuel_trim_analysis']['interpretations'][
                    min(3, int(stft/5))
                ]
            }
            
        # Análise do O2
        o2 = live_data.get('o2', 0)
        if o2 < 0.45:
            correlations['o2'] = {
                'status': 'MISTURA POBRE',
                'value': o2,
                'interpretation': 'Sensor O2 indicando mistura pobre - verificar vazamentos'
            }
        elif o2 > 0.8:
            correlations['o2'] = {
                'status': 'MISTURA RICA',
                'value': o2,
                'interpretation': 'Sensor O2 indicando mistura rica - verificar injeção'
            }
            
        # Análise de MAF
        maf = live_data.get('maf', 0)
        rpm = live_data.get('rpm', 850)
        if maf < 2.5 and rpm > 1000:
            correlations['maf'] = {
                'status': 'ATENÇÃO',
                'value': maf,
                'interpretation': 'MAF baixo para RPM atual - sensor sujo ou com defeito'
            }
            
        return correlations
    
    def _calculate_probabilities(self, dtc: str, live_data: Dict, correlations: Dict) -> List[Dict]:
        """Calcula probabilidades de falha baseado em dados"""
        # Probabilidades base por DTC
        base_probs = {
            'P0171': [
                {'component': 'MAF_SENSOR', 'base': 35, 'part': '0281006322'},
                {'component': 'VACUUM_LEAK', 'base': 25, 'part': 'N/A'},
                {'component': 'FUEL_PRESSURE', 'base': 20, 'part': '13577583'},
                {'component': 'INJECTOR', 'base': 15, 'part': '0261500298'},
                {'component': 'O2_SENSOR', 'base': 5, 'part': '55236131'}
            ],
            'P0300': [
                {'component': 'COIL', 'base': 40, 'part': '06K905110'},
                {'component': 'SPARK_PLUG', 'base': 30, 'part': '04C905616'},
                {'component': 'INJECTOR', 'base': 15, 'part': '0261500298'},
                {'component': 'CKP_SENSOR', 'base': 10, 'part': '06A906433A'},
                {'component': 'COMPRESSION', 'base': 5, 'part': 'N/A'}
            ],
            'P0420': [
                {'component': 'CATALYST', 'base': 50, 'part': 'N/A'},
                {'component': 'O2_SENSOR_POST', 'base': 30, 'part': '36531-5R0-003'},
                {'component': 'EXHAUST_LEAK', 'base': 15, 'part': 'N/A'},
                {'component': 'O2_SENSOR_PRE', 'base': 5, 'part': '55236131'}
            ]
        }
        
        probabilities = base_probs.get(dtc, [
            {'component': 'GENERIC', 'base': 100, 'part': 'GEN001'}
        ])
        
        # Ajusta probabilidades baseado em correlações
        for prob in probabilities:
            if 'fuel_trim' in correlations and prob['component'] in ['MAF_SENSOR', 'VACUUM_LEAK']:
                prob['probability'] = min(99, prob['base'] * 1.3)
            elif 'o2' in correlations and prob['component'] in ['O2_SENSOR', 'CATALYST']:
                prob['probability'] = min(99, prob['base'] * 1.2)
            else:
                prob['probability'] = prob['base']
                
            prob['confidence'] = round(random.uniform(0.7, 0.95) * 100, 1)
            
        # Ordena por probabilidade
        probabilities.sort(key=lambda x: x['probability'], reverse=True)
        return probabilities
    
    def _generate_recommendations(self, dtc: str, probabilities: List[Dict], live_data: Dict) -> List[str]:
        """Gera recomendações personalizadas"""
        recommendations = []
        
        # Recomendação principal baseada no componente mais provável
        if probabilities:
            top = probabilities[0]
            recommendations.append(f"1. Testar {top['component']} - probabilidade {top['probability']:.0f}%")
            
            # Recomendações específicas por componente
            if top['component'] == 'MAF_SENSOR':
                recommendations.append("2. Limpar sensor MAF com cleaner específico")
                recommendations.append("3. Verificar vazamentos após o MAF")
            elif top['component'] == 'COIL':
                recommendations.append("2. Medir resistência da bobina (0.5-1.5Ω)")
                recommendations.append("3. Trocar bobina com outro cilindro para teste")
            elif top['component'] == 'O2_SENSOR':
                recommendations.append("2. Verificar aquecimento da sonda (3-5Ω)")
                recommendations.append("3. Analisar forma de onda no osciloscópio")
            elif top['component'] == 'CKP_SENSOR':
                recommendations.append("2. Verificar resistência do sensor (500-900Ω)")
                recommendations.append("3. Inspecionar anel fônico quanto a danos")
                
        # Recomendações baseadas em dados ao vivo
        if live_data.get('short_term_fuel_trim', 0) > 15:
            recommendations.append("• STFT elevado indica possível vazamento de vácuo")
            
        if live_data.get('rpm', 0) < 700:
            recommendations.append("• Marcha lenta baixa - verificar IAC")
            
        return recommendations
    
    def _estimate_repair(self, dtc: str, probabilities: List[Dict]) -> tuple:
        """Estima tempo e custo de reparo"""
        time_estimates = {
            'COIL': 1.5,
            'SPARK_PLUG': 0.8,
            'INJECTOR': 2.5,
            'MAF_SENSOR': 0.5,
            'O2_SENSOR': 1.2,
            'CKP_SENSOR': 1.0,
            'CATALYST': 3.0
        }
        
        cost_estimates = {
            'COIL': 450,
            'SPARK_PLUG': 85,
            'INJECTOR': 380,
            'MAF_SENSOR': 520,
            'O2_SENSOR': 380,
            'CKP_SENSOR': 290,
            'CATALYST': 1850
        }
        
        if probabilities:
            comp = probabilities[0]['component']
            est_time = time_estimates.get(comp, 1.5)
            est_cost = cost_estimates.get(comp, 300) + est_time * 120
        else:
            est_time = 2.0
            est_cost = 500
            
        return round(est_time, 1), round(est_cost, 2)
    
    def _calculate_confidence(self, probabilities: List[Dict]) -> float:
        """Calcula confiança geral do diagnóstico"""
        if not probabilities:
            return 0
        return round(sum(p['probability'] * p.get('confidence', 80) for p in probabilities) / 
                    sum(p['probability'] for p in probabilities) / 100, 2)
    
    def get_diagnostic_summary(self, dtc: str) -> str:
        """Retorna resumo do diagnóstico em formato texto"""
        recent = [d for d in self.diagnostic_history if d['dtc'] == dtc]
        if not recent:
            return f"Nenhum diagnóstico recente para {dtc}"
            
        d = recent[-1]
        
        summary = f"""
        🔍 DIAGNÓSTICO: {d['dtc']} - {d['description']}
        {'='*50}
        📊 SEVERIDADE: {d['severity']}
        🎯 CONFIANÇA: {d['confidence']*100:.0f}%
        
        📈 PROBABILIDADES:
        """
        
        for p in d['probabilities'][:3]:
            summary += f"\n   • {p['component']}: {p['probability']:.0f}%"
            
        summary += f"\n\n✅ RECOMENDAÇÕES:"
        for r in d['recommendations'][:3]:
            summary += f"\n   {r}"
            
        summary += f"\n\n⏱️ TEMPO ESTIMADO: {d['estimated_repair_time']}h"
        summary += f"\n💰 CUSTO ESTIMADO: R$ {d['estimated_cost']:.2f}"
        
        return summary
