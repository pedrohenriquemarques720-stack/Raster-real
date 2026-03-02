# dtc_database.py - Versão simplificada

from typing import Dict, List

class DTCDatabase:
    """
    Banco de dados de códigos de falha
    """
    
    def __init__(self):
        self.dtc_database = self._build_database()
    
    def _build_database(self) -> Dict:
        return {
            'P0300': {
                'description': 'Falha de ignição aleatória detectada',
                'system': 'Motor',
                'cause': 'Velas, cabos ou bobinas com defeito',
                'solution': 'Verificar velas, cabos e bobinas',
                'severity': 'Alta'
            },
            'P0301': {
                'description': 'Falha de ignição no cilindro 1',
                'system': 'Motor',
                'cause': 'Vela, injetor ou bobina do cilindro 1 com defeito',
                'solution': 'Testar componentes do cilindro 1',
                'severity': 'Alta'
            },
            'P0302': {
                'description': 'Falha de ignição no cilindro 2',
                'system': 'Motor',
                'cause': 'Vela, injetor ou bobina do cilindro 2 com defeito',
                'solution': 'Testar componentes do cilindro 2',
                'severity': 'Alta'
            },
            'P0420': {
                'description': 'Eficiência do catalisador abaixo do limite',
                'system': 'Emissões',
                'cause': 'Catalisador danificado ou sonda lambda com defeito',
                'solution': 'Substituir catalisador ou sonda',
                'severity': 'Média'
            },
            'P0171': {
                'description': 'Mistura pobre (banco 1)',
                'system': 'Combustível',
                'cause': 'Filtro de ar sujo, MAF sujo ou injetores entupidos',
                'solution': 'Limpar MAF, verificar vazamentos',
                'severity': 'Média'
            },
            'P0135': {
                'description': 'Sensor O2 - aquecimento (banco 1)',
                'system': 'Emissões',
                'cause': 'Resistência de aquecimento queimada',
                'solution': 'Substituir sonda lambda',
                'severity': 'Média'
            },
            'P0335': {
                'description': 'Sensor CKP - circuito',
                'system': 'Motor',
                'cause': 'Sensor de rotação com defeito',
                'solution': 'Verificar sensor CKP',
                'severity': 'Alta'
            }
        }
    
    def get_dtc_info(self, code: str) -> Dict:
        return self.dtc_database.get(code, {
            'description': 'Código não encontrado',
            'system': 'Desconhecido',
            'cause': 'Consulte manual',
            'solution': 'Diagnóstico adicional necessário',
            'severity': 'Desconhecida'
        })
    
    def get_all_dtcs(self) -> List[Dict]:
        dtcs = []
        for code, info in self.dtc_database.items():
            info_copy = info.copy()
            info_copy['code'] = code
            dtcs.append(info_copy)
        return dtcs[:5]
