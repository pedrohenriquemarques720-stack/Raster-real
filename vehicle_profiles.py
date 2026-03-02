# vehicle_profiles.py - Versão simplificada

from typing import Dict, Optional

class VehicleDatabase:
    """
    Banco de dados de perfis de veículos
    """
    
    def __init__(self):
        self.vehicles = self._build_database()
    
    def _build_database(self) -> Dict:
        return {
            'VOLKSWAGEN': {
                'Gol': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0','1.6','1.0 TSI']},
                'Polo': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0 TSI','1.6','200 TSI']},
                'Virtus': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0 TSI','1.6']}
            },
            'FIAT': {
                'Uno': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0','1.3']},
                'Mobi': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0']},
                'Argo': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0','1.3','1.8']}
            },
            'CHEVROLET': {
                'Onix': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0 Turbo','1.4']},
                'Tracker': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0 Turbo','1.2 Turbo']}
            },
            'FORD': {
                'Ka': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.0','1.5']},
                'EcoSport': {'years': [2020,2021,2022,2023,2024], 'engines': ['1.5','2.0']}
            }
        }
    
    def identify_vehicle(self, vin: str) -> Optional[Dict]:
        if not vin or len(vin) < 3:
            return None
        
        wmi = vin[:3]
        wmi_map = {
            '9BW': 'VOLKSWAGEN', '9BG': 'CHEVROLET', '9BF': 'FORD',
            '935': 'FIAT', '9BD': 'FIAT', '93R': 'RENAULT',
            '9GD': 'TOYOTA', '9HB': 'HONDA', '9GN': 'NISSAN'
        }
        
        manufacturer = wmi_map.get(wmi, 'DESCONHECIDO')
        
        if len(vin) >= 10:
            year_code = vin[9]
            year_map = {'M':2021,'N':2022,'P':2023,'R':2024,'S':2025,'T':2026}
            year = year_map.get(year_code, 'DESCONHECIDO')
        else:
            year = 'DESCONHECIDO'
        
        return {'manufacturer': manufacturer, 'year': year}
    
    def get_profile(self, manufacturer: str, model: str) -> Optional[Dict]:
        if manufacturer in self.vehicles and model in self.vehicles[manufacturer]:
            return self.vehicles[manufacturer][model]
        return None
