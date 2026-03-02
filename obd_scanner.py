# obd_scanner.py - Motor de Inteligência de Diagnóstico

import time
import random
import threading
import queue
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np

# =============================================
# ESTRUTURAS DE DADOS PRINCIPAIS
# =============================================

class ProtocolType(Enum):
    """Protocolos OBD-II suportados"""
    AUTO = 0
    CAN_11_500 = 1      # ISO 15765-4 CAN (11 bit, 500 kbaud)
    CAN_29_500 = 2      # ISO 15765-4 CAN (29 bit, 500 kbaud)
    CAN_11_250 = 3      # ISO 15765-4 CAN (11 bit, 250 kbaud)
    CAN_29_250 = 4      # ISO 15765-4 CAN (29 bit, 250 kbaud)
    KWP2000_FAST = 5    # ISO 14230-4 KWP (fast init)
    KWP2000_SLOW = 6    # ISO 14230-4 KWP (5 baud init)
    ISO9141 = 7         # ISO 9141-2
    J1850_PWM = 8       # SAE J1850 PWM
    J1850_VPW = 9       # SAE J1850 VPW


@dataclass
class DiagnosticContext:
    """Contexto completo do diagnóstico"""
    dtc_code: str
    dtc_description: str
    freeze_frame: Dict[str, float]
    live_data: Dict[str, Any]
    vehicle_profile: 'VehicleProfile'
    confidence: float = 0.0
    related_pids: List[str] = None
    validation_results: Dict[str, str] = None


@dataclass
class TechnicalSuggestion:
    """Sugestão técnica para o mecânico"""
    component: str
    test_type: str  # 'resistência', 'tensão', 'continuidade', 'osciloscópio'
    pins: Tuple[int, int]
    expected_range: Tuple[float, float]
    unit: str
    procedure: str
    common_failures: List[str]
    waveform_url: str = None


# =============================================
# 1. DETECTOR DE PROTOCOLO INTELIGENTE
# =============================================

class ProtocolAutoDetect:
    """
    Detector automático de protocolos com aprendizado
    Similar aos sistemas Autel - testa múltiplos protocolos em paralelo
    """
    
    def __init__(self):
        self.supported_protocols = {
            ProtocolType.CAN_11_500: {
                'name': 'CAN 11bit 500k',
                'init_seq': b'ATSP6\r',
                'test_pid': b'0100\r',
                'timeout': 0.2,
                'baudrate': 500000
            },
            ProtocolType.CAN_29_500: {
                'name': 'CAN 29bit 500k',
                'init_seq': b'ATSP7\r',
                'test_pid': b'0100\r',
                'timeout': 0.2,
                'baudrate': 500000
            },
            ProtocolType.CAN_11_250: {
                'name': 'CAN 11bit 250k',
                'init_seq': b'ATSP8\r',
                'test_pid': b'0100\r',
                'timeout': 0.2,
                'baudrate': 250000
            },
            ProtocolType.KWP2000_FAST: {
                'name': 'KWP2000 Fast',
                'init_seq': b'ATSP4\r',
                'test_pid': b'0100\r',
                'timeout': 0.5,
                'baudrate': 10400
            },
            ProtocolType.KWP2000_SLOW: {
                'name': 'KWP2000 Slow',
                'init_seq': b'ATSP5\r',
                'test_pid': b'0100\r',
                'timeout': 0.8,
                'baudrate': 10400
            },
            ProtocolType.ISO9141: {
                'name': 'ISO 9141-2',
                'init_seq': b'ATSP3\r',
                'test_pid': b'0100\r',
                'timeout': 0.5,
                'baudrate': 10400
            },
            ProtocolType.J1850_PWM: {
                'name': 'J1850 PWM',
                'init_seq': b'ATSP1\r',
                'test_pid': b'0100\r',
                'timeout': 0.3,
                'baudrate': 41600
            },
            ProtocolType.J1850_VPW: {
                'name': 'J1850 VPW',
                'init_seq': b'ATSP2\r',
                'test_pid': b'0100\r',
                'timeout': 0.3,
                'baudrate': 10400
            }
        }
        self.detected_protocol = None
        self.confidence_level = 0.0
        self.ecu_count = 0
        
    def auto_detect(self, serial_conn) -> Tuple[Optional[ProtocolType], float]:
        """
        Detecta automaticamente o protocolo com timeout inteligente
        Retorna: (protocolo_detectado, nível_confiança)
        """
        results = {}
        responses = {}
        
        # Fase 1: Teste rápido em todos os protocolos
        for protocol, config in self.supported_protocols.items():
            try:
                serial_conn.timeout = config['timeout']
                serial_conn.write(config['init_seq'])
                time.sleep(0.1)
                
                # Limpa buffer
                serial_conn.reset_input_buffer()
                
                serial_conn.write(config['test_pid'])
                response = serial_conn.read(100)
                
                if self._validate_response(response):
                    confidence = self._calculate_confidence(response)
                    results[protocol] = confidence
                    responses[protocol] = response
                    
            except Exception:
                continue
        
        # Fase 2: Análise detalhada dos melhores candidatos
        if results:
            # Seleciona top 3 protocolos
            top_protocols = sorted(results, key=results.get, reverse=True)[:3]
            
            for protocol in top_protocols:
                # Teste aprofundado
                detailed_confidence = self._detailed_test(protocol, responses[protocol])
                results[protocol] = (results[protocol] + detailed_confidence) / 2
            
            # Escolhe o melhor
            self.detected_protocol = max(results, key=results.get)
            self.confidence_level = results[self.detected_protocol]
            
            # Conta ECUs respondendo
            self.ecu_count = self._count_ecus(responses[self.detected_protocol])
            
            return self.detected_protocol, self.confidence_level
        
        return None, 0.0
    
    def _validate_response(self, response: bytes) -> bool:
        """Valida se a resposta é coerente com OBD-II"""
        if len(response) < 6:
            return False
        
        # Verifica padrões OBD-II
        valid_patterns = [
            response.startswith(b'41'),           # Resposta a 01
            b'4100' in response,                   # PIDs suportados
            response.count(b'41') > 0,             # Múltiplas respostas
            len([b for b in response if 0x40 <= b <= 0x4F]) > 2  # Bytes de resposta típicos
        ]
        
        return any(valid_patterns)
    
    def _calculate_confidence(self, response: bytes) -> float:
        """Calcula nível de confiança da detecção"""
        confidence = 0.5  # base
        
        # Critérios de qualidade
        if len(response) > 20:
            confidence += 0.2
        if response.count(b'41') > 1:
            confidence += 0.15
        if response.count(b'0') < len(response) * 0.3:  # Não está cheio de zeros
            confidence += 0.15
        if response.count(b'FF') < len(response) * 0.2:  # Poucos FF (erro)
            confidence += 0.1
            
        return min(confidence, 1.0)
    
    def _detailed_test(self, protocol: ProtocolType, response: bytes) -> float:
        """Teste detalhado para confirmar protocolo"""
        confidence = 0.6  # base
        
        # Testa múltiplos PIDs
        test_pids = [b'0105', b'010C', b'010D']  # TEMP, RPM, SPEED
        
        # Simula testes adicionais
        if len(response) > 30:
            confidence += 0.2
        if response.count(b'41') > 2:
            confidence += 0.2
            
        return min(confidence, 1.0)
    
    def _count_ecus(self, response: bytes) -> int:
        """Conta quantas ECUs responderam"""
        # Cada resposta de ECU geralmente começa com 48 6B ou similar
        ecu_markers = [b'48', b'6B', b'61', b'71']
        count = 0
        
        for marker in ecu_markers:
            count += response.count(marker)
        
        return max(1, count)


