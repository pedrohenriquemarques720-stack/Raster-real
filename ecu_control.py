# ecu_control.py - Módulo de Controle Bidirecional para Scanner Automotivo

import time
import random
import struct
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import threading
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================
# CONSTANTES E CONFIGURAÇÕES
# =============================================

class ProtocolType(Enum):
    """Tipos de protocolo suportados"""
    CAN_11BIT = "CAN 11-bit (500kbps)"
    CAN_29BIT = "CAN 29-bit (500kbps)"
    KWP2000 = "KWP2000"
    ISO9141 = "ISO 9141"

class ServiceID(Enum):
    """IDs de serviço UDS"""
    DIAGNOSTIC_SESSION_CONTROL = 0x10
    ECU_RESET = 0x11
    READ_DATA = 0x22
    READ_SCALING_DATA = 0x24
    WRITE_DATA = 0x2E
    ROUTINE_CONTROL = 0x31
    REQUEST_DOWNLOAD = 0x34
    REQUEST_UPLOAD = 0x35
    TRANSFER_DATA = 0x36
    REQUEST_TRANSFER_EXIT = 0x37
    POSITIVE_RESPONSE = 0x40
    NEGATIVE_RESPONSE = 0x7F
    
    # Respostas específicas para escrita
    WRITE_RESPONSE = 0x6E  # Resposta positiva para 0x2E

class NegativeResponseCode(Enum):
    """Códigos de resposta negativa"""
    GENERAL_REJECT = 0x10
    SERVICE_NOT_SUPPORTED = 0x11
    SUBFUNCTION_NOT_SUPPORTED = 0x12
    INCORRECT_MESSAGE_LENGTH = 0x13
    RESPONSE_TOO_LONG = 0x14
    BUSY_REPEAT_REQUEST = 0x21
    CONDITIONS_NOT_CORRECT = 0x22
    REQUEST_SEQUENCE_ERROR = 0x24
    NO_RESPONSE_FROM_SUBNET = 0x25
    FAILURE_PREVENTS_ACTION = 0x26
    REQUEST_OUT_OF_RANGE = 0x31
    SECURITY_ACCESS_DENIED = 0x33
    INVALID_KEY = 0x35
    EXCEEDED_NUMBER_OF_ATTEMPTS = 0x36
    REQUIRED_TIME_DELAY_NOT_EXPIRED = 0x37
    UPLOAD_DOWNLOAD_NOT_ACCEPTED = 0x70
    TRANSFER_DATA_SUSPENDED = 0x71
    GENERAL_PROGRAMMING_FAILURE = 0x72
    WRONG_BLOCK_SEQUENCE = 0x73
    RESPONSE_PENDING = 0x78

@dataclass
class PIDParameter:
    """Definição de parâmetro OBD/UDS"""
    id: int
    name: str
    unit: str
    min_val: float
    max_val: float
    default_val: float
    step: float
    can_id_request: int
    can_id_response: int
    can_29bit_request: int
    can_29bit_response: int
    kwp_id: int
    data_format: str  # 'uint8', 'uint16', 'float', 'percent'
    scaling_factor: float = 1.0
    description: str = ""
    manufacturer_specific: bool = False

@dataclass
class ECUResponse:
    """Resposta da ECU"""
    success: bool
    service: Optional[ServiceID] = None
    data: Optional[bytes] = None
    value: Optional[float] = None
    nrc: Optional[NegativeResponseCode] = None
    response_time_ms: float = 0
    raw_response: Optional[bytes] = None
    message: str = ""

@dataclass
class SafetyStatus:
    """Status das condições de segurança"""
    safe: bool
    reason: Optional[str] = None
    rpm: Optional[int] = None
    temp: Optional[int] = None
    speed: Optional[int] = None
    battery: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)

# =============================================
# BASE DE DADOS DE PARÂMETROS (PROFISSIONAL)
# =============================================

