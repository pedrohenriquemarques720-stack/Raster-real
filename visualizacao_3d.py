# visualizacao_3d.py - Versão simplificada

from typing import Dict, Optional, List, Tuple

class Componente3D:
    def __init__(self, nome, posicao, rotacao, escala, pinagem):
        self.nome = nome
        self.posicao = posicao
        self.rotacao = rotacao
        self.escala = escala
        self.pinagem = pinagem

class Visualizador3D:
    """
    Visualizador 3D de componentes automotivos
    Versão simplificada
    """
    
    def __init__(self):
        self.componentes_db = self._criar_database()
        
    def _criar_database(self) -> Dict:
        return {
            'CKP_SENSOR': {
                'nome': 'Sensor de Rotação',
                'localizacao': 'Bloco do motor, próximo ao volante do motor',
                'pinagem': {
                    '1': {'funcao': 'Sinal', 'cor': 'Branco', 'valor': '0-5V'},
                    '2': {'funcao': 'GND', 'cor': 'Preto', 'valor': '0V'},
                    '3': {'funcao': 'Alimentação', 'cor': 'Vermelho', 'valor': '5V'}
                },
                'valores_referencia': {
                    'resistencia': '500-900Ω',
                    'folga': '0.5-1.5mm'
                },
                'dtc_codes': ['P0335', 'P0336']
            },
            'O2_SENSOR': {
                'nome': 'Sonda Lambda',
                'localizacao': 'Escapamento, antes do catalisador',
                'pinagem': {
                    '1': {'funcao': 'Sinal', 'cor': 'Preto', 'valor': '0.1-0.9V'},
                    '2': {'funcao': 'GND', 'cor': 'Cinza', 'valor': '0V'},
                    '3': {'funcao': 'Aquecimento+', 'cor': 'Vermelho', 'valor': '12V'},
                    '4': {'funcao': 'Aquecimento-', 'cor': 'Marrom', 'valor': 'GND'}
                },
                'valores_referencia': {
                    'resistencia_aquecimento': '3-5Ω',
                    'tensao': '0.1-0.9V'
                },
                'dtc_codes': ['P0130', 'P0131', 'P0132', 'P0133']
            },
            'COIL': {
                'nome': 'Bobina de Ignição',
                'localizacao': 'Cabeçote do motor, próximo às velas',
                'pinagem': {
                    '1': {'funcao': '12V', 'cor': 'Vermelho/Branco', 'valor': '12V'},
                    '2': {'funcao': 'GND', 'cor': 'Marrom', 'valor': '0V'},
                    '3': {'funcao': 'Sinal', 'cor': 'Verde/Roxo', 'valor': '0-5V'}
                },
                'valores_referencia': {
                    'resistencia_primaria': '0.5-1.5Ω',
                    'resistencia_secundaria': '5-10kΩ'
                },
                'dtc_codes': ['P0300', 'P0301', 'P0302', 'P0303', 'P0304']
            },
            'MAF_SENSOR': {
                'nome': 'Sensor MAF',
                'localizacao': 'Duto de ar, após o filtro',
                'pinagem': {
                    '1': {'funcao': 'Alimentação', 'cor': 'Vermelho', 'valor': '5V'},
                    '2': {'funcao': 'Sinal', 'cor': 'Amarelo', 'valor': '0.5-4.5V'},
                    '3': {'funcao': 'GND', 'cor': 'Preto', 'valor': '0V'}
                },
                'valores_referencia': {
                    'tensao_lenta': '0.5-1.5V',
                    'tensao_2500rpm': '2.5-3.5V'
                },
                'dtc_codes': ['P0100', 'P0101', 'P0102', 'P0103']
            }
        }
    
    def locate_component(self, dtc: str, vehicle_model: str) -> Optional[Dict]:
        """
        Localiza componente baseado no DTC
        """
        # Mapeia DTC para componente
        dtc_map = {
            'P0335': 'CKP_SENSOR', 'P0336': 'CKP_SENSOR',
            'P0130': 'O2_SENSOR', 'P0131': 'O2_SENSOR', 'P0132': 'O2_SENSOR', 'P0133': 'O2_SENSOR',
            'P0300': 'COIL', 'P0301': 'COIL', 'P0302': 'COIL', 'P0303': 'COIL', 'P0304': 'COIL',
            'P0100': 'MAF_SENSOR', 'P0101': 'MAF_SENSOR', 'P0102': 'MAF_SENSOR'
        }
        
        component_key = dtc_map.get(dtc)
        if not component_key:
            return None
            
        comp_data = self.componentes_db.get(component_key)
        if not comp_data:
            return None
            
        return {
            'component': {
                'name': comp_data['nome'],
                'dtc_codes': comp_data['dtc_codes']
            },
            'location': comp_data['localizacao'],
            'pinout': comp_data['pinagem'],
            'reference_values': comp_data['valores_referencia']
        }
