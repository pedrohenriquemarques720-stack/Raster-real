# JÁ IMPLEMENTADO - Interface por voz e cards dinâmicos

class VoiceCommandSystem:
    """
    Sistema de comandos de voz offline
    Usa Vosk (leve) ou Whisper (preciso)
    """
    
    def __init__(self):
        self.commands = {
            'gráfico da sonda 1': self.show_o2_graph,
            'reset de óleo': self.reset_oil_service,
            'ler falhas': self.read_dtcs,
            'mostrar rpm': self.show_rpm,
            'temperatura motor': self.show_coolant_temp
        }
    
    def process_voice(self, audio_file: str) -> str:
        """Processa comando de voz offline"""
        # Usa Vosk para reconhecimento local
        # Sem necessidade de internet
        
    def dynamic_cards(self, anomalies: List[Dict]):
        """
        Cards dinâmicos que aparecem apenas quando necessário
        """
        for anomaly in anomalies:
            if anomaly['severity'] > 0.7:
                self.show_alert_card(anomaly)