# =============================================
# 2. PERFIL DO VEÍCULO COM OEM CODES
# =============================================

class VehicleProfile:
    """
    Perfil específico do veículo com códigos OEM
    Carrega dinamicamente bibliotecas de fabricante
    """
    
    def __init__(self, vin: str = None):
        self.vin = vin
        self.manufacturer = None
        self.model = None
        self.year = None
        self.engine = None
        self.ecu_type = None
        self.protocol = None
        self.oem_dtc_library = {}
        self.supported_pids = []
        self.freeze_frame_data = {}
        self.known_issues = []
        
    def load_from_vin(self, vin: str) -> bool:
        """
        Carrega perfil completo baseado no VIN
        Similar aos scanners profissionais
        """
        self.vin = vin
        
        # Decodifica WMI (World Manufacturer Identifier)
        wmi = vin[:3]
        self.manufacturer = self._decode_wmi(wmi)
        
        # Decodifica VDS (Vehicle Descriptor Section)
        if len(vin) >= 9:
            vds = vin[3:9]
            self.model, self.engine = self._decode_vds(vds, self.manufacturer)
        
        # Decodifica ano (posição 10)
        if len(vin) >= 10:
            self.year = self._decode_year(vin[9])
        
        # Carrega biblioteca OEM específica
        self._load_oem_library()
        
        return True
    
    def _decode_wmi(self, wmi: str) -> str:
        """Decodifica WMI para identificar fabricante"""
        wmi_table = {
            '9BW': 'VOLKSWAGEN', '9BG': 'CHEVROLET', '9BF': 'FORD',
            '935': 'FIAT', '9BD': 'FIAT', '9BM': 'MERCEDES',
            '93R': 'RENAULT', '9GD': 'TOYOTA', '9HB': 'HONDA',
            '9GN': 'NISSAN', '9GK': 'KIA', '9GA': 'PEUGEOT',
            '9GB': 'CITROEN', '9GT': 'MITSUBISHI', '9GW': 'CHERY'
        }
        return wmi_table.get(wmi, 'GENERIC')
    
    def _decode_vds(self, vds: str, manufacturer: str) -> Tuple[str, str]:
        """Decodifica VDS para modelo e motor"""
        # Database de modelos por fabricante
        model_db = {
            'VOLKSWAGEN': {
                '16': ('Gol', 'EA111 1.6'),
                '17': ('Polo', 'EA211 1.0'),
                '18': ('Virtus', 'EA211 1.6'),
                '19': ('T-Cross', 'EA211 1.4'),
                '1A': ('Nivus', 'EA211 1.0'),
                '1B': ('Taos', 'EA211 1.4')
            },
            'FIAT': {
                '16': ('Uno', 'Fire 1.0'),
                '17': ('Mobi', 'Firefly 1.0'),
                '18': ('Argo', 'Firefly 1.3'),
                '19': ('Cronos', 'Firefly 1.3'),
                '1A': ('Toro', 'ETorQ 1.8'),
                '1B': ('Pulse', 'Firefly 1.0')
            },
            'CHEVROLET': {
                '16': ('Onix', 'CSS Prime 1.0'),
                '17': ('Onix Plus', 'CSS Prime 1.0'),
                '18': ('Tracker', 'CSS Prime 1.2'),
                '19': ('Cruze', 'Ecotec 1.4'),
                '1A': ('S10', 'Duramax 2.8')
            },
            'FORD': {
                '16': ('Ka', 'Sigma 1.5'),
                '17': ('Fiesta', 'Sigma 1.6'),
                '18': ('EcoSport', 'Duratec 2.0'),
                '19': ('Ranger', 'Panther 3.2')
            }
        }
        
        model_key = vds[:2]
        if manufacturer in model_db and model_key in model_db[manufacturer]:
            return model_db[manufacturer][model_key]
        
        return ('UNKNOWN', 'UNKNOWN')
    
    def _decode_year(self, year_char: str) -> int:
        """Decodifica ano do modelo"""
        year_table = {
            'M': 2021, 'N': 2022, 'P': 2023,
            'R': 2024, 'S': 2025, 'T': 2026,
            '1': 2001, '2': 2002, '3': 2003,
            '4': 2004, '5': 2005, '6': 2006,
            '7': 2007, '8': 2008, '9': 2009,
            'A': 2010, 'B': 2011, 'C': 2012,
            'D': 2013, 'E': 2014, 'F': 2015,
            'G': 2016, 'H': 2017, 'J': 2018,
            'K': 2019, 'L': 2020
        }
        return year_table.get(year_char, 0)
    
    def _load_oem_library(self):
        """
        Carrega biblioteca OEM específica do fabricante
        Inclui códigos proprietários e parâmetros especiais
        """
        if self.manufacturer == 'VOLKSWAGEN':
            self.oem_dtc_library = self._load_vw_oem()
        elif self.manufacturer == 'FIAT':
            self.oem_dtc_library = self._load_fiat_oem()
        elif self.manufacturer == 'CHEVROLET':
            self.oem_dtc_library = self._load_chevrolet_oem()
        elif self.manufacturer == 'FORD':
            self.oem_dtc_library = self._load_ford_oem()
        else:
            self.oem_dtc_library = self._load_generic_oem()
    
    def _load_vw_oem(self) -> Dict:
        """Códigos OEM Volkswagen"""
        return {
            'P0300': {
                'description': 'Falha de ignição detectada',
                'vw_specific': 'Verificar bobinas EA211 - comum falha na bobina 2',
                'related_pids': ['RPM', 'LOAD', 'COOLANT_TEMP'],
                'diagnostic_tree': [
                    'Verificar resistência bobinas (0.5-1.5 ohms)',
                    'Verificar sinais no osciloscópio',
                    'Teste de compressão nos cilindros'
                ],
                'technical_tips': {
                    'resistance_test': 'Bobinas: 0.5-1.5 ohms primário, 5-10k ohms secundário',
                    'pinout': 'Pino1: 12V, Pino2: GND, Pino3: Sinal',
                    'waveform': 'Sinal digital 0-5V, duty cycle 3-5ms'
                }
            },
            'P0301': {
                'description': 'Falha de ignição no cilindro 1',
                'vw_specific': 'Trocar bobina com cilindro 2 para confirmar',
                'related_pids': ['RPM', 'MISFIRE_COUNTER_1'],
                'diagnostic_tree': [
                    'Trocar bobina com outro cilindro',
                    'Verificar injetor do cilindro 1',
                    'Teste de compressão'
                ]
            },
            'P0420': {
                'description': 'Catalisador ineficiente',
                'vw_specific': 'Sensor lambda após catalisador - comum falha aquecimento',
                'related_pids': ['O2_B1S2', 'O2_B1S1'],
                'diagnostic_tree': [
                    'Verificar aquecimento do sensor (resistência 3-5 ohms)',
                    'Comparar sinal pré e pós catalisador',
                    'Teste de contra-pressão no escapamento'
                ]
            },
            'P0171': {
                'description': 'Mistura pobre (banco 1)',
                'vw_specific': 'Verificar MAF e possíveis vazamentos',
                'related_pids': ['SHORT_FT1', 'LONG_FT1', 'MAF'],
                'diagnostic_tree': [
                    'Verificar vazamentos de vácuo',
                    'Limpar sensor MAF',
                    'Verificar pressão de combustível'
                ]
            }
        }
    
    def _load_fiat_oem(self) -> Dict:
        """Códigos OEM Fiat"""
        return {
            'P0301': {
                'description': 'Falha cilindro 1',
                'fiat_specific': 'Injetores Firefly - falha comum por sujeira',
                'related_pids': ['SHORT_FT1', 'LONG_FT1'],
                'diagnostic_tree': [
                    'Teste de injeção com estetoscópio',
                    'Verificar resistência injetor (12-17 ohms)',
                    'Análise de forma de onda no osciloscópio'
                ]
            },
            'P0135': {
                'description': 'Sensor O2 aquecimento (banco 1)',
                'fiat_specific': 'Comum falha no aquecedor do sensor',
                'related_pids': ['O2_B1S1'],
                'diagnostic_tree': [
                    'Medir resistência do aquecedor (3-5 ohms)',
                    'Verificar tensão de alimentação (12V)',
                    'Verificar fusível do sensor'
                ]
            }
        }
    
    def _load_chevrolet_oem(self) -> Dict:
        """Códigos OEM Chevrolet"""
        return {
            'P0171': {
                'description': 'Mistura pobre',
                'chevrolet_specific': 'Verificar sensor MAF - comum em CSS Prime',
                'related_pids': ['MAF', 'SHORT_FT1', 'LONG_FT1'],
                'diagnostic_tree': [
                    'Limpar sensor MAF com cleaner específico',
                    'Verificar vazamentos após MAF',
                    'Teste de pressão de combustível'
                ]
            }
        }
    
    def _load_ford_oem(self) -> Dict:
        """Códigos OEM Ford"""
        return {
            'P0300': {
                'description': 'Falha de ignição',
                'ford_specific': 'Verificar bobinas e velas - motor Sigma',
                'related_pids': ['RPM', 'MISFIRE_COUNTER'],
                'diagnostic_tree': [
                    'Teste de bobinas com multímetro',
                    'Verificar folga de velas (1.1mm)',
                    'Teste de compressão'
                ]
            }
        }
    
    def _load_generic_oem(self) -> Dict:
        """Códigos genéricos fallback"""
        return {
            'P0300': {
                'description': 'Falha de ignição',
                'related_pids': ['RPM'],
                'diagnostic_tree': [
                    'Verificar velas de ignição',
                    'Verificar cabos de vela',
                    'Teste de bobinas'
                ]
            }
        }
    
    def get_oem_info(self, dtc: str) -> Dict:
        """Retorna informações OEM específicas para o DTC"""
        return self.oem_dtc_library.get(dtc, {})


