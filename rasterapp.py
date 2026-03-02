# app.py - Interface Completa com Controle Ativo do Motor

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
from sgw_autopass import SGWAutoPass
from visualizacao_3d import Visualizador3D
from orcamento_automatico import OrcamentoAutomatico
from ecu_control import ECUControl, ProtocolType, create_tuning_interface

# Configuração da página
st.set_page_config(
    page_title="AUTEL PRO - Scanner Inteligente",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# CSS - NOVA INTERFACE MODERNA
# =============================================
st.markdown("""
<style>
    /* Reset e estilos globais */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', 'Roboto Mono', 'Arial', sans-serif;
    }

    .stApp {
        background: #0a0c10;
        color: #ffffff;
        padding: 0px;
    }
    
    .main > .block-container {
        max-width: 100%;
        margin: 0;
        padding: 0px !important;
        background: #0a0c10;
    }
    
    /* Header Neon */
    .header-neon {
        background: linear-gradient(135deg, #0a0c10, #001a33);
        padding: 15px 25px;
        border-bottom: 2px solid #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    .logo-neon {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-icon {
        font-size: 40px;
        color: #00ffff;
        text-shadow: 0 0 20px #00ffff;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; text-shadow: 0 0 20px #00ffff; }
        50% { opacity: 0.8; text-shadow: 0 0 40px #00ffff; }
        100% { opacity: 1; text-shadow: 0 0 20px #00ffff; }
    }
    
    .logo-text h1 {
        font-size: 24px;
        font-weight: bold;
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff;
        margin: 0;
        font-family: 'Roboto Mono', monospace;
        letter-spacing: 3px;
    }
    
    .logo-text p {
        color: #4d4d4d;
        font-size: 11px;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .status-neon {
        background: #000000;
        padding: 8px 20px;
        border-radius: 30px;
        border: 1px solid #00ffff;
        color: #00ff00;
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
    }
    
    /* Connection Bar */
    .connection-bar-modern {
        background: #1a1d24;
        padding: 15px 25px;
        border-radius: 12px;
        margin: 0 20px 20px 20px;
        display: flex;
        gap: 20px;
        align-items: center;
        border-left: 5px solid #00ffff;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
    }
    
    .conn-info-modern {
        display: flex;
        gap: 30px;
        flex: 1;
    }
    
    .conn-item-modern {
        display: flex;
        flex-direction: column;
    }
    
    .conn-label-modern {
        font-size: 10px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .conn-value-modern {
        font-size: 14px;
        font-weight: bold;
        color: #00ffff;
        font-family: 'Roboto Mono', monospace;
    }
    
    .conn-button-neon {
        background: linear-gradient(135deg, #00ff00, #00cc00);
        color: #000;
        padding: 10px 30px;
        border: none;
        border-radius: 30px;
        font-weight: bold;
        cursor: pointer;
        font-size: 13px;
        white-space: nowrap;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
        transition: 0.3s;
    }
    
    .conn-button-neon:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.8);
    }
    
    .conn-button-neon.off {
        background: linear-gradient(135deg, #ff0000, #cc0000);
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        color: white;
    }
    
    /* Menu de Navegação com Botões */
    .nav-menu-buttons {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin: 0 20px 20px 20px;
        flex-wrap: wrap;
    }
    
    .nav-button {
        background: #1a1d24;
        color: #888;
        padding: 10px 20px;
        border-radius: 30px;
        border: 1px solid #333;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .nav-button:hover {
        border-color: #00ffff;
        color: #00ffff;
    }
    
    .nav-button.active {
        background: #00ffff;
        color: black;
        border-color: #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    /* Círculo de Saúde */
    .health-circle-container {
        position: relative;
        width: 250px;
        height: 250px;
        margin: 0 auto;
    }
    
    .health-circle {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: conic-gradient(
            from 0deg,
            #00ff00 0deg,
            #ffff00 180deg,
            #ff0000 360deg
        );
        mask: radial-gradient(circle at center, transparent 70%, black 71%);
        -webkit-mask: radial-gradient(circle at center, transparent 70%, black 71%);
        animation: pulse-glow 2s infinite;
    }
    
    @keyframes pulse-glow {
        0% { filter: drop-shadow(0 0 10px #00ffff); }
        50% { filter: drop-shadow(0 0 30px #00ffff); }
        100% { filter: drop-shadow(0 0 10px #00ffff); }
    }
    
    .health-value {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    
    .health-value span {
        font-size: 42px;
        font-weight: bold;
        color: white;
        text-shadow: 0 0 20px #00ffff;
        font-family: 'Roboto Mono', monospace;
    }
    
    .health-label {
        font-size: 12px;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Cards de Sistema */
    .system-card {
        background: #1a1d24;
        border-radius: 10px;
        padding: 12px;
        margin: 5px 0;
        border-left: 3px solid #333;
        transition: 0.3s;
        cursor: pointer;
    }
    
    .system-card:hover {
        transform: translateX(5px);
        border-left-color: #00ffff;
    }
    
    .system-card.warning {
        border-left-color: #ffaa00;
        background: #332200;
    }
    
    .system-card.critical {
        border-left-color: #ff0000;
        background: #330000;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .system-name {
        font-size: 11px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .system-value {
        font-size: 16px;
        font-weight: bold;
        font-family: 'Roboto Mono', monospace;
    }
    
    .dtc-code {
        font-size: 14px;
        font-weight: bold;
        color: #ff6666;
        font-family: 'Roboto Mono', monospace;
    }
    
    /* Cards do Co-Piloto */
    .copilot-card-modern {
        background: linear-gradient(135deg, #001a33, #002244);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
    
    .copilot-title-modern {
        color: #00ffff;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 10px;
        font-family: 'Roboto Mono', monospace;
        letter-spacing: 1px;
    }
    
    .probability-bar {
        height: 6px;
        background: #333;
        border-radius: 3px;
        margin: 8px 0;
        overflow: hidden;
    }
    
    .probability-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff00, #ffff00, #ff0000);
        border-radius: 3px;
        transition: width 0.5s;
    }
    
    /* Visualizador 3D */
    .viewer-3d {
        background: #111;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #00ffff;
        height: 450px;
        position: relative;
        overflow: hidden;
    }
    
    .engine-3d {
        width: 100%;
        height: 100%;
        background: #222;
        border-radius: 8px;
        position: relative;
    }
    
    .control-btn-3d {
        background: #1a1d24;
        color: #00ffff;
        border: 1px solid #00ffff;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 12px;
        cursor: pointer;
        margin: 5px;
        transition: 0.3s;
    }
    
    .control-btn-3d:hover {
        background: #00ffff;
        color: black;
    }
    
    /* Modo Cliente */
    .cliente-card {
        background: #1a1d24;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #00ffff;
    }
    
    .severidade-bar {
        height: 30px;
        border-radius: 15px;
        background: linear-gradient(90deg, #00ff00, #ffff00, #ff0000);
        margin: 10px 0;
        position: relative;
    }
    
    .severidade-indicator {
        height: 30px;
        background: white;
        border-radius: 15px;
        width: 0%;
        mix-blend-mode: overlay;
        transition: width 0.5s;
    }
    
    .assinatura-area {
        border: 2px dashed #00ffff;
        border-radius: 10px;
        height: 120px;
        margin: 10px 0;
        cursor: crosshair;
        background: #000;
        position: relative;
    }
    
    /* Estatísticas */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin: 10px 0;
    }
    
    .stat-item {
        background: #1a1d24;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #333;
    }
    
    .stat-value {
        font-size: 26px;
        font-weight: bold;
        color: #00ffff;
        font-family: 'Roboto Mono', monospace;
    }
    
    .stat-label {
        font-size: 10px;
        color: #888;
        text-transform: uppercase;
    }
    
    /* Gráfico Simples */
    .chart-simple {
        background: #1a1d24;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        height: 150px;
        position: relative;
        overflow: hidden;
    }
    
    .chart-line {
        position: absolute;
        bottom: 20px;
        left: 0;
        width: 100%;
        height: 2px;
        background: #00ffff;
        animation: moveLine 3s linear infinite;
    }
    
    @keyframes moveLine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Controle Ativo - Sliders e Indicadores */
    .tuning-card {
        background: #1a1d24;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #00ffff;
    }
    
    .safety-ok {
        background: #004400;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #00ff00;
        margin-bottom: 15px;
    }
    
    .safety-blocked {
        background: #440000;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #ff0000;
        margin-bottom: 15px;
        animation: pulse-red 1s infinite;
    }
    
    @keyframes pulse-red {
        0% { opacity: 1; }
        50% { opacity: 0.8; background: #660000; }
        100% { opacity: 1; }
    }
    
    .metric-box {
        background: #000;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #00ffff;
    }
    
    .metric-title {
        color: #888;
        font-size: 11px;
        text-transform: uppercase;
    }
    
    .metric-number {
        color: #00ffff;
        font-size: 24px;
        font-weight: bold;
        font-family: 'Roboto Mono', monospace;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Botões */
    .stButton > button {
        width: 100%;
        padding: 10px !important;
        font-size: 12px !important;
        background: linear-gradient(135deg, #00ffff, #0088ff) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 30px !important;
        margin: 2px 0 !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5) !important;
        transition: 0.3s !important;
        font-family: 'Roboto Mono', monospace !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.8) !important;
    }
    
    /* Colunas */
    div[data-testid="column"] {
        padding: 0 5px !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 5px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO
# =============================================
if 'scanner' not in st.session_state:
    st.session_state.scanner = OBDScannerPro()
    st.session_state.copiloto = CoPilotoOficina()
    st.session_state.sgw = SGWAutoPass()
    st.session_state.visualizador = Visualizador3D()
    st.session_state.orcamento = OrcamentoAutomatico()
    st.session_state.ecu_control = ECUControl(
        protocol=ProtocolType.CAN_11BIT,
        manufacturer="VOLKSWAGEN",
        use_simulator=True  # Use False para CAN real
    )
    st.session_state.dtc_db = DTCDatabase()
    st.session_state.vehicle_db = VehicleDatabase()
    st.session_state.connected = False
    st.session_state.sgw_unlocked = False
    st.session_state.current_page = "Dashboard"
    st.session_state.progress = 0
    st.session_state.vehicle_info = {
        'manufacturer': '---',
        'model': '---',
        'year': '---',
        'engine': '---',
        'transmission': '---',
        'vin': '9BWZZZ377VT004251',
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
    st.session_state.selected_component = None
    st.session_state.modo_cliente = False
    st.session_state.assinatura = False
    st.session_state.orcamento_atual = None
    st.session_state.tuning_results = None

# =============================================
# HEADER NEON
# =============================================
sgw_status = "DESBLOQUEADO" if st.session_state.sgw_unlocked else "BLOQUEADO"
sgw_color = "#00ff00" if st.session_state.sgw_unlocked else "#ff0000"

st.markdown(f"""
<div class="header-neon">
    <div class="logo-neon">
        <div class="logo-icon">🔧</div>
        <div class="logo-text">
            <h1>AUTEL PRO</h1>
            <p>SCANNER INTELIGENTE</p>
        </div>
    </div>
    <div class="status-neon">
        <span style="color: {sgw_color};">●</span> SGW: {sgw_status} • SN: TM20250301
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================
# CONNECTION BAR MODERNA
# =============================================
col1, col2 = st.columns([4, 1])

with col1:
    vehicle_display = f"{st.session_state.vehicle_info.get('model', '---')} {st.session_state.vehicle_info.get('year', '')}"
    protocol_display = st.session_state.vehicle_info.get('protocol', '---')
    ecu_display = st.session_state.vehicle_info.get('ecu', '---')
    version_display = st.session_state.vehicle_info.get('version', '---')
    
    st.markdown(f"""
    <div class="connection-bar-modern">
        <div class="conn-info-modern">
            <div class="conn-item-modern">
                <span class="conn-label-modern">VEÍCULO</span>
                <span class="conn-value-modern">{vehicle_display}</span>
            </div>
            <div class="conn-item-modern">
                <span class="conn-label-modern">PROTOCOLO</span>
                <span class="conn-value-modern">{protocol_display}</span>
            </div>
            <div class="conn-item-modern">
                <span class="conn-label-modern">ECU</span>
                <span class="conn-value-modern">{ecu_display}</span>
            </div>
            <div class="conn-item-modern">
                <span class="conn-label-modern">VERSÃO</span>
                <span class="conn-value-modern">{version_display}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not st.session_state.connected:
        if st.button("🔌 CONECTAR", key="connect_btn"):
            with st.spinner("Conectando ao veículo..."):
                time.sleep(1.5)
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
                    'protocol': 'CAN-BUS 500K',
                    'km': '15.234 km'
                }
                
                # Atualiza dados no ECU control
                st.session_state.ecu_control.live_data['rpm'] = st.session_state.live_data['rpm']
                st.session_state.ecu_control.live_data['coolant_temp'] = st.session_state.live_data['temp']
                st.session_state.ecu_control.live_data['speed'] = st.session_state.live_data['speed']
                st.session_state.ecu_control.live_data['o2_voltage'] = st.session_state.live_data['o2']
                st.session_state.ecu_control.live_data['stft'] = st.session_state.live_data['short_term_fuel_trim']
                st.session_state.ecu_control.live_data['ltft'] = st.session_state.live_data['long_term_fuel_trim']
                
                st.session_state.log.append("> Conectado ao veículo")
                st.rerun()
    else:
        if st.button("🔌 DESCONECTAR", key="disconnect_btn"):
            st.session_state.connected = False
            st.session_state.sgw_unlocked = False
            st.session_state.dtcs = []
            st.session_state.diagnosis_result = None
            st.session_state.tuning_results = None
            st.session_state.log.append("> Desconectado")
            st.rerun()

# =============================================
# SGW AUTO-PASS
# =============================================
if st.session_state.connected and not st.session_state.sgw_unlocked:
    with st.spinner("🔄 Desbloqueando Security Gateway..."):
        time.sleep(2)
        st.session_state.sgw_unlocked = True
        st.session_state.log.append("✅ SGW desbloqueado com sucesso")
        st.balloons()

# =============================================
# MENU DE NAVEGAÇÃO COM BOTÕES SIMPLES
# =============================================
st.markdown('<div class="nav-menu-buttons">', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    active_class = "active" if st.session_state.current_page == "Dashboard" else ""
    if st.button("📊 DASHBOARD", key="nav_dash"):
        st.session_state.current_page = "Dashboard"
        st.rerun()

with col2:
    active_class = "active" if st.session_state.current_page == "Controle Ativo" else ""
    if st.button("⚡ CONTROLE ATIVO", key="nav_tuning"):
        st.session_state.current_page = "Controle Ativo"
        st.rerun()

with col3:
    active_class = "active" if st.session_state.current_page == "Visualizador 3D" else ""
    if st.button("🔍 VISUALIZADOR 3D", key="nav_3d"):
        st.session_state.current_page = "Visualizador 3D"
        st.rerun()

with col4:
    active_class = "active" if st.session_state.current_page == "Modo Cliente" else ""
    if st.button("👤 MODO CLIENTE", key="nav_cliente"):
        st.session_state.current_page = "Modo Cliente"
        st.rerun()

with col5:
    active_class = "active" if st.session_state.current_page == "Diagnóstico IA" else ""
    if st.button("🤖 DIAGNÓSTICO IA", key="nav_ia"):
        st.session_state.current_page = "Diagnóstico IA"
        st.rerun()

with col6:
    active_class = "active" if st.session_state.current_page == "Orçamentos" else ""
    if st.button("💰 ORÇAMENTOS", key="nav_orc"):
        st.session_state.current_page = "Orçamentos"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# ATUALIZA ECU_CONTROL COM DADOS AO VIVO
# =============================================
if st.session_state.connected:
    st.session_state.ecu_control.live_data['rpm'] = st.session_state.live_data['rpm']
    st.session_state.ecu_control.live_data['coolant_temp'] = st.session_state.live_data['temp']
    st.session_state.ecu_control.live_data['speed'] = st.session_state.live_data['speed']
    st.session_state.ecu_control.live_data['o2_voltage'] = st.session_state.live_data['o2']
    st.session_state.ecu_control.live_data['stft'] = st.session_state.live_data['short_term_fuel_trim']
    st.session_state.ecu_control.live_data['ltft'] = st.session_state.live_data['long_term_fuel_trim']
    st.session_state.ecu_control.live_data['lambda'] = st.session_state.live_data.get('lambda', 1.0)

# =============================================
# CONTEÚDO BASEADO NA PÁGINA SELECIONADA
# =============================================

# DASHBOARD
if st.session_state.current_page == "Dashboard":
    st.markdown("## 🎯 PAINEL DE DIAGNÓSTICO")
    
    col1, col2, col3 = st.columns([1.2, 2, 1.2])
    
    # COLUNA ESQUERDA - Círculo de Saúde
    with col1:
        st.markdown("### 🩺 SAÚDE DO VEÍCULO")
        
        total_falhas = len(st.session_state.dtcs)
        severidade_total = sum(1 for dtc in st.session_state.dtcs if dtc.get('severity') == 'critical') * 15
        severidade_total += sum(1 for dtc in st.session_state.dtcs if dtc.get('severity') == 'warning') * 8
        saude = max(0, min(100, 100 - severidade_total))
        
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <div class="health-circle-container">
                <div class="health-circle" style="background: conic-gradient(
                    from 0deg,
                    #00ff00 0deg,
                    #ffff00 {saude * 3.6}deg,
                    #ff0000 360deg
                );"></div>
                <div class="health-value">
                    <span>{saude}%</span>
                    <div class="health-label">SAUDÁVEL</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="stat-grid">', unsafe_allow_html=True)
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value">{len(st.session_state.dtcs)}</div>
                <div class="stat-label">FALHAS</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stat2:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value">45</div>
                <div class="stat-label">ECUs</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # COLUNA CENTRAL - Dados em Tempo Real
    with col2:
        st.markdown("### 📊 DADOS EM TEMPO REAL")
        
        data = st.session_state.live_data
        
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1:
            st.markdown(f"""
            <div class="system-card">
                <div class="system-name">RPM</div>
                <div class="system-value">{data['rpm']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_d2:
            st.markdown(f"""
            <div class="system-card">
                <div class="system-name">TEMP</div>
                <div class="system-value">{data['temp']}°C</div>
            </div>
            """, unsafe_allow_html=True)
        with col_d3:
            carga_class = "critical" if data['engine_load'] > 70 else "warning" if data['engine_load'] > 40 else ""
            st.markdown(f"""
            <div class="system-card {carga_class}">
                <div class="system-name">CARGA</div>
                <div class="system-value">{data['engine_load']}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_d4:
            st.markdown(f"""
            <div class="system-card">
                <div class="system-name">BATERIA</div>
                <div class="system-value">{data['battery']}V</div>
            </div>
            """, unsafe_allow_html=True)
        
        col_extra1, col_extra2, col_extra3 = st.columns(3)
        with col_extra1:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:8px; border-radius:5px; text-align:center;">
                <div style="color:#888; font-size:10px;">STFT</div>
                <div style="color:#00ffff; font-size:14px;">{data.get('short_term_fuel_trim', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_extra2:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:8px; border-radius:5px; text-align:center;">
                <div style="color:#888; font-size:10px;">LTFT</div>
                <div style="color:#00ffff; font-size:14px;">{data.get('long_term_fuel_trim', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_extra3:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:8px; border-radius:5px; text-align:center;">
                <div style="color:#888; font-size:10px;">MAF</div>
                <div style="color:#00ffff; font-size:14px;">{data.get('maf', 0)} g/s</div>
            </div>
            """, unsafe_allow_html=True)
    
    # COLUNA DIREITA - DTCs
    with col3:
        st.markdown("### ⚠️ CÓDIGOS DE FALHA")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔍 ESCANEAR", key="scan_dtc", use_container_width=True):
                with st.spinner("Escaneando sistemas..."):
                    time.sleep(2)
                    st.session_state.dtcs = [
                        {'code': 'P0301', 'desc': 'Falha de ignição no cilindro 1', 'system': 'Motor', 'severity': 'critical'},
                        {'code': 'P0420', 'desc': 'Eficiência do catalisador abaixo do limite', 'system': 'Emissões', 'severity': 'warning'},
                        {'code': 'P0171', 'desc': 'Mistura pobre (banco 1)', 'system': 'Combustível', 'severity': 'warning'}
                    ]
                    st.session_state.log.append("> Escaneamento concluído")
        
        with col_btn2:
            if st.button("✅ LIMPAR", key="clear_dtc", use_container_width=True):
                st.session_state.dtcs = []
                st.session_state.diagnosis_result = None
                st.session_state.log.append("> Códigos limpos")
                st.success("Códigos limpos com sucesso!")
        
        if st.session_state.dtcs:
            for i, dtc in enumerate(st.session_state.dtcs):
                status_class = "critical" if dtc['severity'] == 'critical' else "warning" if dtc['severity'] == 'warning' else ""
                
                with st.container():
                    st.markdown(f"""
                    <div class="system-card {status_class}">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="system-name">{dtc['system']}</span>
                            <span class="dtc-code">{dtc['code']}</span>
                        </div>
                        <div style="font-size:11px; color:#ccc; margin-top:5px;">{dtc['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🔮 ANALISAR", key=f"analyze_{i}", use_container_width=True):
                        with st.spinner("IA analisando dados..."):
                            time.sleep(2)
                            live_data_for_ia = {
                                'short_term_fuel_trim': st.session_state.live_data.get('short_term_fuel_trim', 0),
                                'long_term_fuel_trim': st.session_state.live_data.get('long_term_fuel_trim', 0),
                                'o2_voltage': st.session_state.live_data.get('o2', 0),
                                'maf': st.session_state.live_data.get('maf', 0),
                                'rpm': st.session_state.live_data.get('rpm', 0)
                            }
                            
                            resultado = st.session_state.copiloto.diagnose(
                                dtc['code'],
                                live_data_for_ia,
                                st.session_state.live_history[-10:] if st.session_state.live_history else [],
                                st.session_state.vehicle_info
                            )
                            st.session_state.diagnosis_result = resultado
                            st.session_state.selected_component = resultado['probabilities'][0]['component'] if resultado['probabilities'] else None
                            st.rerun()
        else:
            st.markdown("""
            <div style="background:#1a1d24; padding:20px; border-radius:10px; text-align:center; color:#666;">
                Nenhum código de falha encontrado
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.diagnosis_result:
            res = st.session_state.diagnosis_result
            st.markdown('<div class="copilot-card-modern">', unsafe_allow_html=True)
            st.markdown(f'<div class="copilot-title-modern">🎯 DIAGNÓSTICO IA - {res["dtc"]}</div>', unsafe_allow_html=True)
            
            for p in res['probabilities'][:2]:
                prob = p['probability']
                cor = "#00ff00" if prob > 70 else "#ffff00" if prob > 40 else "#ff0000"
                
                st.markdown(f"""
                <div style="margin:10px 0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
                        <span style="font-size:12px;">{p['component']}</span>
                        <span style="color:{cor}; font-weight:bold; font-size:12px;">{prob}%</span>
                    </div>
                    <div class="probability-bar">
                        <div class="probability-fill" style="width:{prob}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# CONTROLE ATIVO (TUNING)
# =============================================
elif st.session_state.current_page == "Controle Ativo":
    st.markdown("## ⚡ CONTROLE ATIVO DO MOTOR")
    st.markdown("### Ajuste de Parâmetros em Tempo Real (UDS Service 0x2E)")
    
    # Verifica se está conectado
    if not st.session_state.connected:
        st.warning("⚠️ Conecte-se a um veículo para usar o Controle Ativo")
    else:
        # Status de segurança
        safety = st.session_state.ecu_control.check_safety_conditions()
        
        if not safety.safe:
            st.markdown(f"""
            <div class="safety-blocked">
                <span style="color:#ff0000; font-weight:bold;">⛔ BLOQUEADO POR SEGURANÇA</span><br>
                <span style="color:#ff6666;">{safety.reason}</span><br>
                <span style="color:#888; font-size:11px;">RPM: {safety.rpm} | Temp: {safety.temp}°C | Vel: {safety.speed} km/h</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safety-ok">
                <span style="color:#00ff00; font-weight:bold;">✅ CONDIÇÕES DE SEGURANÇA OK</span><br>
                <span style="color:#888; font-size:11px;">RPM: {safety.rpm} | Temp: {safety.temp}°C | Vel: {safety.speed} km/h</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Métricas em tempo real
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">RPM ATUAL</div>
                <div class="metric-number">{st.session_state.live_data['rpm']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">TEMP MOTOR</div>
                <div class="metric-number">{st.session_state.live_data['temp']}°C</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">LAMBDA</div>
                <div class="metric-number">{st.session_state.ecu_control.live_data.get('lambda', 1.02):.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">SONDA O2</div>
                <div class="metric-number">{st.session_state.live_data['o2']:.3f}V</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Interface de tuning principal
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("### 🔧 Ajustes Manuais")
            
            # Ajuste de Mistura (Fuel Trim)
            fuel_trim = st.slider(
                "Ajuste de Mistura (Fuel Trim)",
                min_value=-25.0,
                max_value=25.0,
                value=st.session_state.live_data.get('long_term_fuel_trim', 0.0),
                step=0.5,
                format="%.1f %%",
                help="Ajuste fino da mistura ar/combustível. Valores positivos enriquecem, negativos empobrecem."
            )
            
            if st.button("🚀 APLICAR AJUSTE DE MISTURA", key="apply_fuel", use_container_width=True):
                with st.spinner("Enviando comando UDS 0x2E..."):
                    resp = st.session_state.ecu_control.adjust_fuel_trim(fuel_trim, force=not safety.safe)
                    if resp.success:
                        st.success(f"✅ Ajuste aplicado! Resposta em {resp.response_time_ms:.1f}ms")
                        st.balloons()
                    else:
                        st.error(f"❌ Falha: {resp.message}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Ajuste de Marcha Lenta
            idle_rpm = st.slider(
                "RPM de Marcha Lenta",
                min_value=600,
                max_value=1200,
                value=800,
                step=10,
                format="%d RPM",
                help="RPM alvo para marcha lenta (quando veículo parado)"
            )
            
            if st.button("🚀 APLICAR RPM", key="apply_rpm", use_container_width=True):
                with st.spinner("Enviando comando UDS 0x2E..."):
                    resp = st.session_state.ecu_control.adjust_idle_speed(idle_rpm, force=not safety.safe)
                    if resp.success:
                        st.success(f"✅ RPM ajustado! Resposta em {resp.response_time_ms:.1f}ms")
                    else:
                        st.error(f"❌ Falha: {resp.message}")
        
        with col_t2:
            st.markdown("### ⚙️ Ajustes Avançados")
            
            # Ajuste de Injeção
            inj_time = st.slider(
                "Tempo de Injeção",
                min_value=1.5,
                max_value=8.0,
                value=3.5,
                step=0.1,
                format="%.1f ms",
                help="Tempo de abertura dos injetores (específico do fabricante)"
            )
            
            if st.button("🚀 APLICAR INJEÇÃO", key="apply_inj", use_container_width=True):
                with st.spinner("Enviando comando específico do fabricante..."):
                    resp = st.session_state.ecu_control.adjust_injection_pulse(inj_time, force=not safety.safe)
                    if resp.success:
                        st.success(f"✅ Injeção ajustada! Resposta em {resp.response_time_ms:.1f}ms")
                    else:
                        st.error(f"❌ Falha: {resp.message}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Reset Flex Fuel
            st.markdown("### 🔄 Reset de Adaptações")
            
            if st.button("🔄 RESET FLEX FUEL", key="reset_flex", use_container_width=True):
                with st.spinner("Resetando parâmetros autoadaptativos..."):
                    resp = st.session_state.ecu_control.reset_flex_fuel(force=not safety.safe)
                    if resp.success:
                        st.success("✅ Parâmetros flex fuel resetados com sucesso!")
                    else:
                        st.error(f"❌ Falha: {resp.message}")
        
        # Otimização Automática
        st.markdown("---")
        st.markdown("### 🎯 OTIMIZAÇÃO AUTOMÁTICA")
        
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            st.markdown(f"""
            <div style="background:#001a33; padding:10px; border-radius:5px; text-align:center;">
                <span style="color:#888;">Lambda Atual</span><br>
                <span style="color:#00ffff; font-size:28px; font-weight:bold;">{st.session_state.ecu_control.live_data.get('lambda', 1.02):.3f}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_l2:
            st.markdown(f"""
            <div style="background:#001a33; padding:10px; border-radius:5px; text-align:center;">
                <span style="color:#888;">Sonda O2</span><br>
                <span style="color:#00ffff; font-size:28px; font-weight:bold;">{st.session_state.live_data['o2']:.3f}V</span>
            </div>
            """, unsafe_allow_html=True)
        with col_l3:
            st.markdown(f"""
            <div style="background:#001a33; padding:10px; border-radius:5px; text-align:center;">
                <span style="color:#888;">STFT/LTFT</span><br>
                <span style="color:#00ffff; font-size:28px; font-weight:bold;">{st.session_state.live_data.get('short_term_fuel_trim', 0):.1f}/{st.session_state.live_data.get('long_term_fuel_trim', 0):.1f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚀 OTIMIZAR FUNCIONAMENTO (Lambda 1.0)", use_container_width=True):
            with st.spinner("Otimizando parâmetros em tempo real..."):
                results = st.session_state.ecu_control.auto_tune_to_lambda1(max_attempts=10)
                st.session_state.tuning_results = results
                
                if results['success']:
                    st.success(f"✅ Otimização concluída em {results['attempts']} tentativas!")
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.metric("Lambda Final", f"{results['lambda_final']:.3f}", 
                                 delta=f"{results['lambda_final'] - results['lambda_inicial']:.3f}")
                    with col_r2:
                        st.metric("Tempo Injeção Final", f"{results['injection_final']:.2f}ms")
                else:
                    st.error(f"❌ Otimização falhou: {results.get('reason', 'Erro desconhecido')}")
        
        # Logs Técnicos
        with st.expander("📋 Logs Técnicos da ECU"):
            logs = st.session_state.ecu_control.get_logs(15)
            for log in logs:
                st.code(f"[{log['timestamp']}] {log['level']}: {log['message']}")

# =============================================
# VISUALIZADOR 3D
# =============================================
elif st.session_state.current_page == "Visualizador 3D":
    st.markdown("## 🔍 VISUALIZADOR 3D DE COMPONENTES")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="viewer-3d">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="engine-3d" style="position: relative; height: 400px; background: linear-gradient(135deg, #222, #111); border-radius: 8px; padding: 20px;">
            <svg width="100%" height="100%" viewBox="0 0 800 400" style="background: transparent;">
                <rect x="200" y="100" width="400" height="200" fill="#444" stroke="#00ffff" stroke-width="2" rx="10"/>
                <rect x="250" y="50" width="300" height="50" fill="#555" stroke="#888" stroke-width="1" rx="5"/>
                <rect x="280" y="130" width="50" height="80" fill="#666" stroke="#ffff00" stroke-width="3" rx="3"/>
                <text x="295" y="175" fill="#ffff00" font-size="12" font-family="Roboto Mono">C1</text>
                <rect x="360" y="130" width="50" height="80" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
                <text x="375" y="175" fill="white" font-size="12">C2</text>
                <rect x="440" y="130" width="50" height="80" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
                <text x="455" y="175" fill="white" font-size="12">C3</text>
                <rect x="520" y="130" width="50" height="80" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
                <text x="535" y="175" fill="white" font-size="12">C4</text>
                <circle cx="305" cy="70" r="15" fill="#ffaa00" stroke="#ffff00" stroke-width="3"/>
                <text x="298" y="75" fill="black" font-size="10" font-family="Roboto Mono">BOB</text>
                <line x1="305" y1="70" x2="250" y2="30" stroke="#ffff00" stroke-width="2" stroke-dasharray="5,3"/>
                <text x="200" y="20" fill="#ffff00" font-size="12" font-family="Roboto Mono">Componente afetado</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            if st.button("🔄 ROTACIONAR", key="rotate_3d", use_container_width=True):
                st.session_state.log.append("> Rotacionando modelo 3D")
        with col_b:
            if st.button("🔍 ZOOM IN", key="zoom_in", use_container_width=True):
                pass
        with col_c:
            if st.button("🔎 ZOOM OUT", key="zoom_out", use_container_width=True):
                pass
        with col_d:
            if st.button("🎯 CENTRALIZAR", key="center", use_container_width=True):
                pass
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📋 INFORMAÇÕES DO COMPONENTE")
        
        if st.session_state.selected_component:
            comp = st.session_state.selected_component
            
            st.markdown(f"""
            <div class="cliente-card">
                <h4 style="color:#00ffff; margin-bottom:15px;">{comp}</h4>
                
                <div style="margin-bottom:15px;">
                    <div style="color:#888; font-size:11px; margin-bottom:5px;">📍 LOCALIZAÇÃO</div>
                    <div style="font-size:12px;">Cabeçote do motor, lado direito, próximo à válvula borboleta</div>
                </div>
                
                <div style="margin-bottom:15px;">
                    <div style="color:#888; font-size:11px; margin-bottom:5px;">🔌 PINAGEM</div>
                    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:5px;">
                        <div style="background:#000; padding:8px; border-radius:5px; text-align:center;">
                            <div style="color:#00ffff;">1</div>
                            <div style="font-size:10px;">12V</div>
                            <div style="color:#888; font-size:8px;">Vermelho</div>
                        </div>
                        <div style="background:#000; padding:8px; border-radius:5px; text-align:center;">
                            <div style="color:#00ffff;">2</div>
                            <div style="font-size:10px;">GND</div>
                            <div style="color:#888; font-size:8px;">Preto</div>
                        </div>
                        <div style="background:#000; padding:8px; border-radius:5px; text-align:center;">
                            <div style="color:#00ffff;">3</div>
                            <div style="font-size:10px;">Sinal</div>
                            <div style="color:#888; font-size:8px;">Verde</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Selecione um componente no diagnóstico para visualização 3D")

# =============================================
# MODO CLIENTE
# =============================================
elif st.session_state.current_page == "Modo Cliente":
    st.markdown("## 👤 MODO CLIENTE - INFORMAÇÕES SIMPLIFICADAS")
    
    if not st.session_state.dtcs:
        st.warning("Nenhum diagnóstico disponível. Execute um escaneamento primeiro.")
    else:
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("### 🚗 RESUMO DO DIAGNÓSTICO")
            
            severidade_max = 0
            
            for dtc in st.session_state.dtcs:
                if dtc['code'] == 'P0301':
                    titulo = "🔥 Problema na Queima de Combustível"
                    desc = "O motor está tendo dificuldade para queimar o combustível no cilindro 1"
                    severidade = 0.8
                elif dtc['code'] == 'P0420':
                    titulo = "🌫️ Sistema de Filtragem de Poluição Comprometido"
                    desc = "O catalisador não está filtrando os gases corretamente"
                    severidade = 0.6
                else:
                    titulo = f"⚠️ Problema no Sistema {dtc['system']}"
                    desc = dtc['desc']
                    severidade = 0.5
                
                severidade_max = max(severidade_max, severidade)
                
                st.markdown(f"""
                <div class="cliente-card">
                    <h4 style="color:#ff0000;">{titulo}</h4>
                    <p style="color:#ccc;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📝 AUTORIZAÇÃO DE REPARO")
            
            if st.button("✍️ ASSINAR E AUTORIZAR", use_container_width=True):
                st.session_state.assinatura = True
                st.success("✅ Autorização registrada com sucesso!")

# =============================================
# DIAGNÓSTICO IA
# =============================================
elif st.session_state.current_page == "Diagnóstico IA":
    st.markdown("## 🤖 DIAGNÓSTICO AVANÇADO COM IA")
    
    if st.session_state.dtcs:
        dtc_options = [dtc['code'] for dtc in st.session_state.dtcs]
        selected_dtc = st.selectbox("Selecione o DTC para análise", dtc_options)
        
        if st.button("🔮 EXECUTAR ANÁLISE", use_container_width=True):
            with st.spinner("IA analisando dados..."):
                time.sleep(2)
                live_data_for_ia = {
                    'short_term_fuel_trim': st.session_state.live_data.get('short_term_fuel_trim', 0),
                    'long_term_fuel_trim': st.session_state.live_data.get('long_term_fuel_trim', 0),
                    'o2_voltage': st.session_state.live_data.get('o2', 0),
                    'maf': st.session_state.live_data.get('maf', 0),
                    'rpm': st.session_state.live_data.get('rpm', 0)
                }
                
                resultado = st.session_state.copiloto.diagnose(
                    selected_dtc,
                    live_data_for_ia,
                    st.session_state.live_history[-20:] if st.session_state.live_history else [],
                    st.session_state.vehicle_info
                )
                st.session_state.diagnosis_result = resultado

# =============================================
# ORÇAMENTOS
# =============================================
elif st.session_state.current_page == "Orçamentos":
    st.markdown("## 💰 ORÇAMENTOS E PEÇAS")
    
    if st.session_state.diagnosis_result:
        st.info("Sistema de orçamentos disponível em breve!")
    else:
        st.info("Execute um diagnóstico primeiro")

# =============================================
# BOTTOM BAR
# =============================================
st.markdown("---")

last_log = st.session_state.log[-1] if st.session_state.log else "> Sistema pronto"
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"""
    <div style="background:#1a1d24; padding:10px 15px; border-radius:8px;">
        <span style="color:#00ff00; font-family:'Roboto Mono';">{last_log}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="display:flex; gap:15px; justify-content:center;">
        <span style="color:#888;">🔵 ONLINE</span>
        <span style="color:#ffaa00;">🟡 CAN</span>
        <span style="color:#00ffff;">🟢 KWP</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    uptime = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="color:#888; text-align:right;">
        Uptime: {uptime}
    </div>
    """, unsafe_allow_html=True)

# =============================================
# ATUALIZAÇÃO DE DADOS
# =============================================
if st.session_state.connected:
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
        'maf': round(2.5 + random.random() * 3, 1),
        'lambda': round(random.uniform(0.95, 1.05), 3)
    }
    
    st.session_state.live_data = novo_dado
    st.session_state.live_history.append(novo_dado)
    if len(st.session_state.live_history) > 50:
        st.session_state.live_history.pop(0)
    
    time.sleep(1)
    st.rerun()
