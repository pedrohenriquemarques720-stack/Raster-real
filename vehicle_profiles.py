# vehicle_profiles.py - Perfis de veículos
from typing import Dict, List, Optional, Tuple

class VehicleDatabase:
    """
    Banco de dados de perfis de veículos
    """
    
    def __init__(self):
        self.vehicles = self._build_database()
    
    def _build_database(self) -> Dict:
        """Constrói banco de dados de veículos"""
        return {
            'VOLKSWAGEN': {
                'Gol': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.6', '1.0 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Polo': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI', '1.6', '200 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Virtus': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI', '1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'T-Cross': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI', '1.4 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Nivus': {
                    'years': [2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Taos': {
                    'years': [2022, 2023, 2024],
                    'engines': ['1.4 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                }
            },
            'FIAT': {
                'Uno': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.3'],
                    'protocol': 'KWP2000',
                    'ecu': 'Magneti Marelli'
                },
                'Mobi': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0'],
                    'protocol': 'KWP2000',
                    'ecu': 'Magneti Marelli'
                },
                'Argo': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.3', '1.8'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'Cronos': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.3', '1.8'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'Toro': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.3 Turbo', '1.8', '2.0 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'Pulse': {
                    'years': [2022, 2023, 2024],
                    'engines': ['1.0', '1.3 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                }
            },
            'CHEVROLET': {
                'Onix': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 Turbo', '1.4'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Onix Plus': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 Turbo', '1.4'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Tracker': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 Turbo', '1.2 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Cruze': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.4 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'S10': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.5', '2.8 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch EDC17'
                }
            },
            'FORD': {
                'Ka': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Fiesta': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.5', '1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'EcoSport': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.5', '2.0'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65'
                },
                'Ranger': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.2 Diesel', '3.2 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch EDC17'
                },
                'Territory': {
                    'years': [2021, 2022, 2023, 2024],
                    'engines': ['1.5 EcoBoost'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                }
            },
            'TOYOTA': {
                'Corolla': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.0', '1.8 Hybrid'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso'
                },
                'Hilux': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.4 Diesel', '2.8 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso'
                },
                'Yaris': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.3', '1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso'
                },
                'Etios': {
                    'years': [2020, 2021, 2022, 2023],
                    'engines': ['1.3', '1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso'
                },
                'SW4': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.8 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso'
                }
            },
            'HONDA': {
                'Civic': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.0', '1.5 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'HR-V': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.5', '1.5 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'Fit': {
                    'years': [2020, 2021, 2022, 2023],
                    'engines': ['1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'City': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'CR-V': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.5 Turbo', '2.0 Hybrid'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                }
            },
            'NISSAN': {
                'Kicks': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Hitachi'
                },
                'Versa': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Hitachi'
                },
                'Frontier': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.3 Diesel', '2.5', '4.0'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch EDC17'
                },
                'Sentra': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.0'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Hitachi'
                }
            },
            'RENAULT': {
                'Kwid': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'Sandero': {
                    'years': [2020, 2021, 2022, 2023],
                    'engines': ['1.0', '1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'Duster': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.6', '2.0'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                },
                'Oroch': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch'
                }
            }
        }
    
    def identify_vehicle(self, vin: str) -> Optional[Dict]:
        """Identifica veículo pelo VIN"""
        if not vin or vin == '---':
            return None
        
        # WMI (primeiros 3 caracteres)
        wmi = vin[:3]
        
        # Mapeamento WMI para fabricante
        wmi_map = {
            '9BW': 'VOLKSWAGEN',
            '9BG': 'CHEVROLET',
            '9BF': 'FORD',
            '935': 'FIAT',
            '9BD': 'FIAT',
            '93R': 'RENAULT',
            '9GD': 'TOYOTA',
            '9HB': 'HONDA',
            '9GN': 'NISSAN',
            '9GK': 'KIA',
            '9GA': 'PEUGEOT',
            '9GB': 'CITROEN',
            '9GT': 'MITSUBISHI',
            '9BM': 'MERCEDES',
            '9BS': 'SCANIA'
        }
        
        manufacturer = wmi_map.get(wmi, 'DESCONHECIDO')
        
        # Ano (posição 10 do VIN)
        year = 'DESCONHECIDO'
        if len(vin) >= 10:
            year_code = vin[9]
            year_map = {
                'M': 2021, 'N': 2022, 'P': 2023,
                'R': 2024, 'S': 2025, 'T': 2026
            }
            year = year_map.get(year_code, 'DESCONHECIDO')
        
        return {
            'manufacturer': manufacturer,
            'year': year
        }
    
    def get_profile(self, manufacturer: str, model: str) -> Optional[Dict]:
        """Retorna perfil do veículo"""
        if manufacturer in self.vehicles:
            if model in self.vehicles[manufacturer]:
                return self.vehicles[manufacturer][model]
        return None
