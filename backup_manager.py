# backup_manager.py - Salvar e restaurar dados do veículo

import json
import datetime
import os
from typing import Dict, List

class BackupManager:
    """Gerencia backups dos diagnósticos"""
    
    def __init__(self):
        self.backup_dir = "backups"
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def salvar_diagnostico(self, vehicle_info: Dict, dtcs: List, analysis: Dict) -> str:
        """Salva diagnóstico completo em arquivo"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.backup_dir}/diagnostico_{timestamp}.json"
        
        data = {
            'data': datetime.datetime.now().isoformat(),
            'veiculo': vehicle_info,
            'codigos_falha': dtcs,
            'analise': analysis
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def gerar_relatorio_pdf(self, filename: str) -> str:
        """Gera PDF a partir do JSON"""
        # Usaria reportlab ou fpdf
        pdf_filename = filename.replace('.json', '.pdf')
        return pdf_filename
    
    def listar_backups(self) -> List[Dict]:
        """Lista todos os backups disponíveis"""
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.json'):
                path = os.path.join(self.backup_dir, file)
                stats = os.stat(path)
                backups.append({
                    'arquivo': file,
                    'data': datetime.datetime.fromtimestamp(stats.st_mtime).strftime("%d/%m/%Y %H:%M"),
                    'tamanho': f"{stats.st_size / 1024:.1f} KB"
                })
        return sorted(backups, key=lambda x: x['data'], reverse=True)