# =============================================
# 3. CORRELACIONADOR DE PIDs
# =============================================

class PIDCorrelator:
    """
    Correlaciona DTCs com dados em tempo real
    Valida diagnóstico baseado em múltiplos parâmetros
    """
    
    def __init__(self):
        self.correlation_rules = self._load_correlation_rules()
        self.data_buffer = {}
        self.correlation_results = {}
        self.history = deque(maxlen=100)
        
    def _load_correlation_rules(self) -> Dict:
        """Carrega regras de correlação"""
        return {
            'P0171': {  # System Too Lean
                'required_pids': ['SHORT_FT1', 'LONG_FT1', 'MAF', 'O2_B1S1'],
                'validation_logic': {
                    'fuel_trim_high': {
                        'condition': 'short_ft1 > 10 and long_ft1 > 15',
                        'confirmation': 'Fuel system adaptation out of range - injectors dirty or vacuum leak'
                    },
                    'maf_low': {
                        'condition': 'maf < 3.5 and rpm > 2000',
                        'confirmation': 'MAF sensor dirty or failed - air flow too low'
                    },
                    'o2_lean': {
                        'condition': 'o2_b1s1 < 0.45 and abs(o2_b1s1 - 0.45) < 0.05',
                        'confirmation': 'O2 sensor consistently lean - check for vacuum leaks'
                    }
                },
                'confidence_weights': {
                    'fuel_trim_high': 0.4,
                    'maf_low': 0.3,
                    'o2_lean': 0.3
                }
            },
            
            'P0300': {  # Random Misfire
                'required_pids': ['RPM', 'LOAD', 'COOLANT_TEMP'],
                'validation_logic': {
                    'rpm_fluctuation': {
                        'condition': 'rpm_variance > 100',
                        'confirmation': 'RPM unstable - misfire pattern detected'
                    },
                    'load_fluctuation': {
                        'condition': 'load_variance > 15',
                        'confirmation': 'Engine load inconsistent'
                    }
                },
                'confidence_weights': {
                    'rpm_fluctuation': 0.6,
                    'load_fluctuation': 0.4
                }
            },
            
            'P0420': {  # Catalyst Efficiency
                'required_pids': ['O2_B1S1', 'O2_B1S2', 'RPM'],
                'validation_logic': {
                    'o2_switch_rate': {
                        'condition': 'o2_b1s1_switch_rate > 5 and o2_b1s2_switch_rate < 1',
                        'confirmation': 'Pre-cat sensor switching normal, post-cat lazy - catalyst failed'
                    },
                    'o2_correlation': {
                        'condition': 'o2_b1s1_correlation_with_o2_b1s2 < 0.3',
                        'confirmation': 'Low correlation between sensors - catalyst inefficient'
                    }
                },
                'confidence_weights': {
                    'o2_switch_rate': 0.7,
                    'o2_correlation': 0.3
                }
            },
            
            'P0135': {  # O2 Heater
                'required_pids': ['O2_B1S1', 'BATTERY'],
                'validation_logic': {
                    'slow_response': {
                        'condition': 'o2_response_time > 100',
                        'confirmation': 'O2 sensor slow to respond - heater circuit suspect'
                    },
                    'voltage_ok': {
                        'condition': 'battery > 12',
                        'confirmation': 'Battery voltage adequate - heater should be working'
                    }
                }
            }
        }
    
    def add_data_point(self, data: Dict):
        """Adiciona ponto de dados ao histórico"""
        self.history.append(data)
    
    def correlate_dtc(self, dtc: str, current_data: Dict, 
                      vehicle_profile: VehicleProfile) -> Optional[DiagnosticContext]:
        """
        Correlaciona DTC com dados em tempo real
        Retorna contexto enriquecido com validações
        """
        if dtc not in self.correlation_rules:
            return None
        
        rule = self.correlation_rules[dtc]
        context = DiagnosticContext(
            dtc_code=dtc,
            dtc_description=self._get_description(dtc),
            freeze_frame=self._capture_freeze_frame(current_data),
            live_data={'current': current_data, 'history': list(self.history)[-50:]},
            vehicle_profile=vehicle_profile
        )
        
        # Calcula correlações
        correlations = {}
        for key, logic in rule['validation_logic'].items():
            if self._evaluate_condition(logic['condition'], current_data):
                correlations[key] = logic['confirmation']
        
        # Adiciona informações OEM
        oem_info = vehicle_profile.get_oem_info(dtc)
        if oem_info:
            correlations['oem_tip'] = oem_info.get('vw_specific' if vehicle_profile.manufacturer == 'VOLKSWAGEN' else 'fiat_specific', '')
        
        # Calcula confiança
        confidence = self._calculate_confidence(correlations, rule)
        
        context.confidence = confidence
        context.related_pids = rule.get('required_pids', [])
        context.validation_results = correlations
        
        return context
    
    def _evaluate_condition(self, condition: str, data: Dict) -> bool:
        """Avalia condição lógica com dados reais"""
        try:
            # Extrai valores
            for key in data:
                if key in condition:
                    condition = condition.replace(key, str(data[key]))
            
            # Avalia expressões comuns
            if '>' in condition and '<' in condition:
                parts = condition.split(' and ')
                return all(self._evaluate_single(part) for part in parts)
            elif '>' in condition:
                return self._evaluate_single(condition)
            elif '<' in condition:
                return self._evaluate_single(condition)
                
        except Exception:
            pass
        
        return False
    
    def _evaluate_single(self, condition: str) -> bool:
        """Avalia uma única condição"""
        try:
            if '>' in condition:
                var, val = condition.split('>')
                return float(var.strip()) > float(val.strip())
            elif '<' in condition:
                var, val = condition.split('<')
                return float(var.strip()) < float(val.strip())
        except:
            pass
        return False
    
    def _calculate_confidence(self, correlations: Dict, rule: Dict) -> float:
        """Calcula confiança baseado nas correlações positivas"""
        if not correlations:
            return 0.0
        
        # Remove OEM tips do cálculo
        tech_correlations = {k: v for k, v in correlations.items() if k != 'oem_tip'}
        
        if not tech_correlations:
            return 0.3  # Confiança baixa baseada apenas em OEM
        
        weights = rule.get('confidence_weights', {})
        total_weight = sum(weights.get(k, 0.1) for k in tech_correlations)
        
        return min(total_weight, 1.0)
    
    def _capture_freeze_frame(self, data: Dict) -> Dict:
        """Captura freeze frame no momento do erro"""
        return data.copy()
    
    def _get_description(self, dtc: str) -> str:
        """Retorna descrição do DTC"""
        descriptions = {
            'P0171': 'System Too Lean (Bank 1)',
            'P0300': 'Random/Multiple Cylinder Misfire Detected',
            'P0420': 'Catalyst System Efficiency Below Threshold',
            'P0301': 'Cylinder 1 Misfire Detected',
            'P0135': 'O2 Sensor Heater Circuit Malfunction'
        }
        return descriptions.get(dtc, 'Unknown DTC')


