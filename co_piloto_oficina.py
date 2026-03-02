# co_piloto_oficina.py - Sistema de Diagnóstico com IA

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
from datetime import datetime
import time

# =============================================
# 1. BASE DE CONHECIMENTO RAG (Retrieval-Augmented Generation)
# =============================================

@dataclass
class TechnicalBulletin:
    """Boletim Técnico (TSB)"""
    bulletin_id: str
    manufacturer: str
    models: List[str]
    years: List[int]
    dtc_codes: List[str]
    symptoms: List[str]
    root_cause: str
    solution: str
    parts_needed: List[str]
    labor_time: float
    confidence_score: float

@dataclass
class WiringDiagram:
    """Esquema Elétrico"""
    component: str
    pinout: Dict[int, str]
    wire_colors: Dict[int, str]
    expected_voltage: Dict[str, Tuple[float, float]]
    expected_resistance: Dict[str, Tuple[float, float]]
    connector_location: str
    diagram_url: str

@dataclass
class ComponentFailureProbability:
    """Probabilidade de falha de componente"""
    component: str
    probability: float
    confidence: float
    symptoms_matched: List[str]
    recommended_test: str
    expected_values: Dict[str, Tuple[float, float]]
    part_number: Optional[str] = None

class KnowledgeBaseRAG:
    """
    Base de conhecimento com RAG (Retrieval-Augmented Generation)
    Integra TSBs, esquemas elétricos e casos resolvidos
    """
    
    def __init__(self):
        self.tsb_database = self._load_tsb_database()
        self.wiring_database = self._load_wiring_database()
        self.resolved_cases = self._load_resolved_cases()
        
    def _load_tsb_database(self) -> Dict[str, TechnicalBulletin]:
        """Carrega boletins técnicos"""
        return {
            'VW_P0300_2023': TechnicalBulletin(
                bulletin_id='VW-23-05',
                manufacturer='VOLKSWAGEN',
                models=['Gol', 'Polo', 'Virtus', 'T-Cross'],
                years=[2020, 2021, 2022, 2023],
                dtc_codes=['P0300', 'P0301', 'P0302', 'P0303', 'P0304'],
                symptoms=['Falha intermitente', 'Marcha lenta irregular', 'Perda de potência'],
                root_cause='Bobinas de ignição EA211 com falha prematura devido à expansão térmica',
                solution='Substituir bobinas (06K905110) e velas (04C905616)',
                parts_needed=['06K905110', '04C905616'],
                labor_time=1.5,
                confidence_score=0.95
            ),
            'FIA_P0420_2024': TechnicalBulletin(
                bulletin_id='FIA-24-02',
                manufacturer='FIAT',
                models=['Argo', 'Cronos', 'Toro', 'Pulse'],
                years=[2021, 2022, 2023, 2024],
                dtc_codes=['P0420'],
                symptoms=['Luz da injeção acesa', 'Aumento de consumo'],
                root_cause='Sonda lambda após catalisador com falha no aquecimento',
                solution='Substituir sonda lambda (55236131) e verificar catalisador',
                parts_needed=['55236131'],
                labor_time=0.8,
                confidence_score=0.88
            ),
            'CHEV_P0171_2023': TechnicalBulletin(
                bulletin_id='CHEV-23-11',
                manufacturer='CHEVROLET',
                models=['Onix', 'Onix Plus', 'Tracker', 'Cruze'],
                years=[2020, 2021, 2022, 2023],
                dtc_codes=['P0171', 'P0174'],
                symptoms=['Mistura pobre', 'Marcha lenta instável'],
                root_cause='Sensor MAF contaminado por óleo do filtro de ar',
                solution='Limpar sensor MAF com cleaner específico (89024122)',
                parts_needed=['89024122'],
                labor_time=0.3,
                confidence_score=0.92
            ),
            'FOR_P0300_2023': TechnicalBulletin(
                bulletin_id='FOR-23-08',
                manufacturer='FORD',
                models=['Ka', 'Fiesta', 'EcoSport', 'Ranger'],
                years=[2020, 2021, 2022, 2023],
                dtc_codes=['P0300', 'P0301'],
                symptoms=['Motor engasgando', 'Falha na aceleração'],
                root_cause='Bobinas do motor Sigma com isolamento danificado',
                solution='Substituir bobinas (CM5G-12A366-BA)',
                parts_needed=['CM5G-12A366-BA'],
                labor_time=1.2,
                confidence_score=0.91
            ),
            'TOY_P0300_2024': TechnicalBulletin(
                bulletin_id='TOY-24-01',
                manufacturer='TOYOTA',
                models=['Corolla', 'Hilux', 'Yaris'],
                years=[2021, 2022, 2023, 2024],
                dtc_codes=['P0300', 'P0301'],
                symptoms=['Falha de ignição', 'Motor irregular'],
                root_cause='Velas de ignição com desgaste prematuro',
                solution='Substituir velas (90919-01256)',
                parts_needed=['90919-01256'],
                labor_time=0.8,
                confidence_score=0.89
            ),
            'HON_P0420_2024': TechnicalBulletin(
                bulletin_id='HON-24-03',
                manufacturer='HONDA',
                models=['Civic', 'HR-V', 'Fit'],
                years=[2020, 2021, 2022, 2023],
                dtc_codes=['P0420'],
                symptoms=['Catalisador ineficiente'],
                root_cause='Sensor O2 pós-catalisador com falha',
                solution='Substituir sensor O2 (36531-5R0-003)',
                parts_needed=['36531-5R0-003'],
                labor_time=0.6,
                confidence_score=0.87
            )
        }
    
    def _load_wiring_database(self) -> Dict[str, WiringDiagram]:
        """Carrega esquemas elétricos"""
        return {
            'VW_COIL': WiringDiagram(
                component='Bobina de Ignição',
                pinout={1: 'Alimentação 12V', 2: 'GND', 3: 'Sinal da ECU'},
                wire_colors={1: 'Vermelho/Branco', 2: 'Marrom', 3: 'Verde/Roxo'},
                expected_voltage={'ignicao_on': (11.5, 14.5), 'motor_ligado': (13.0, 14.5)},
                expected_resistance={'primario': (0.5, 1.5), 'secundario': (5000, 10000)},
                connector_location='Lado direito do motor, próximo à válvula borboleta',
                diagram_url='/diagrams/vw_coil.png'
            ),
            'VW_O2': WiringDiagram(
                component='Sonda Lambda',
                pinout={1: 'Sinal', 2: 'GND', 3: 'Aquecimento +', 4: 'Aquecimento -'},
                wire_colors={1: 'Preto', 2: 'Cinza', 3: 'Vermelho', 4: 'Marrom'},
                expected_voltage={'sinal': (0.1, 0.9), 'aquecimento': (11.5, 14.5)},
                expected_resistance={'aquecimento': (3.0, 5.0)},
                connector_location='No escapamento, após o catalisador',
                diagram_url='/diagrams/vw_o2.png'
            ),
            'FIA_INJECTOR': WiringDiagram(
                component='Injetor de Combustível',
                pinout={1: 'Alimentação', 2: 'Sinal ECU'},
                wire_colors={1: 'Azul', 2: 'Marrom'},
                expected_voltage={'alimentacao': (11.5, 14.5)},
                expected_resistance={'bobina': (12.0, 17.0)},
                connector_location='No trilho de combustível',
                diagram_url='/diagrams/fia_injector.png'
            ),
            'FIA_O2': WiringDiagram(
                component='Sonda Lambda Firefly',
                pinout={1: 'Sinal', 2: 'GND', 3: 'Aquecimento +', 4: 'Aquecimento -'},
                wire_colors={1: 'Branco', 2: 'Cinza', 3: 'Vermelho', 4: 'Preto'},
                expected_voltage={'sinal': (0.1, 0.9), 'aquecimento': (11.5, 14.5)},
                expected_resistance={'aquecimento': (3.5, 4.5)},
                connector_location='No escapamento, próximo ao catalisador',
                diagram_url='/diagrams/fia_o2.png'
            ),
            'CHEV_MAF': WiringDiagram(
                component='Sensor MAF',
                pinout={1: 'Alimentação', 2: 'Sinal', 3: 'GND'},
                wire_colors={1: 'Vermelho', 2: 'Amarelo', 3: 'Preto'},
                expected_voltage={'sinal': (0.5, 1.5)},
                expected_resistance={'alimentacao': (10000, 20000)},
                connector_location='No duto de ar, após o filtro',
                diagram_url='/diagrams/chev_maf.png'
            ),
            'TOY_COIL': WiringDiagram(
                component='Bobina de Ignição',
                pinout={1: 'Alimentação', 2: 'GND', 3: 'Sinal'},
                wire_colors={1: 'Vermelho', 2: 'Marrom', 3: 'Azul'},
                expected_voltage={'ignicao_on': (11.5, 14.5)},
                expected_resistance={'primario': (0.8, 1.2)},
                connector_location='Na tampa das velas',
                diagram_url='/diagrams/toy_coil.png'
            )
        }
    
    def _load_resolved_cases(self) -> List[Dict]:
        """Carrega casos resolvidos anteriores"""
        return [
            {
                'case_id': 'CASE-2024-001',
                'vehicle': 'VW Gol 2022',
                'dtc': 'P0302',
                'symptoms': ['Falha cilindro 2', 'Perda de potência'],
                'live_data': {'rpm': 850, 'stft': 8.5, 'ltft': 12.3, 'o2_v': 0.78},
                'diagnosis': 'Bobina do cilindro 2 com curto interno',
                'solution': 'Troca da bobina (06K905110)',
                'verified': True
            },
            {
                'case_id': 'CASE-2024-002',
                'vehicle': 'Fiat Argo 2023',
                'dtc': 'P0420',
                'symptoms': ['Catalisador ineficiente', 'Cheiro de combustível'],
                'live_data': {'o2_pre': 0.65, 'o2_pos': 0.58, 'stft': 5.2},
                'diagnosis': 'Sonda lambda pós-catalisador com falha no aquecimento',
                'solution': 'Troca da sonda lambda (55236131)',
                'verified': True
            },
            {
                'case_id': 'CASE-2024-003',
                'vehicle': 'Chevrolet Onix 2021',
                'dtc': 'P0171',
                'symptoms': ['Mistura pobre', 'Marcha lenta instável'],
                'live_data': {'stft': 18.5, 'ltft': 22.3, 'maf': 2.1},
                'diagnosis': 'Sensor MAF contaminado',
                'solution': 'Limpeza do sensor MAF com cleaner específico',
                'verified': True
            },
            {
                'case_id': 'CASE-2024-004',
                'vehicle': 'Toyota Corolla 2023',
                'dtc': 'P0301',
                'symptoms': ['Falha cilindro 1', 'Motor irregular'],
                'live_data': {'rpm': 820, 'stft': 3.2, 'ltft': 4.1},
                'diagnosis': 'Vela de ignição desgastada',
                'solution': 'Troca das velas (90919-01256)',
                'verified': True
            },
            {
                'case_id': 'CASE-2024-005',
                'vehicle': 'Honda HR-V 2022',
                'dtc': 'P0420',
                'symptoms': ['Catalisador ineficiente'],
                'live_data': {'o2_pre': 0.72, 'o2_pos': 0.68, 'stft': 2.1},
                'diagnosis': 'Sensor O2 pós-catalisador com falha',
                'solution': 'Troca do sensor O2 (36531-5R0-003)',
                'verified': True
            }
        ]
    
    def retrieve_relevant_info(self, dtc: str, manufacturer: str, 
                                model: str, year: int) -> Dict:
        """
        Recupera informações relevantes baseado no contexto
        Similar ao RAG - busca semântica
        """
        results = {
            'tsb': [],
            'wiring': [],
            'similar_cases': []
        }
        
        # Busca TSBs relevantes
        for tsb_id, tsb in self.tsb_database.items():
            if (tsb.manufacturer == manufacturer and 
                dtc in tsb.dtc_codes and
                year in tsb.years):
                results['tsb'].append({
                    'id': tsb.bulletin_id,
                    'root_cause': tsb.root_cause,
                    'solution': tsb.solution,
                    'parts': tsb.parts_needed,
                    'confidence': tsb.confidence_score
                })
        
        # Busca esquemas elétricos relacionados
        if 'P030' in dtc:
            if manufacturer == 'VOLKSWAGEN':
                results['wiring'].append(self._format_wiring('VW_COIL'))
            elif manufacturer == 'TOYOTA':
                results['wiring'].append(self._format_wiring('TOY_COIL'))
        elif 'P042' in dtc:
            if manufacturer == 'FIAT':
                results['wiring'].append(self._format_wiring('FIA_O2'))
            elif manufacturer == 'VOLKSWAGEN':
                results['wiring'].append(self._format_wiring('VW_O2'))
        elif 'P017' in dtc:
            if manufacturer == 'CHEVROLET':
                results['wiring'].append(self._format_wiring('CHEV_MAF'))
            elif manufacturer == 'FIAT':
                results['wiring'].append(self._format_wiring('FIA_INJECTOR'))
        
        # Busca casos similares
        for case in self.resolved_cases:
            if case['dtc'] == dtc and case['verified']:
                results['similar_cases'].append({
                    'vehicle': case['vehicle'],
                    'symptoms': case['symptoms'],
                    'diagnosis': case['diagnosis'],
                    'solution': case['solution']
                })
        
        return results
    
    def _format_wiring(self, key: str) -> Dict:
        """Formata esquema elétrico para saída"""
        if key in self.wiring_database:
            w = self.wiring_database[key]
            return {
                'component': w.component,
                'pinout': w.pinout,
                'wire_colors': w.wire_colors,
                'expected_voltage': w.expected_voltage,
                'expected_resistance': w.expected_resistance,
                'connector_location': w.connector_location
            }
        return {}


