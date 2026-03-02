# app.py - Interface do Scanner Automotivo Profissional (Tudo na mesma tela)

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import threading
from datetime import datetime

# Importando nossos módulos
from obd_scanner import OBDScannerRevolucionario as OBDScannerPro
from dtc_database import DTCDatabase
from vehicle_profiles import VehicleDatabase

# Configuração da página
st.set_page_config(
    page_title="AUTEL PRO - Diagnóstico Inteligente",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# CSS - ESTILO RASTER 3S (TUDO NA MESMA TELA)
# =============================================
st.markdown("""
<style>
    /* Reset e estilos globais */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }

    .stApp {
        background: #1a1a1a;
        color: #ffffff;
        padding: 10px;
    }
    
    .main > .block-container {
        max-width: 100%;
        margin: 0;
        padding: 10px !important;
        background: #2d2d2d;
        border-radius: 10px;
    }
    
    /* Header com gradiente - IGUAL AO RASTER */
    .header {
        background: linear-gradient(135deg, #0047AB, #002B5C);
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-left: 5px solid #ff6600;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo-icon {
        font-size: 32px;
        filter: drop-shadow(0 0 10px rgba(0,255,255,0.5));
    }
    
    .logo-text h1 {
        font-size: 22px;
        font-weight: bold;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .logo-text p {
        color: #00ffff;
        font-size: 10px;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .device-status {
        background: #000;
        padding: 6px 15px;
        border-radius: 30px;
        border: 1px solid #00ffff;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 12px;
    }
    
    /* Connection Bar - IGUAL AO RASTER */
    .connection-bar {
        background: #1a1a1a;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
        display: flex;
        gap: 15px;
        align-items: center;
        border-left: 5px solid #ff6600;
        border: 1px solid #333;
    }
    
    .conn-info {
        display: flex;
        gap: 20px;
        flex: 1;
    }
    
    .conn-item {
        display: flex;
        flex-direction: column;
    }
    
    .conn-label {
        font-size: 11px;
        color: #888;
        text-transform: uppercase;
    }
    
    .conn-value {
        font-size: 13px;
        font-weight: bold;
        color: #ff6600;
        font-family: 'Courier New', monospace;
    }
    
    .conn-button {
        background: #00ff00;
        color: #000;
        padding: 8px 20px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
        font-size: 13px;
        white-space: nowrap;
    }
    
    .conn-button:hover {
        background: #00cc00;
    }
    
    .conn-button.off {
        background: #ff0000;
        color: white;
    }
    
    /* MAIN GRID - 2 COLUNAS (TUDO NA MESMA TELA) */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 12px;
    }
    
    /* PANELS */
    .left-panel, .right-panel {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #333;
    }
    
    /* Panel Title */
    .panel-title {
        color: #ff6600;
        font-size: 13px;
        font-weight: bold;
        margin-bottom: 10px;
        padding-bottom: 3px;
        border-bottom: 2px solid #ff6600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Vehicle Info */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid #333;
        font-size: 12px;
    }
    
    .info-label {
        color: #888;
    }
    
    .info-value {
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-align: right;
    }
    
    /* DTC List */
    .dtc-item {
        background: #330000;
        border-left: 3px solid #ff0000;
        padding: 8px;
        margin-bottom: 5px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        border-radius: 0 4px 4px 0;
    }
    
    .dtc-code {
        color: #ff6666;
        font-weight: bold;
        font-size: 13px;
    }
    
    .dtc-desc {
        font-size: 11px;
        color: #aaa;
    }
    
    /* Function Tabs */
    .function-tabs {
        display: flex;
        gap: 4px;
        margin-bottom: 12px;
        background: #333;
        padding: 4px;
        border-radius: 5px;
    }
    
    .tab {
        flex: 1;
        padding: 6px 4px;
        text-align: center;
        cursor: pointer;
        border-radius: 4px;
        font-size: 11px;
        background: #333;
        color: white;
        border: none;
        white-space: nowrap;
        font-weight: 500;
    }
    
    .tab:hover {
        background: #444;
    }
    
    .tab.active {
        background: #ff6600;
        color: #000;
        font-weight: bold;
    }
    
    /* LIVE DATA GRID - 2 COLUNAS */
    .live-data-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }
    
    .live-item {
        background: #333;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #00ff00;
    }
    
    .live-label {
        font-size: 10px;
        color: #888;
        margin-bottom: 3px;
        text-transform: uppercase;
    }
    
    .live-value {
        font-size: 16px;
        font-weight: bold;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    
    .live-unit {
        font-size: 10px;
        color: #888;
        margin-left: 3px;
    }
    
    .live-graph {
        height: 3px;
        background: #444;
        margin-top: 6px;
        border-radius: 2px;
        overflow: hidden;
    }
    
    .graph-fill {
        height: 100%;
        background: #00ff00;
        width: 0%;
        transition: 0.3s;
    }
    
    /* Oscilloscope */
    .scope-channel {
        background: #000;
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 8px;
        border: 1px solid #333;
    }
    
    .channel-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        font-size: 10px;
    }
    
    .channel-1 { color: #ffff00; }
    .channel-2 { color: #00ffff; }
    
    .waveform {
        height: 50px;
        background: #111;
        position: relative;
        overflow: hidden;
        border-radius: 3px;
    }
    
    .wave-line {
        position: absolute;
        width: 100%;
        height: 2px;
        background: #ffff00;
        bottom: 25px;
        animation: wave 2s linear infinite;
    }
    
    .wave-line2 {
        background: #00ffff;
        bottom: 15px;
        animation: wave2 1.5s linear infinite;
    }
    
    @keyframes wave {
        0% { transform: translateX(0) translateY(0); }
        25% { transform: translateX(-25%) translateY(-5px); }
        50% { transform: translateX(-50%) translateY(0); }
        75% { transform: translateX(-75%) translateY(5px); }
        100% { transform: translateX(-100%) translateY(0); }
    }
    
    @keyframes wave2 {
        0% { transform: translateX(0) translateY(0); }
        33% { transform: translateX(-33%) translateY(3px); }
        66% { transform: translateX(-66%) translateY(-3px); }
        100% { transform: translateX(-100%) translateY(0); }
    }
    
    /* Quick Tools */
    .tools-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 5px;
        margin-top: 10px;
    }
    
    .tool-btn {
        background: #333;
        color: white;
        padding: 8px;
        border: 1px solid #444;
        border-radius: 5px;
        font-size: 11px;
        cursor: pointer;
        text-align: center;
    }
    
    .tool-btn:hover {
        background: #ff6600;
    }
    
    /* Bottom Bar */
    .bottom-bar {
        margin-top: 15px;
        background: #1a1a1a;
        padding: 8px 12px;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        font-family: 'Courier New', monospace;
        font-size: 11px;
        color: #00ff00;
        border: 1px solid #333;
    }
    
    .log-messages {
        display: flex;
        gap: 15px;
    }
    
    .log-entry {
        color: #888;
    }
    
    .log-entry.active {
        color: #00ff00;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Botões */
    .stButton > button {
        width: 100%;
        padding: 6px 8px !important;
        font-size: 11px !important;
        background-color: #ff6600 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 4px !important;
        margin: 2px 0 !important;
        min-height: 30px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #ff8533 !important;
    }
    
    /* Colunas Streamlit */
    div[data-testid="column"] {
        padding: 0 3px !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 3px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO DOS SISTEMAS
# =============================================
if 'scanner' not in st.session_state:
    st.session_state.scanner = OBDScannerPro()
    st.session_state.dtc_db = DTCDatabase()
    st.session_state.vehicle_db = VehicleDatabase()
    st.session_state.connected = False
    st.session_state.osc_running = False
    st.session_state.scanning = False
    st.session_state.progress = 0
    st.session_state.vehicle_info = {
        'manufacturer': '---',
        'model': '---',
        'year': '---',
        'engine': '---',
        'transmission': '---',
        'vin': '---',
        'ecu': '---',
        'version': '---',
        'protocol': '---',
        'km': '---'
    }
    st.session_state.dtcs = []
    st.session_state.live_data = {
        'rpm': 845,
        'speed': 0,
        'temp': 89,
        'oil_pressure': 4.2,
        'battery': 13.8,
        'engine_load': 23,
        'o2': 0.78,
        'timing': 12
    }
    st.session_state.log = ["> Sistema pronto. Conecte ao veículo."]

# =============================================
# HEADER
# =============================================
st.markdown("""
<div class="header">
    <div class="logo">
        <div class="logo-icon">🔧</div>
        <div class="logo-text">
            <h1>AUTEL PRO</h1>
            <p>DIAGNÓSTICO INTELIGENTE</p>
        </div>
    </div>
    <div class="device-status">
        <span>●</span> HARDWARE v2.45 • SN: TM20250301
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================
# CONNECTION BAR
# =============================================
col1, col2 = st.columns([3, 1])

with col1:
    vehicle_display = f"{st.session_state.vehicle_info.get('model', '---')} {st.session_state.vehicle_info.get('year', '')}"
    st.markdown(f"""
    <div class="connection-bar">
        <div class="conn-info">
            <div class="conn-item">
                <span class="conn-label">VEÍCULO</span>
                <span class="conn-value">{vehicle_display}</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">PROTOCOLO</span>
                <span class="conn-value">{st.session_state.vehicle_info.get('protocol', '---')}</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">ECU</span>
                <span class="conn-value">{st.session_state.vehicle_info.get('ecu', '---')}</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">VERSÃO</span>
                <span class="conn-value">{st.session_state.vehicle_info.get('version', '---')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not st.session_state.connected:
        if st.button("🔌 CONECTAR", key="connect_main"):
            with st.spinner("Conectando ao veículo..."):
                st.session_state.connected = True
                st.session_state.vehicle_info = {
                    'manufacturer': 'Volkswagen',
                    'model': 'Gol 1.6 MSI',
                    'year': '2024',
                    'engine': 'EA211 (16V)',
                    'transmission': 'MQ200 (MANUAL)',
                    'vin': '9BWZZZ377VT004251',
                    'ecu': 'BOSCH ME17.9.65',
                    'version': '03H906023AB 3456',
                    'protocol': 'CAN-BUS 500K',
                    'km': '15.234 km'
                }
                st.session_state.log.append("> Conectado ao veículo (modo simulação)")
                st.rerun()
    else:
        if st.button("🔌 DESCONECTAR", key="disconnect_main"):
            st.session_state.connected = False
            st.session_state.log.append("> Desconectado")
            st.rerun()

# =============================================
# MAIN GRID (2 COLUNAS - TUDO NA MESMA TELA)
# =============================================
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# =============================================
# LEFT PANEL - Vehicle Info e Dados em Tempo Real
# =============================================
st.markdown('<div class="left-panel">', unsafe_allow_html=True)

# INFORMAÇÕES DO VEÍCULO
st.markdown('<div class="panel-title">📋 INFORMAÇÕES DO VEÍCULO</div>', unsafe_allow_html=True)

info_data = [
    ("Fabricante:", st.session_state.vehicle_info.get('manufacturer', '---')),
    ("Modelo:", st.session_state.vehicle_info.get('model', '---')),
    ("Ano:", str(st.session_state.vehicle_info.get('year', '---'))),
    ("Motor:", st.session_state.vehicle_info.get('engine', '---')),
    ("Câmbio:", st.session_state.vehicle_info.get('transmission', '---')),
    ("KM:", st.session_state.vehicle_info.get('km', '---')),
    ("VIN:", st.session_state.vehicle_info.get('vin', '---'))
]

for label, value in info_data:
    st.markdown(f"""
    <div class="info-row">
        <span class="info-label">{label}</span>
        <span class="info-value">{value}</span>
    </div>
    """, unsafe_allow_html=True)

# CÓDIGOS DE FALHA
st.markdown('<div class="panel-title" style="margin-top: 12px;">⚠️ CÓDIGOS DE FALHA (DTC)</div>', unsafe_allow_html=True)

if st.session_state.dtcs:
    for dtc in st.session_state.dtcs:
        st.markdown(f"""
        <div class="dtc-item">
            <div class="dtc-code">{dtc.get('code', '')}</div>
            <div class="dtc-desc">{dtc.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="color: #888; padding: 8px; text-align: center; font-size: 12px; background: #1a1a1a; border-radius: 4px;">
        Nenhum código de falha
    </div>
    """, unsafe_allow_html=True)

# DADOS EM TEMPO REAL
st.markdown('<div class="panel-title" style="margin-top: 12px;">📊 DADOS EM TEMPO REAL</div>', unsafe_allow_html=True)

data = st.session_state.live_data

st.markdown('<div class="live-data-grid">', unsafe_allow_html=True)

st.markdown(f"""
<div class="live-item">
    <div class="live-label">RPM</div>
    <div class="live-value">{data['rpm']}<span class="live-unit">rpm</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {min(data['rpm']/35, 100)}%;"></div></div>
</div>

<div class="live-item">
    <div class="live-label">TEMP. MOTOR</div>
    <div class="live-value">{data['temp']}<span class="live-unit">°C</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {data['temp']}%;"></div></div>
</div>

<div class="live-item">
    <div class="live-label">PRESSÃO ÓLEO</div>
    <div class="live-value">{data['oil_pressure']}<span class="live-unit">bar</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {data['oil_pressure']*20}%;"></div></div>
</div>

<div class="live-item">
    <div class="live-label">SINAL O2</div>
    <div class="live-value">{data['o2']}<span class="live-unit">V</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {data['o2']*100}%;"></div></div>
</div>

<div class="live-item">
    <div class="live-label">VELOCIDADE</div>
    <div class="live-value">{data['speed']}<span class="live-unit">km/h</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {min(data['speed'], 100)}%;"></div></div>
</div>

<div class="live-item">
    <div class="live-label">TENSÃO BATERIA</div>
    <div class="live-value">{data['battery']}<span class="live-unit">V</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {(data['battery']-10)*25}%;"></div></div>
</div>

<div class="live-item">
    <div class="live-label">CARGA MOTOR</div>
    <div class="live-value">{data['engine_load']}<span class="live-unit">%</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {data['engine_load']}%;"></div></div>
</div>

<div class="live-item">
    <div class="live-label">AVANÇO IGNIÇÃO</div>
    <div class="live-value">{data['timing']}<span class="live-unit">°</span></div>
    <div class="live-graph"><div class="graph-fill" style="width: {data['timing']*4}%;"></div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Fecha left-panel

# =============================================
# RIGHT PANEL - Controles, Osciloscópio e Ferramentas
# =============================================
st.markdown('<div class="right-panel">', unsafe_allow_html=True)

# CONTROLES
st.markdown('<div class="panel-title">⚡ CONTROLES</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 ESCANEAR FALHAS", key="scan_btn"):
        with st.spinner("Escaneando sistemas..."):
            time.sleep(2)
            st.session_state.dtcs = [
                {'code': 'P0301', 'description': 'Falha de ignição no cilindro 1'},
                {'code': 'P0420', 'description': 'Catalisador ineficiente'},
                {'code': 'P0171', 'description': 'Mistura pobre'}
            ]
            st.session_state.log.append("> Escaneamento concluído")

with col2:
    if st.button("✅ LIMPAR FALHAS", key="clear_btn"):
        st.session_state.dtcs = []
        st.session_state.log.append("> Códigos de falha limpos")
        st.success("Códigos limpos com sucesso!")

col1, col2 = st.columns(2)
with col1:
    if st.button("📖 LER ECU", key="read_btn"):
        st.session_state.log.append("> Lendo ECU...")
        st.session_state.progress = 0
        for i in range(0, 101, 10):
            st.session_state.progress = i
            time.sleep(0.05)
        st.session_state.log.append("> Leitura concluída")

with col2:
    if st.button("💾 BACKUP", key="backup_btn"):
        st.session_state.log.append("> Fazendo backup...")
        st.session_state.progress = 0
        for i in range(0, 101, 10):
            st.session_state.progress = i
            time.sleep(0.05)
        st.session_state.log.append("> Backup concluído")

# Progress Bar
st.markdown(f"""
<div class="progress-bar">
    <div class="progress-fill" style="width: {st.session_state.progress}%;"></div>
    <div class="progress-text">{st.session_state.progress}%</div>
</div>
""", unsafe_allow_html=True)

# OSCILOSCÓPIO
st.markdown('<div class="panel-title" style="margin-top: 12px;">📊 OSCILOSCÓPIO</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ INICIAR", key="start_scope", use_container_width=True):
        st.session_state.osc_running = True
with col2:
    if st.button("⏹️ PARAR", key="stop_scope", use_container_width=True):
        st.session_state.osc_running = False

st.markdown("""
<div class="scope-channel">
    <div class="channel-header">
        <span class="channel-1">CH1 - SENSOR DETONAÇÃO</span>
        <span class="channel-1">0.45V</span>
    </div>
    <div class="waveform"><div class="wave-line"></div></div>
</div>

<div class="scope-channel">
    <div class="channel-header">
        <span class="channel-2">CH2 - BOMBA INJETORA</span>
        <span class="channel-2">12.4V</span>
    </div>
    <div class="waveform"><div class="wave-line wave-line2"></div></div>
</div>
""", unsafe_allow_html=True)

# FERRAMENTAS RÁPIDAS
st.markdown('<div class="panel-title" style="margin-top: 12px;">🔧 FERRAMENTAS RÁPIDAS</div>', unsafe_allow_html=True)

tools = ["Atuador Borboleta", "Teste Injetores", "Sangria ABS", "Reset Adaptações"]
cols = st.columns(2)
for i, tool in enumerate(tools):
    with cols[i % 2]:
        if st.button(tool, key=f"tool_{i}", use_container_width=True):
            st.session_state.log.append(f"> Executando: {tool}")

# ESTATÍSTICAS
st.markdown('<div class="panel-title" style="margin-top: 12px;">📊 ESTATÍSTICAS</div>', unsafe_allow_html=True)

stats = [
    ("Tempo de uso:", "00:00:00"),
    ("Picos de RPM:", f"{st.session_state.live_data['rpm']} rpm"),
    ("Temp. máxima:", f"{st.session_state.live_data['temp']} °C")
]

for label, value in stats:
    st.markdown(f"""
    <div class="info-row">
        <span class="info-label">{label}</span>
        <span class="info-value">{value}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Fecha right-panel
st.markdown('</div>', unsafe_allow_html=True)  # Fecha main-grid

# =============================================
# BOTTOM BAR
# =============================================
st.markdown("---")

last_log = st.session_state.log[-1] if st.session_state.log else "> Sistema pronto"
st.markdown(f"""
<div class="bottom-bar">
    <div class="log-messages">
        <span class="log-entry active">🔵 ONLINE</span>
        <span class="log-entry">🟡 KWP2000</span>
        <span class="log-entry">🟢 CAN BUS</span>
    </div>
    <div style="color: #888; font-size: 11px;">
        {last_log}
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================
# ATUALIZAÇÃO DE DADOS
# =============================================
if st.session_state.connected:
    st.session_state.live_data = {
        'rpm': random.randint(750, 3500),
        'speed': random.randint(0, 120),
        'temp': random.randint(82, 98),
        'oil_pressure': round(3.5 + random.random() * 1.5, 1),
        'battery': round(12 + random.random() * 2, 1),
        'engine_load': random.randint(15, 55),
        'o2': round(0.7 + random.random() * 0.2, 2),
        'timing': random.randint(8, 22)
    }
    
    time.sleep(0.5)
    st.rerun()
