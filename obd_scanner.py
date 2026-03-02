# obd_scanner.py - Detecção automática de veículos

import serial
import time
import threading
from datetime import datetime

class OBDScanner:
    def __init__(self):
        self.connection = None
        self.vehicle_info = {}
        self.supported_protocols = [
            'CAN 11bit 500k',
            'CAN 29bit 500k',
            'KWP2000 fast',
            'KWP2000 slow',
            'ISO9141-2',
            'J1850 PWM',
            'J1850 VPW'
        ]
        
    def scan_ports(self):
        """Escaneia portas seriais disponíveis"""
        ports = []
        for i in range(0, 10):
            try:
                port = f'COM{i}'
                s = serial.Serial(port)
                ports.append(port)
                s.close()
            except:
                pass
        
        # Linux ports
        for i in range(0, 4):
            try:
                port = f'/dev/ttyUSB{i}'
                s = serial.Serial(port)
                ports.append(port)
                s.close()
            except:
                pass
        
        return ports
    
    def auto_detect_protocol(self, port):
        """Detecta automaticamente o protocolo OBD2"""
        try:
            ser = serial.Serial(port, baudrate=38400, timeout=2)
            
            # Tenta cada protocolo
            for protocol in self.supported_protocols:
                ser.write(b'ATSP0\r')  # Auto protocol
                time.sleep(0.1)
                response = ser.read(100)
                
                if b'OK' in response:
                    ser.write(b'0100\r')  # PIDs suportados
                    time.sleep(0.2)
                    data = ser.read(100)
                    
                    if len(data) > 6:
                        return protocol
            
            ser.close()
        except:
            pass
        
        return None
    
    def get_vin(self, port, protocol):
        """Obtém o número VIN do veículo"""
        try:
            ser = serial.Serial(port, baudrate=38400, timeout=2)
            
            # Comando para ler VIN (modo 9, PID 02)
            ser.write(b'0902\r')
            time.sleep(0.5)
            data = ser.read(200)
            
            # Processa resposta
            if data and len(data) > 10:
                vin = data[10:27].decode('ascii', errors='ignore')
                return vin.strip()
            
            ser.close()
        except:
            pass
        
        return None
    
    def get_ecu_info(self, port, protocol):
        """Obtém informações da ECU"""
        try:
            ser = serial.Serial(port, baudrate=38400, timeout=2)
            
            # Comando para obter identificação da ECU
            ser.write(b'090A\r')
            time.sleep(0.5)
            data = ser.read(200)
            
            if data:
                return {
                    'ecu_id': data[10:20].decode('ascii', errors='ignore'),
                    'software_version': data[20:30].decode('ascii', errors='ignore'),
                    'hardware_version': data[30:40].decode('ascii', errors='ignore')
                }
            
            ser.close()
        except:
            pass
        
        return {}
    
    def scan_vehicle(self):
        """Escaneia o veículo completo"""
        result = {
            'status': 'scanning',
            'ports_found': [],
            'protocol': None,
            'vin': None,
            'manufacturer': None,
            'model': None,
            'year': None,
            'engine': None,
            'ecu_info': {}
        }
        
        # 1. Escaneia portas
        result['ports_found'] = self.scan_ports()
        
        if not result['ports_found']:
            result['status'] = 'no_device'
            return result
        
        # 2. Tenta cada porta
        for port in result['ports_found']:
            # Detecta protocolo
            protocol = self.auto_detect_protocol(port)
            if protocol:
                result['protocol'] = protocol
                result['port'] = port
                
                # Obtém VIN
                vin = self.get_vin(port, protocol)
                if vin:
                    result['vin'] = vin
                    # Decodifica VIN para obter informações
                    vehicle_info = self.decode_vin(vin)
                    result.update(vehicle_info)
                
                # Obtém info da ECU
                result['ecu_info'] = self.get_ecu_info(port, protocol)
                
                result['status'] = 'success'
                break
        
        if not result['protocol']:
            result['status'] = 'no_protocol'
        
        return result
    
    def decode_vin(self, vin):
        """Decodifica VIN para obter informações do veículo"""
        # Base de dados simplificada
        vin_database = {
            '9BW': {'manufacturer': 'Volkswagen', 'country': 'Brasil'},
            '935': {'manufacturer': 'Fiat', 'country': 'Brasil'},
            '9BG': {'manufacturer': 'Chevrolet', 'country': 'Brasil'},
            '9BF': {'manufacturer': 'Ford', 'country': 'Brasil'}
        }
        
        result = {
            'manufacturer': 'Desconhecido',
            'model': 'Não identificado',
            'year': None,
            'engine': None
        }
        
        if vin and len(vin) >= 3:
            prefix = vin[:3]
            if prefix in vin_database:
                result['manufacturer'] = vin_database[prefix]['manufacturer']
            
            # Ano (posição 10 do VIN)
            if len(vin) >= 10:
                year_code = vin[9]
                year_map = {
                    'M': 2021, 'N': 2022, 'P': 2023, 
                    'R': 2024, 'S': 2025, 'T': 2026
                }
                result['year'] = year_map.get(year_code, 'Desconhecido')
        
        return result

# Singleton
scanner = OBDScanner()

def scan_vehicle():
    return scanner.scan_vehicle()

def connect(device):
    # Implementar conexão real
    return True

def read_dtc():
    # Implementar leitura de DTCs
    return [
        {'code': 'P0301', 'description': 'Falha de ignição no cilindro 1', 
         'system': 'Motor', 'severity': 'Alta'},
        {'code': 'P0420', 'description': 'Eficiência do catalisador abaixo do limite', 
         'system': 'Emissões', 'severity': 'Média'}
    ]

def clear_dtc():
    # Implementar limpeza de DTCs
    return True