# =============================================
# 2. MOTOR DE DIAGNÓSTICO PROBABILÍSTICO
# =============================================

class LiveDataAnalyzer:
    """
    Analisa dados em tempo real e calcula probabilidades
    """
    
    def __init__(self):
        self.normal_ranges = {
            'short_term_fuel_trim': (-10, 10),
            'long_term_fuel_trim': (-15, 15),
            'o2_voltage': (0.1, 0.9),
            'o2_cross_count': (5, 20),
            'maf': (2.5, 6.0),
            'map': (25, 45),
            'rpm_deviation': (-100, 100),
            'coolant_temp': (80, 100),
            'engine_load': (15, 45),
            'timing_advance': (8, 22)
        }
        
        self.failure_patterns = self._load_failure_patterns()
    
    def _load_failure_patterns(self) -> Dict:
        """Carrega padrões de falha"""
        return {
            'lean_mixture': {
                'components': ['MAF_SENSOR', 'O2_SENSOR', 'VACUUM_LEAK', 'FUEL_PRESSURE'],
                'patterns': [
                    {'pid': 'short_term_fuel_trim', 'condition': '> 10', 'weight': 0.35},
                    {'pid': 'long_term_fuel_trim', 'condition': '> 15', 'weight': 0.35},
                    {'pid': 'o2_voltage', 'condition': '< 0.45', 'weight': 0.15},
                    {'pid': 'maf', 'condition': '< 2.5', 'weight': 0.15}
                ]
            },
            'misfire': {
                'components': ['COIL', 'SPARK_PLUG', 'INJECTOR', 'COMPRESSION'],
                'patterns': [
                    {'pid': 'rpm', 'condition': 'fluctuating', 'weight': 0.4},
                    {'pid': 'short_term_fuel_trim', 'condition': 'fluctuating', 'weight': 0.3},
                    {'pid': 'o2_voltage', 'condition': 'fluctuating', 'weight': 0.3}
                ]
            },
            'catalyst_failure': {
                'components': ['CATALYST', 'O2_SENSOR_POST'],
                'patterns': [
                    {'pid': 'o2_voltage', 'condition': '> 0.6', 'weight': 0.3},
                    {'pid': 'o2_cross_count', 'condition': '< 3', 'weight': 0.4},
                    {'pid': 'long_term_fuel_trim', 'condition': '> 5', 'weight': 0.3}
                ]
            },
            'rich_mixture': {
                'components': ['MAF_SENSOR', 'O2_SENSOR', 'INJECTOR', 'FUEL_PRESSURE'],
                'patterns': [
                    {'pid': 'short_term_fuel_trim', 'condition': '< -10', 'weight': 0.35},
                    {'pid': 'long_term_fuel_trim', 'condition': '< -15', 'weight': 0.35},
                    {'pid': 'o2_voltage', 'condition': '> 0.8', 'weight': 0.15},
                    {'pid': 'maf', 'condition': '> 6.0', 'weight': 0.15}
                ]
            },
            'ignition_failure': {
                'components': ['COIL', 'SPARK_PLUG', 'CKP_SENSOR'],
                'patterns': [
                    {'pid': 'rpm', 'condition': 'erratic', 'weight': 0.5},
                    {'pid': 'timing_advance', 'condition': '< 5', 'weight': 0.3},
                    {'pid': 'engine_load', 'condition': 'fluctuating', 'weight': 0.2}
                ]
            }
        }
    
    def calculate_probabilities(self, dtc: str, live_data: Dict,
                                 history: List[Dict]) -> List[ComponentFailureProbability]:
        """
        Calcula probabilidades de falha baseado em dados ao vivo
        """
        results = []
        
        # Mapeia DTC para padrões de falha
        dtc_pattern_map = {
            'P0171': 'lean_mixture',
            'P0174': 'lean_mixture',
            'P0172': 'rich_mixture',
            'P0175': 'rich_mixture',
            'P0300': 'misfire',
            'P0301': 'misfire',
            'P0302': 'misfire',
            'P0303': 'misfire',
            'P0304': 'misfire',
            'P0305': 'misfire',
            'P0306': 'misfire',
            'P0420': 'catalyst_failure',
            'P0430': 'catalyst_failure',
            'P0350': 'ignition_failure',
            'P0351': 'ignition_failure',
            'P0352': 'ignition_failure',
            'P0353': 'ignition_failure',
            'P0354': 'ignition_failure'
        }
        
        pattern_key = dtc_pattern_map.get(dtc)
        if not pattern_key:
            return results
        
        pattern = self.failure_patterns.get(pattern_key, {})
        
        # Analisa cada componente candidato
        for component in pattern.get('components', []):
            probability = self._calculate_component_probability(
                component, pattern, live_data, history
            )
            
            if probability > 0.3:  # Threshold mínimo
                results.append(self._create_probability_report(
                    component, probability, live_data
                ))
        
        # Ordena por probabilidade
        results.sort(key=lambda x: x.probability, reverse=True)
        
        return results
    
    def _calculate_component_probability(self, component: str,
                                          pattern: Dict,
                                          live_data: Dict,
                                          history: List[Dict]) -> float:
        """Calcula probabilidade para um componente específico"""
        total_weight = 0.0
        matched_weight = 0.0
        
        for pattern_item in pattern.get('patterns', []):
            pid = pattern_item['pid']
            condition = pattern_item['condition']
            weight = pattern_item['weight']
            
            if pid in live_data:
                if self._check_condition(live_data[pid], condition, history, pid):
                    matched_weight += weight
                total_weight += weight
        
        if total_weight > 0:
            return matched_weight / total_weight
        return 0.0
    
    def _check_condition(self, value: float, condition: str,
                          history: List[Dict], pid: str) -> bool:
        """Verifica condição do padrão"""
        try:
            if '>' in condition:
                threshold = float(condition.split('>')[1])
                return value > threshold
            elif '<' in condition:
                threshold = float(condition.split('<')[1])
                return value < threshold
            elif 'fluctuating' in condition or 'erratic' in condition:
                # Verifica variação no histórico
                if len(history) > 5:
                    recent = [h.get(pid, 0) for h in history[-5:]]
                    variance = np.var(recent) if len(recent) > 0 else 0
                    return variance > 50 if pid == 'rpm' else variance > 1.0
        except:
            pass
        return False
    
    def _create_probability_report(self, component: str,
                                    probability: float,
                                    live_data: Dict) -> ComponentFailureProbability:
        """Cria relatório de probabilidade"""
        
        # Define testes recomendados baseado no componente
        tests = {
            'COIL': {
                'test': 'Medir resistência primária entre pinos 1 e 2 (0.5-1.5Ω)',
                'values': {'resistencia_primaria': (0.5, 1.5)}
            },
            'SPARK_PLUG': {
                'test': 'Verificar folga do eletrodo (0.8-1.1mm) e depósitos',
                'values': {'folga': (0.8, 1.1)}
            },
            'INJECTOR': {
                'test': 'Medir resistência da bobina (12-17Ω) e verificar padrão de spray',
                'values': {'resistencia': (12.0, 17.0)}
            },
            'O2_SENSOR': {
                'test': 'Medir resistência do aquecimento entre pinos 3 e 4 (3-5Ω)',
                'values': {'resistencia_aquecimento': (3.0, 5.0)}
            },
            'O2_SENSOR_POST': {
                'test': 'Medir resistência do aquecimento (3-5Ω) e verificar tensão pós-catalisador',
                'values': {'resistencia_aquecimento': (3.0, 5.0)}
            },
            'MAF_SENSOR': {
                'test': 'Verificar tensão de saída com scanner (0.5-1.5V em marcha lenta)',
                'values': {'tensao_saida': (0.5, 1.5)}
            },
            'VACUUM_LEAK': {
                'test': 'Usar spray de carburador ao redor das mangueiras com STFT monitorado',
                'values': {'stft_variacao': (5.0, 20.0)}
            },
            'FUEL_PRESSURE': {
                'test': 'Instalar manômetro no trilho (pressão deve ser 3.0-4.0 bar)',
                'values': {'pressao': (3.0, 4.0)}
            },
            'CATALYST': {
                'test': 'Medir temperatura na entrada e saída (diferença > 100°C em carga)',
                'values': {'diferenca_temp': (100.0, 300.0)}
            },
            'COMPRESSION': {
                'test': 'Teste de compressão (mínimo 120 psi, variação < 10% entre cilindros)',
                'values': {'compressao': (120.0, 180.0)}
            },
            'CKP_SENSOR': {
                'test': 'Verificar sinal com osciloscópio e resistência (500-900Ω)',
                'values': {'resistencia': (500.0, 900.0)}
            }
        }
        
        test_info = tests.get(component, {
            'test': 'Verificar componente com multímetro',
            'values': {}
        })
        
        # Mapeia números de peça
        part_numbers = {
            'COIL': '06K905110',
            'SPARK_PLUG': '04C905616',
            'INJECTOR': '0261500298',
            'O2_SENSOR': '55236131',
            'O2_SENSOR_POST': '36531-5R0-003',
            'MAF_SENSOR': '0281006322',
            'FUEL_PRESSURE': '13577583',
            'CKP_SENSOR': '06A906433A'
        }
        
        return ComponentFailureProbability(
            component=component,
            probability=round(probability * 100, 1),
            confidence=round(min(0.95, probability + 0.2) * 100, 1),
            symptoms_matched=[],
            recommended_test=test_info['test'],
            expected_values=test_info['values'],
            part_number=part_numbers.get(component)
        )


