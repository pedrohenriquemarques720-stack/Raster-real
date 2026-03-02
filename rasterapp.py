# app.py - Versão idêntica ao Raster 3S

import streamlit as st
import time
import random
import numpy as np
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Raster 3S Pro - Simulador Automotivo",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado - IDÊNTICO AO INDEX.HTML
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
        padding: 20px;
    }
    
    .main > .block-container {
        max-width: 1400px;
        margin: 0 auto;
        background: #2d2d2d;
        border-radius: 10px;
        padding: 20px !important;
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
    }
    
    /* Header com gradiente */
    .header {
        background: linear-gradient(135deg, #0047AB, #002B5C);
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-icon {
        font-size: 40px;
        filter: drop-shadow(0 0 10px rgba(0,255,255,0.5));
    }
    
    .logo-text h1 {
        font-size: 28px;
        font-weight: bold;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
    }
    
    .logo-text p {
        color: #00ffff;
        font-size: 12px;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .device-status {
        background: #000;
        padding: 10px 20px;
        border-radius: 30px;
        border: 1px solid #00ffff;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    
    /* Connection Bar */
    .connection-bar {
        background: #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        gap: 20px;
        align-items: center;
        border-left: 5px solid #ff6600;
    }
    
    .conn-info {
        display: flex;
        gap: 30px;
        flex: 1;
    }
    
    .conn-item {
        display: flex;
        flex-direction: column;
    }
    
    .conn-label {
        font-size: 12px;
        color: #888;
    }
    
    .conn-value {
        font-size: 16px;
        font-weight: bold;
        color: #ff6600;
        font-family: 'Courier New', monospace;
    }
    
    .conn-button {
        background: #00ff00;
        color: #000;
        padding: 10px 30px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }
    
    .conn-button:hover {
        background: #00cc00;
        transform: scale(1.05);
    }
    
    .conn-button.off {
        background: #ff0000;
        color: white;
    }
    
    /* Main Grid */
    .main-grid {
        display: grid;
        grid-template-columns: 300px 1fr 300px;
        gap: 20px;
        margin-top: 20px;
    }
    
    /* Panels */
    .panel {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 15px;
    }
    
    .panel-title {
        color: #ff6600;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 15px;
        padding-bottom: 5px;
        border-bottom: 2px solid #ff6600;
        text-transform: uppercase;
    }
    
    /* Vehicle Info */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #333;
    }
    
    .info-label {
        color: #888;
    }
    
    .info-value {
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    
    /* DTC List */
    .dtc-item {
        background: #330000;
        border-left: 3px solid #ff0000;
        padding: 10px;
        margin-bottom: 5px;
        font-family: 'Courier New', monospace;
    }
    
    .dtc-code {
        color: #ff6666;
        font-weight: bold;
    }
    
    .dtc-desc {
        font-size: 12px;
        color: #aaa;
    }
    
    /* Function Tabs */
    .function-tabs {
        display: flex;
        gap: 5px;
        margin-bottom: 20px;
        background: #333;
        padding: 5px;
        border-radius: 5px;
    }
    
    .tab {
        flex: 1;
        padding: 10px;
        text-align: center;
        cursor: pointer;
        border-radius: 5px;
        transition: 0.3s;
        font-size: 13px;
        background: #333;
        color: white;
    }
    
    .tab:hover {
        background: #444;
    }
    
    .tab.active {
        background: #ff6600;
        color: #000;
        font-weight: bold;
    }
    
    /* Live Data Grid */
    .live-data-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }
    
    .live-item {
        background: #333;
        padding: 15px;
        border-radius: 5px;
        border-left: 3px solid #00ff00;
    }
    
    .live-label {
        font-size: 12px;
        color: #888;
        margin-bottom: 5px;
    }
    
    .live-value {
        font-size: 24px;
        font-weight: bold;
        color: #00ff00;
    }
    
    .live-unit {
        font-size: 12px;
        color: #888;
        margin-left: 5px;
    }
    
    .live-graph {
        height: 4px;
        background: #444;
        margin-top: 10px;
        border-radius: 2px;
        overflow: hidden;
    }
    
    .graph-fill {
        height: 100%;
        background: #00ff00;
        width: 0%;
        transition: 0.3s;
    }
    
    /* Flashing Area */
    .flashing-area {
        text-align: center;
        padding: 20px;
    }
    
    .file-select {
        background: #333;
        padding: 30px;
        border-radius: 10px;
        border: 2px dashed #ff6600;
        cursor: pointer;
        margin-bottom: 20px;
    }
    
    .file-select:hover {
        background: #3a3a3a;
    }
    
    .progress-bar {
        height: 30px;
        background: #333;
        border-radius: 15px;
        overflow: hidden;
        margin: 20px 0;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff00, #00cc00);
        width: 0%;
        transition: 0.3s;
    }
    
    .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #000;
        font-weight: bold;
    }
    
    .flash-warning {
        color: #ff6600;
        font-size: 12px;
        margin-top: 10px;
        padding: 10px;
        background: #331900;
        border-radius: 5px;
    }
    
    /* Oscilloscope */
    .scope-channel {
        background: #000;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    .channel-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        font-size: 12px;
    }
    
    .channel-1 { color: #ffff00; }
    .channel-2 { color: #00ffff; }
    
    .waveform {
        height: 60px;
        background: #111;
        position: relative;
        overflow: hidden;
    }
    
    .wave-line {
        position: absolute;
        width: 100%;
        height: 2px;
        background: #ffff00;
        bottom: 30px;
        animation: wave 2s linear infinite;
    }
    
    .wave-line2 {
        background: #00ffff;
        bottom: 20px;
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
    
    /* Bottom Bar */
    .bottom-bar {
        margin-top: 20px;
        background: #1a1a1a;
        padding: 10px 15px;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #00ff00;
    }
    
    .log-messages {
        display: flex;
        gap: 20px;
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
    
    /* Fix para elementos Streamlit */
    .stButton > button {
        width: 100%;
        background-color: #ff6600;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        margin: 2px 0;
        border-radius: 5px;
    }
    
    .stButton > button:hover {
        background-color: #ff8533;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO DO ESTADO
# =============================================
if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.current_tab = 'live'
    st.session_state.osc_running = False
    st.session_state.rpm = 845
    st.session_state.speed = 0
    st.session_state.temp = 89
    st.session_state.oil_pressure = 4.2
    st.session_state.battery = 13.8
    st.session_state.engine_load = 23
    st.session_state.o2 = 0.78
    st.session_state.timing = 12
    st.session_state.progress = 0
    st.session_state.log = ["> Aguardando comando..."]

# =============================================
# HEADER
# =============================================
st.markdown("""
<div class="header">
    <div class="logo">
        <div class="logo-icon">🔧</div>
        <div class="logo-text">
            <h1>RASTER 3S PRO</h1>
            <p>TECNOMOTOR - DIAGNÓSTICO AUTOMOTIVO</p>
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
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(f"""
    <div class="connection-bar">
        <div class="conn-info">
            <div class="conn-item">
                <span class="conn-label">VEÍCULO</span>
                <span class="conn-value" id="vehicleName">VW GOL 1.6 2024</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">PROTOCOLO</span>
                <span class="conn-value">CAN-BUS 500K</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">ECU</span>
                <span class="conn-value">BOSCH ME17.9.65</span>
            </div>
            <div class="conn-item">
                <span class="conn-label">VERSÃO</span>
                <span class="conn-value">03H906023AB 3456</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🔌 CONECTAR" if not st.session_state.connected else "🔌 DESCONECTAR", key="connect_main"):
        st.session_state.connected = not st.session_state.connected
        if st.session_state.connected:
            st.session_state.log.append("> Conectado ao veículo")
        else:
            st.session_state.log.append("> Desconectado")
        st.rerun()

# =============================================
# MAIN GRID
# =============================================
col_left, col_center, col_right = st.columns([1.2, 2, 1.2])

# =============================================
# LEFT PANEL - Vehicle Info
# =============================================
with col_left:
    st.markdown('<div class="panel-title">📋 INFORMAÇÕES DO VEÍCULO</div>', unsafe_allow_html=True)
    
    info_data = [
        ("Fabricante:", "VOLKSWAGEN"),
        ("Modelo:", "GOL 1.6 MSI"),
        ("Ano:", "2024"),
        ("Motor:", "EA211 (16V)"),
        ("Câmbio:", "MQ200 (MANUAL)"),
        ("KM:", "15.234 km"),
        ("VIN:", "9BWZZZ377VT004251")
    ]
    
    for label, value in info_data:
        st.markdown(f"""
        <div class="info-row">
            <span class="info-label">{label}</span>
            <span class="info-value">{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="panel-title" style="margin-top: 20px;">⚠️ CÓDIGOS DE FALHA (DTC)</div>', unsafe_allow_html=True)
    
    dtcs = [
        ("P0301", "Falha de ignição no cilindro 1"),
        ("P0420", "Eficiência do catalisador abaixo do limite"),
        ("P0171", "Mistura pobre (banco 1)")
    ]
    
    for code, desc in dtcs:
        st.markdown(f"""
        <div class="dtc-item">
            <div class="dtc-code">{code}</div>
            <div class="dtc-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="panel-title" style="margin-top: 20px;">📊 ESTATÍSTICAS</div>', unsafe_allow_html=True)
    
    stats = [
        ("Tempo de uso:", "02:34:15"),
        ("Picos de RPM:", "6.850 rpm"),
        ("Temp. máxima:", "104 °C")
    ]
    
    for label, value in stats:
        st.markdown(f"""
        <div class="info-row">
            <span class="info-label">{label}</span>
            <span class="info-value">{value}</span>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# CENTER PANEL - Main Functions
# =============================================
with col_center:
    # Function Tabs
    tab1, tab2, tab3, tab4, tab5 = st.columns(5)
    
    with tab1:
        if st.button("📈 DADOS REAIS", key="tab_live", use_container_width=True):
            st.session_state.current_tab = 'live'
    
    with tab2:
        if st.button("🔍 DIAGNÓSTICO", key="tab_dtc", use_container_width=True):
            st.session_state.current_tab = 'dtc'
    
    with tab3:
        if st.button("⚡ FLASH/REPROGRAMAÇÃO", key="tab_flash", use_container_width=True):
            st.session_state.current_tab = 'flash'
    
    with tab4:
        if st.button("📊 OSCILOSCÓPIO", key="tab_scope", use_container_width=True):
            st.session_state.current_tab = 'scope'
    
    with tab5:
        if st.button("⚙️ CONFIGURAÇÕES", key="tab_config", use_container_width=True):
            st.session_state.current_tab = 'config'
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LIVE DATA TAB
    if st.session_state.current_tab == 'live':
        st.markdown('<div class="panel-title" style="margin-top: 0;">📊 DADOS EM TEMPO REAL</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # RPM
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">RPM</div>
                <div class="live-value">{st.session_state.rpm} <span class="live-unit">rpm</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.rpm/60}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Temperatura
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">TEMP. MOTOR</div>
                <div class="live-value">{st.session_state.temp} <span class="live-unit">°C</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.temp}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pressão Óleo
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">PRESSÃO ÓLEO</div>
                <div class="live-value">{st.session_state.oil_pressure} <span class="live-unit">bar</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.oil_pressure*20}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sinal O2
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">SINAL O2 (B1)</div>
                <div class="live-value">{st.session_state.o2} <span class="live-unit">V</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.o2*100}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Velocidade
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">VELOCIDADE</div>
                <div class="live-value">{st.session_state.speed} <span class="live-unit">km/h</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.speed}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tensão Bateria
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">TENSÃO BATERIA</div>
                <div class="live-value">{st.session_state.battery} <span class="live-unit">V</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.battery*6}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Carga Motor
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">CARGA MOTOR</div>
                <div class="live-value">{st.session_state.engine_load} <span class="live-unit">%</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.engine_load}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Avanço Ignição
            st.markdown(f"""
            <div class="live-item">
                <div class="live-label">AVANÇO IGNIÇÃO</div>
                <div class="live-value">{st.session_state.timing} <span class="live-unit">°</span></div>
                <div class="live-graph"><div class="graph-fill" style="width: {st.session_state.timing*4}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
    
    # FLASH TAB
    elif st.session_state.current_tab == 'flash':
        st.markdown('<div class="flashing-area">', unsafe_allow_html=True)
        
        # File select
        st.markdown("""
        <div class="file-select" onclick="alert('Selecionar arquivo...')">
            <div style="font-size: 40px; margin-bottom: 10px;">📂</div>
            <div style="color: #ff6600; font-weight: bold;">SELECIONE O ARQUIVO .BIN</div>
            <div style="color: #888; font-size: 12px; margin-top: 10px;">
                Arquivos suportados: .bin, .hex, .mot, .s19
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 LER ECU", key="read_ecu", use_container_width=True):
                st.session_state.log.append("> Lendo ECU...")
                st.session_state.progress = 0
        
        with col2:
            if st.button("💾 GRAVAR ECU", key="write_ecu", use_container_width=True):
                st.session_state.log.append("> Gravando ECU...")
                st.session_state.progress = 0
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ VERIFICAR", key="verify_ecu", use_container_width=True):
                st.session_state.log.append("> Verificação OK - Checksum válido")
        
        with col2:
            if st.button("💿 BACKUP", key="backup_ecu", use_container_width=True):
                st.session_state.log.append("> Fazendo backup...")
                st.session_state.progress = 0
        
        # Progress bar
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {st.session_state.progress}%;"></div>
            <div class="progress-text">{st.session_state.progress}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="flash-warning">
            ⚠️ ATENÇÃO: Não desligue o equipamento ou o veículo durante a gravação!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SCOPE TAB
    elif st.session_state.current_tab == 'scope':
        st.markdown('<div class="panel-title">📊 OSCILOSCÓPIO (2 CANAIS)</div>', unsafe_allow_html=True)
        
        # Scope controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("▶️ INICIAR", key="start_scope", use_container_width=True):
                st.session_state.osc_running = True
        with col2:
            if st.button("⏹️ PARAR", key="stop_scope", use_container_width=True):
                st.session_state.osc_running = False
        with col3:
            if st.button("💾 SALVAR", key="save_scope", use_container_width=True):
                st.session_state.log.append("> Forma de onda salva")
        
        # CH1
        st.markdown("""
        <div class="scope-channel">
            <div class="channel-header">
                <span class="channel-1">CH1 - SENSOR DE DETONAÇÃO</span>
                <span class="channel-1">0.45 V</span>
            </div>
            <div class="waveform">
                <div class="wave-line"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # CH2
        st.markdown("""
        <div class="scope-channel">
            <div class="channel-header">
                <span class="channel-2">CH2 - SINAL DA BOMBA INJETORA</span>
                <span class="channel-2">12.4 V</span>
            </div>
            <div class="waveform">
                <div class="wave-line wave-line2"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Scope settings
        st.markdown("""
        <div style="margin-top: 15px; background: #333; padding: 10px; border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; font-size: 12px;">
                <span>TIME/DIV: 10ms</span>
                <span>VOLTS/DIV: 2V</span>
                <span>TRIGGER: CH1</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# RIGHT PANEL - Oscilloscope & Tools
# =============================================
with col_right:
    st.markdown('<div class="panel-title">📊 OSCILOSCÓPIO (2 CANAIS)</div>', unsafe_allow_html=True)
    
    # Scope controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ INICIAR", key="start_scope_right", use_container_width=True):
            st.session_state.osc_running = True
    with col2:
        if st.button("⏹️ PARAR", key="stop_scope_right", use_container_width=True):
            st.session_state.osc_running = False
    
    # CH1
    st.markdown("""
    <div class="scope-channel">
        <div class="channel-header">
            <span class="channel-1">CH1 - SENSOR DE DETONAÇÃO</span>
            <span class="channel-1">0.45 V</span>
        </div>
        <div class="waveform">
            <div class="wave-line"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CH2
    st.markdown("""
    <div class="scope-channel">
        <div class="channel-header">
            <span class="channel-2">CH2 - SINAL DA BOMBA INJETORA</span>
            <span class="channel-2">12.4 V</span>
        </div>
        <div class="waveform">
            <div class="wave-line wave-line2"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick tools
    st.markdown('<div class="panel-title" style="margin-top: 20px;">🔧 FERRAMENTAS RÁPIDAS</div>', unsafe_allow_html=True)
    
    tools = ["Atuador de Borboleta", "Teste de Injetores", "Sangria de ABS", "Reset de Adaptações"]
    cols = st.columns(2)
    for i, tool in enumerate(tools):
        with cols[i % 2]:
            if st.button(tool, key=f"tool_{i}", use_container_width=True):
                st.session_state.log.append(f"> Executando: {tool}")

# =============================================
# BOTTOM BAR
# =============================================
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    last_log = st.session_state.log[-1] if st.session_state.log else "> Sistema pronto"
    st.markdown(f"""
    <div class="bottom-bar">
        <div class="log-messages">
            <span class="log-entry active">🔵 ONLINE</span>
            <span class="log-entry">🟡 KWP2000</span>
            <span class="log-entry">🟢 CAN BUS</span>
        </div>
        <div>
            Protocolo: ISO 15765-4 | Buffer: 512kb | Taxa: 500Kbps
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='color: #00ff00; font-family: Courier New; padding: 5px;'>{last_log}</div>", unsafe_allow_html=True)

# =============================================
# ATUALIZAÇÃO DE DADOS EM TEMPO REAL
# =============================================
if st.session_state.connected:
    # Atualiza dados com variação aleatória
    st.session_state.rpm = random.randint(750, 3500)
    st.session_state.speed = random.randint(0, 120)
    st.session_state.temp = random.randint(82, 98)
    st.session_state.oil_pressure = round(3.5 + random.random() * 1.5, 1)
    st.session_state.battery = round(12 + random.random() * 2, 1)
    st.session_state.engine_load = random.randint(15, 55)
    st.session_state.o2 = round(0.7 + random.random() * 0.2, 2)
    st.session_state.timing = random.randint(8, 22)
    
    # Atualiza progresso se estiver em flash
    if st.session_state.current_tab == 'flash' and st.session_state.progress < 100:
        st.session_state.progress += random.randint(1, 5)
        if st.session_state.progress >= 100:
            st.session_state.log.append("> Operação concluída com sucesso!")
    
    time.sleep(0.5)
    st.rerun()
