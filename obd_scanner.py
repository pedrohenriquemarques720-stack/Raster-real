# obd_scanner.py - Versão sem dependência de serial
import time
import random
from datetime import datetime

class OBDScannerPro:
    """
    Scanner automotivo - Versão simplificada sem dependências externas
    """
    
    def __init__(self):
        self.vehicle_info = {
            'manufacturer': '---',
            'model': '---',
            'year': '---',
            'engine': '---',
            'transmission': '---',
            'vin': '---',
            'ecu': '---',
            'version': '---',
            'protocol': '---',
            'km': '---'
        }
        self.stats = {
            'uptime': '00:00:00',
            'max_rpm': 0,
            'max_temp': 0,
            'start_time': time.time()
        }
        self.is_real = False
        self.running = False
        
    def scan_ports(self):
        """Modo simulação - sempre retorna False para usar simulação"""
        return False
    
    def _identify_vehicle(self):
        """Identifica veículo simulado"""
        self.vehicle_info = {
            'manufacturer': 'Volkswagen',
            'model': 'Gol 1.6 MSI',
            'year': '2024',
            'engine': 'EA211 (16V)',
            'transmission': 'MQ200 (MANUAL)',
            'vin': '9BWZZZ377VT004251',
            'ecu': 'BOSCH ME17.9.65',
            'version': '03H906023AB 3456',
            'protocol': 'CAN-BUS 500K',
            'km': '15.234 km'
        }
        return self.vehicle_info
    
    def get_live_data(self):
        """Retorna dados simulados"""
        # Atualiza estatísticas
        uptime_seconds = int(time.time() - self.stats['start_time'])
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        self.stats['uptime'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Gera dados simulados realistas
        rpm = random.randint(750, 3500)
        if rpm > self.stats['max_rpm']:
            self.stats['max_rpm'] = rpm
            
        temp = random.randint(82, 98)
        if temp > self.stats['max_temp']:
            self.stats['max_temp'] = temp
        
        return {
            'rpm': rpm,
            'speed': random.randint(0, 120),
            'temp': temp,
            'oil_pressure': round(3.5 + random.random() * 1.5, 1),
            'battery': round(12 + random.random() * 2, 1),
            'engine_load': random.randint(15, 55),
            'o2': round(0.7 + random.random() * 0.2, 2),
            'timing': random.randint(8, 22)
        }
    
    def read_dtc(self):
        """Retorna códigos de falha simulados"""
        return [
            {'code': 'P0301', 'description': 'Falha de ignição no cilindro 1', 'system': 'Motor'},
            {'code': 'P0420', 'description': 'Eficiência do catalisador abaixo do limite', 'system': 'Emissões'},
            {'code': 'P0171', 'description': 'Mistura pobre (banco 1)', 'system': 'Combustível'}
        ]
    
    def clear_dtc(self):
        """Limpa códigos de falha"""
        return True
    
    def disconnect(self):
        """Desconecta"""
        self.running = False
        return True
    
    def start_simulation(self):
        """Inicia modo simulação"""
        self.is_real = False
        self._identify_vehicle()
        self.running = True
        return True