# =============================================
# 3. ASSISTENTE DE CONFIRMAÇÃO RÁPIDA
# =============================================

class QuickTestAssistant:
    """
    Sugere testes rápidos para confirmar diagnóstico
    """
    
    def __init__(self):
        self.test_procedures = self._load_test_procedures()
    
    def _load_test_procedures(self) -> Dict:
        """Carrega procedimentos de teste rápido"""
        return {
            'COIL': {
                'name': 'Teste Rápido de Bobina',
                'steps': [
                    '1. Desconecte o conector da bobina',
                    '2. Meça resistência entre os pinos 1 e 2 (primário)',
                    '3. Valor esperado: 0.5 a 1.5 ohms',
                    '4. Meça resistência entre o terminal de alta tensão e massa',
                    '5. Valor esperado: 5k a 10k ohms',
                    '6. Com scanner, monitore contagem de falhas por cilindro'
                ],
                'time_seconds': 120,
                'tools': ['Multímetro', 'Scanner'],
                'confirmation': 'Se fora da faixa ou falha persistente, bobina com defeito'
            },
            'O2_SENSOR': {
                'name': 'Teste Rápido de Sonda Lambda',
                'steps': [
                    '1. Com scanner, monitore tensão da sonda pré-catalisador',
                    '2. Motor em marcha lenta: tensão deve variar 0.1-0.9V',
                    '3. Acelere rapidamente a 3000 RPM: deve ir a 0.9V',
                    '4. Desacelere bruscamente: deve cair a 0.1V',
                    '5. A frequência de oscilação deve ser > 5 vezes em 10 segundos'
                ],
                'time_seconds': 180,
                'tools': ['Scanner'],
                'confirmation': 'Se não variar ou resposta lenta, sensor com defeito'
            },
            'MAF_SENSOR': {
                'name': 'Teste Rápido de Sensor MAF',
                'steps': [
                    '1. Com scanner, leia valor do MAF em marcha lenta',
                    '2. Valor esperado: 2.5 a 4.5 g/s (depende da cilindrada)',
                    '3. Acelere até 2500 RPM e segure',
                    '4. Valor deve subir proporcionalmente (6-12 g/s)',
                    '5. Desacelere: valor deve cair suavemente'
                ],
                'time_seconds': 90,
                'tools': ['Scanner'],
                'confirmation': 'Se valor baixo, errático ou sem resposta, sensor sujo ou com defeito'
            },
            'VACUUM_LEAK': {
                'name': 'Teste de Vazamento de Vácuo',
                'steps': [
                    '1. Com scanner, monitore Short Term Fuel Trim (STFT)',
                    '2. Em marcha lenta, STFT deve estar entre -10 e +10',
                    '3. Se STFT > +10, suspeite de vazamento',
                    '4. Use spray de carburador ou propano ao redor das mangueiras',
                    '5. Se STFT mudar drasticamente (>5%), localizou o vazamento',
                    '6. Verifique mangueiras, gaxeta do coletor, válvula PCV'
                ],
                'time_seconds': 240,
                'tools': ['Scanner', 'Spray de teste ou propano'],
                'confirmation': 'Mudança no STFT indica local do vazamento'
            },
            'FUEL_PRESSURE': {
                'name': 'Teste de Pressão de Combustível',
                'steps': [
                    '1. Instale manômetro no trilho de combustível',
                    '2. Com ignição ligada (motor desligado): pressão deve subir e segurar',
                    '3. Valor esperado: 3.0 a 4.0 bar (depende do sistema)',
                    '4. Motor em marcha lenta: pressão deve manter',
                    '5. Acelere: pressão pode subir ligeiramente',
                    '6. Desligue: pressão deve cair lentamente (> 30 segundos)'
                ],
                'time_seconds': 300,
                'tools': ['Manômetro de combustível'],
                'confirmation': 'Pressão baixa indica bomba fraca ou regulador; queda rápida indica vazamento'
            },
            'INJECTOR': {
                'name': 'Teste Rápido de Injetor',
                'steps': [
                    '1. Com estetoscópio mecânico, escute o clique do injetor',
                    '2. Deve ter clique rítmico e uniforme',
                    '3. Meça resistência entre os terminais: 12-17 ohms',
                    '4. Compare com outros cilindros',
                    '5. Com scanner, desative cada injetor e veja variação no RPM'
                ],
                'time_seconds': 180,
                'tools': ['Multímetro', 'Estetoscópio', 'Scanner'],
                'confirmation': 'Falta de clique, resistência fora ou RPM não varia indica injetor com defeito'
            },
            'COMPRESSION': {
                'name': 'Teste de Compressão',
                'steps': [
                    '1. Remova todos os cabos de vela e fusível da bomba',
                    '2. Instale manômetro no cilindro 1',
                    '3. Dê partida por 5 segundos',
                    '4. Anote o valor máximo',
                    '5. Repita para todos os cilindros',
                    '6. Compressão mínima: 120 psi',
                    '7. Variação entre cilindros: < 10%'
                ],
                'time_seconds': 600,
                'tools': ['Manômetro de compressão'],
                'confirmation': 'Baixa compressão indica problemas em anéis, válvulas ou junta'
            },
            'CKP_SENSOR': {
                'name': 'Teste do Sensor de Rotação',
                'steps': [
                    '1. Desconecte o sensor',
                    '2. Meça resistência entre os terminais: 500-900 ohms',
                    '3. Verifique folga do anel fônico (0.5-1.5mm)',
                    '4. Com osciloscópio, verifique forma de onda'
                ],
                'time_seconds': 240,
                'tools': ['Multímetro', 'Osciloscópio'],
                'confirmation': 'Resistência fora ou sem sinal indica sensor com defeito'
            },
            'CATALYST': {
                'name': 'Teste de Catalisador',
                'steps': [
                    '1. Com scanner, monitore O2 pré e pós-catalisador',
                    '2. Motor em 2500 RPM: O2 pré deve oscilar, O2 pós deve estar estável',
                    '3. Meça temperatura na entrada e saída com termômetro infravermelho',
                    '4. Diferença deve ser > 100°C em carga'
                ],
                'time_seconds': 300,
                'tools': ['Scanner', 'Termômetro infravermelho'],
                'confirmation': 'O2 pós seguindo o pré ou diferença de temperatura baixa indica catalisador ineficiente'
            }
        }
    
    def get_quick_test(self, component: str) -> Dict:
        """Retorna teste rápido para o componente"""
        if component in self.test_procedures:
            test = self.test_procedures[component]
            return {
                'name': test['name'],
                'steps': test['steps'],
                'time_seconds': test['time_seconds'],
                'time_minutes': round(test['time_seconds'] / 60, 1),
                'tools': test['tools'],
                'confirmation': test['confirmation']
            }
        
        # Teste genérico
        return {
            'name': 'Teste Genérico',
            'steps': ['Consulte o manual de serviço do veículo'],
            'time_seconds': 300,
            'time_minutes': 5.0,
            'tools': ['Scanner', 'Multímetro'],
            'confirmation': 'Verifique especificações do fabricante'
        }
    
    def get_test_by_dtc(self, dtc: str, probabilities: List[ComponentFailureProbability]) -> List[Dict]:
        """Retorna testes recomendados baseado no DTC e probabilidades"""
        tests = []
        
        for prob in probabilities:
            test = self.get_quick_test(prob.component)
            test['component'] = prob.component
            test['probability'] = prob.probability
            test['part_number'] = prob.part_number
            tests.append(test)
        
        return tests


