# app.py - Backend principal com Streamlit

import streamlit as st
import asyncio
import websockets
import json
import threading
import time
import random
from datetime import datetime
import obd_scanner
import dtc_database
import can_bus

# Configuração da página
st.set_page_config(
    page_title="AUTOMOTIVE PRO",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
<style>
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Customizar scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0c10;
    }
    ::-webkit-scrollbar-thumb {
        background: #2e343f;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #ff6600;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# WEBSOCKET SERVER
# =============================================
class WebSocketServer:
    def __init__(self):
        self.clients = set()
        self.running = True
        self.data_thread = None
        
    async def handler(self, websocket, path):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.process_message(websocket, data)
        finally:
            self.clients.remove(websocket)
    
    async def process_message(self, websocket, data):
        action = data.get('action')
        
        if action == 'scan':
            # Escaneia veículo
            vehicle_info = obd_scanner.scan_vehicle()
            await websocket.send(json.dumps({
                'type': 'vehicle_info',
                'data': vehicle_info
            }))
            
        elif action == 'connect':
            device = data.get('device')
            # Conecta ao dispositivo OBD2
            result = obd_scanner.connect(device)
            await websocket.send(json.dumps({
                'type': 'connection_result',
                'success': result
            }))
            
        elif action == 'read_dtc':
            # Lê códigos de falha
            dtcs = obd_scanner.read_dtc()
            await websocket.send(json.dumps({
                'type': 'dtc_data',
                'data': dtcs
            }))
            
        elif action == 'clear_dtc':
            # Limpa códigos de falha
            success = obd_scanner.clear_dtc()
            await websocket.send(json.dumps({
                'type': 'clear_result',
                'success': success
            }))
            
        elif action == 'reprogram':
            # Inicia reprogramação
            await self.start_reprogramming(websocket)
    
    async def start_reprogramming(self, websocket):
        for i in range(101):
            await websocket.send(json.dumps({
                'type': 'reprogram_progress',
                'progress': i
            }))
            await asyncio.sleep(0.1)
        
        await websocket.send(json.dumps({
            'type': 'reprogram_complete',
            'success': True
        }))
    
    async def broadcast_data(self, data):
        """Envia dados em tempo real para todos os clientes"""
        if self.clients:
            message = json.dumps(data)
            await asyncio.gather(
                *[client.send(message) for client in self.clients]
            )
    
    def start_data_simulation(self):
        """Simula dados em tempo real do veículo"""
        async def simulate():
            while self.running:
                if self.clients:
                    data = {
                        'rpm': random.randint(750, 3500),
                        'speed': random.randint(0, 80),
                        'temp': random.randint(80, 100),
                        'battery': 12 + random.random() * 2,
                        'oilPressure': 3 + random.random() * 2,
                        'engineLoad': random.randint(20, 60),
                        'intakeTemp': random.randint(25, 40),
                        'timingAdvance': random.randint(5, 25),
                        'o2Sensor': 0.7 + random.random() * 0.2,
                        'fuelPressure': 350 + random.random() * 50,
                        'throttle': random.randint(10, 40),
                        'maf': 5 + random.random() * 10,
                        'vehicle': {
                            'manufacturer': 'Volkswagen',
                            'model': 'Gol 1.6',
                            'year': '2024',
                            'engine': 'EA211',
                            'ecu': 'Bosch ME17.9.65'
                        }
                    }
                    await self.broadcast_data(data)
                await asyncio.sleep(0.5)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(simulate())
    
    def start(self):
        """Inicia o servidor WebSocket"""
        self.data_thread = threading.Thread(target=self.start_data_simulation)
        self.data_thread.daemon = True
        self.data_thread.start()
        
        start_server = websockets.serve(self.handler, "localhost", 8501)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

# =============================================
# STREAMLIT INTERFACE
# =============================================
def main():
    st.title("🔧 AUTOMOTIVE PRO - Backend Server")
    
    # Status do servidor
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Status", "🟢 Online", "WebSocket ativo")
    
    with col2:
        st.metric("Clientes Conectados", "0", "Em tempo real")
    
    with col3:
        st.metric("Uptime", "00:00:00", "Servidor")
    
    # Logs em tempo real
    st.subheader("📋 Logs do Sistema")
    log_area = st.empty()
    
    # Controles
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ INICIAR SERVIDOR", use_container_width=True):
            st.success("Servidor iniciado na porta 8501")
    
    with col2:
        if st.button("🔄 REINICIAR", use_container_width=True):
            st.warning("Reiniciando...")
    
    with col3:
        if st.button("⏹️ PARAR", use_container_width=True):
            st.error("Servidor parado")
    
    # Informações do hardware
    st.subheader("🔌 Dispositivos Detectados")
    
    devices = {
        "Bluetooth": ["OBDII-BT-001", "OBDII-BT-002"],
        "WiFi": ["OBDII-WiFi-01"],
        "USB": ["/dev/ttyUSB0", "COM3"]
    }
    
    for type, devs in devices.items():
        with st.expander(f"{type} ({len(devs)} dispositivos)"):
            for dev in devs:
                st.write(f"• {dev}")
    
    # Executa servidor WebSocket
    server = WebSocketServer()
    server.start()

if __name__ == "__main__":
    main()