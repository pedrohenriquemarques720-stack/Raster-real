# dtc_database.py - Banco de dados completo de falhas

class DTCDatabase:
    """
    Banco de dados completo de códigos de falha (DTC)
    Baseado em padrões SAE J2012
    """
    
    def __init__(self):
        self.dtc_database = self._build_database()
    
    def _build_database(self):
        """Constrói banco de dados de DTCs"""
        return {
            # =========================================
            # POWERTRAIN (P0xxx)
            # =========================================
            'P0300': {
                'description': 'Falha de ignição aleatória detectada',
                'system': 'Motor - Ignição',
                'cause': 'Velas defeituosas, cabos, bobinas, injeção',
                'solution': 'Verificar velas, cabos, bobinas de ignição',
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
            'P0101': {
                'description': 'Sensor MAF - faixa/performance',
                'system': 'Admissão',
                'cause': 'Sensor MAF sujo ou com defeito',
                'solution': 'Limpar ou substituir sensor MAF',
                'severity': 'Média'
            },
            'P0113': {
                'description': 'Sensor IAT - circuito alto',
                'system': 'Admissão',
                'cause': 'Sensor IAT com defeito, curto no circuito',
                'solution': 'Verificar sensor IAT e conectores',
                'severity': 'Baixa'
            },
            'P0121': {
                'description': 'Sensor TPS - faixa/performance',
                'system': 'Aceleração',
                'cause': 'Sensor TPS desgastado ou sujo',
                'solution': 'Limpar ou substituir sensor TPS',
                'severity': 'Média'
            },
            'P0135': {
                'description': 'Sonda O2 - aquecimento (banco 1 sensor 1)',
                'system': 'Emissões',
                'cause': 'Resistência de aquecimento da sonda queimada',
                'solution': 'Substituir sonda lambda',
                'severity': 'Média'
            },
            'P0141': {
                'description': 'Sonda O2 - aquecimento (banco 1 sensor 2)',
                'system': 'Emissões',
                'cause': 'Resistência de aquecimento da sonda queimada',
                'solution': 'Substituir sonda lambda',
                'severity': 'Média'
            },
            'P0325': {
                'description': 'Sensor de detonação - circuito',
                'system': 'Motor',
                'cause': 'Sensor de detonação com defeito',
                'solution': 'Verificar sensor e conectores',
                'severity': 'Média'
            },
            'P0335': {
                'description': 'Sensor CKP - circuito',
                'system': 'Motor',
                'cause': 'Sensor de rotação com defeito',
                'solution': 'Verificar sensor CKP e conectores',
                'severity': 'Alta'
            },
            'P0340': {
                'description': 'Sensor CMP - circuito',
                'system': 'Motor',
                'cause': 'Sensor de fase com defeito',
                'solution': 'Verificar sensor CMP e conectores',
                'severity': 'Alta'
            },
            'P0401': {
                'description': 'EGR - fluxo insuficiente',
                'system': 'Emissões',
                'cause': 'Válvula EGR suja ou com defeito',
                'solution': 'Limpar ou substituir válvula EGR',
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
                'cause': 'Vazamento no sistema de combustível',
                'solution': 'Verificar mangueiras e canister',
                'severity': 'Média'
            },
            'P0500': {
                'description': 'Sensor de velocidade - circuito',
                'system': 'Transmissão',
                'cause': 'Sensor VSS com defeito',
                'solution': 'Verificar sensor de velocidade',
                'severity': 'Média'
            },
            'P0505': {
                'description': 'Sistema de marcha lenta',
                'system': 'Motor',
                'cause': 'Motor de passo sujo, IAC com defeito',
                'solution': 'Limpar motor de passo, verificar IAC',
                'severity': 'Baixa'
            },
            'P0600': {
                'description': 'Falha de comunicação serial',
                'system': 'Eletrônico',
                'cause': 'Problema na comunicação CAN bus',
                'solution': 'Verificar rede CAN e módulos',
                'severity': 'Alta'
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
            
            # =========================================
            # CHASSIS (C0xxx)
            # =========================================
            'C0035': {
                'description': 'Sensor de velocidade roda dianteira esquerda',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'C0040': {
                'description': 'Sensor de velocidade roda dianteira direita',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'C0045': {
                'description': 'Sensor de velocidade roda traseira esquerda',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'C0050': {
                'description': 'Sensor de velocidade roda traseira direita',
                'system': 'ABS',
                'cause': 'Sensor ABS com defeito',
                'solution': 'Verificar sensor e anel dentado',
                'severity': 'Média'
            },
            'C0110': {
                'description': 'Bomba do ABS - circuito',
                'system': 'ABS',
                'cause': 'Relé da bomba ou motor com defeito',
                'solution': 'Verificar relé e motor da bomba',
                'severity': 'Alta'
            },
            'C0121': {
                'description': 'Válvula solenoide ABS - circuito',
                'system': 'ABS',
                'cause': 'Válvula do módulo hidráulico com defeito',
                'solution': 'Substituir módulo ABS',
                'severity': 'Alta'
            },
            
            # =========================================
            # BODY (B0xxx)
            # =========================================
            'B1000': {
                'description': 'Falha interna no módulo da carroceria',
                'system': 'BCM',
                'cause': 'Problema no módulo BCM',
                'solution': 'Verificar alimentação e reprogramar',
                'severity': 'Média'
            },
            'B1325': {
                'description': 'Tensão da bateria - fora da faixa',
                'system': 'Elétrico',
                'cause': 'Bateria fraca ou alternador com defeito',
                'solution': 'Verificar bateria e alternador',
                'severity': 'Média'
            },
            'B1400': {
                'description': 'Sensor de temperatura interna',
                'system': 'Climatização',
                'cause': 'Sensor com defeito',
                'solution': 'Substituir sensor',
                'severity': 'Baixa'
            },
            'B1410': {
                'description': 'Motor do ventilador - circuito',
                'system': 'Climatização',
                'cause': 'Motor do ventilador ou resistor com defeito',
                'solution': 'Verificar motor e resistor',
                'severity': 'Baixa'
            },
            'B1420': {
                'description': 'Sensor de temperatura externa',
                'system': 'Climatização',
                'cause': 'Sensor com defeito',
                'solution': 'Substituir sensor',
                'severity': 'Baixa'
            },
            'B1600': {
                'description': 'Chave de ignição - circuito',
                'system': 'Imobilizador',
                'cause': 'Problema na chave ou leitor',
                'solution': 'Verificar chave e antena',
                'severity': 'Alta'
            },
            'B1620': {
                'description': 'Comunicação com chave codificada',
                'system': 'Imobilizador',
                'cause': 'Chave não reconhecida',
                'solution': 'Reprogramar chaves',
                'severity': 'Alta'
            },
            'B1800': {
                'description': 'Airbag motorista - resistência alta',
                'system': 'SRS',
                'cause': 'Conector do airbag com mau contato',
                'solution': 'Verificar conector do airbag',
                'severity': 'Crítica'
            },
            'B1805': {
                'description': 'Airbag passageiro - resistência alta',
                'system': 'SRS',
                'cause': 'Conector do airbag com mau contato',
                'solution': 'Verificar conector do airbag',
                'severity': 'Crítica'
            },
            'B1810': {
                'description': 'Sensor de impacto lateral - circuito',
                'system': 'SRS',
                'cause': 'Sensor com defeito',
                'solution': 'Substituir sensor',
                'severity': 'Crítica'
            },
            'B1860': {
                'description': 'Pré-tensor do cinto - circuito',
                'system': 'SRS',
                'cause': 'Pré-tensor com defeito',
                'solution': 'Substituir pré-tensor',
                'severity': 'Crítica'
            },
            'B1900': {
                'description': 'Sensor de colisão frontal - circuito',
                'system': 'SRS',
                'cause': 'Sensor com defeito',
                'solution': 'Substituir sensor',
                'severity': 'Crítica'
            },
            
            # =========================================
            # NETWORK (U0xxx)
            # =========================================
            'U0100': {
                'description': 'Perda de comunicação com ECU',
                'system': 'Rede CAN',
                'cause': 'Falha na rede CAN, módulo sem comunicação',
                'solution': 'Verificar terminações CAN, alimentação do módulo',
                'severity': 'Alta'
            },
            'U0101': {
                'description': 'Perda de comunicação com TCM',
                'system': 'Rede CAN',
                'cause': 'Módulo da transmissão sem comunicação',
                'solution': 'Verificar TCM e rede CAN',
                'severity': 'Alta'
            },
            'U0121': {
                'description': 'Perda de comunicação com ABS',
                'system': 'Rede CAN',
                'cause': 'Módulo ABS sem comunicação',
                'solution': 'Verificar módulo ABS',
                'severity': 'Alta'
            },
            'U0140': {
                'description': 'Perda de comunicação com BCM',
                'system': 'Rede CAN',
                'cause': 'Módulo BCM sem comunicação',
                'solution': 'Verificar BCM',
                'severity': 'Alta'
            },
            'U0155': {
                'description': 'Perda de comunicação com cluster',
                'system': 'Rede CAN',
                'cause': 'Painel de instrumentos sem comunicação',
                'solution': 'Verificar cluster',
                'severity': 'Média'
            },
            'U1000': {
                'description': 'Falha na comunicação CAN bus',
                'system': 'Rede CAN',
                'cause': 'Problema geral na rede CAN',
                'solution': 'Verificar cabos CAN e terminações',
                'severity': 'Alta'
            }
        }
    
    def get_dtc_info(self, code):
        """Retorna informações detalhadas de um DTC"""
        return self.dtc_database.get(code, {
            'description': 'Código não encontrado',
            'system': 'Desconhecido',
            'cause': 'Consulte manual do veículo',
            'solution': 'Diagnóstico adicional necessário',
            'severity': 'Desconhecida'
        })
    
    def get_all_dtcs(self):
        """Retorna lista de todos os DTCs com informações"""
        dtcs = []
        for code, info in self.dtc_database.items():
            dtc_info = info.copy()
            dtc_info['code'] = code
            dtcs.append(dtc_info)
        return dtcs[:5]  # Retorna apenas 5 para simulação
    
    def search_dtcs(self, query):
        """Busca DTCs por código ou descrição"""
        results = []
        query = query.upper()
        for code, info in self.dtc_database.items():
            if query in code or query.lower() in info['description'].lower():
                result = info.copy()
                result['code'] = code
                results.append(result)
        return results
