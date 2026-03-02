# vehicle_profiles.py - Banco de dados de veículos

class VehicleDatabase:
    """
    Banco de dados de perfis de veículos
    Similar ao Autel - reconhece automaticamente
    """
    
    def __init__(self):
        self.vehicles = self._build_database()
    
    def _build_database(self):
        """Constrói banco de dados de veículos"""
        return {
            # =========================================
            # VOLKSWAGEN
            # =========================================
            'VOLKSWAGEN': {
                'Gol': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.6', '1.0 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Polo': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI', '1.6', '200 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Virtus': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI', '1.6', '200 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'T-Cross': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI', '1.4 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Nivus': {
                    'years': [2021, 2022, 2023, 2024],
                    'engines': ['1.0 TSI'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                }
            },
            
            # =========================================
            # FIAT
            # =========================================
            'FIAT': {
                'Uno': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.3', '1.4'],
                    'protocol': 'KWP2000',
                    'ecu': 'Magneti Marelli IAW',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F]
                },
                'Mobi': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0'],
                    'protocol': 'KWP2000',
                    'ecu': 'Magneti Marelli IAW',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F]
                },
                'Argo': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.3', '1.8'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Cronos': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.3', '1.8'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Toro': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.3 Turbo', '1.8', '2.0 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch EDC17',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                }
            },
            
            # =========================================
            # CHEVROLET
            # =========================================
            'CHEVROLET': {
                'Onix': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 Turbo', '1.4'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Onix Plus': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 Turbo', '1.4'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Tracker': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0 Turbo', '1.2 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Cruze': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.4 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'S10': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.5', '2.8 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch EDC17',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                }
            },
            
            # =========================================
            # FORD
            # =========================================
            'FORD': {
                'Ka': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Fiesta': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.0', '1.5', '1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'EcoSport': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.5', '2.0'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch ME17.9.65',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Ranger': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.2 Diesel', '3.2 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch EDC17',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                }
            },
            
            # =========================================
            # TOYOTA
            # =========================================
            'TOYOTA': {
                'Corolla': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.0', '1.8 Hybrid'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Hilux': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.4 Diesel', '2.8 Diesel'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Yaris': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.3', '1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Denso',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                }
            },
            
            # =========================================
            # HONDA
            # =========================================
            'HONDA': {
                'Civic': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.0', '1.5 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'HR-V': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.5', '1.5 Turbo'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Fit': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.5'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                }
            },
            
            # =========================================
            # NISSAN
            # =========================================
            'NISSAN': {
                'Kicks': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Hitachi',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Versa': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['1.6'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Hitachi',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                },
                'Frontier': {
                    'years': [2020, 2021, 2022, 2023, 2024],
                    'engines': ['2.3 Diesel', '2.5', '4.0'],
                    'protocol': 'CAN 500kbps',
                    'ecu': 'Bosch EDC17',
                    'pids_supported': [0x0C, 0x0D, 0x05, 0x0F, 0x10, 0x11]
                }
            }
        }
    
    def identify_vehicle(self, vin):
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
            '9BM': 'MERCEDES-BENZ',
            '9BS': 'SCANIA',
            '93R': 'RENAULT',
            '9GK': 'KIA',
            '9HB': 'HONDA',
            '9FB': 'RENAULT',
            '9GA': 'PEUGEOT',
            '9GD': 'TOYOTA',
            '9GN': 'NISSAN'
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
    
    def get_profile(self, manufacturer, model):
        """Retorna perfil completo do veículo"""
        if manufacturer in self.vehicles:
            if model in self.vehicles[manufacturer]:
                return self.vehicles[manufacturer][model]
        return None
