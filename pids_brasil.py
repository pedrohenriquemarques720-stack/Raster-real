# pids_brasil.py - PIDs específicos para veículos brasileiros

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PIDBrasil:
    """Estrutura para PIDs específicos do Brasil"""
    id: int
    nome: str
    fabricante: str
    motor: List[str]
    unidade: str
    min_val: float
    max_val: float
    descricao: str
    formato: str  # 'uint8', 'uint16', 'float'
    escala: float
    endereco_memoria: Optional[str] = None

class PIDsBrasil:
    """
    Banco de dados de PIDs específicos para veículos brasileiros
    VW, Fiat, GM - comandos exclusivos
    """
    
    def __init__(self):
        self.pids_vw = self._get_vw_pids()
        self.pids_fiat = self._get_fiat_pids()
        self.pids_gm = self._get_gm_pids()
        self.todos_pids = {**self.pids_vw, **self.pids_fiat, **self.pids_gm}
    
    def _get_vw_pids(self) -> Dict[int, PIDBrasil]:
        """PIDs específicos Volkswagen Brasil"""
        return {
            # Reset de Adaptação Flex (EA111/EA211)
            0xF101: PIDBrasil(
                id=0xF101,
                nome="Reset Flex Fuel",
                fabricante="VOLKSWAGEN",
                motor=["EA111", "EA211", "EA888"],
                unidade="",
                min_val=0,
                max_val=1,
                descricao="Reset da adaptação de combustível flex (etanol/gasolina)",
                formato="uint8",
                escala=1.0,
                endereco_memoria="0x7E0"
            ),
            
            # Aprendizado de Marcha Lenta
            0xF102: PIDBrasil(
                id=0xF102,
                nome="Idle Adaptation Reset",
                fabricante="VOLKSWAGEN",
                motor=["EA111", "EA211"],
                unidade="",
                min_val=0,
                max_val=1,
                descricao="Reset dos parâmetros de adaptação da marcha lenta",
                formato="uint8",
                escala=1.0,
                endereco_memoria="0x7E0"
            ),
            
            # Correção de Injeção por Cilindro (EA211)
            0xF103: PIDBrasil(
                id=0xF103,
                nome="Cylinder Injection Trim",
                fabricante="VOLKSWAGEN",
                motor=["EA211"],
                unidade="%",
                min_val=-15.0,
                max_val=15.0,
                descricao="Correção individual da injeção por cilindro (1-4)",
                formato="int8",
                escala=0.5,
                endereco_memoria="0x7E0"
            ),
            
            # Sensor de Detonação - Limiar
            0xF104: PIDBrasil(
                id=0xF104,
                nome="Knock Sensor Threshold",
                fabricante="VOLKSWAGEN",
                motor=["EA111", "EA211"],
                unidade="",
                min_val=0,
                max_val=255,
                descricao="Limiar de detonação adaptativo",
                formato="uint8",
                escala=1.0
            )
        }
    
    def _get_fiat_pids(self) -> Dict[int, PIDBrasil]:
        """PIDs específicos Fiat Brasil"""
        return {
            # Ajuste de Marcha Lenta (Fire/Firefly)
            0xF201: PIDBrasil(
                id=0xF201,
                nome="Idle Speed Adjustment",
                fabricante="FIAT",
                motor=["Fire", "Firefly", "E.torQ"],
                unidade="RPM",
                min_val=650,
                max_val=950,
                descricao="Ajuste fino da rotação de marcha lenta",
                formato="uint16",
                escala=1.0,
                endereco_memoria="0x7E0"
            ),
            
            # Aprendizado de Injeção (Firefly)
            0xF202: PIDBrasil(
                id=0xF202,
                nome="Injection Learning Reset",
                fabricante="FIAT",
                motor=["Firefly"],
                unidade="",
                min_val=0,
                max_val=1,
                descricao="Reset do aprendizado dos injetores",
                formato="uint8",
                escala=1.0
            ),
            
            # Adaptação Etanol (Flex)
            0xF203: PIDBrasil(
                id=0xF203,
                nome="Ethanol Adaptation",
                fabricante="FIAT",
                motor=["Fire", "Firefly"],
                unidade="%",
                min_val=0,
                max_val=100,
                descricao="Percentual de adaptação para etanol",
                formato="uint8",
                escala=1.0
            ),
            
            # Correção de Fase (VVT)
            0xF204: PIDBrasil(
                id=0xF204,
                nome="VVT Correction",
                fabricante="FIAT",
                motor=["Firefly"],
                unidade="°",
                min_val=-10,
                max_val=10,
                descricao="Correção manual do ângulo de fase",
                formato="int8",
                escala=0.5
            )
        }
    
    def _get_gm_pids(self) -> Dict[int, PIDBrasil]:
        """PIDs específicos GM Brasil"""
        return {
            # Aprendizado de Detonação (CSS Prime)
            0xF301: PIDBrasil(
                id=0xF301,
                nome="Knock Learn Reset",
                fabricante="CHEVROLET",
                motor=["CSS Prime", "Ecotec"],
                unidade="",
                min_val=0,
                max_val=1,
                descricao="Reset da tabela de aprendizado de detonação",
                formato="uint8",
                escala=1.0,
                endereco_memoria="0x7E0"
            ),
            
            # Ajuste de Mistura por Banco
            0xF302: PIDBrasil(
                id=0xF302,
                nome="Bank Fuel Trim",
                fabricante="CHEVROLET",
                motor=["CSS Prime"],
                unidade="%",
                min_val=-20,
                max_val=20,
                descricao="Correção individual da mistura por banco",
                formato="int8",
                escala=0.5
            ),
            
            # Adaptação de Etanol (FlexPower)
            0xF303: PIDBrasil(
                id=0xF303,
                nome="FlexPower Adaptation",
                fabricante="CHEVROLET",
                motor=["CSS Prime"],
                unidade="%",
                min_val=0,
                max_val=100,
                descricao="Fator de adaptação para etanol",
                formato="uint8",
                escala=1.0
            ),
            
            # Reset de Adaptações Longas
            0xF304: PIDBrasil(
                id=0xF304,
                nome="Long Term Reset",
                fabricante="CHEVROLET",
                motor=["Ecotec", "CSS Prime"],
                unidade="",
                min_val=0,
                max_val=1,
                descricao="Reset de todas as adaptações de longo prazo",
                formato="uint8",
                escala=1.0
            )
        }
    
    def get_pid(self, fabricante: str, nome: str) -> Optional[PIDBrasil]:
        """Busca PID por fabricante e nome"""
        for pid in self.todos_pids.values():
            if pid.fabricante == fabricante.upper() and pid.nome == nome:
                return pid
        return None
    
    def get_pids_by_engine(self, motor: str) -> List[PIDBrasil]:
        """Retorna todos PIDs para um motor específico"""
        return [pid for pid in self.todos_pids.values() if motor in pid.motor]
    
    def get_pids_by_manufacturer(self, fabricante: str) -> List[PIDBrasil]:
        """Retorna todos PIDs de um fabricante"""
        return [pid for pid in self.todos_pids.values() if pid.fabricante == fabricante.upper()]
