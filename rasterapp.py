# app.py - Backend para Streamlit

import streamlit as st
import time
import random
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Scanner Automotivo Pro",
    page_icon="🔧",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    /* Esconde elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Ajustes de layout */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    /* Cards */
    .metric-card {
        background: #1a1d24;
        border: 1px solid #ff6600;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 5px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #ff6600;
        font-family: 'Courier New', monospace;
    }
    
    .metric-label {
        color: #888;
        font-size: 14px;
    }
    
    /* Status */
    .status-online {
        color: #00ff00;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff0000;
        font-weight: bold;
    }
    
    /* Botões */
    .stButton > button {
        background-color: #ff6600;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #ff8533;
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

# =============================================
# HEADER
# =============================================
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🔧 SCANNER AUTOMOTIVO PRO")

with col2:
    if st.session_state.connected:
        st.markdown("### 🟢 **CONECTADO**")
    else:
        st.markdown("### 🔴 **DESCONECTADO**")

st.divider()

# =============================================
# LAYOUT PRINCIPAL
# =============================================
col_left, col_center, col_right = st.columns([1.2, 2, 1])

# =============================================
# COLUNA ESQUERDA - CONEXÃO E INFOS
# =============================================
with col_left:
    st.subheader("🔌 CONEXÃO")
    
    # Controles de conexão
    port = st.selectbox("Porta", ["COM3", "COM4", "/dev/ttyUSB0"])
    baud = st.selectbox("Baud Rate", ["38400", "115200", "9600"])
    
    if st.button("🔌 CONECTAR", use_container_width=True):
        st.session_state.connected = not st.session_state.connected
    
    st.divider()
    
    # Informações do veículo
    st.subheader("🚗 INFORMAÇÕES DO VEÍCULO")
    
    info_data = {
        "Fabricante": "VOLKSWAGEN",
        "Modelo": "GOL 1.6 MSI",
        "Ano": "2024",
        "Motor": "EA211 (16V)",
        "Câmbio": "MQ200 (MANUAL)",
        "KM": "15.234 km",
        "VIN": "9BWZZZ377VT004251"
    }
    
    for key, value in info_data.items():
        st.markdown(f"**{key}:** `{value}`")
    
    st.divider()
    
    # Dados em tempo real
    st.subheader("📊 DADOS EM TEMPO REAL")
    
    if st.session_state.connected:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.rpm}</div>
                <div class="metric-label">RPM</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.temp}°C</div>
                <div class="metric-label">TEMP. MOTOR</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.voltage}V</div>
                <div class="metric-label">TENSÃO</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.oil_pressure}</div>
                <div class="metric-label">PRESSÃO ÓLEO</div>
            </div>
            """, unsafe_allow_html=True)

# =============================================
# COLUNA CENTRAL - OSCILOSCÓPIO
# =============================================
with col_center:
    st.subheader("📈 OSCILOSCÓPIO")
    
    # Gráfico do osciloscópio
    import numpy as np
    import pandas as pd
    
    x = np.linspace(0, 100, 500)
    y1 = np.sin(x * 0.2) * 30 + 50
    y2 = np.sin(x * 0.1) * 40 + 50
    
    osc_data = pd.DataFrame({
        'CH1': y1,
        'CH2': y2
    })
    
    st.line_chart(osc_data, height=300)
    
    # Controles
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.selectbox("TIME/DIV", ["10ms", "5ms", "20ms"])
    with col2:
        st.selectbox("VOLTS/DIV", ["2V", "1V", "5V"])
    with col3:
        st.selectbox("TRIGGER", ["CH1", "CH2", "AUTO"])
    with col4:
        st.button("▶ INICIAR", use_container_width=True)
    with col5:
        st.button("⏹ PARAR", use_container_width=True)

# =============================================
# COLUNA DIREITA - CONTROLES
# =============================================
with col_right:
    st.subheader("⚡ CONTROLES")
    
    # Botões de ação
    if st.button("🔍 ESCANEAR VEÍCULO", use_container_width=True):
        st.success("Veículo identificado: VW GOL 1.6 2024")
    
    if st.button("⚠️ LER FALHAS", use_container_width=True):
        st.warning("3 códigos de falha encontrados")
        st.code("P0301 - Falha no cilindro 1\nP0420 - Catalisador\nP0171 - Mistura pobre")
    
    if st.button("✅ LIMPAR FALHAS", use_container_width=True):
        st.success("Códigos de falha limpos")
    
    if st.button("📊 DADOS REAIS", use_container_width=True):
        st.info("Coletando dados em tempo real...")
    
    if st.button("⚡ REPROGRAMAR ECU", use_container_width=True, type="primary"):
        with st.spinner("Reprogramando ECU..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress.progress(i + 1)
        st.success("Reprogramação concluída!")
    
    st.divider()
    
    # Botões INICIAR/PARAR
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ INICIAR", use_container_width=True):
            st.session_state.running = True
    with col2:
        if st.button("⏹ PARAR", use_container_width=True):
            st.session_state.running = False
    
    st.divider()
    
    # Últimas leituras
    st.subheader("📋 ÚLTIMAS LEITURAS")
    
    # Simula histórico
    historico = [
        "15:23:45 - RPM: 2345",
        "15:23:44 - RPM: 2310",
        "15:23:43 - RPM: 2280",
        "15:23:42 - RPM: 2245",
        "15:23:41 - RPM: 2210"
    ]
    
    for item in historico:
        st.caption(item)

# =============================================
# FOOTER
# =============================================
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    st.caption("> Sistema pronto | Conectado ao veículo")

with col2:
    st.caption("CAN BUS: OK | ECU: ONLINE | FW: v2.1.0")

# =============================================
# ATUALIZAÇÃO AUTOMÁTICA
# =============================================
if st.session_state.connected:
    # Atualiza dados em tempo real
    st.session_state.rpm = random.randint(750, 3500)
    st.session_state.temp = random.randint(82, 98)
    st.session_state.voltage = round(12 + random.random() * 2, 1)
    st.session_state.oil_pressure = round(3.5 + random.random() * 1.5, 1)
    st.session_state.engine_load = random.randint(15, 45)
    
    time.sleep(1)
    st.rerun()
