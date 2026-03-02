# dtc_database.py - Banco de dados de códigos de falha
from typing import Dict, List

class DTCDatabase:
    """
    Banco de dados de códigos de falha (DTC)
    """
    
    def __init__(self):
        self.dtc_database = self._build_database()
    
    def _build_database(self) -> Dict:
        """Constrói banco de dados de DTCs"""
        return {
            'P0300': {
                'description': 'Falha de ignição aleatória detectada',
                'system': 'Motor - Ignição',
                'cause': 'Velas defeituosas, cabos, bobinas',
                'solution': 'Verificar velas, cabos, bobinas',
                'severity': 'Alta'
            },
            'P0301': {
                'description': 'Falha de ignição no cilindro 1',
                'system': 'Motor - Ignição',
                'cause': 'Vela, injetor ou bobina do cilindro 1 com defeito',
                'solution': 'Testar vela, injetor e bobina do cilindro 1',
                'severity': 'Alta'
            },
            'P0302': {
                'description': 'Falha de ignição no cilindro 2',
                'system': 'Motor - Ignição',
                'cause': 'Vela, injetor ou bobina do cilindro 2 com defeito',
                'solution': 'Testar vela, injetor e bobina do cilindro 2',
                'severity': 'Alta'
            },
            'P0303': {
                'description': 'Falha de ignição no cilindro 3',
                'system': 'Motor - Ignição',
                'cause': 'Vela, injetor ou bobina do cilindro 3 com defeito',
                'solution': 'Testar vela, injetor e bobina do cilindro 3',
                'severity': 'Alta'
            },
            'P0304': {
                'description': 'Falha de ignição no cilindro 4',
                'system': 'Motor - Ignição',
                'cause': 'Vela, injetor ou bobina do cilindro 4 com defeito',
                'solution': 'Testar vela, injetor e bobina do cilindro 4',
                'severity': 'Alta'
            },
            'P0420': {
                'description': 'Eficiência do catalisador abaixo do limite',
                'system': 'Emissões',
                'cause': 'Catalisador danificado, sonda lambda com defeito',
                'solution': 'Substituir catalisador ou sonda lambda',
                'severity': 'Média'
            },
            'P0430': {
                'description': 'Eficiência do catalisador - banco 2',
                'system': 'Emissões',
                'cause': 'Catalisador danificado, sonda lambda com defeito',
                'solution': 'Substituir catalisador ou sonda lambda',
                'severity': 'Média'
            },
            'P0171': {
                'description': 'Mistura pobre (banco 1)',
                'system': 'Combustível',
                'cause': 'Filtro de ar sujo, sensor MAF sujo, injetores entupidos',
                'solution': 'Limpar filtro de ar, verificar sensor MAF',
                'severity': 'Média'
            },
            'P0172': {
                'description': 'Mistura rica (banco 1)',
                'system': 'Combustível',
                'cause': 'Injetores vazando, pressão de combustível alta',
                'solution': 'Verificar injetores e regulador de pressão',
                'severity': 'Média'
            },
            'P0174': {
                'description': 'Mistura pobre (banco 2)',
                'system': 'Combustível',
                'cause': 'Filtro de ar sujo, sensor MAF sujo',
                'solution': 'Limpar filtro de ar, verificar sensor MAF',
                'severity': 'Média'
            },
            'P0101': {
                'description': 'Sensor MAF - faixa/performance',
                'system': 'Admissão',
                'cause': 'Sensor MAF sujo ou com defeito',
                'solution': 'Limpar ou substituir sensor MAF',
                'severity': 'Média'
            },
            'P0102': {
                'description': 'Sensor MAF - entrada baixa',
                'system': 'Admissão',
                'cause': 'Circuito aberto, sensor com defeito',
                'solution': 'Verificar fiação e conector',
                'severity': 'Média'
            },
            'P0113': {
                'description': 'Sensor IAT - circuito alto',
                'system': 'Admissão',
                'cause': 'Sensor IAT com defeito',
                'solution': 'Verificar sensor IAT e conectores',
                'severity': 'Baixa'
            },
            'P0115': {
                'description': 'Sensor ECT - circuito',
                'system': 'Motor',
                'cause': 'Sensor de temperatura com defeito',
                'solution': 'Verificar sensor e fiação',
                'severity': 'Média'
            },
            'P0116': {
                'description': 'Sensor ECT - faixa/performance',
                'system': 'Motor',
                'cause': 'Sensor com leitura errática',
                'solution': 'Testar resistência do sensor',
                'severity': 'Média'
            },
            'P0120': {
                'description': 'Sensor TPS - circuito',
                'system': 'Aceleração',
                'cause': 'Sensor TPS com defeito',
                'solution': 'Verificar sensor e fiação',
                'severity': 'Média'
            },
            'P0121': {
                'description': 'Sensor TPS - faixa/performance',
                'system': 'Aceleração',
                'cause': 'Sensor TPS desgastado',
                'solution': 'Limpar ou substituir sensor TPS',
                'severity': 'Média'
            },
            'P0122': {
                'description': 'Sensor TPS - entrada baixa',
                'system': 'Aceleração',
                'cause': 'Curto à massa, sensor com defeito',
                'solution': 'Verificar fiação e sensor',
                'severity': 'Média'
            },
            'P0123': {
                'description': 'Sensor TPS - entrada alta',
                'system': 'Aceleração',
                'cause': 'Curto à alimentação',
                'solution': 'Verificar fiação',
                'severity': 'Média'
            },
            'P0130': {
                'description': 'Sensor O2 - circuito (banco 1 sensor 1)',
                'system': 'Emissões',
                'cause': 'Sensor com defeito, fiação danificada',
                'solution': 'Verificar sensor e fiação',
                'severity': 'Média'
            },
            'P0131': {
                'description': 'Sensor O2 - baixa tensão (banco 1 sensor 1)',
                'system': 'Emissões',
                'cause': 'Mistura pobre, sensor contaminado',
                'solution': 'Verificar mistura, substituir sensor',
                'severity': 'Média'
            },
            'P0132': {
                'description': 'Sensor O2 - alta tensão (banco 1 sensor 1)',
                'system': 'Emissões',
                'cause': 'Mistura rica, sensor contaminado',
                'solution': 'Verificar mistura, substituir sensor',
                'severity': 'Média'
            },
            'P0133': {
                'description': 'Sensor O2 - resposta lenta (banco 1 sensor 1)',
                'system': 'Emissões',
                'cause': 'Sensor envelhecido, contaminação',
                'solution': 'Substituir sensor',
                'severity': 'Média'
            },
            'P0134': {
                'description': 'Sensor O2 - circuito inativo (banco 1 sensor 1)',
                'system': 'Emissões',
                'cause': 'Sensor desconectado, fiação partida',
                'solution': 'Verificar conexão do sensor',
                'severity': 'Média'
            },
            'P0135': {
                'description': 'Sensor O2 - aquecimento (banco 1 sensor 1)',
                'system': 'Emissões',
                'cause': 'Resistência de aquecimento queimada',
                'solution': 'Verificar resistência, substituir sensor',
                'severity': 'Média'
            },
            'P0140': {
                'description': 'Sensor O2 - circuito inativo (banco 1 sensor 2)',
                'system': 'Emissões',
                'cause': 'Sensor desconectado',
                'solution': 'Verificar conexão',
                'severity': 'Média'
            },
            'P0141': {
                'description': 'Sensor O2 - aquecimento (banco 1 sensor 2)',
                'system': 'Emissões',
                'cause': 'Aquecedor com defeito',
                'solution': 'Substituir sensor',
                'severity': 'Média'
            },
            'P0325': {
                'description': 'Sensor de detonação - circuito',
                'system': 'Motor',
                'cause': 'Sensor de detonação com defeito',
                'solution': 'Verificar sensor e conectores',
                'severity': 'Média'
            },
            'P0326': {
                'description': 'Sensor de detonação - faixa/performance',
                'system': 'Motor',
                'cause': 'Sensor com leitura incorreta',
                'solution': 'Testar sensor, verificar torque de aperto',
                'severity': 'Média'
            },
            'P0335': {
                'description': 'Sensor CKP - circuito',
                'system': 'Motor',
                'cause': 'Sensor de rotação com defeito',
                'solution': 'Verificar sensor CKP',
                'severity': 'Alta'
            },
            'P0336': {
                'description': 'Sensor CKP - faixa/performance',
                'system': 'Motor',
                'cause': 'Sinal inconsistente, anel fônico danificado',
                'solution': 'Verificar anel fônico e sensor',
                'severity': 'Alta'
            },
            'P0340': {
                'description': 'Sensor CMP - circuito',
                'system': 'Motor',
                'cause': 'Sensor de fase com defeito',
                'solution': 'Verificar sensor CMP',
                'severity': 'Alta'
            },
            'P0341': {
                'description': 'Sensor CMP - faixa/performance',
                'system': 'Motor',
                'cause': 'Sinal fora de fase',
                'solution': 'Verificar sincronismo do motor',
                'severity': 'Alta'
            },
            'P0400': {
                'description': 'EGR - fluxo insuficiente',
                'system': 'Emissões',
                'cause': 'Válvula EGR entupida',
                'solution': 'Limpar válvula EGR',
                'severity': 'Baixa'
            },
            'P0401': {
                'description': 'EGR - fluxo insuficiente detectado',
                'system': 'Emissões',
                'cause': 'Válvula EGR suja, passagens obstruídas',
                'solution': 'Limpar válvula EGR e dutos',
                'severity': 'Baixa'
            },
            'P0402': {
                'description': 'EGR - fluxo excessivo',
                'system': 'Emissões',
                'cause': 'Válvula EGR aberta continuamente',
                'solution': 'Verificar válvula EGR',
                'severity': 'Baixa'
            },
            'P0442': {
                'description': 'Sistema EVAP - vazamento pequeno',
                'system': 'Emissões',
                'cause': 'Tampa do combustível mal fechada',
                'solution': 'Verificar tampa do combustível',
                'severity': 'Baixa'
            },
            'P0455': {
                'description': 'Sistema EVAP - vazamento grande',
                'system': 'Emissões',
                'cause': 'Vazamento no sistema',
                'solution': 'Verificar mangueiras',
                'severity': 'Média'
            },
            'P0500': {
                'description': 'Sensor de velocidade - circuito',
                'system': 'Transmissão',
                'cause': 'Sensor VSS com defeito',
                'solution': 'Verificar sensor de velocidade',
                'severity': 'Média'
            },
            'P0501': {
                'description': 'Sensor de velocidade - faixa/performance',
                'system': 'Transmissão',
                'cause': 'Sinal inconsistente',
                'solution': 'Verificar sensor e relutância',
                'severity': 'Média'
            },
            'P0505': {
                'description': 'Sistema de marcha lenta',
                'system': 'Motor',
                'cause': 'Motor de passo sujo, IAC com defeito',
                'solution': 'Limpar motor de passo',
                'severity': 'Baixa'
            },
            'P0506': {
                'description': 'Marcha lenta baixa',
                'system': 'Motor',
                'cause': 'IAC sujo, vazamento de vácuo',
                'solution': 'Limpar IAC, verificar vácuo',
                'severity': 'Baixa'
            },
            'P0507': {
                'description': 'Marcha lenta alta',
                'system': 'Motor',
                'cause': 'Vazamento de vácuo, IAC com defeito',
                'solution': 'Verificar vazamentos',
                'severity': 'Baixa'
            },
            'P0600': {
                'description': 'Falha de comunicação serial',
                'system': 'Eletrônico',
                'cause': 'Problema na rede CAN',
                'solution': 'Verificar rede CAN',
                'severity': 'Alta'
            },
            'P0601': {
                'description': 'Falha de memória interna',
                'system': 'Eletrônico',
                'cause': 'Checksum da ECU inválido',
                'solution': 'Reprogramar ou substituir ECU',
                'severity': 'Crítica'
            },
            'P0606': {
                'description': 'Falha interna da ECU',
                'system': 'Eletrônico',
                'cause': 'Processador da ECU com defeito',
                'solution': 'Substituir ECU',
                'severity': 'Crítica'
            },
            'P0700': {
                'description': 'Falha no sistema de transmissão',
                'system': 'Transmissão',
                'cause': 'Falha detectada pelo TCM',
                'solution': 'Verificar módulo da transmissão',
                'severity': 'Alta'
            },
            'P0705': {
                'description': 'Sensor de faixa da transmissão',
                'system': 'Transmissão',
                'cause': 'Sensor de posição do seletor com defeito',
                'solution': 'Verificar sensor e fiação',
                'severity': 'Alta'
            },
            'P0710': {
                'description': 'Sensor de temperatura do fluido',
                'system': 'Transmissão',
                'cause': 'Sensor TFT com defeito',
                'solution': 'Verificar sensor',
                'severity': 'Média'
            },
            'P0720': {
                'description': 'Sensor de velocidade de saída',
                'system': 'Transmissão',
                'cause': 'Sensor OSS com defeito',
                'solution': 'Verificar sensor',
                'severity': 'Alta'
            },
            'P0730': {
                'description': 'Relação de marcha incorreta',
                'system': 'Transmissão',
                'cause': 'Deslizamento da transmissão',
                'solution': 'Verificar nível de fluido, solenoides',
                'severity': 'Alta'
            },
            'P0740': {
                'description': 'Solenoide do conversor de torque',
                'system': 'Transmissão',
                'cause': 'Solenoide TCC com defeito',
                'solution': 'Verificar solenoide',
                'severity': 'Média'
            },
            'P0750': {
                'description': 'Solenoide de mudança A',
                'system': 'Transmissão',
                'cause': 'Solenoide com defeito',
                'solution': 'Testar solenoide',
                'severity': 'Média'
            },
            'C0035': {
                'description': 'Sensor ABS dianteiro esquerdo',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'C0040': {
                'description': 'Sensor ABS dianteiro direito',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'C0045': {
                'description': 'Sensor ABS traseiro esquerdo',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'C0050': {
                'description': 'Sensor ABS traseiro direito',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'U0100': {
                'description': 'Perda de comunicação com ECU',
                'system': 'Rede CAN',
                'cause': 'Falha na rede CAN',
                'solution': 'Verificar terminações CAN',
                'severity': 'Alta'
            },
            'U0101': {
                'description': 'Perda de comunicação com TCM',
                'system': 'Rede CAN',
                'cause': 'Falha na comunicação',
                'solution': 'Verificar módulo TCM',
                'severity': 'Alta'
            },
            'U0121': {
                'description': 'Perda de comunicação com ABS',
                'system': 'Rede CAN',
                'cause': 'Falha na comunicação',
                'solution': 'Verificar módulo ABS',
                'severity': 'Alta'
            }
        }
    
    def get_dtc_info(self, code: str) -> Dict:
        """Retorna informações detalhadas de um DTC"""
        return self.dtc_database.get(code, {
            'description': 'Código não encontrado',
            'system': 'Desconhecido',
            'cause': 'Consulte manual do veículo',
            'solution': 'Diagnóstico adicional necessário',
            'severity': 'Desconhecida'
        })
    
    def get_all_dtcs(self) -> List[Dict]:
        """Retorna lista de DTCs para simulação"""
        dtcs = []
        codes = ['P0301', 'P0420', 'P0171', 'P0335', 'P0101']
        for code in codes:
            info = self.dtc_database.get(code, {}).copy()
            info['code'] = code
            dtcs.append(info)
        return dtcs
    
    def search_dtcs(self, query: str) -> List[Dict]:
        """Busca DTCs por código"""
        results = []
        query = query.upper()
        for code, info in self.dtc_database.items():
            if query in code:
                result = info.copy()
                result['code'] = code
                results.append(result)
        return results