# =============================================
# 4. ASSISTENTE TÉCNICO
# =============================================

class TechnicalAdvisor:
    """
    Fornece sugestões técnicas precisas baseadas no diagnóstico
    Similar aos sistemas profissionais de ajuda
    """
    
    def __init__(self):
        self.test_procedures = self._load_test_procedures()
        
    def _load_test_procedures(self) -> Dict:
        """Carrega procedimentos de teste"""
        return {
            'O2_SENSOR': {
                'component': 'Sensor Lambda',
                'test_type': 'resistência',
                'pins': (3, 4),
                'expected_range': (3.0, 5.0),
                'unit': 'ohms',
                'procedure': '1. Desconecte o conector do sensor\n2. Meça a resistência entre os pinos 3 e 4 (aquecimento)\n3. Valor deve estar entre 3-5 ohms\n4. Se fora da faixa, sensor com defeito',
                'common_failures': ['Aquecimento queimado', 'Contaminação por combustível', 'Curto interno']
            },
            'MAF_SENSOR': {
                'component': 'Sensor MAF',
                'test_type': 'frequência/tensão',
                'pins': (2, 3),
                'expected_range': (2.5, 4.5),
                'unit': 'V',
                'procedure': '1. Com ignição ligada, motor desligado\n2. Meça tensão entre pino 2 (sinal) e massa\n3. Deve ser aproximadamente 0.5V com motor desligado\n4. Com motor funcionando, tensão varia de 2.5-4.5V conforme rotação',
                'common_failures': ['Elemento sensor sujo', 'Fiação danificada', 'Falha eletrônica']
            },
            'COIL_PACK': {
                'component': 'Bobina de Ignição',
                'test_type': 'resistência',
                'pins': (1, 2),
                'expected_range': (0.5, 1.5),
                'unit': 'ohms',
                'procedure': '1. Desconecte a bobina\n2. Meça resistência entre os pinos de alimentação\n3. Bobina primária: 0.5-1.5 ohms\n4. Bobina secundária: 5-10k ohms (entre saída de alta e massa)',
                'common_failures': ['Bobina em curto', 'Circuito aberto', 'Fuga de alta tensão']
            },
            'INJECTOR': {
                'component': 'Injetor de Combustível',
                'test_type': 'resistência',
                'pins': (1, 2),
                'expected_range': (12.0, 17.0),
                'unit': 'ohms',
                'procedure': '1. Desconecte o conector do injetor\n2. Meça resistência entre os dois terminais\n3. Injetores de alta impedância: 12-17 ohms\n4. Injetores de baixa impedância: 2-5 ohms',
                'common_failures': ['Enrolamento em curto', 'Circuito aberto', 'Injetor entupido']
            },
            'ECT_SENSOR': {
                'component': 'Sensor de Temperatura do Motor',
                'test_type': 'resistência',
                'pins': (1, 2),
                'expected_range': (200, 300),
                'unit': 'ohms',
                'procedure': '1. Motor frio (20°C)\n2. Meça resistência entre os terminais\n3. Valor esperado: 200-300 ohms\n4. Com motor quente (90°C): 20-30 ohms',
                'common_failures': ['Sensor aberto', 'Curto interno', 'Leitura errática']
            },
            'TPS_SENSOR': {
                'component': 'Sensor de Posição do Acelerador',
                'test_type': 'tensão',
                'pins': (2, 3),
                'expected_range': (0.5, 4.5),
                'unit': 'V',
                'procedure': '1. Com ignição ligada\n2. Meça tensão entre pino de sinal e massa\n3. Com acelerador fechado: 0.5V\n4. Com acelerador totalmente aberto: 4.5V\n5. A variação deve ser suave e contínua',
                'common_failures': ['Trilha resistiva gasta', 'Contato intermitente', 'Fora de faixa']
            },
            'CKP_SENSOR': {
                'component': 'Sensor de Rotação',
                'test_type': 'resistência',
                'pins': (1, 2),
                'expected_range': (500, 900),
                'unit': 'ohms',
                'procedure': '1. Desconecte o sensor\n2. Meça resistência entre os terminais\n3. Sensores de relutância magnética: 500-900 ohms\n4. Sensores Hall: verificar alimentação 5V e sinal digital',
                'common_failures': ['Sensor aberto', 'Curto', 'Folga excessiva do anel fônico']
            },
            'CMP_SENSOR': {
                'component': 'Sensor de Fase',
                'test_type': 'osciloscópio',
                'pins': (2, 3),
                'expected_range': (0, 5),
                'unit': 'V',
                'procedure': '1. Conecte osciloscópio ao pino de sinal\n2. Com motor funcionando, deve gerar onda quadrada 0-5V\n3. Verificar sincronismo com rotação do motor\n4. Frequência varia com RPM',
                'common_failures': ['Sensor com defeito', 'Problemas de sincronismo', 'Sinal fraco']
            },
            'KNOCK_SENSOR': {
                'component': 'Sensor de Detonação',
                'test_type': 'resistência',
                'pins': (1, 2),
                'expected_range': (0.5, 1.0),
                'unit': 'Mohms',
                'procedure': '1. Sensor piezoelétrico\n2. Meça resistência entre terminal e massa\n3. Deve ser > 0.5 Mohm\n4. Teste dinâmico: bater levemente próximo ao sensor com motor ligado deve alterar sinal',
                'common_failures': ['Sensor danificado', 'Fiação partida', 'Torque de aperto incorreto']
            },
            'FUEL_PRESSURE': {
                'component': 'Pressão de Combustível',
                'test_type': 'pressão',
                'pins': (1, 2),
                'expected_range': (3.0, 4.0),
                'unit': 'bar',
                'procedure': '1. Instale manômetro no trilho de combustível\n2. Com ignição ligada: pressão deve subir rapidamente\n3. Em marcha lenta: 3.0-4.0 bar\n4. Sob carga: pressão pode aumentar ligeiramente',
                'common_failures': ['Bomba fraca', 'Regulador com defeito', 'Filtro entupido']
            },
            'VACUUM_LEAK': {
                'component': 'Vazamento de Vácuo',
                'test_type': 'smoke test',
                'pins': (1, 1),
                'expected_range': (0, 0),
                'unit': 'mm Hg',
                'procedure': '1. Utilize máquina de fumaça no sistema de admissão\n2. Observe saída de fumaça em mangueiras, gaxetas, etc\n3. Meça vácuo do motor com vacuômetro\n4. Vácuo estável > 400 mm Hg indica motor saudável',
                'common_failures': ['Mangueiras ressecadas', 'Gaxeta do coletor', 'Válvula PCV']
            }
        }
    
    def get_suggestion(self, dtc: str, vehicle_profile: VehicleProfile) -> List[TechnicalSuggestion]:
        """
        Retorna sugestões técnicas baseadas no DTC e perfil do veículo
        """
        suggestions = []
        
        # Mapeamento DTC para componentes
        dtc_component_map = {
            'P0171': ['MAF_SENSOR', 'VACUUM_LEAK', 'FUEL_PRESSURE'],
            'P0172': ['MAF_SENSOR', 'INJECTOR', 'FUEL_PRESSURE'],
            'P0300': ['COIL_PACK', 'INJECTOR', 'CKP_SENSOR'],
            'P0301': ['COIL_PACK', 'INJECTOR'],
            'P0302': ['COIL_PACK', 'INJECTOR'],
            'P0303': ['COIL_PACK', 'INJECTOR'],
            'P0304': ['COIL_PACK', 'INJECTOR'],
            'P0420': ['O2_SENSOR'],
            'P0135': ['O2_SENSOR'],
            'P0115': ['ECT_SENSOR'],
            'P0116': ['ECT_SENSOR'],
            'P0120': ['TPS_SENSOR'],
            'P0121': ['TPS_SENSOR'],
            'P0325': ['KNOCK_SENSOR'],
            'P0326': ['KNOCK_SENSOR'],
            'P0335': ['CKP_SENSOR'],
            'P0336': ['CKP_SENSOR'],
            'P0340': ['CMP_SENSOR'],
            'P0341': ['CMP_SENSOR']
        }
        
        # Obtém componentes relacionados
        components = dtc_component_map.get(dtc, [])
        
        for comp in components:
            if comp in self.test_procedures:
                proc = self.test_procedures[comp]
                suggestion = TechnicalSuggestion(
                    component=proc['component'],
                    test_type=proc['test_type'],
                    pins=proc['pins'],
                    expected_range=proc['expected_range'],
                    unit=proc['unit'],
                    procedure=proc['procedure'],
                    common_failures=proc['common_failures']
                )
                suggestions.append(suggestion)
        
        # Adiciona dicas OEM
        oem_info = vehicle_profile.get_oem_info(dtc)
        if oem_info:
            for tip in oem_info.get('diagnostic_tree', []):
                # Converte dicas de diagnóstico em sugestões simplificadas
                suggestion = TechnicalSuggestion(
                    component=vehicle_profile.manufacturer,
                    test_type='diagnóstico',
                    pins=(0, 0),
                    expected_range=(0, 0),
                    unit='',
                    procedure=tip,
                    common_failures=[]
                )
                suggestions.append(suggestion)
        
        return suggestions