class ParameterDatabase:
    """Banco de dados de parâmetros por fabricante"""
    
    def __init__(self):
        self.parameters = self._init_parameters()
        self.manufacturer_params = self._init_manufacturer_params()
        
    def _init_parameters(self) -> Dict[int, PIDParameter]:
        """Inicializa parâmetros universais"""
        return {
            # Long Term Fuel Trim (Bank 1)
            0x0107: PIDParameter(
                id=0x0107,
                name="Long Term Fuel Trim",
                unit="%",
                min_val=-25.0,
                max_val=25.0,
                default_val=0.0,
                step=0.5,
                can_id_request=0x7E0,
                can_id_response=0x7E8,
                can_29bit_request=0x18DAF100,
                can_29bit_response=0x18DAF108,
                kwp_id=0x0107,
                data_format="int8",
                scaling_factor=0.5,
                description="Correção de longo prazo da mistura ar/combustível"
            ),
            
            # Idle Speed Target
            0x0105: PIDParameter(
                id=0x0105,
                name="Idle Speed Target",
                unit="RPM",
                min_val=600,
                max_val=1200,
                default_val=800,
                step=10,
                can_id_request=0x7E0,
                can_id_response=0x7E8,
                can_29bit_request=0x18DAF100,
                can_29bit_response=0x18DAF108,
                kwp_id=0x0105,
                data_format="uint16",
                description="RPM alvo para marcha lenta"
            ),
            
            # O2 Sensor Voltage (Bank 1 Sensor 1)
            0x0014: PIDParameter(
                id=0x0014,
                name="O2 Sensor Voltage",
                unit="V",
                min_val=0.0,
                max_val=1.275,
                default_val=0.45,
                step=0.01,
                can_id_request=0x7E0,
                can_id_response=0x7E8,
                can_29bit_request=0x18DAF100,
                can_29bit_response=0x18DAF108,
                kwp_id=0x0014,
                data_format="uint16",
                scaling_factor=0.005,
                description="Tensão do sensor de oxigênio"
            ),
            
            # Lambda Actual Value
            0x002E: PIDParameter(
                id=0x002E,
                name="Lambda Value",
                unit="λ",
                min_val=0.7,
                max_val=1.3,
                default_val=1.0,
                step=0.01,
                can_id_request=0x7E0,
                can_id_response=0x7E8,
                can_29bit_request=0x18DAF100,
                can_29bit_response=0x18DAF108,
                kwp_id=0x002E,
                data_format="uint16",
                scaling_factor=0.001,
                description="Fator Lambda em tempo real"
            ),
        }
    
    def _init_manufacturer_params(self) -> Dict[str, Dict[int, PIDParameter]]:
        """Inicializa parâmetros específicos por fabricante"""
        return {
            'VOLKSWAGEN': {
                # Injection Pulse Width (VW specific)
                0x2210: PIDParameter(
                    id=0x2210,
                    name="Injection Pulse Width",
                    unit="ms",
                    min_val=1.5,
                    max_val=8.0,
                    default_val=3.5,
                    step=0.1,
                    can_id_request=0x7E0,
                    can_id_response=0x7E8,
                    can_29bit_request=0x18DAF100,
                    can_29bit_response=0x18DAF108,
                    kwp_id=0x2210,
                    data_format="uint16",
                    scaling_factor=0.01,
                    description="Tempo de injeção (EA211)",
                    manufacturer_specific=True
                ),
                
                # Flex Fuel Adaptation Reset (VW specific)
                0x3301: PIDParameter(
                    id=0x3301,
                    name="Flex Fuel Reset",
                    unit="",
                    min_val=0,
                    max_val=1,
                    default_val=0,
                    step=1,
                    can_id_request=0x7E0,
                    can_id_response=0x7E8,
                    can_29bit_request=0x18DAF100,
                    can_29bit_response=0x18DAF108,
                    kwp_id=0x3301,
                    data_format="uint8",
                    description="Reset das adaptações de combustível flex",
                    manufacturer_specific=True
                ),
            },
            'FIAT': {
                # Injection Time (FIA specific)
                0x2211: PIDParameter(
                    id=0x2211,
                    name="Injection Time",
                    unit="ms",
                    min_val=1.5,
                    max_val=8.0,
                    default_val=3.2,
                    step=0.1,
                    can_id_request=0x7E0,
                    can_id_response=0x7E8,
                    can_29bit_request=0x18DAF100,
                    can_29bit_response=0x18DAF108,
                    kwp_id=0x2211,
                    data_format="uint16",
                    scaling_factor=0.01,
                    description="Tempo de injeção (Firefly)",
                    manufacturer_specific=True
                ),
            }
        }
    
    def get_parameter(self, pid: int, manufacturer: str = "GENERIC") -> Optional[PIDParameter]:
        """Obtém parâmetro por ID e fabricante"""
        # Primeiro tenta parâmetro específico do fabricante
        if manufacturer in self.manufacturer_params:
            if pid in self.manufacturer_params[manufacturer]:
                return self.manufacturer_params[manufacturer][pid]
        
        # Depois tenta parâmetro universal
        return self.parameters.get(pid)

