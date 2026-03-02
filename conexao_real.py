# conexao_real.py - Integração com carro real via OBD-II

import obd
import serial
import serial.tools.list_ports
import time
import threading
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionType(Enum):
    USB = "USB"
    BLUETOOTH = "Bluetooth"
    WIFI = "WiFi"
    SIMULATOR = "Simulador"

@dataclass
class VehicleConnection:
    type: ConnectionType
    port: str
    baudrate: int
    protocol: str
    connected: bool = False
    vin: Optional[str] = None

class OBDRealConnection:
    """
    Classe para conexão real com veículo via OBD-II
    Suporta ELM327, STN2120, J2534
    """
    
    def __init__(self):
        self.connection = None
        self.connected = False
        self.connection_type = ConnectionType.SIMULATOR
        self.supported_commands = {}
        self.live_data = {}
        self._stop_thread = False
        self._data_thread = None
        
    def scan_ports(self) -> Dict[str, list]:
        """
        Escaneia portas disponíveis para conexão
        """
        ports = {
            'usb': [],
            'bluetooth': [],
            'wifi': []
        }
        
        # Lista todas as portas seriais
        for port in serial.tools.list_ports.comports():
            if 'USB' in port.description.upper():
                ports['usb'].append({
                    'port': port.device,
                    'description': port.description,
                    'hwid': port.hwid
                })
            elif 'BLUETOOTH' in port.description.upper():
                ports['bluetooth'].append({
                    'port': port.device,
                    'description': port.description
                })
                
        return ports
    
    def connect(self, port: str, baudrate: int = 38400, 
                connection_type: ConnectionType = ConnectionType.USB) -> bool:
        """
        Conecta ao veículo via porta serial
        """
        try:
            logger.info(f"Conectando em {port} a {baudrate} baud...")
            
            # Tenta conectar com ELM327
            self.connection = obd.OBD(port, baudrate=baudrate)
            
            if self.connection.is_connected():
                self.connected = True
                self.connection_type = connection_type
                
                # Obtém informações do veículo
                self._get_vehicle_info()
                
                # Inicia thread de leitura contínua
                self._start_data_stream()
                
                logger.info(f"✅ Conectado! Protocolo: {self.connection.protocol_name()}")
                return True
            else:
                logger.error("❌ Falha na conexão")
                return False
                
        except Exception as e:
            logger.error(f"Erro na conexão: {e}")
            return False
    
    def _get_vehicle_info(self):
        """Obtém informações do veículo"""
        # Tenta ler VIN
        vin_cmd = obd.commands.VIN
        if self.connection.supports(vin_cmd):
            response = self.connection.query(vin_cmd)
            if response.value:
                self.vin = str(response.value)
                logger.info(f"VIN: {self.vin}")
        
        # Verifica comandos suportados
        for cmd in obd.commands.base_commands:
            if self.connection.supports(cmd):
                self.supported_commands[cmd.name] = cmd
        
        logger.info(f"Comandos suportados: {len(self.supported_commands)}")
    
    def _start_data_stream(self):
        """Inicia thread de leitura contínua"""
        self._stop_thread = False
        self._data_thread = threading.Thread(target=self._data_loop)
        self._data_thread.daemon = True
        self._data_thread.start()
    
    def _data_loop(self):
        """Loop de leitura de dados em tempo real"""
        while not self._stop_thread and self.connected:
            try:
                # RPM
                if self.connection.supports(obd.commands.RPM):
                    rpm = self.connection.query(obd.commands.RPM)
                    if rpm.value:
                        self.live_data['rpm'] = int(rpm.value.magnitude)
                
                # Velocidade
                if self.connection.supports(obd.commands.SPEED):
                    speed = self.connection.query(obd.commands.SPEED)
                    if speed.value:
                        self.live_data['speed'] = int(speed.value.magnitude)
                
                # Temperatura do motor
                if self.connection.supports(obd.commands.COOLANT_TEMP):
                    temp = self.connection.query(obd.commands.COOLANT_TEMP)
                    if temp.value:
                        self.live_data['coolant_temp'] = int(temp.value.magnitude)
                
                # Short Term Fuel Trim
                if self.connection.supports(obd.commands.SHORT_FUEL_TRIM_1):
                    stft = self.connection.query(obd.commands.SHORT_FUEL_TRIM_1)
                    if stft.value:
                        self.live_data['stft'] = stft.value.magnitude
                
                # Long Term Fuel Trim
                if self.connection.supports(obd.commands.LONG_FUEL_TRIM_1):
                    ltft = self.connection.query(obd.commands.LONG_FUEL_TRIM_1)
                    if ltft.value:
                        self.live_data['ltft'] = ltft.value.magnitude
                
                # Tensão da bateria
                if self.connection.supports(obd.commands.ELM_VOLTAGE):
                    volt = self.connection.query(obd.commands.ELM_VOLTAGE)
                    if volt.value:
                        self.live_data['battery'] = float(volt.value.magnitude)
                
                # MAF
                if self.connection.supports(obd.commands.MAF):
                    maf = self.connection.query(obd.commands.MAF)
                    if maf.value:
                        self.live_data['maf'] = float(maf.value.magnitude)
                
                time.sleep(0.1)  # 10 Hz
                
            except Exception as e:
                logger.error(f"Erro na leitura: {e}")
                time.sleep(1)
    
    def read_dtc(self) -> list:
        """Lê códigos de falha"""
        if not self.connected:
            return []
        
        dtc_response = self.connection.query(obd.commands.GET_DTC)
        if dtc_response.value:
            return [{'code': str(code)} for code in dtc_response.value]
        return []
    
    def clear_dtc(self) -> bool:
        """Limpa códigos de falha"""
        if not self.connected:
            return False
        
        self.connection.query(obd.commands.CLEAR_DTC)
        return True
    
    def get_live_data(self) -> Dict:
        """Retorna dados ao vivo mais recentes"""
        return self.live_data.copy()
    
    def disconnect(self):
        """Desconecta do veículo"""
        self._stop_thread = True
        if self._data_thread:
            self._data_thread.join(timeout=2)
        if self.connection:
            self.connection.close()
        self.connected = False
        logger.info("Desconectado")

# Função auxiliar para encontrar porta ELM327
def find_elm327_port() -> Optional[str]:
    """Procura automaticamente por dispositivo ELM327"""
    for port in serial.tools.list_ports.comports():
        if 'USB' in port.description.upper() or 'ELM' in port.description.upper():
            return port.device
    return None
