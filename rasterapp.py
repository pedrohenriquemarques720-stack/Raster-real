# app.py - Interface Original (Tudo na mesma tela, sem rolagem)

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
# CSS - INTERFACE ORIGINAL (SEM ROLAGEM)
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
        padding: 5px;
    }
    
    .main > .block-container {
        max-width: 100%;
        margin: 0;
        padding: 5px !important;
        background: #2d2d2d;
        border-radius: 8px;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #0047AB, #002B5C);
        padding: 8px 15px;
        border-radius: 6px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .logo-icon {
        font-size: 24px;
    }
    
    .logo-text h1 {
        font-size: 18px;
        font-weight: bold;
        color: #fff;
        margin: 0;
    }
    
    .logo-text p {
        color: #00ffff;
        font-size: 9px;
        margin: 0;
    }
    
    .device-status {
        background: #000;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid #00ffff;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 10px;
    }
    
    /* Connection Bar */
    .connection-bar {
        background: #1a1a1a;
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 8px;
        display: flex;
        gap: 10px;
        align-items: center;
        border-left: 4px solid #ff6600;
    }
    
    .conn-info {
        display: flex;
        gap: 15px;
        flex: 1;
    }
    
    .conn-item {
        display: flex;
        flex-direction: column;
    }
    
    .conn-label {
        font-size: 9px;
        color: #888;
    }
    
    .conn-value {
        font-size: 11px;
        font-weight: bold;
        color: #ff6600;
        font-family: 'Courier New', monospace;
    }
    
    .conn-button {
        background: #00ff00;
        color: #000;
        padding: 5px 15px;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        cursor: pointer;
        font-size: 11px;
        white-space: nowrap;
    }
    
    .conn-button.off {
        background: #ff0000;
        color: white;
    }
    
    /* MAIN GRID - 3 COLUNAS ORIGINAIS */
    .main-grid {
        display: grid;
        grid-template-columns: 300px 1fr 300px;
        gap: 8px;
        margin-top: 5px;
    }
    
    /* PANELS */
    .left-panel, .center-panel, .right-panel {
        background: #1a1a1a;
        border-radius: 6px;
        padding: 8px;
    }
    
    /* Panel Title */
    .panel-title {
        color: #ff6600;
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 6px;
        padding-bottom: 2px;
        border-bottom: 1px solid #ff6600;
        text-transform: uppercase;
    }
    
    /* Vehicle Info */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 3px 0;
        border-bottom: 1px solid #333;
        font-size: 10px;
    }
    
    .info-label {
        color: #888;
    }
    
    .info-value {
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    /* DTC List */
    .dtc-item {
        background: #330000;
        border-left: 2px solid #ff0000;
        padding: 5px;
        margin-bottom: 4px;
        font-size: 10px;
    }
    
    .dtc-code {
        color: #ff6666;
        font-weight: bold;
        font-size: 11px;
    }
    
    .dtc-desc {
        font-size: 9px;
        color: #aaa;
    }
    
    /* Function Tabs */
    .function-tabs {
        display: flex;
        gap: 3px;
        margin-bottom: 8px;
        background: #333;
        padding: 3px;
        border-radius: 4px;
    }
    
    .tab {
        flex: 1;
        padding: 4px 2px;
        text-align: center;
        border-radius: 3px;
        font-size: 9px;
        background: #333;
        color: white;
        border: none;
        white-space: nowrap;
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
        gap: 5px;
    }
    
    .live-item {
        background: #333;
        padding: 6px;
        border-radius: 4px;
        border-left: 2px solid #00ff00;
    }
    
    .live-label {
        font-size: 8px;
        color: #888;
        margin-bottom: 2px;
    }
    
    .live-value {
        font-size: 13px;
        font-weight: bold;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    
    .live-unit {
        font-size: 8px;
        color: #888;
        margin-left: 2px;
    }
    
    .live-graph {
        height: 2px;
        background: #444;
        margin-top: 4px;
        border-radius: 1px;
    }
    
    .graph-fill {
        height: 100%;
        background: #00ff00;
        width: 0%;
    }
    
    /* Flashing Area */
    .flashing-area {
        text-align: center;
        padding: 5px;
    }
    
    .file-select {
        background: #333;
        padding: 10px;
        border-radius: 5px;
        border: 1px dashed #ff6600;
        margin-bottom: 8px;
    }
    
    .progress-bar {
        height: 16px;
        background: #333;
        border-radius: 8px;
        margin: 8px 0;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff00, #00cc00);
        width: 0%;
        border-radius: 8px;
    }
    
    .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #000;
        font-weight: bold;
        font-size: 9px;
    }
    
    .flash-warning {
        color: #ff6600;
        font-size: 9px;
        padding: 5px;
        background: #331900;
        border-radius: 4px;
    }
    
    /* Oscilloscope */
    .scope-channel {
        background: #000;
        padding: 5px;
        border-radius: 4px;
        margin-bottom: 5px;
    }
    
    .channel-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 3px;
        font-size: 8px;
    }
    
    .channel-1 { color: #ffff00; }
    .channel-2 { color: #00ffff; }
    
    .waveform {
        height: 40px;
        background: #111;
        position: relative;
        overflow: hidden;
    }
    
    .wave-line {
        position: absolute;
        width: 100%;
        height: 1px;
        background: #ffff00;
        bottom: 20px;
        animation: wave 2s linear infinite;
    }
    
    .wave-line2 {
        background: #00ffff;
        bottom: 12px;
        animation: wave2 1.5s linear infinite;
    }
    
    @keyframes wave {
        0% { transform: translateX(0) translateY(0); }
        100% { transform: translateX(-100%) translateY(0); }
    }
    
    @keyframes wave2 {
        0% { transform: translateX(0) translateY(0); }
        100% { transform: translateX(-100%) translateY(0); }
    }
    
    /* Bottom Bar */
    .bottom-bar {
        margin-top: 8px;
        background: #1a1a1a;
        padding: 5px 10px;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        font-family: 'Courier New', monospace;
        font-size: 9px;
        color: #00ff00;
    }
    
    .log-messages {
        display: flex;
        gap: 10px;
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
        padding: 4px 6px !important;
        font-size: 9px !important;
        background-color: #ff6600 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 3px !important;
        margin: 1px 0 !important;
        min-height: 24px;
    }
    
    /* Colunas */
    div[data-testid="column"] {
        padding: 0 2px !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 2px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO
# =============================================
if 'scanner' not in st.session_state:
    st.session_state.scanner = OBDScannerPro()
    st.session_state.dtc_db = DTCDatabase()
    st.session_state.vehicle_db = VehicleDatabase()
    st.session_state.connected = False
    st.session_state.current_tab = 'live'
    st.session_state.osc_running = False
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
    st.session_state.log = ["> Sistema pronto"]

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
        <span>●</span> HARDWARE v2.45
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================
# CONNECTION BAR
# =============================================
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(f"""
    <div class="connection-bar">
        <div class="conn-info">
            <div class="conn-item">
                <span class="conn-label">VEÍCULO</span>
                <span class="conn-value">{st.session_state.vehicle_info.get('model', '---')}</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">PROTOCOLO</span>
                <span class="conn-value">{st.session_state.vehicle_info.get('protocol', '---')}</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">ECU</span>
                <span class="conn-value">{st.session_state.vehicle_info.get('ecu', '---')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🔌 CONECTAR" if not st.session_state.connected else "🔌 DESCONECTAR"):
        st.session_state.connected = not st.session_state.connected
        if st.session_state.connected:
            st.session_state.vehicle_info = {
                'manufacturer': 'Volkswagen',
                'model': 'Gol 1.6',
                'year': '2024',
                'engine': 'EA211',
                'transmission': 'Manual',
                'vin': '9BWZZZ377VT004251',
                'ecu': 'BOSCH ME17.9.65',
                'version': '03H906023AB',
                'protocol': 'CAN-BUS',
                'km': '15.234 km'
            }
            st.session_state.log.append("> Conectado")
        st.rerun()

# =============================================
# MAIN GRID - 3 COLUNAS (TUDO NA TELA)
# =============================================
col_left, col_center, col_right = st.columns([1, 1.5, 1])

# =============================================
# COLUNA ESQUERDA - Vehicle Info e DTCs
# =============================================
with col_left:
    st.markdown('<div class="panel-title">📋 INFORMAÇÕES</div>', unsafe_allow_html=True)
    
    info_items = [
        ("Fabricante:", st.session_state.vehicle_info.get('manufacturer')),
        ("Modelo:", st.session_state.vehicle_info.get('model')),
        ("Ano:", str(st.session_state.vehicle_info.get('year'))),
        ("Motor:", st.session_state.vehicle_info.get('engine')),
        ("VIN:", st.session_state.vehicle_info.get('vin')),
        ("KM:", st.session_state.vehicle_info.get('km'))
    ]
    
    for label, value in info_items:
        st.markdown(f"""
        <div class="info-row">
            <span class="info-label">{label}</span>
            <span class="info-value">{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="panel-title" style="margin-top: 8px;">⚠️ DTCs</div>', unsafe_allow_html=True)
    
    if st.button("🔍 ESCANEAR", key="scan_dtc", use_container_width=True):
        st.session_state.dtcs = [
            {'code': 'P0301', 'desc': 'Falha cilindro 1'},
            {'code': 'P0420', 'desc': 'Catalisador'}
        ]
        st.session_state.log.append("> Escaneado")
    
    if st.session_state.dtcs:
        for dtc in st.session_state.dtcs:
            st.markdown(f"""
            <div class="dtc-item">
                <div class="dtc-code">{dtc['code']}</div>
                <div class="dtc-desc">{dtc['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#666; font-size:9px; padding:5px;'>Nenhum código</div>", unsafe_allow_html=True)

# =============================================
# COLUNA CENTRAL - Dados em Tempo Real
# =============================================
with col_center:
    st.markdown('<div class="panel-title">📊 DADOS EM TEMPO REAL</div>', unsafe_allow_html=True)
    
    data = st.session_state.live_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="live-item">
            <div class="live-label">RPM</div>
            <div class="live-value">{data['rpm']}<span class="live-unit">rpm</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{min(data['rpm']/35,100)}%"></div></div>
        </div>
        <div class="live-item">
            <div class="live-label">TEMP. MOTOR</div>
            <div class="live-value">{data['temp']}<span class="live-unit">°C</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{data['temp']}%"></div></div>
        </div>
        <div class="live-item">
            <div class="live-label">PRESSÃO ÓLEO</div>
            <div class="live-value">{data['oil_pressure']}<span class="live-unit">bar</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{data['oil_pressure']*20}%"></div></div>
        </div>
        <div class="live-item">
            <div class="live-label">SINAL O2</div>
            <div class="live-value">{data['o2']}<span class="live-unit">V</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{data['o2']*100}%"></div></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="live-item">
            <div class="live-label">VELOCIDADE</div>
            <div class="live-value">{data['speed']}<span class="live-unit">km/h</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{min(data['speed'],100)}%"></div></div>
        </div>
        <div class="live-item">
            <div class="live-label">TENSÃO BATERIA</div>
            <div class="live-value">{data['battery']}<span class="live-unit">V</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{(data['battery']-10)*25}%"></div></div>
        </div>
        <div class="live-item">
            <div class="live-label">CARGA MOTOR</div>
            <div class="live-value">{data['engine_load']}<span class="live-unit">%</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{data['engine_load']}%"></div></div>
        </div>
        <div class="live-item">
            <div class="live-label">AVANÇO</div>
            <div class="live-value">{data['timing']}<span class="live-unit">°</span></div>
            <div class="live-graph"><div class="graph-fill" style="width:{data['timing']*4}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# COLUNA DIREITA - Controles e Osciloscópio
# =============================================
with col_right:
    st.markdown('<div class="panel-title">⚡ CONTROLES</div>', unsafe_allow_html=True)
    
    if st.button("✅ LIMPAR FALHAS", use_container_width=True):
        st.session_state.dtcs = []
        st.session_state.log.append("> Falhas limpas")
    
    st.markdown('<div class="panel-title" style="margin-top:8px;">📊 OSCILOSCÓPIO</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️", key="start_osc"):
            st.session_state.osc_running = True
    with col2:
        if st.button("⏹️", key="stop_osc"):
            st.session_state.osc_running = False
    
    st.markdown("""
    <div class="scope-channel">
        <div class="channel-header"><span class="channel-1">CH1</span><span class="channel-1">0.45V</span></div>
        <div class="waveform"><div class="wave-line"></div></div>
    </div>
    <div class="scope-channel">
        <div class="channel-header"><span class="channel-2">CH2</span><span class="channel-2">12.4V</span></div>
        <div class="waveform"><div class="wave-line wave-line2"></div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="panel-title" style="margin-top:8px;">🔧 FERRAMENTAS</div>', unsafe_allow_html=True)
    
    tools = ["Atuador", "Injetores", "ABS", "Reset"]
    cols = st.columns(2)
    for i, tool in enumerate(tools):
        with cols[i%2]:
            if st.button(tool, key=f"t{i}", use_container_width=True):
                st.session_state.log.append(f"> {tool}")

# =============================================
# BOTTOM BAR
# =============================================
st.markdown("---")
last_log = st.session_state.log[-1] if st.session_state.log else "> Pronto"
st.markdown(f"""
<div class="bottom-bar">
    <div class="log-messages">
        <span class="log-entry active">🔵 ONLINE</span>
        <span class="log-entry">🟡 CAN</span>
        <span class="log-entry">🟢 KWP</span>
    </div>
    <div>{last_log}</div>
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