# =============================================
# SIMULADOR DE CAN BUS (para desenvolvimento)
# =============================================

class CANSIMULATOR:
    """Simulador de barramento CAN para testes"""
    
    def __init__(self):
        self.messages = []
        self.responses = {}
        self._setup_responses()
        
    def _setup_responses(self):
        """Configura respostas simuladas"""
        self.responses = {
            0x7E0: {
                0x0107: lambda x: struct.pack('>B', int((x + 100) / 0.5)),  # LTFT
                0x0105: lambda x: struct.pack('>H', x),  # Idle RPM
                0x2210: lambda x: struct.pack('>H', int(x * 100)),  # Injection
                0x3301: lambda x: struct.pack('>B', 0x01),  # Flex Reset
            }
        }
    
    def send(self, arbitration_id: int, data: bytes, extended: bool = False) -> bool:
        """Simula envio de mensagem CAN"""
        msg = {
            'id': arbitration_id,
            'data': data,
            'extended': extended,
            'timestamp': time.time()
        }
        self.messages.append(msg)
        logger.debug(f"CAN Send: ID=0x{arbitration_id:X} Data={data.hex()}")
        return True
    
    def recv(self, timeout: float = 1.0) -> Optional[Dict]:
        """Simula recebimento de resposta"""
        time.sleep(0.05)  # Simula latência
        
        if self.messages:
            last_msg = self.messages[-1]
            
            # Simula resposta positiva
            if last_msg['id'] == 0x7E0:
                # Resposta positiva UDS (0x6E + Request ID + data)
                response_id = 0x7E8 if not last_msg['extended'] else 0x18DAF108
                response_data = bytearray([0x6E, last_msg['data'][1], last_msg['data'][2]])
                
                # Adiciona dados de resposta simulados
                if len(last_msg['data']) > 3 and last_msg['data'][2] in self.responses.get(0x7E0, {}):
                    func = self.responses[0x7E0][last_msg['data'][2]]
                    value_data = func(last_msg['data'][3])
                    response_data.extend(value_data)
                
                return {
                    'id': response_id,
                    'data': bytes(response_data),
                    'extended': last_msg['extended']
                }
        
        return None

# =============================================
# CLASSE PRINCIPAL DE CONTROLE DA ECU
# =============================================

