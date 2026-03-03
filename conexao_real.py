# conexao_real.py - Integração com carro real via OBD-II

import time
import threading
from typing import Dict, Optional
from enum import Enum
import logging

# Tentativa de importar obd com tratamento de erro
try:
    import obd
    OBD_AVAILABLE = True
except ImportError:
    OBD_AVAILABLE = False
    print("⚠️ Biblioteca 'obd' não encontrada. Instale com: pip install obd")

# Tentativa de importar serial
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("⚠️ Biblioteca 'pyserial' não encontrada. Instale com: pip install pyserial")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionType(Enum):
    USB = "USB"
    BLUETOOTH = "Bluetooth"
    WIFI = "WiFi"
    SIMULATOR = "Simulador"

class OBDRealConnection:
    """
    Classe para conexão real com veículo via OBD-II
    Suporta ELM327, STN2120, J2534
    Versão com tratamento de erro para quando as bibliotecas não estão disponíveis
    """
    
    def __init__(self):
        self.connection = None
        self.connected = False
        self.connection_type = ConnectionType.SIMULATOR
        self.supported_commands = {}
        self.live_data = {}
        self.vin = None
        self._stop_thread = False
        self._data_thread = None
        self.serial_ports = []
        
    def scan_ports(self) -> Dict[str, list]:
        """
        Escaneia portas disponíveis para conexão
        """
        ports = {
            'usb': [],
            'bluetooth': [],
            'wifi': []
        }
        
        if not SERIAL_AVAILABLE:
            logger.warning("Biblioteca pyserial não disponível. Use modo simulação.")
            return ports
        
        try:
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
        except Exception as e:
            logger.error(f"Erro ao escanear portas: {e}")
                
        return ports
    
    def connect(self, port: str = None, baudrate: int = 38400, 
                connection_type: ConnectionType = ConnectionType.USB) -> bool:
        """
        Conecta ao veículo via porta serial
        """
        if not OBD_AVAILABLE:
            logger.error("Biblioteca OBD não disponível. Use modo simulação.")
            self.connected = False
            return False
            
        try:
            logger.info(f"Conectando em {port or 'auto'} a {baudrate} baud...")
            
            # Tenta conectar com ELM327
            if port:
                self.connection = obd.OBD(port, baudrate=baudrate)
            else:
                # Auto-detect
                self.connection = obd.OBD()
            
            if self.connection and self.connection.is_connected():
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
        if not self.connection or not OBD_AVAILABLE:
            return
            
        try:
            # Tenta ler VIN
            vin_cmd = obd.commands.VIN
            if self.connection.supports(vin_cmd):
                response = self.connection.query(vin_cmd)
                if response and response.value:
                    self.vin = str(response.value)
                    logger.info(f"VIN: {self.vin}")
        except:
            pass
    
    def _start_data_stream(self):
        """Inicia thread de leitura contínua"""
        if not OBD_AVAILABLE:
            return
            
        self._stop_thread = False
        self._data_thread = threading.Thread(target=self._data_loop)
        self._data_thread.daemon = True
        self._data_thread.start()
    
    def _data_loop(self):
        """Loop de leitura de dados em tempo real"""
        while not self._stop_thread and self.connected and OBD_AVAILABLE:
            try:
                # RPM
                if hasattr(obd.commands, 'RPM') and self.connection.supports(obd.commands.RPM):
                    rpm = self.connection.query(obd.commands.RPM)
                    if rpm and rpm.value:
                        self.live_data['rpm'] = int(rpm.value.magnitude)
                
                # Velocidade
                if hasattr(obd.commands, 'SPEED') and self.connection.supports(obd.commands.SPEED):
                    speed = self.connection.query(obd.commands.SPEED)
                    if speed and speed.value:
                        self.live_data['speed'] = int(speed.value.magnitude)
                
                # Temperatura do motor
                if hasattr(obd.commands, 'COOLANT_TEMP') and self.connection.supports(obd.commands.COOLANT_TEMP):
                    temp = self.connection.query(obd.commands.COOLANT_TEMP)
                    if temp and temp.value:
                        self.live_data['coolant_temp'] = int(temp.value.magnitude)
                
                # Short Term Fuel Trim
                if hasattr(obd.commands, 'SHORT_FUEL_TRIM_1') and self.connection.supports(obd.commands.SHORT_FUEL_TRIM_1):
                    stft = self.connection.query(obd.commands.SHORT_FUEL_TRIM_1)
                    if stft and stft.value:
                        self.live_data['stft'] = stft.value.magnitude
                
                # Long Term Fuel Trim
                if hasattr(obd.commands, 'LONG_FUEL_TRIM_1') and self.connection.supports(obd.commands.LONG_FUEL_TRIM_1):
                    ltft = self.connection.query(obd.commands.LONG_FUEL_TRIM_1)
                    if ltft and ltft.value:
                        self.live_data['ltft'] = ltft.value.magnitude
                
                # Tensão da bateria
                if hasattr(obd.commands, 'ELM_VOLTAGE') and self.connection.supports(obd.commands.ELM_VOLTAGE):
                    volt = self.connection.query(obd.commands.ELM_VOLTAGE)
                    if volt and volt.value:
                        self.live_data['battery'] = float(volt.value.magnitude)
                
                # MAF
                if hasattr(obd.commands, 'MAF') and self.connection.supports(obd.commands.MAF):
                    maf = self.connection.query(obd.commands.MAF)
                    if maf and maf.value:
                        self.live_data['maf'] = float(maf.value.magnitude)
                
                time.sleep(0.1)  # 10 Hz
                
            except Exception as e:
                logger.error(f"Erro na leitura: {e}")
                time.sleep(1)
    
    def read_dtc(self) -> list:
        """Lê códigos de falha"""
        if not self.connected or not OBD_AVAILABLE or not self.connection:
            return []
        
        try:
            dtc_response = self.connection.query(obd.commands.GET_DTC)
            if dtc_response and dtc_response.value:
                return [{'code': str(code)} for code in dtc_response.value]
        except:
            pass
        return []
    
    def clear_dtc(self) -> bool:
        """Limpa códigos de falha"""
        if not self.connected or not OBD_AVAILABLE or not self.connection:
            return False
        
        try:
            self.connection.query(obd.commands.CLEAR_DTC)
            return True
        except:
            return False
    
    def get_live_data(self) -> Dict:
        """Retorna dados ao vivo mais recentes"""
        return self.live_data.copy()
    
    def disconnect(self):
        """Desconecta do veículo"""
        self._stop_thread = True
        if self._data_thread:
            self._data_thread.join(timeout=2)
        if self.connection and OBD_AVAILABLE:
            try:
                self.connection.close()
            except:
                pass
        self.connected = False
        logger.info("Desconectado")

# Função auxiliar para encontrar porta ELM327
def find_elm327_port() -> Optional[str]:
    """Procura automaticamente por dispositivo ELM327"""
    if not SERIAL_AVAILABLE:
        return None
        
    try:
        for port in serial.tools.list_ports.comports():
            if 'USB' in port.description.upper() or 'ELM' in port.description.upper():
                return port.device
    except:
        pass
    return None