# =============================================
# 4. CO-PILOTO PRINCIPAL
# =============================================

class CoPilotoOficina:
    """
    Assistente inteligente para diagnóstico automotivo
    Integra RAG, análise probabilística e testes rápidos
    """
    
    def __init__(self):
        self.knowledge_base = KnowledgeBaseRAG()
        self.data_analyzer = LiveDataAnalyzer()
        self.test_assistant = QuickTestAssistant()
        self.diagnostic_history = []
        
    def diagnose(self, dtc: str, live_data: Dict, history: List[Dict],
                 vehicle_info: Dict) -> Dict:
        """
        Diagnóstico completo integrando todas as fontes
        """
        result = {
            'dtc': dtc,
            'timestamp': datetime.now().isoformat(),
            'vehicle': vehicle_info,
            'probabilities': [],
            'knowledge_base': {},
            'recommended_tests': [],
            'final_recommendation': {},
            'confidence_score': 0,
            'success': True
        }
        
        # 1. Análise probabilística
        probabilities = self.data_analyzer.calculate_probabilities(
            dtc, live_data, history
        )
        result['probabilities'] = [
            {
                'component': p.component,
                'probability': p.probability,
                'confidence': p.confidence,
                'part_number': p.part_number,
                'recommended_test': p.recommended_test
            }
            for p in probabilities
        ]
        
        # 2. Busca na base de conhecimento
        kb_info = self.knowledge_base.retrieve_relevant_info(
            dtc,
            vehicle_info.get('manufacturer', ''),
            vehicle_info.get('model', ''),
            vehicle_info.get('year', 0)
        )
        result['knowledge_base'] = kb_info
        
        # 3. Recomenda testes
        tests = self.test_assistant.get_test_by_dtc(dtc, probabilities)
        result['recommended_tests'] = tests
        
        # 4. Gera recomendação final
        result['final_recommendation'] = self._generate_recommendation(
            probabilities, kb_info, tests
        )
        
        # 5. Calcula confiança geral
        if probabilities:
            result['confidence_score'] = round(
                sum(p.confidence for p in probabilities) / len(probabilities), 1
            )
        
        # Salva no histórico
        self.diagnostic_history.append(result)
        
        return result
    
    def _generate_recommendation(self, probabilities: List[ComponentFailureProbability],
                                   kb_info: Dict, tests: List[Dict]) -> Dict:
        """Gera recomendação final consolidada"""
        
        if not probabilities:
            return {
                'priority': 'BAIXA',
                'message': 'Não foi possível determinar a causa com os dados atuais',
                'action': 'Execute testes manuais ou consulte TSBs',
                'action_plan': ['1. Execute diagnóstico manual', '2. Consulte TSBs do fabricante']
            }
        
        # Componente mais provável
        top = probabilities[0]
        
        # Busca TSB correspondente
        tsb_match = None
        for tsb in kb_info.get('tsb', []):
            if top.component.replace('_', ' ') in tsb.get('solution', '').upper():
                tsb_match = tsb
                break
        
        recommendation = {
            'priority': 'ALTA' if top.probability > 70 else 'MÉDIA',
            'primary_suspect': {
                'component': top.component,
                'probability': top.probability,
                'confidence': top.confidence,
                'part_number': top.part_number
            },
            'recommended_test': tests[0] if tests else None,
            'action_plan': []
        }
        
        # Plano de ação
        recommendation['action_plan'].append(f"1. {top.recommended_test}")
        
        if tsb_match:
            recommendation['action_plan'].append(
                f"2. Boletim Técnico: {tsb_match['root_cause']}"
            )
            recommendation['action_plan'].append(
                f"3. Solução TSB: {tsb_match['solution']}"
            )
        else:
            recommendation['action_plan'].append(
                "2. Consulte diagrama elétrico para localização do componente"
            )
        
        if len(probabilities) > 1:
            alt = probabilities[1]
            recommendation['action_plan'].append(
                f"4. Se não resolver, testar: {alt.component} ({alt.probability}%)"
            )
        
        return recommendation
    
    def explain_diagnosis(self, dtc: str) -> str:
        """Gera explicação textual do diagnóstico"""
        # Busca diagnósticos recentes
        recent = [d for d in self.diagnostic_history if d['dtc'] == dtc]
        if not recent:
            return f"Nenhum diagnóstico recente para {dtc}"
        
        latest = recent[-1]
        
        explanation = f"""
        🔍 DIAGNÓSTICO PARA {dtc}
        ================================
        Veículo: {latest['vehicle'].get('model', 'N/A')} {latest['vehicle'].get('year', '')}
        Confiança: {latest['confidence_score']}%
        
        📊 COMPONENTES MAIS PROVÁVEIS:
        """
        
        for p in latest['probabilities'][:3]:
            explanation += f"\n   • {p['component']}: {p['probability']}% de chance"
        
        explanation += f"\n\n✅ RECOMENDAÇÃO:\n   {latest['final_recommendation']['action_plan'][0]}"
        
        if latest['knowledge_base']['tsb']:
            tsb = latest['knowledge_base']['tsb'][0]
            explanation += f"\n\n📋 BOLETIM TÉCNICO:\n   {tsb['root_cause']}"
        
        return explanation