class ECUControl:
    """
    Classe principal para controle bidirecional da ECU
    Suporta UDS (ISO 14229) e protocolos específicos
    """
    
    def __init__(self, protocol: ProtocolType = ProtocolType.CAN_11BIT, 
                 manufacturer: str = "VOLKSWAGEN",
                 use_simulator: bool = True):
        """
        Inicializa controlador da ECU
        
        Args:
            protocol: Protocolo de comunicação
            manufacturer: Fabricante do veículo
            use_simulator: Usar simulador (True) ou CAN real (False)
        """
        self.protocol = protocol
        self.manufacturer = manufacturer
        self.use_simulator = use_simulator
        self.param_db = ParameterDatabase()
        self.simulator = CANSIMULATOR() if use_simulator else None
        self.can_bus = None  # Placeholder para CAN real
        self.session_active = False
        self.security_level = 0
        self.logs = []
        
        # Dados ao vivo (simulados ou reais)
        self.live_data = {
            'rpm': 850,
            'speed': 0,
            'coolant_temp': 89,
            'battery': 13.8,
            'o2_voltage': 0.78,
            'lambda': 1.02,
            'stft': 2.5,
            'ltft': 3.2
        }
        
    def _log(self, message: str, level: str = "INFO"):
        """Adiciona entrada ao log técnico"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.logs.append(entry)
        getattr(logger, level.lower(), logger.info)(message)
        
    def check_safety_conditions(self, rpm: Optional[int] = None, 
                                 temp: Optional[int] = None,
                                 speed: Optional[int] = None) -> SafetyStatus:
        """
        Verifica condições de segurança para escrita
        
        Args:
            rpm: RPM atual (se None, usa dado simulado)
            temp: Temperatura do motor (se None, usa dado simulado)
            speed: Velocidade (se None, usa dado simulado)
            
        Returns:
            SafetyStatus indicando se é seguro escrever
        """
        # Usa valores fornecidos ou simulados
        rpm_val = rpm if rpm is not None else self.live_data['rpm']
        temp_val = temp if temp is not None else self.live_data['coolant_temp']
        speed_val = speed if speed is not None else self.live_data['speed']
        
        # Verificações de segurança
        if rpm_val > 1200:
            return SafetyStatus(
                safe=False,
                reason=f"RPM elevado: {rpm_val} > 1200 (máx. permitido)",
                rpm=rpm_val,
                temp=temp_val,
                speed=speed_val
            )
            
        if temp_val < 80:
            return SafetyStatus(
                safe=False,
                reason=f"Motor frio: {temp_val}°C < 80°C (mínimo necessário)",
                rpm=rpm_val,
                temp=temp_val,
                speed=speed_val
            )
            
        if speed_val > 0:
            return SafetyStatus(
                safe=False,
                reason=f"Veículo em movimento: {speed_val} km/h > 0",
                rpm=rpm_val,
                temp=temp_val,
                speed=speed_val
            )
            
        return SafetyStatus(
            safe=True,
            rpm=rpm_val,
            temp=temp_val,
            speed=speed_val
        )
    
    def _build_uds_write_request(self, pid: PIDParameter, value: float) -> bytes:
        """
        Constrói requisição UDS Write (0x2E)
        
        Formato: [Service ID (0x2E)] [PID High] [PID Low] [Data...]
        """
        request = bytearray()
        request.append(ServiceID.WRITE_DATA.value)  # 0x2E
        
        # PID em 2 bytes
        request.append((pid.id >> 8) & 0xFF)  # PID High
        request.append(pid.id & 0xFF)          # PID Low
        
        # Codifica valor conforme formato
        if pid.data_format == "uint8":
            request.append(int(value) & 0xFF)
        elif pid.data_format == "uint16":
            request.extend(struct.pack('>H', int(value)))
        elif pid.data_format == "int8":
            request.append(struct.pack('b', int(value))[0] & 0xFF)
        elif pid.data_format == "float":
            # Converte float para inteiro escalado
            scaled = int(value / pid.scaling_factor)
            request.extend(struct.pack('>H', scaled))
        elif pid.data_format == "percent":
            scaled = int(value / pid.scaling_factor)
            request.append(scaled & 0xFF)
        else:
            # Default: uint8
            request.append(int(value) & 0xFF)
            
        return bytes(request)
    
    def _parse_uds_response(self, response: bytes, pid: PIDParameter) -> ECUResponse:
        """
        Analisa resposta UDS
        
        Args:
            response: Bytes recebidos da ECU
            pid: Parâmetro que foi escrito
            
        Returns:
            ECUResponse com resultado da operação
        """
        if not response or len(response) < 2:
            return ECUResponse(
                success=False,
                message="Resposta vazia ou muito curta"
            )
        
        first_byte = response[0]
        
        # Verifica se é resposta negativa
        if first_byte == ServiceID.NEGATIVE_RESPONSE.value:
            nrc = response[2] if len(response) > 2 else 0
            try:
                nrc_enum = NegativeResponseCode(nrc)
                message = f"Resposta negativa: {nrc_enum.name}"
            except:
                message = f"Resposta negativa: Código {nrc:02X}"
                
            return ECUResponse(
                success=False,
                service=ServiceID.NEGATIVE_RESPONSE,
                nrc=NegativeResponseCode(nrc) if nrc in NegativeResponseCode._value2member_map_ else None,
                raw_response=response,
                message=message
            )
            
        # Verifica se é resposta positiva para escrita (0x6E)
        if first_byte == ServiceID.WRITE_RESPONSE.value:
            # Resposta positiva: [0x6E] [PID High] [PID Low] [Data...]
            return ECUResponse(
                success=True,
                service=ServiceID.WRITE_RESPONSE,
                data=response[3:] if len(response) > 3 else None,
                raw_response=response,
                message="Escrita realizada com sucesso"
            )
            
        return ECUResponse(
            success=False,
            raw_response=response,
            message=f"Resposta não reconhecida: {response.hex()}"
        )
    
    def write_parameter(self, pid: int, value: float, 
                        force: bool = False) -> ECUResponse:
        """
        Escreve parâmetro na ECU
        
        Args:
            pid: ID do parâmetro
            value: Valor a ser escrito
            force: Ignora verificações de segurança (apenas para testes)
            
        Returns:
            ECUResponse com resultado da operação
        """
        # 1. Verifica segurança (a menos que force=True)
        if not force:
            safety = self.check_safety_conditions()
            if not safety.safe:
                self._log(f"Bloqueado por segurança: {safety.reason}", "WARNING")
                return ECUResponse(
                    success=False,
                    message=f"Condições de segurança não atendidas: {safety.reason}"
                )
        
        # 2. Obtém definição do parâmetro
        param = self.param_db.get_parameter(pid, self.manufacturer)
        if not param:
            self._log(f"Parâmetro 0x{pid:04X} não encontrado", "ERROR")
            return ECUResponse(
                success=False,
                message=f"Parâmetro 0x{pid:04X} não suportado"
            )
        
        # 3. Valida valor dentro da faixa
        if value < param.min_val or value > param.max_val:
            self._log(f"Valor fora da faixa: {value} ({param.min_val}-{param.max_val})", "WARNING")
            return ECUResponse(
                success=False,
                message=f"Valor deve estar entre {param.min_val} e {param.max_val}"
            )
        
        # 4. Determina IDs CAN baseado no protocolo
        if self.protocol == ProtocolType.CAN_29BIT:
            req_id = param.can_29bit_request
            resp_id = param.can_29bit_response
        else:
            req_id = param.can_id_request
            resp_id = param.can_id_response
        
        # 5. Constrói requisição
        request = self._build_uds_write_request(param, value)
        
        self._log(f"Enviando escrita: PID=0x{pid:04X} Valor={value}{param.unit} "
                  f"Protocolo={self.protocol.value}")
        
        start_time = time.time()
        
        try:
            # 6. Envia via simulador ou CAN real
            if self.use_simulator:
                self.simulator.send(req_id, request, extended=(self.protocol == ProtocolType.CAN_29BIT))
                response_msg = self.simulator.recv(timeout=1.0)
                
                if response_msg:
                    response = response_msg['data']
                else:
                    response = None
            else:
                # Placeholder para CAN real
                # self.can_bus.send(req_id, request)
                # response = self.can_bus.recv(timeout=1.0)
                response = None
                
            elapsed_ms = (time.time() - start_time) * 1000
            
            # 7. Analisa resposta
            if response:
                result = self._parse_uds_response(response, param)
                result.response_time_ms = elapsed_ms
                
                if result.success:
                    self._log(f"Sucesso! Resposta em {elapsed_ms:.1f}ms: {result.message}")
                else:
                    self._log(f"Falha: {result.message}", "ERROR")
                    
                return result
            else:
                self._log("Timeout - sem resposta da ECU", "ERROR")
                return ECUResponse(
                    success=False,
                    message="Timeout - sem resposta da ECU",
                    response_time_ms=elapsed_ms
                )
                
        except Exception as e:
            self._log(f"Erro na comunicação: {str(e)}", "ERROR")
            return ECUResponse(
                success=False,
                message=f"Erro de comunicação: {str(e)}"
            )
    
    # =========================================
    # FUNÇÕES ESPECÍFICAS DE AJUSTE
    # =========================================
    
    def adjust_fuel_trim(self, value: float, force: bool = False) -> ECUResponse:
        """
        Ajusta Long Term Fuel Trim
        
        Args:
            value: Valor em percentual (-25 a +25)
            force: Ignora verificações de segurança
        """
        return self.write_parameter(0x0107, value, force)
    
    def adjust_idle_speed(self, rpm: int, force: bool = False) -> ECUResponse:
        """
        Ajusta RPM de marcha lenta
        
        Args:
            rpm: RPM alvo (600-1200)
            force: Ignora verificações de segurança
        """
        return self.write_parameter(0x0105, rpm, force)
    
    def adjust_injection_pulse(self, ms: float, force: bool = False) -> ECUResponse:
        """
        Ajusta tempo de injeção (específico do fabricante)
        
        Args:
            ms: Tempo de injeção em milissegundos
            force: Ignora verificações de segurança
        """
        # Tenta parâmetro específico do fabricante
        if self.manufacturer == "VOLKSWAGEN":
            return self.write_parameter(0x2210, ms, force)
        elif self.manufacturer == "FIAT":
            return self.write_parameter(0x2211, ms, force)
        else:
            return ECUResponse(
                success=False,
                message=f"Fabricante {self.manufacturer} não suporta ajuste de injeção"
            )
    
    def reset_flex_fuel(self, force: bool = False) -> ECUResponse:
        """
        Reseta parâmetros de adaptação de combustível flex
        
        Args:
            force: Ignora verificações de segurança
        """
        return self.write_parameter(0x3301, 1, force)
    
    def auto_tune_to_lambda1(self, max_attempts: int = 10) -> Dict[str, Any]:
        """
        Otimização automática para Lambda = 1.0
        
        Args:
            max_attempts: Número máximo de tentativas
            
        Returns:
            Dicionário com resultados da otimização
        """
        self._log("Iniciando otimização automática para Lambda 1.0", "INFO")
        
        # Verifica segurança
        safety = self.check_safety_conditions()
        if not safety.safe:
            self._log(f"Otimização bloqueada: {safety.reason}", "WARNING")
            return {
                'success': False,
                'reason': safety.reason,
                'lambda_final': None,
                'injection_final': None,
                'attempts': 0
            }
        
        current_lambda = self.live_data.get('lambda', 1.02)
        current_injection = 3.5  # Valor inicial simulado
        
        results = {
            'success': False,
            'lambda_inicial': current_lambda,
            'injection_inicial': current_injection,
            'lambda_final': None,
            'injection_final': None,
            'attempts': 0,
            'history': []
        }
        
        # Algoritmo de busca do lambda ideal
        for attempt in range(max_attempts):
            # Lê lambda atual (simulado)
            current_lambda = self.live_data.get('lambda', 1.0 + random.uniform(-0.1, 0.1))
            
            # Calcula erro
            error = current_lambda - 1.0
            
            # Ajusta injeção baseado no erro
            if abs(error) < 0.01:
                results['success'] = True
                results['lambda_final'] = current_lambda
                results['injection_final'] = current_injection
                results['attempts'] = attempt + 1
                self._log(f"Lambda ideal alcançado: {current_lambda:.3f} após {attempt+1} tentativas")
                break
                
            # Ajuste proporcional
            adjustment = -error * 0.5  # Ganho de correção
            current_injection += adjustment
            current_injection = max(1.5, min(8.0, current_injection))  # Limites
            
            # Simula escrita
            resp = self.adjust_injection_pulse(current_injection, force=True)
            
            results['history'].append({
                'attempt': attempt + 1,
                'lambda': current_lambda,
                'injection': current_injection,
                'error': error,
                'response': resp.message if resp else "N/A"
            })
            
            time.sleep(0.2)  # Aguarda resposta da ECU
            
        return results
    
    def get_logs(self, last_n: int = 20) -> List[Dict]:
        """Retorna últimos logs"""
        return self.logs[-last_n:]

# =============================================
# EXPLICAÇÃO DOS PROTOCOLOS
# =============================================

"""
DIFERENÇAS ENTRE PROTOCOLOS CAN 11-bit e 29-bit:

1. CAN 11-bit (Padrão OBD-II):
   - ID: 11 bits (0x000 a 0x7FF)
   - Request: 0x7E0 (ECU de powertrain)
   - Response: 0x7E8 (ECU respondendo)
   - Usado em veículos até ~2010
   - Mais simples, menor overhead

2. CAN 29-bit (CAN Extended):
   - ID: 29 bits (0x00000000 a 0x1FFFFFFF)
   - Request: 0x18DAF100 (Formato: 0x18DA + F1 + 00)
   - Response: 0x18DAF108 (0x18DA + F1 + 08)
   - Usado em veículos mais novos
   - Permite mais ECUs e priorização

3. UDS sobre CAN:
   - Mesmo formato base, independente do ID
   - Service 0x2E: Write Data By Identifier
   - Formato: [Service] [PID High] [PID Low] [Data...]
   - Resposta positiva: 0x6E + PID + Data
   - Resposta negativa: 0x7F + Service + NRC

4. KWP2000 (ISO 14230):
   - Protocolo mais antigo, predecessor do UDS
   - Usa IDs diferentes para parâmetros
   - Formato de mensagem diferente
"""

# =============================================
# COMPONENTE STREAMLIT
# =============================================

def create_tuning_interface(ecu_control: ECUControl):
    """
    Cria interface de tuning para Streamlit
    
    Args:
        ecu_control: Instância de ECUControl
    
    Returns:
        Componente Streamlit
    """
    import streamlit as st
    
    st.markdown("## ⚡ CONTROLE ATIVO DO MOTOR")
    st.markdown("### Ajuste de Parâmetros em Tempo Real")
    
    # Status de segurança
    safety = ecu_control.check_safety_conditions()
    
    if not safety.safe:
        st.error(f"⚠️ **BLOQUEADO POR SEGURANÇA**: {safety.reason}")
        st.info(f"RPM: {safety.rpm} | Temp: {safety.temp}°C | Vel: {safety.speed} km/h")
    else:
        st.success("✅ **Condições de segurança OK** - Ajustes permitidos")
        st.info(f"RPM: {safety.rpm} | Temp: {safety.temp}°C | Vel: {safety.speed} km/h")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Ajustes Manuais")
        
        # Ajuste de Mistura (Fuel Trim)
        fuel_trim = st.slider(
            "Ajuste de Mistura (Fuel Trim)",
            min_value=-25.0,
            max_value=25.0,
            value=0.0,
            step=0.5,
            format="%.1f %%",
            help="Ajuste fino da mistura ar/combustível"
        )
        
        if st.button("APLICAR AJUSTE DE MISTURA", key="apply_fuel"):
            with st.spinner("Enviando comando..."):
                resp = ecu_control.adjust_fuel_trim(fuel_trim)
                if resp.success:
                    st.success(f"✅ Ajuste aplicado! Resposta em {resp.response_time_ms:.1f}ms")
                else:
                    st.error(f"❌ Falha: {resp.message}")
        
        # Ajuste de Marcha Lenta
        idle_rpm = st.slider(
            "RPM de Marcha Lenta",
            min_value=600,
            max_value=1200,
            value=800,
            step=10,
            format="%d RPM",
            help="RPM alvo para marcha lenta"
        )
        
        if st.button("APLICAR RPM", key="apply_rpm"):
            with st.spinner("Enviando comando..."):
                resp = ecu_control.adjust_idle_speed(idle_rpm)
                if resp.success:
                    st.success(f"✅ RPM ajustado! Resposta em {resp.response_time_ms:.1f}ms")
                else:
                    st.error(f"❌ Falha: {resp.message}")
    
    with col2:
        st.markdown("### ⚙️ Ajustes Avançados")
        
        # Ajuste de Injeção
        inj_time = st.slider(
            "Tempo de Injeção",
            min_value=1.5,
            max_value=8.0,
            value=3.5,
            step=0.1,
            format="%.1f ms",
            help="Tempo de abertura dos injetores"
        )
        
        if st.button("APLICAR INJEÇÃO", key="apply_inj"):
            with st.spinner("Enviando comando..."):
                resp = ecu_control.adjust_injection_pulse(inj_time)
                if resp.success:
                    st.success(f"✅ Injeção ajustada! Resposta em {resp.response_time_ms:.1f}ms")
                else:
                    st.error(f"❌ Falha: {resp.message}")
        
        # Reset Flex Fuel
        st.markdown("---")
        if st.button("🔄 RESET FLEX FUEL", key="reset_flex"):
            with st.spinner("Resetando adaptações..."):
                resp = ecu_control.reset_flex_fuel()
                if resp.success:
                    st.success("✅ Parâmetros flex fuel resetados!")
                else:
                    st.error(f"❌ Falha: {resp.message}")
    
    # Otimização Automática
    st.markdown("---")
    st.markdown("### 🎯 OTIMIZAÇÃO AUTOMÁTICA")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lambda Atual", f"{ecu_control.live_data.get('lambda', 0):.3f}")
    with col2:
        st.metric("Sonda O2", f"{ecu_control.live_data.get('o2_voltage', 0):.3f}V")
    with col3:
        st.metric("STFT/LTFT", f"{ecu_control.live_data.get('stft', 0):.1f}/{ecu_control.live_data.get('ltft', 0):.1f}%")
    
    if st.button("🚀 OTIMIZAR FUNCIONAMENTO (Lambda 1.0)", use_container_width=True):
        with st.spinner("Otimizando parâmetros em tempo real..."):
            results = ecu_control.auto_tune_to_lambda1(max_attempts=10)
            
            if results['success']:
                st.success(f"✅ Otimização concluída em {results['attempts']} tentativas!")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Lambda Final", f"{results['lambda_final']:.3f}", 
                             delta=f"{results['lambda_final'] - results['lambda_inicial']:.3f}")
                with col2:
                    st.metric("Tempo Injeção Final", f"{results['injection_final']:.2f}ms")
            else:
                st.error(f"❌ Otimização falhou: {results.get('reason', 'Erro desconhecido')}")
    
    # Logs Técnicos
    with st.expander("📋 Logs Técnicos da ECU"):
        logs = ecu_control.get_logs(10)
        for log in logs:
            st.code(f"[{log['timestamp']}] {log['level']}: {log['message']}")

# =============================================
# EXEMPLO DE USO
# =============================================

if __name__ == "__main__":
    # Teste do módulo
    ecu = ECUControl(protocol=ProtocolType.CAN_11BIT, manufacturer="VOLKSWAGEN")
    
    print("=" * 60)
    print("TESTE DO MÓDULO DE CONTROLE ATIVO")
    print("=" * 60)
    
    # Teste de segurança
    print("\n1. Verificando condições de segurança:")
    safety = ecu.check_safety_conditions(rpm=850, temp=89, speed=0)
    print(f"   Seguro: {safety.safe}")
    if not safety.safe:
        print(f"   Motivo: {safety.reason}")
    
    # Teste de escrita
    print("\n2. Testando escrita de parâmetros:")
    
    # Ajuste Fuel Trim
    print("\n   a) Ajuste de Fuel Trim (+5%):")
    resp = ecu.adjust_fuel_trim(5.0, force=True)
    print(f"      Resposta: {resp.message}")
    
    # Ajuste RPM
    print("\n   b) Ajuste de Marcha Lenta (750 RPM):")
    resp = ecu.adjust_idle_speed(750, force=True)
    print(f"      Resposta: {resp.message}")
    
    # Ajuste Injeção
    print("\n   c) Ajuste de Injeção (3.8 ms):")
    resp = ecu.adjust_injection_pulse(3.8, force=True)
    print(f"      Resposta: {resp.message}")
    
    # Reset Flex
    print("\n   d) Reset Flex Fuel:")
    resp = ecu.reset_flex_fuel(force=True)
    print(f"      Resposta: {resp.message}")
    
    # Logs
    print("\n3. Últimos logs técnicos:")
    for log in ecu.get_logs(5):
        print(f"   [{log['timestamp']}] {log['level']}: {log['message']}")
