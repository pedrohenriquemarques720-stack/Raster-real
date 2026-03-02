# app.py - Interface Original (Tudo na mesma tela)

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
from co_piloto_oficina import CoPilotoOficina

# Configuração da página
st.set_page_config(
    page_title="AUTEL PRO - Diagnóstico Inteligente",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# CSS - INTERFACE ORIGINAL (TUDO NA MESMA TELA)
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
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #0047AB, #002B5C);
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo-icon {
        font-size: 32px;
    }
    
    .logo-text h1 {
        font-size: 22px;
        font-weight: bold;
        color: #fff;
        margin: 0;
    }
    
    .logo-text p {
        color: #00ffff;
        font-size: 10px;
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
    
    /* Connection Bar */
    .connection-bar {
        background: #1a1a1a;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
        display: flex;
        gap: 15px;
        align-items: center;
        border-left: 5px solid #ff6600;
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
        font-size: 13px;
        white-space: nowrap;
    }
    
    .conn-button.off {
        background: #ff0000;
        color: white;
    }
    
    /* MAIN GRID - 3 COLUNAS */
    .main-grid {
        display: grid;
        grid-template-columns: 300px 1fr 300px;
        gap: 10px;
        margin-top: 10px;
    }
    
    /* PANELS */
    .left-panel, .center-panel, .right-panel {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 12px;
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
    }
    
    /* DTC List */
    .dtc-item {
        background: #330000;
        border-left: 3px solid #ff0000;
        padding: 8px;
        margin-bottom: 5px;
        font-size: 12px;
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
        margin-bottom: 10px;
        background: #333;
        padding: 4px;
        border-radius: 5px;
    }
    
    .tab {
        flex: 1;
        padding: 6px 4px;
        text-align: center;
        border-radius: 4px;
        font-size: 11px;
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
        gap: 6px;
    }
    
    .live-item {
        background: #333;
        padding: 8px;
        border-radius: 5px;
        border-left: 3px solid #00ff00;
    }
    
    .live-label {
        font-size: 9px;
        color: #888;
        margin-bottom: 2px;
    }
    
    .live-value {
        font-size: 14px;
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
        height: 3px;
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
        padding: 8px;
    }
    
    .file-select {
        background: #333;
        padding: 12px;
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
        border-radius: 5px;
    }
    
    /* Oscilloscope */
    .scope-channel {
        background: #000;
        padding: 6px;
        border-radius: 5px;
        margin-bottom: 6px;
    }
    
    .channel-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 3px;
        font-size: 9px;
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
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    
    @keyframes wave2 {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    
    /* Bottom Bar */
    .bottom-bar {
        margin-top: 10px;
        background: #1a1a1a;
        padding: 6px 12px;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        font-family: 'Courier New', monospace;
        font-size: 10px;
        color: #00ff00;
    }
    
    .log-messages {
        display: flex;
        gap: 12px;
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
        padding: 5px 8px !important;
        font-size: 11px !important;
        background-color: #ff6600 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 4px !important;
        margin: 2px 0 !important;
        min-height: 28px;
    }
    
    /* Colunas */
    div[data-testid="column"] {
        padding: 0 3px !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 3px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO
# =============================================
if 'scanner' not in st.session_state:
    st.session_state.scanner = OBDScannerPro()
    st.session_state.copiloto = CoPilotoOficina()
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
        'timing': 12,
        'short_term_fuel_trim': 2.5,
        'long_term_fuel_trim': 3.2,
        'maf': 3.8
    }
    st.session_state.live_history = []
    st.session_state.log = ["> Sistema pronto"]
    st.session_state.diagnosis_result = None

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
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not st.session_state.connected:
        if st.button("🔌 CONECTAR"):
            with st.spinner("Conectando..."):
                st.session_state.connected = True
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
    else:
        if st.button("🔌 DESCONECTAR"):
            st.session_state.connected = False
            st.session_state.log.append("> Desconectado")
            st.rerun()

# =============================================
# MAIN GRID - 3 COLUNAS
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
    
    st.markdown('<div class="panel-title" style="margin-top: 10px;">⚠️ CÓDIGOS DE FALHA</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 ESCANEAR", key="scan_dtc", use_container_width=True):
            with st.spinner("Escaneando..."):
                time.sleep(1)
                st.session_state.dtcs = [
                    {'code': 'P0301', 'desc': 'Falha cilindro 1', 'system': 'Motor'},
                    {'code': 'P0420', 'desc': 'Catalisador', 'system': 'Emissões'},
                    {'code': 'P0171', 'desc': 'Mistura pobre', 'system': 'Combustível'}
                ]
                st.session_state.log.append("> Escaneamento concluído")
    
    with col2:
        if st.button("✅ LIMPAR", key="clear_dtc", use_container_width=True):
            st.session_state.dtcs = []
            st.session_state.log.append("> Falhas limpas")
    
    if st.session_state.dtcs:
        for dtc in st.session_state.dtcs:
            st.markdown(f"""
            <div class="dtc-item">
                <div class="dtc-code">{dtc['code']}</div>
                <div class="dtc-desc">{dtc['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#666; padding:5px;'>Nenhum código</div>", unsafe_allow_html=True)
    
    # Diagnóstico Rápido
    if st.session_state.dtcs:
        st.markdown('<div class="panel-title" style="margin-top: 10px;">🤖 CO-PILOTO IA</div>', unsafe_allow_html=True)
        
        if st.button("🔮 ANALISAR DTCs", use_container_width=True):
            with st.spinner("Analisando padrões..."):
                # Pega o primeiro DTC para diagnóstico
                dtc_atual = st.session_state.dtcs[0]['code']
                
                # Executa diagnóstico com IA
                resultado = st.session_state.copiloto.diagnose(
                    dtc_atual,
                    st.session_state.live_data,
                    st.session_state.live_history[-10:] if st.session_state.live_history else [],
                    st.session_state.vehicle_info
                )
                st.session_state.diagnosis_result = resultado
                st.session_state.log.append(f"> IA analisou {dtc_atual}")
        
        if st.session_state.diagnosis_result:
            res = st.session_state.diagnosis_result
            st.markdown(f"""
            <div style='background:#002800; padding:8px; border-radius:5px; margin-top:5px;'>
                <span style='color:#00ff00; font-weight:bold;'>🎯 PROBABILIDADES:</span>
            """, unsafe_allow_html=True)
            
            for p in res['probabilities'][:2]:
                st.markdown(f"<div style='font-size:11px; margin:3px 0;'>• {p['component']}: {p['probability']}%</div>", unsafe_allow_html=True)
            
            if res['final_recommendation']['action_plan']:
                st.markdown(f"<div style='color:#ff6600; font-size:11px; margin-top:5px;'>{res['final_recommendation']['action_plan'][0]}</div>", unsafe_allow_html=True)

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
    
    # Parâmetros adicionais para diagnóstico
    if st.session_state.connected:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("STFT", f"{data.get('short_term_fuel_trim', 0)}%", delta=None)
        with col2:
            st.metric("LTFT", f"{data.get('long_term_fuel_trim', 0)}%", delta=None)

# =============================================
# COLUNA DIREITA - Osciloscópio e Controles
# =============================================
with col_right:
    st.markdown('<div class="panel-title">⚡ CONTROLES</div>', unsafe_allow_html=True)
    
    # Flash / Reprogramação
    if st.button("⚡ FLASH ECU", use_container_width=True):
        st.session_state.log.append("> Iniciando flash...")
        st.session_state.progress = 0
        progress_bar = st.progress(0)
        for i in range(0, 101, 10):
            st.session_state.progress = i
            progress_bar.progress(i/100)
            time.sleep(0.1)
        st.session_state.log.append("> Flash concluído")
        st.rerun()
    
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width:{st.session_state.progress}%"></div>
        <div class="progress-text">{st.session_state.progress}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Osciloscópio
    st.markdown('<div class="panel-title" style="margin-top:10px;">📊 OSCILOSCÓPIO</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ INICIAR", key="start_osc"):
            st.session_state.osc_running = True
    with col2:
        if st.button("⏹️ PARAR", key="stop_osc"):
            st.session_state.osc_running = False
    
    st.markdown("""
    <div class="scope-channel">
        <div class="channel-header">
            <span class="channel-1">CH1 - DETONAÇÃO</span>
            <span class="channel-1">0.45V</span>
        </div>
        <div class="waveform"><div class="wave-line"></div></div>
    </div>
    <div class="scope-channel">
        <div class="channel-header">
            <span class="channel-2">CH2 - INJEÇÃO</span>
            <span class="channel-2">12.4V</span>
        </div>
        <div class="waveform"><div class="wave-line wave-line2"></div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ferramentas Rápidas
    st.markdown('<div class="panel-title" style="margin-top:10px;">🔧 FERRAMENTAS</div>', unsafe_allow_html=True)
    
    tools = ["Atuador", "Injetores", "Sangria", "Reset"]
    cols = st.columns(2)
    for i, tool in enumerate(tools):
        with cols[i%2]:
            if st.button(tool, key=f"tool_{i}", use_container_width=True):
                st.session_state.log.append(f"> Executando: {tool}")

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
    # Atualiza dados
    novo_dado = {
        'rpm': random.randint(750, 3500),
        'speed': random.randint(0, 120),
        'temp': random.randint(82, 98),
        'oil_pressure': round(3.5 + random.random() * 1.5, 1),
        'battery': round(12 + random.random() * 2, 1),
        'engine_load': random.randint(15, 55),
        'o2': round(0.7 + random.random() * 0.2, 2),
        'timing': random.randint(8, 22),
        'short_term_fuel_trim': round(random.uniform(-5, 15), 1),
        'long_term_fuel_trim': round(random.uniform(-8, 18), 1),
        'maf': round(2.5 + random.random() * 3, 1)
    }
    
    st.session_state.live_data = novo_dado
    st.session_state.live_history.append(novo_dado)
    if len(st.session_state.live_history) > 50:
        st.session_state.live_history.pop(0)
    
    time.sleep(0.5)
    st.rerun()