# =============================================
# 5. EXEMPLO DE USO
# =============================================

if __name__ == "__main__":
    # Inicializa o co-piloto
    copiloto = CoPilotoOficina()
    
    # Dados de exemplo - P0171 (Mistura Pobre)
    dtc_example = "P0171"
    
    live_data_example = {
        'short_term_fuel_trim': 18.5,
        'long_term_fuel_trim': 22.3,
        'o2_voltage': 0.32,
        'maf': 2.1,
        'rpm': 825,
        'coolant_temp': 89,
        'engine_load': 35,
        'timing_advance': 12
    }
    
    history_example = [
        {'short_term_fuel_trim': 17.2, 'o2_voltage': 0.35, 'rpm': 830},
        {'short_term_fuel_trim': 18.8, 'o2_voltage': 0.31, 'rpm': 820},
        {'short_term_fuel_trim': 19.5, 'o2_voltage': 0.28, 'rpm': 825}
    ]
    
    vehicle_info_example = {
        'manufacturer': 'VOLKSWAGEN',
        'model': 'Gol 1.6',
        'year': 2022,
        'engine': 'EA211'
    }
    
    # Executa diagnóstico
    resultado = copiloto.diagnose(
        dtc_example,
        live_data_example,
        history_example,
        vehicle_info_example
    )
    
    # Mostra resultado formatado
    print("=" * 50)
    print("DIAGNÓSTICO COMPLETO")
    print("=" * 50)
    print(f"DTC: {resultado['dtc']}")
    print(f"Confiança: {resultado['confidence_score']}%")
    print("\n📊 PROBABILIDADES:")
    for p in resultado['probabilities']:
        print(f"  • {p['component']}: {p['probability']}% (confiança: {p['confidence']}%)")
        print(f"    Teste: {p['recommended_test']}")
        if p['part_number']:
            print(f"    Peça: {p['part_number']}")
    
    print("\n📋 RECOMENDAÇÃO FINAL:")
    for step in resultado['final_recommendation']['action_plan']:
        print(f"  {step}")
    
    print("\n" + copiloto.explain_diagnosis(dtc_example))