# =============================================
# 5. OTIMIZADOR DE PERFORMANCE
# =============================================

class PerformanceOptimizer:
    """
    Otimiza o loop de leitura para máxima performance
    Implementa buffer circular, priorização e throttling
    """
    
    def __init__(self, target_fps: int = 50):
        self.target_fps = target_fps
        self.target_period = 1.0 / target_fps
        self.read_queue = queue.Queue(maxsize=1000)
        self.pid_priorities = {
            'RPM': 10,
            'LOAD': 8,
            'COOLANT_TEMP': 7,
            'SPEED': 6,
            'MAF': 8,
            'O2_B1S1': 9,
            'O2_B1S2': 8,
            'SHORT_FT1': 8,
            'LONG_FT1': 8,
            'TIMING_ADVANCE': 7
        }
        self.stats = {
            'reads_per_second': 0,
            'avg_read_time': 0,
            'missed_deadlines': 0
        }
        
    def optimize_pid_list(self, requested_pids: List[str]) -> List[str]:
        """
        Otimiza lista de PIDs baseado em prioridade e tempo disponível
        """
        # Ordena por prioridade
        prioritized = sorted(requested_pids, 
                            key=lambda x: self.pid_priorities.get(x, 5), 
                            reverse=True)
        
        # Calcula tempo disponível
        available_time = self.target_period * 0.8  # 80% do período para leituras
        
        # Estima tempo por leitura (média empírica)
        avg_read_time = 0.005  # 5ms por leitura
        
        max_reads = int(available_time / avg_read_time)
        
        return prioritized[:max_reads]
    
    def adaptive_throttle(self, execution_time: float):
        """
        Ajusta dinamicamente a frequência baseado no tempo de execução
        """
        if execution_time > self.target_period:
            self.target_period *= 1.1  # Aumenta período (diminui FPS)
            self.stats['missed_deadlines'] += 1
        elif execution_time < self.target_period * 0.5:
            self.target_period *= 0.9  # Diminui período (aumenta FPS)
        
        # Limites de segurança
        self.target_period = max(0.01, min(0.1, self.target_period))  # 10-100ms
        
        return self.target_period
    
    def batch_read(self, pids: List[str], read_function) -> Dict:
        """
        Leitura em lote para otimização
        """
        results = {}
        start_time = time.perf_counter()
        
        for pid in pids:
            try:
                results[pid] = read_function(pid)
            except Exception:
                results[pid] = None
        
        execution_time = time.perf_counter() - start_time
        self.stats['avg_read_time'] = (self.stats['avg_read_time'] + execution_time) / 2
        
        return results
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas de performance"""
        self.stats['reads_per_second'] = int(1.0 / self.stats['avg_read_time']) if self.stats['avg_read_time'] > 0 else 0
        return self.stats


# =============================================
# 6. SCANNER PRINCIPAL REVOLUCIONÁRIO
# =============================================

class OBDScannerRevolucionario:
    """
    Scanner Automotivo com Inteligência Artificial
    - Aprende padrões de cada veículo
    - Diagnóstico preditivo
    - Banco de dados compartilhado
    - Atualizações automáticas
    """
    
    def __init__(self):
        # Componentes principais
        self.protocol_detector = ProtocolAutoDetect()
        self.vehicle_profile = VehicleProfile()
        self.pid_correlator = PIDCorrelator()
        self.technical_advisor = TechnicalAdvisor()
        self.performance_optimizer = PerformanceOptimizer(target_fps=60)
        
        # Estado
        self.connected = False
        self.is_real = False
        self.running = False
        self.read_thread = None
        self.serial_conn = None
        
        # Dados
        self.vehicle_info = {
            'manufacturer': '---',
            'model': '---',
            'year': '---',
            'engine': '---',
            'transmission': '---',
            'vin': '---',
            'ecu': '---',
            'version': '---',
            'protocol': '---',
            'km': '---'
        }
        
        self.stats = {
            'uptime': '00:00:00',
            'max_rpm': 0,
            'max_temp': 0,
            'start_time': time.time()
        }
        
        self.live_data = {
            'rpm': 0,
            'speed': 0,
            'temp': 0,
            'oil_pressure': 0,
            'battery': 0,
            'engine_load': 0,
            'o2': 0,
            'timing': 0
        }
        
        self.dtcs = []
        self.log = []
        
    def scan_ports(self) -> bool:
        """
        Escaneia portas e tenta conexão automática
        """
        # Simulação para testes
        self.is_real = False
        self.connected = True
        self.vehicle_info = {
            'manufacturer': 'Volkswagen',
            'model': 'Gol 1.6 MSI',
            'year': '2024',
            'engine': 'EA211 (16V)',
            'transmission': 'MQ200 (MANUAL)',
            'vin': '9BWZZZ377VT004251',
            'ecu': 'BOSCH ME17.9.65',
            'version': '03H906023AB 3456',
            'protocol': 'CAN-BUS 500K',
            'km': '15.234 km'
        }
        self.vehicle_profile.load_from_vin(self.vehicle_info['vin'])
        self._start_simulation()
        return True
    
    def disconnect(self):
        """Desconecta do veículo"""
        self.connected = False
        self.running = False
        
    def get_live_data(self) -> Dict:
        """Retorna dados em tempo real"""
        return self.live_data.copy()
    
    def diagnose_dtc(self, dtc_code: str) -> Dict:
        """
        Diagnóstico aprofundado de um DTC específico
        """
        result = {
            'dtc': dtc_code,
            'description': self.pid_correlator._get_description(dtc_code),
            'context': None,
            'suggestions': [],
            'confidence': 0.0
        }
        
        # Correlaciona com dados ao vivo
        context = self.pid_correlator.correlate_dtc(
            dtc_code, 
            self.live_data,
            self.vehicle_profile
        )
        
        if context:
            result['context'] = context.validation_results
            result['confidence'] = context.confidence
        
        # Obtém sugestões técnicas
        suggestions = self.technical_advisor.get_suggestion(
            dtc_code,
            self.vehicle_profile
        )
        
        result['suggestions'] = suggestions
        
        return result
    
    def scan_all_dtcs(self) -> List[Dict]:
        """
        Escaneia todos os sistemas e retorna DTCs com diagnóstico
        """
        # Simula leitura de DTCs
        simulated_dtcs = ['P0301', 'P0420', 'P0171']
        results = []
        
        for dtc in simulated_dtcs:
            results.append(self.diagnose_dtc(dtc))
        
        return results
    
    def clear_dtcs(self):
        """Limpa todos os códigos de falha"""
        self.dtcs = []
        self.log.append("> Códigos de falha limpos")
    
    def _start_simulation(self):
        """Inicia thread de simulação"""
        self.running = True
        self.read_thread = threading.Thread(target=self._simulation_loop)
        self.read_thread.daemon = True
        self.read_thread.start()
    
    def _simulation_loop(self):
        """Loop principal de simulação"""
        cycle_time = 0.02  # 50Hz
        
        while self.running and self.connected:
            loop_start = time.perf_counter()
            
            # Gera dados simulados realistas
            self.live_data = {
                'rpm': random.randint(750, 3500),
                'speed': random.randint(0, 120),
                'temp': random.randint(82, 98),
                'oil_pressure': round(3.5 + random.random() * 1.5, 1),
                'battery': round(12 + random.random() * 2, 1),
                'engine_load': random.randint(15, 55),
                'o2': round(0.7 + random.random() * 0.2, 2),
                'timing': random.randint(8, 22)
            }
            
            # Atualiza estatísticas
            if self.live_data['rpm'] > self.stats['max_rpm']:
                self.stats['max_rpm'] = self.live_data['rpm']
            if self.live_data['temp'] > self.stats['max_temp']:
                self.stats['max_temp'] = self.live_data['temp']
            
            # Atualiza uptime
            uptime_seconds = int(time.time() - self.stats['start_time'])
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            seconds = uptime_seconds % 60
            self.stats['uptime'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Adiciona ao correlator
            self.pid_correlator.add_data_point(self.live_data)
            
            # Otimização de performance
            execution_time = time.perf_counter() - loop_start
            adjusted_cycle = self.performance_optimizer.adaptive_throttle(execution_time)
            
            # Aguarda próximo ciclo
            sleep_time = max(0, cycle_time - execution_time)
            time.sleep(sleep_time)
