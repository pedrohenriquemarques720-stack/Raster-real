# rasterapp.py - Versão otimizada para Streamlit Cloud

import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="AUTOMOTIVE PRO - Diagnóstico Profissional",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    /* Tema automotivo profissional */
    .stApp {
        background-color: #0a0c10;
    }
    
    /* Header com gradiente */
    .header-gradient {
        background: linear-gradient(135deg, #ff6600, #00b0ff);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .main-title {
        color: white;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(145deg, #1a1d24, #0f1217);
        border: 2px solid #ff6600;
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 10px 20px rgba(255,102,0,0.2);
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(255,102,0,0.3);
    }
    
    .metric-value {
        font-size: 54px;
        font-weight: bold;
        color: #ff6600;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    
    .metric-label {
        color: #9aa4b8;
        font-size: 18px;
        text-align: center;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .metric-unit {
        color: #666;
        font-size: 14px;
        text-align: center;
    }
    
    /* Cards de informação */
    .info-card {
        background: #1a1d24;
        border-left: 5px solid #ff6600;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    /* Status LED */
    .led-red {
        width: 12px;
        height: 12px;
        background-color: #ff3d00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #ff3d00;
        animation: pulse-red 2s infinite;
    }
    
    .led-green {
        width: 12px;
        height: 12px;
        background-color: #00c853;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00c853;
        animation: pulse-green 2s infinite;
    }
    
    @keyframes pulse-red {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    @keyframes pulse-green {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* DTC Cards */
    .dtc-card {
        background: #1a1d24;
        border-left: 5px solid #ff3d00;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .dtc-code {
        color: #ff3d00;
        font-weight: bold;
        font-size: 20px;
        font-family: 'Courier New', monospace;
    }
    
    .dtc-desc {
        color: white;
        font-size: 14px;
    }
    
    /* Botões */
    .stButton > button {
        background-color: #ff6600;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #ff8533;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,102,0,0.3);
    }
    
    /* Tabelas */
    .dataframe {
        background-color: #1a1d24;
        color: white;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        padding: 20px;
        font-size: 12px;
        border-top: 1px solid #333;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO DO ESTADO
# =============================================
if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.vehicle_info = {}
    st.session_state.dtcs = []
    st.session_state.data_history = []
    st.session_state.current_data = {
        'rpm': 0,
        'speed': 0,
        'temp': 85,
        'battery': 12.5,
        'oil_pressure': 4.2,
        'engine_load': 25,
        'intake_temp': 32,
        'timing_advance': 12,
        'o2_sensor': 0.78,
        'fuel_pressure': 380,
        'throttle': 18,
        'maf': 8.5
    }

# =============================================
# HEADER
# =============================================
st.markdown("""
<div class="header-gradient">
    <div class="main-title">🔧 AUTOMOTIVE PRO</div>
</div>
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR
# =============================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x150/ff6600/000000?text=AUTOMOTIVE+PRO", use_container_width=True)
    
    st.markdown("## 🔌 CONEXÃO")
    
    # Status
    if st.session_state.connected:
        st.markdown(f"""
        <div style="background: #1a1d24; padding: 15px; border-radius: 10px; border-left: 5px solid #00c853;">
            <span class="led-green"></span> <span class="status-online"> CONECTADO</span><br>
            <span style="color: #888;">Dispositivo: OBDII-ELM327</span><br>
            <span style="color: #888;">Protocolo: CAN 500kbps</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: #1a1d24; padding: 15px; border-radius: 10px; border-left: 5px solid #ff3d00;">
            <span class="led-red"></span> <span style="color: #ff3d00;"> DESCONECTADO</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Botão de conexão
    if st.button("🔌 CONECTAR/DESCONECTAR", use_container_width=True):
        st.session_state.connected = not st.session_state.connected
        if st.session_state.connected:
            st.session_state.vehicle_info = {
                'manufacturer': 'Volkswagen',
                'model': 'Gol 1.6 MSI',
                'year': '2024',
                'engine': 'EA211 16V',
                'ecu': 'Bosch ME17.9.65',
                'vin': '9BWZZZ377VT004251',
                'software': '03H906023AB 3456'
            }
        st.rerun()
    
    st.markdown("---")
    st.markdown("## ⚡ AÇÕES RÁPIDAS")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 LER FALHAS", use_container_width=True):
            st.session_state.dtcs = [
                {'code': 'P0301', 'desc': 'Falha de ignição no cilindro 1', 'system': 'Motor', 'severity': 'Alta'},
                {'code': 'P0420', 'desc': 'Eficiência do catalisador abaixo do limite', 'system': 'Emissões', 'severity': 'Média'}
            ]
            st.success("3 códigos de falha encontrados!")
    
    with col2:
        if st.button("✅ LIMPAR FALHAS", use_container_width=True):
            st.session_state.dtcs = []
            st.success("Códigos de falha limpos!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 DADOS REAIS", use_container_width=True):
            st.info("Coletando dados em tempo real...")
    
    with col2:
        if st.button("⚡ REPROGRAMAR", use_container_width=True):
            st.warning("⚠️ INICIANDO REPROGRAMAÇÃO")
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress.progress(i + 1)
            st.success("✅ Reprogramação concluída!")

# =============================================
# CONTEÚDO PRINCIPAL
# =============================================
if st.session_state.connected:
    # Atualiza dados simulados
    st.session_state.current_data = {
        'rpm': random.randint(750, 3500),
        'speed': random.randint(0, 120),
        'temp': random.randint(82, 98),
        'battery': round(12 + random.random() * 2, 1),
        'oil_pressure': round(3.5 + random.random() * 1.5, 1),
        'engine_load': random.randint(15, 55),
        'intake_temp': random.randint(25, 40),
        'timing_advance': random.randint(8, 22),
        'o2_sensor': round(0.7 + random.random() * 0.2, 2),
        'fuel_pressure': random.randint(340, 400),
        'throttle': random.randint(8, 35),
        'maf': round(5 + random.random() * 8, 1)
    }
    
    # LINHA 1: MÉTRICAS PRINCIPAIS
    st.markdown("## 📊 PAINEL PRINCIPAL")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.current_data['rpm']}</div>
            <div class="metric-label">RPM</div>
            <div class="metric-unit">rotações/min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.current_data['speed']}</div>
            <div class="metric-label">VELOCIDADE</div>
            <div class="metric-unit">km/h</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.current_data['temp']}°</div>
            <div class="metric-label">TEMP. MOTOR</div>
            <div class="metric-unit">°C</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.current_data['battery']}V</div>
            <div class="metric-label">BATERIA</div>
            <div class="metric-unit">volts</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # LINHA 2: INFORMAÇÕES DO VEÍCULO E DADOS DO MOTOR
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚗 INFORMAÇÕES DO VEÍCULO")
        info_df = pd.DataFrame({
            'Parâmetro': ['Fabricante', 'Modelo', 'Ano', 'Motor', 'ECU', 'VIN', 'Software'],
            'Valor': [
                st.session_state.vehicle_info.get('manufacturer', 'N/A'),
                st.session_state.vehicle_info.get('model', 'N/A'),
                st.session_state.vehicle_info.get('year', 'N/A'),
                st.session_state.vehicle_info.get('engine', 'N/A'),
                st.session_state.vehicle_info.get('ecu', 'N/A'),
                st.session_state.vehicle_info.get('vin', 'N/A'),
                st.session_state.vehicle_info.get('software', 'N/A')
            ]
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 🔧 DADOS DO MOTOR")
        motor_df = pd.DataFrame({
            'Parâmetro': [
                'Pressão do Óleo (bar)',
                'Carga do Motor (%)',
                'Temp. Ar Admissão (°C)',
                'Avanço Ignição (°)',
                'Sonda Lambda (V)',
                'Pressão Combustível (kPa)',
                'Posição Acelerador (%)',
                'Fluxo de Ar (g/s)'
            ],
            'Valor': [
                st.session_state.current_data['oil_pressure'],
                st.session_state.current_data['engine_load'],
                st.session_state.current_data['intake_temp'],
                st.session_state.current_data['timing_advance'],
                st.session_state.current_data['o2_sensor'],
                st.session_state.current_data['fuel_pressure'],
                st.session_state.current_data['throttle'],
                st.session_state.current_data['maf']
            ]
        })
        st.dataframe(motor_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # LINHA 3: CÓDIGOS DE FALHA
    st.markdown("### ⚠️ CÓDIGOS DE FALHA (DTC)")
    
    if st.session_state.dtcs:
        for dtc in st.session_state.dtcs:
            severity_color = {
                'Alta': '#ff3d00',
                'Média': '#ffb300',
                'Baixa': '#00c853'
            }.get(dtc['severity'], '#888')
            
            st.markdown(f"""
            <div class="dtc-card" style="border-left-color: {severity_color};">
                <div class="dtc-code">{dtc['code']}</div>
                <div class="dtc-desc">{dtc['desc']}</div>
                <div style="color: #888; font-size: 12px; margin-top: 5px;">
                    Sistema: {dtc['system']} | Gravidade: {dtc['severity']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum código de falha encontrado. O veículo está em condições normais de operação.")
    
    # LINHA 4: OSCILOSCÓPIO SIMULADO
    st.markdown("---")
    st.markdown("### 📈 OSCILOSCÓPIO - SINAIS EM TEMPO REAL")
    
    # Simula dados de osciloscópio
    import numpy as np
    import pandas as pd
    
    x = np.linspace(0, 100, 100)
    y1 = np.sin(x * 0.2) * 0.5
    y2 = np.sin(x * 0.1) * 5 + 7
    
    osc_df = pd.DataFrame({
        'Tempo': x,
        'CH1 - Sensor Detonação (V)': y1,
        'CH2 - Sinal Injeção (V)': y2
    })
    
    st.line_chart(osc_df.set_index('Tempo'))
    
else:
    # Tela de boas-vindas quando desconectado
    st.markdown("""
    <div style="text-align: center; padding: 100px 20px;">
        <div style="font-size: 80px; margin-bottom: 20px;">🔧</div>
        <h2 style="color: #ff6600;">AUTOMOTIVE PRO</h2>
        <p style="color: #888; font-size: 18px; margin: 20px 0;">
            Conecte-se a um veículo para iniciar o diagnóstico
        </p>
        <p style="color: #666;">
            • Leitura de dados em tempo real<br>
            • Diagnóstico de falhas (DTC)<br>
            • Osciloscópio integrado<br>
            • Reprogramação de ECU
        </p>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# FOOTER
# =============================================
st.markdown("""
<div class="footer">
    <p>🔧 AUTOMOTIVE PRO v2.0 - Sistema Profissional de Diagnóstico Automotivo</p>
    <p>Desenvolvido para mecânicos e preparadores | © 2026</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh se conectado
if st.session_state.connected:
    time.sleep(1)
    st.rerun()
