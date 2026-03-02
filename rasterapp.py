# app.py - Versão corrigida sem erros de ID duplicado

import streamlit as st
import time
import random
from datetime import datetime
import numpy as np
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Scanner Automotivo Pro",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    /* Esconde elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Tema automotivo */
    .stApp {
        background-color: #1a1a1a;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: #2d2d2d;
        border-left: 4px solid #ff6600;
        border-radius: 5px;
        padding: 15px;
        margin: 5px 0;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #ff6600;
        font-family: 'Courier New', monospace;
    }
    
    .metric-label {
        color: #888;
        font-size: 14px;
        text-transform: uppercase;
    }
    
    /* Status LED */
    .led-green {
        width: 12px;
        height: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        animation: pulse 2s infinite;
    }
    
    .led-red {
        width: 12px;
        height: 12px;
        background-color: #ff0000;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Info grid */
    .info-grid {
        background: #2d2d2d;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid #444;
    }
    
    .info-label {
        color: #888;
    }
    
    .info-value {
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    /* Osciloscópio */
    .oscilloscope-card {
        background: #000;
        border: 2px solid #ff6600;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    /* Botões */
    .stButton > button {
        width: 100%;
        background-color: #ff6600;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        margin: 2px 0;
    }
    
    .stButton > button:hover {
        background-color: #ff8533;
    }
    
    /* Footer */
    .footer {
        background: #2d2d2d;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO DO ESTADO
# =============================================
if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.rpm = 845
    st.session_state.temp = 89
    st.session_state.voltage = 13.8
    st.session_state.oil_pressure = 4.2
    st.session_state.engine_load = 23
    st.session_state.osc_running = False
    st.session_state.log = []

# =============================================
# HEADER
# =============================================
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("## 🔧")

with col2:
    st.markdown("<h1 style='text-align: center; color: #ff6600;'>SCANNER AUTOMOTIVO PRO</h1>", unsafe_allow_html=True)

with col3:
    if st.session_state.connected:
        st.markdown("<p style='text-align: right;'><span class='led-green'></span> CONECTADO</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align: right;'><span class='led-red'></span> DESCONECTADO</p>", unsafe_allow_html=True)

st.divider()

# =============================================
# LAYOUT PRINCIPAL (3 COLUNAS)
# =============================================
col_left, col_center, col_right = st.columns([1.2, 2, 1])

# =============================================
# COLUNA ESQUERDA - CONEXÃO E INFOS
# =============================================
with col_left:
    st.markdown("### 🔌 CONEXÃO")
    
    # Controles de conexão em container único
    with st.container():
        port = st.selectbox("Porta", ["COM3", "COM4", "/dev/ttyUSB0"], key="port_select")
        baud = st.selectbox("Baud Rate", ["38400", "115200", "9600"], key="baud_select")
        st.markdown("<p><span class='info-label'>Protocolo:</span> <span class='info-value'>CAN 500kbps</span></p>", unsafe_allow_html=True)
        
        # Botão de conexão único
        if st.button("🔌 CONECTAR", key="connect_btn"):
            st.session_state.connected = not st.session_state.connected
            if st.session_state.connected:
                st.session_state.log.append("Conectado ao veículo")
            else:
                st.session_state.log.append("Desconectado")
            st.rerun()
    
    st.divider()
    
    # Informações do veículo
    st.markdown("### 🚗 INFORMAÇÕES DO VEÍCULO")
    
    with st.container():
        st.markdown("""
        <div class="info-grid">
            <div class="info-row"><span class="info-label">Fabricante:</span><span class="info-value">VOLKSWAGEN</span></div>
            <div class="info-row"><span class="info-label">Modelo:</span><span class="info-value">GOL 1.6 MSI</span></div>
            <div class="info-row"><span class="info-label">Ano:</span><span class="info-value">2024</span></div>
            <div class="info-row"><span class="info-label">Motor:</span><span class="info-value">EA211 (16V)</span></div>
            <div class="info-row"><span class="info-label">Câmbio:</span><span class="info-value">MQ200 (MANUAL)</span></div>
            <div class="info-row"><span class="info-label">KM:</span><span class="info-value">15.234 km</span></div>
            <div class="info-row"><span class="info-label">VIN:</span><span class="info-value">9BWZZZ377VT004251</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Dados em tempo real
    st.markdown("### 📊 DADOS EM TEMPO REAL")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RPM</div>
            <div class="metric-value">{st.session_state.rpm}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TEMP. MOTOR</div>
            <div class="metric-value">{st.session_state.temp}°C</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TENSÃO</div>
            <div class="metric-value">{st.session_state.voltage}V</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">PRESSÃO ÓLEO</div>
            <div class="metric-value">{st.session_state.oil_pressure} bar</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# COLUNA CENTRAL - OSCILOSCÓPIO
# =============================================
with col_center:
    st.markdown("### 📈 OSCILOSCÓPIO")
    
    # Gráfico do osciloscópio
    x = np.linspace(0, 100, 500)
    t = time.time() if 't' not in st.session_state else st.session_state.t
    
    if st.session_state.osc_running:
        st.session_state.t = t + 0.1
    else:
        st.session_state.t = t
    
    # Sinais simulados
    y1 = np.sin(x * 0.2 + st.session_state.t) * 30 + 50
    y2 = np.sin(x * 0.1 + st.session_state.t * 2) * 40 + 50
    
    osc_data = pd.DataFrame({
        'CH1 - Sensor Detonação': y1,
        'CH2 - Bomba Injetora': y2
    })
    
    st.line_chart(osc_data, height=300)
    
    # Controles do osciloscópio em colunas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.selectbox("TIME/DIV", ["10ms", "5ms", "20ms"], key="time_div")
    with col2:
        st.selectbox("VOLTS/DIV", ["2V", "1V", "5V"], key="volts_div")
    with col3:
        st.selectbox("TRIGGER", ["CH1", "CH2", "AUTO"], key="trigger")
    with col4:
        if st.button("▶ INICIAR", key="start_osc"):
            st.session_state.osc_running = True
    with col5:
        if st.button("⏹ PARAR", key="stop_osc"):
            st.session_state.osc_running = False

# =============================================
# COLUNA DIREITA - CONTROLES
# =============================================
with col_right:
    st.markdown("### ⚡ CONTROLES")
    
    # Botões de ação (cada um com key única)
    if st.button("🔍 ESCANEAR VEÍCULO", key="scan_btn"):
        st.session_state.log.append("Escaneando veículo...")
        st.success("Veículo identificado: VW GOL 1.6 2024")
    
    if st.button("⚠️ LER FALHAS", key="dtc_btn"):
        st.session_state.log.append("Lendo códigos de falha...")
        st.warning("Códigos de falha encontrados:")
        st.code("P0301 - Falha no cilindro 1\nP0420 - Catalisador ineficiente\nP0171 - Mistura pobre")
    
    if st.button("✅ LIMPAR FALHAS", key="clear_btn"):
        st.session_state.log.append("Códigos de falha limpos")
        st.success("Códigos de falha limpos com sucesso!")
    
    if st.button("📊 DADOS REAIS", key="data_btn"):
        st.session_state.log.append("Coletando dados em tempo real")
        st.info("Coletando dados...")
    
    # Botão de reprogramação com progresso
    if st.button("⚡ REPROGRAMAR ECU", key="reprog_btn"):
        st.session_state.log.append("INICIANDO REPROGRAMAÇÃO")
        with st.spinner("Reprogramando ECU. NÃO DESLIGUE O VEÍCULO!"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
            st.success("✅ Reprogramação concluída!")
            st.session_state.log.append("Reprogramação concluída com sucesso")
    
    st.divider()
    
    # Botões INICIAR/PARAR
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶ INICIAR", key="start_acq", use_container_width=True):
            st.session_state.log.append("Aquisição iniciada")
            st.session_state.running = True
    
    with col2:
        if st.button("⏹ PARAR", key="stop_acq", use_container_width=True):
            st.session_state.log.append("Aquisição parada")
            st.session_state.running = False
    
    st.divider()
    
    # Últimas leituras
    st.markdown("### 📋 ÚLTIMAS LEITURAS")
    
    # Mostra últimas 5 entradas do log
    recent_logs = st.session_state.log[-5:] if st.session_state.log else []
    for log in reversed(recent_logs):
        st.caption(f"📌 {log}")

# =============================================
# FOOTER
# =============================================
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    last_log = st.session_state.log[-1] if st.session_state.log else "Sistema pronto"
    st.markdown(f"<div class='footer'>> {last_log}</div>", unsafe_allow_html=True)

with col2:
    status = "🟢 ONLINE" if st.session_state.connected else "🔴 OFFLINE"
    st.markdown(f"<div style='text-align: right; color: #888;'>CAN BUS: OK | ECU: {status}</div>", unsafe_allow_html=True)

# =============================================
# ATUALIZAÇÃO DOS DADOS EM TEMPO REAL
# =============================================
if st.session_state.connected and st.session_state.get('running', False):
    # Atualiza dados com variação realista
    st.session_state.rpm = random.randint(750, 3500)
    st.session_state.temp = random.randint(82, 98)
    st.session_state.voltage = round(12 + random.random() * 2, 1)
    st.session_state.oil_pressure = round(3.5 + random.random() * 1.5, 1)
    st.session_state.engine_load = random.randint(15, 45)
    
    # Adiciona ao log a cada 10 atualizações (para não encher)
    if random.randint(1, 10) == 1:
        st.session_state.log.append(f"RPM: {st.session_state.rpm}")
    
    # Mantém log com no máximo 20 itens
    if len(st.session_state.log) > 20:
        st.session_state.log = st.session_state.log[-20:]
    
    time.sleep(1)
    st.rerun()
