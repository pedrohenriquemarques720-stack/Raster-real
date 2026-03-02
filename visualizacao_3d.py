# visualizacao_3d.py - Visualizador 3D Profissional

from typing import Dict, Optional, List, Tuple
import json
from enum import Enum

class ComponentType(Enum):
    ENGINE = "Motor"
    TRANSMISSION = "Transmissão"
    SENSOR = "Sensor"
    ACTUATOR = "Atuador"
    ELECTRICAL = "Componente Elétrico"

class Component3D:
    """Modelo 3D de componente automotivo"""
    
    def __init__(self, comp_id: str, name: str, comp_type: ComponentType):
        self.id = comp_id
        self.name = name
        self.type = comp_type
        self.location_3d = {}
        self.pinout = {}
        self.waveform_data = {}
        self.technical_data = {}
        
class Visualizador3D:
    """
    Visualizador 3D profissional de componentes automotivos
    """
    
    def __init__(self):
        self.components_db = self._load_component_database()
        self.vehicle_models = self._load_vehicle_models()
        
    def _load_component_database(self) -> Dict:
        """Carrega banco de dados completo de componentes"""
        return {
            'CKP_SENSOR': {
                'name': 'Sensor de Rotação (CKP)',
                'type': ComponentType.SENSOR.value,
                'manufacturers': ['Bosch', 'Denso', 'Delphi'],
                'location': {
                    'engine': 'Bloco do motor',
                    'position': 'Próximo ao volante do motor',
                    'access': 'Por baixo do veículo',
                    'torque': '8-12 Nm'
                },
                'pinout': {
                    '1': {'function': 'Sinal +', 'wire': 'Branco/Azul', 'voltage': '0-5V AC'},
                    '2': {'function': 'Sinal -', 'wire': 'Branco/Preto', 'voltage': 'GND'},
                    '3': {'function': 'Shield', 'wire': 'Transparente', 'voltage': 'GND'}
                },
                'specifications': {
                    'resistance': '500-900 Ω',
                    'air_gap': '0.5-1.5 mm',
                    'output_frequency': '10-1000 Hz',
                    'operating_temp': '-40 a 150°C'
                },
                'waveform': {
                    'type': 'Senoidal',
                    'amplitude': '0-5V',
                    'frequency_vs_rpm': 'Proporcional'
                },
                'dtc_codes': ['P0335', 'P0336', 'P0337', 'P0338', 'P0339'],
                'replacement_tips': [
                    'Limpar área antes de remover',
                    'Verificar integridade do anel fônico',
                    'Aplicar anti-corrosivo nos contatos',
                    'Torquear conforme especificação'
                ]
            },
            'O2_SENSOR': {
                'name': 'Sonda Lambda (O2)',
                'type': ComponentType.SENSOR.value,
                'manufacturers': ['Bosch', 'NGK', 'Denso'],
                'location': {
                    'engine': 'Sistema de escapamento',
                    'position': 'Antes do catalisador (pré)',
                    'access': 'Por baixo do veículo',
                    'torque': '40-50 Nm'
                },
                'pinout': {
                    '1': {'function': 'Sinal', 'wire': 'Preto', 'voltage': '0.1-0.9V'},
                    '2': {'function': 'GND', 'wire': 'Cinza', 'voltage': '0V'},
                    '3': {'function': 'Aquecimento +', 'wire': 'Vermelho', 'voltage': '12V'},
                    '4': {'function': 'Aquecimento -', 'wire': 'Marrom', 'voltage': 'GND'}
                },
                'specifications': {
                    'heater_resistance': '3-5 Ω',
                    'response_time': '< 100 ms',
                    'operating_temp': '300-800°C',
                    'voltage_range': '0.1-0.9V'
                },
                'waveform': {
                    'type': 'Oscilante',
                    'frequency': '1-5 Hz',
                    'cross_count': '>5 em 10s'
                },
                'dtc_codes': ['P0130', 'P0131', 'P0132', 'P0133', 'P0134', 'P0135'],
                'replacement_tips': [
                    'Usar chave específica para sonda',
                    'Aplicar anti-aderente na rosca',
                    'Não usar lubrificante nos contatos',
                    'Verificar integridade do chicote'
                ]
            },
            'COIL': {
                'name': 'Bobina de Ignição',
                'type': ComponentType.ACTUATOR.value,
                'manufacturers': ['Bosch', 'Delphi', 'Valeo'],
                'location': {
                    'engine': 'Cabeçote',
                    'position': 'Sobre as velas',
                    'access': 'Superior do motor',
                    'torque': '8-10 Nm'
                },
                'pinout': {
                    '1': {'function': '12V', 'wire': 'Vermelho/Branco', 'voltage': '12V'},
                    '2': {'function': 'GND', 'wire': 'Marrom', 'voltage': '0V'},
                    '3': {'function': 'Sinal', 'wire': 'Verde/Roxo', 'voltage': '0-5V'}
                },
                'specifications': {
                    'primary_resistance': '0.5-1.5 Ω',
                    'secondary_resistance': '5-10 kΩ',
                    'inductance': '5-10 mH',
                    'spark_energy': '30-50 mJ'
                },
                'waveform': {
                    'type': 'Quadrada',
                    'dwell_time': '3-5 ms',
                    'spark_duration': '1-2 ms'
                },
                'dtc_codes': ['P0300', 'P0301', 'P0302', 'P0303', 'P0304', 'P0350'],
                'replacement_tips': [
                    'Substituir todas as bobinas do conjunto',
                    'Verificar alimentação 12V',
                    'Testar antes da instalação',
                    'Limpar poços das velas'
                ]
            },
            'MAF_SENSOR': {
                'name': 'Sensor de Fluxo de Massa de Ar (MAF)',
                'type': ComponentType.SENSOR.value,
                'manufacturers': ['Bosch', 'Hitachi', 'Denso'],
                'location': {
                    'engine': 'Sistema de admissão',
                    'position': 'Após o filtro de ar',
                    'access': 'Superior do motor',
                    'torque': '3-5 Nm'
                },
                'pinout': {
                    '1': {'function': 'Alimentação', 'wire': 'Vermelho', 'voltage': '5V'},
                    '2': {'function': 'Sinal', 'wire': 'Amarelo', 'voltage': '0.5-4.5V'},
                    '3': {'function': 'GND', 'wire': 'Preto', 'voltage': '0V'}
                },
                'specifications': {
                    'idle_output': '0.5-1.5V (2.5-4.5 g/s)',
                    '2500rpm_output': '2.0-3.0V (6-12 g/s)',
                    'response_time': '< 50 ms',
                    'accuracy': '±3%'
                },
                'waveform': {
                    'type': 'Linear',
                    'voltage_vs_flow': 'Diretamente proporcional'
                },
                'dtc_codes': ['P0100', 'P0101', 'P0102', 'P0103'],
                'replacement_tips': [
                    'Usar cleaner específico para MAF',
                    'Não tocar no elemento sensor',
                    'Verificar vedação do duto',
                    'Limpar conector com contato elétrico'
                ]
            },
            'INJECTOR': {
                'name': 'Injetor de Combustível',
                'type': ComponentType.ACTUATOR.value,
                'manufacturers': ['Bosch', 'Siemens', 'Delphi'],
                'location': {
                    'engine': 'Trilho de combustível',
                    'position': 'No cabeçote',
                    'access': 'Superior do motor',
                    'torque': '20-25 Nm'
                },
                'pinout': {
                    '1': {'function': 'Alimentação', 'wire': 'Azul', 'voltage': '12V'},
                    '2': {'function': 'Sinal', 'wire': 'Marrom', 'voltage': '0-12V (PWM)'}
                },
                'specifications': {
                    'resistance': '12-17 Ω (alta impedância)',
                    'flow_rate': '180-220 cc/min',
                    'spray_angle': '30-40°',
                    'opening_time': '1-2 ms'
                },
                'waveform': {
                    'type': 'PWM',
                    'frequency': '10-100 Hz',
                    'duty_cycle': '3-5% (lenta)'
                },
                'dtc_codes': ['P0201', 'P0202', 'P0203', 'P0204', 'P0261'],
                'replacement_tips': [
                    'Lubrificar O-ring com vaselina',
                    'Não misturar injetores de diferentes cilindros',
                    'Verificar pressão do sistema',
                    'Fazer adaptação após troca'
                ]
            }
        }
        
    def _load_vehicle_models(self) -> Dict:
        """Carrega modelos 3D de veículos"""
        return {
            'VW_GOL': {
                'engine_position': (0, 0, 0),
                'camera_presets': {
                    'front': (0, 0, 5),
                    'rear': (0, 0, -5),
                    'top': (0, 5, 0),
                    'engine': (2, 1, 1)
                },
                'component_offsets': {
                    'CKP_SENSOR': (1.5, -0.5, 0.2),
                    'O2_SENSOR': (2.0, -0.8, 0.1),
                    'COIL': (0.8, 0.5, 1.0),
                    'MAF_SENSOR': (0.5, 1.2, 0.3),
                    'INJECTOR': (0.9, 0.6, 0.8)
                }
            }
        }
        
    def locate_component(self, dtc: str, vehicle_model: str = "VW_GOL") -> Optional[Dict]:
        """
        Localiza componente baseado no DTC
        """
        # Mapeamento DTC -> Componente
        dtc_map = {
            'P0335': 'CKP_SENSOR', 'P0336': 'CKP_SENSOR',
            'P0130': 'O2_SENSOR', 'P0131': 'O2_SENSOR', 'P0132': 'O2_SENSOR', 'P0133': 'O2_SENSOR',
            'P0135': 'O2_SENSOR',
            'P0300': 'COIL', 'P0301': 'COIL', 'P0302': 'COIL', 'P0303': 'COIL', 'P0304': 'COIL',
            'P0350': 'COIL',
            'P0100': 'MAF_SENSOR', 'P0101': 'MAF_SENSOR', 'P0102': 'MAF_SENSOR',
            'P0201': 'INJECTOR', 'P0202': 'INJECTOR', 'P0203': 'INJECTOR'
        }
        
        component_key = dtc_map.get(dtc)
        if not component_key:
            return None
            
        comp_data = self.components_db.get(component_key)
        if not comp_data:
            return None
            
        # Calcula posição 3D
        vehicle_data = self.vehicle_models.get(vehicle_model, {})
        offset = vehicle_data.get('component_offsets', {}).get(component_key, (0, 0, 0))
        
        return {
            'component': {
                'name': comp_data['name'],
                'type': comp_data['type'],
                'manufacturers': comp_data['manufacturers'],
                'dtc_codes': comp_data['dtc_codes']
            },
            'location': comp_data['location'],
            'pinout': comp_data['pinout'],
            'specifications': comp_data['specifications'],
            'waveform': comp_data.get('waveform', {}),
            'replacement_tips': comp_data.get('replacement_tips', []),
            'position_3d': {
                'x': offset[0],
                'y': offset[1],
                'z': offset[2],
                'camera_focus': (offset[0] + 0.5, offset[1] + 0.2, offset[2] + 0.5)
            }
        }
        
    def get_pinout_html(self, component_key: str) -> str:
        """Gera HTML para exibição do esquema elétrico"""
        comp = self.components_db.get(component_key)
        if not comp:
            return "<p>Esquema não disponível</p>"
            
        html = "<div style='background:#000; padding:15px; border-radius:8px;'>"
        html += f"<h4 style='color:#00ffff;'>{comp['name']} - Pinagem</h4>"
        html += "<table style='width:100%; border-collapse:collapse;'>"
        html += "<tr><th>Pino</th><th>Função</th><th>Cor</th><th>Valor</th></tr>"
        
        for pin, info in comp['pinout'].items():
            html += f"<tr>"
            html += f"<td style='border:1px solid #333; padding:5px;'><strong>{pin}</strong></td>"
            html += f"<td style='border:1px solid #333; padding:5px;'>{info['function']}</td>"
            html += f"<td style='border:1px solid #333; padding:5px; color:#888;'>{info['wire']}</td>"
            html += f"<td style='border:1px solid #333; padding:5px; color:#00ffff;'>{info['voltage']}</td>"
            html += f"</tr>"
            
        html += "</table>"
        html += "</div>"
        
        return html
