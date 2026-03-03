# hardware/can_interface.py
import can
import threading
import time
from typing import Dict, Optional

class CANInterface:
    """Interface CAN real para Raspberry Pi"""
    
    def __init__(self, channel='can0', bitrate=500000):
        self.channel = channel
        self.bitrate = bitrate
        self.bus = None
        self.connected = False
        self.callbacks = []
        
    def connect(self) -> bool:
        """Conecta ao barramento CAN"""
        try:
            # Configurar interface CAN
            import os
            os.system(f'sudo ip link set {self.channel} type can bitrate {self.bitrate}')
            os.system(f'sudo ifconfig {self.channel} up')
            
            # Conectar
            self.bus = can.interface.Bus(channel=self.channel, bustype='socketcan')
            self.connected = True
            return True
        except Exception as e:
            print(f"Erro CAN: {e}")
            return False
    
    def send_message(self, arbitration_id: int, data: bytes) -> bool:
        """Envia mensagem CAN"""
        if not self.connected or not self.bus:
            return False
        
        try:
            msg = can.Message(
                arbitration_id=arbitration_id,
                data=data,
                is_extended_id=False
            )
            self.bus.send(msg)
            return True
        except Exception as e:
            print(f"Erro ao enviar: {e}")
            return False
    
    def read_messages(self, timeout=1.0) -> Optional[can.Message]:
        """Lê mensagens CAN"""
        if not self.connected or not self.bus:
            return None
        
        return self.bus.recv(timeout)
    
    def start_listener(self):
        """Inicia listener em thread separada"""
        def listener():
            while self.connected:
                msg = self.read_messages()
                if msg:
                    for callback in self.callbacks:
                        callback(msg)
                time.sleep(0.01)
        
        thread = threading.Thread(target=listener)
        thread.daemon = True
        thread.start()
    
    def add_callback(self, callback):
        """Adiciona callback para mensagens recebidas"""
        self.callbacks.append(callback)
    
    def disconnect(self):
        """Desconecta do barramento CAN"""
        self.connected = False
        if self.bus:
            self.bus.shutdown()
        os.system(f'sudo ifconfig {self.channel} down')
