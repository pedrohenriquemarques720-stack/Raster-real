# hardware/obd_interface.py
import obd
import threading
import time
from typing import Dict, Optional

class OBDInterface:
    """Interface OBD-II para conexão com o veículo"""
    
    def __init__(self):
        self.connection = None
        self.connected = False
        self.live_data = {}
        self._running = False
        
    def connect_usb(self, port='/dev/ttyUSB0', baudrate=38400) -> bool:
        """Conecta via USB"""
        try:
            self.connection = obd.OBD(port, baudrate=baudrate)
            if self.connection.is_connected():
                self.connected = True
                self._start_stream()
                return True
        except Exception as e:
            print(f"Erro USB: {e}")
        return False
    
    def connect_bluetooth(self, port='/dev/rfcomm0') -> bool:
        """Conecta via Bluetooth"""
        try:
            self.connection = obd.OBD(port)
            if self.connection.is_connected():
                self.connected = True
                self._start_stream()
                return True
        except Exception as e:
            print(f"Erro Bluetooth: {e}")
        return False
    
    def _start_stream(self):
        """Inicia streaming de dados"""
        self._running = True
        thread = threading.Thread(target=self._update_loop)
        thread.daemon = True
        thread.start()
    
    def _update_loop(self):
        """Loop de atualização de dados"""
        while self._running and self.connected:
            try:
                # RPM
                rpm = self.connection.query(obd.commands.RPM)
                if rpm.value:
                    self.live_data['rpm'] = int(rpm.value.magnitude)
                
                # Velocidade
                speed = self.connection.query(obd.commands.SPEED)
                if speed.value:
                    self.live_data['speed'] = int(speed.value.magnitude)
                
                # Temperatura
                temp = self.connection.query(obd.commands.COOLANT_TEMP)
                if temp.value:
                    self.live_data['temp'] = int(temp.value.magnitude)
                
                # Fuel Trim
                stft = self.connection.query(obd.commands.SHORT_FUEL_TRIM_1)
                if stft.value:
                    self.live_data['stft'] = stft.value.magnitude
                
                ltft = self.connection.query(obd.commands.LONG_FUEL_TRIM_1)
                if ltft.value:
                    self.live_data['ltft'] = ltft.value.magnitude
                
                # MAF
                maf = self.connection.query(obd.commands.MAF)
                if maf.value:
                    self.live_data['maf'] = maf.value.magnitude
                
            except Exception as e:
                print(f"Erro na leitura: {e}")
            
            time.sleep(0.1)
    
    def get_live_data(self) -> Dict:
        """Retorna últimos dados lidos"""
        return self.live_data.copy()
    
    def read_dtc(self) -> list:
        """Lê códigos de falha"""
        if not self.connected:
            return []
        
        response = self.connection.query(obd.commands.GET_DTC)
        if response.value:
            return [{'code': str(code)} for code in response.value]
        return []
    
    def clear_dtc(self) -> bool:
        """Limpa códigos de falha"""
        if not self.connected:
            return False
        self.connection.query(obd.commands.CLEAR_DTC)
        return True
    
    def disconnect(self):
        """Desconecta"""
        self._running = False
        if self.connection:
            self.connection.close()
        self.connected = False
