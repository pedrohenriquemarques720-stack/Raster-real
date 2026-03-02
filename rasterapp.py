# app.py - Interface Moderna com Círculo de Saúde, Visualizador 3D e Modo Cliente

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import threading
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
import base64

# Importando nossos módulos
from obd_scanner import OBDScannerRevolucionario as OBDScannerPro
from dtc_database import DTCDatabase
from vehicle_profiles import VehicleDatabase
from co_piloto_oficina import CoPilotoOficina
from sgw_autopass import SGWAutoPass
from visualizacao_3d import Visualizador3D
from orcamento_automatico import OrcamentoAutomatico

# Configuração da página
st.set_page_config(
    page_title="AUTEL PRO - Scanner Inteligente",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# CSS - NOVA INTERFACE MODERNA COM CÍRCULO DE SAÚDE
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
    
    /* Menu de Navegação */
    .nav-menu {
        background: #1a1d24;
        padding: 10px 20px;
        border-radius: 50px;
        margin: 0 20px 20px 20px;
        border: 1px solid #00ffff;
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
        transform-style: preserve-3d;
    }
    
    .component-highlight {
        position: absolute;
        border: 3px solid #ffff00;
        border-radius: 5px;
        animation: blink-yellow 0.5s infinite;
        box-shadow: 0 0 20px #ffff00;
    }
    
    @keyframes blink-yellow {
        0% { border-color: #ffff00; box-shadow: 0 0 10px #ffff00; }
        50% { border-color: #ffaa00; box-shadow: 0 0 30px #ffaa00; }
        100% { border-color: #ffff00; box-shadow: 0 0 10px #ffff00; }
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
    
    .assinatura-canvas {
        width: 100%;
        height: 100%;
        cursor: crosshair;
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
    
    /* Gráfico */
    .chart-container {
        background: #1a1d24;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
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
    
    /* Metric cards */
    .metric-card {
        background: #1a1d24;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
    
    .metric-value-big {
        font-size: 32px;
        font-weight: bold;
        color: #00ffff;
        font-family: 'Roboto Mono', monospace;
    }
    
    /* Tabs personalizadas */
    .custom-tab {
        background: #1a1d24;
        padding: 8px 15px;
        border-radius: 20px;
        color: #888;
        text-align: center;
        cursor: pointer;
    }
    
    .custom-tab.active {
        background: #00ffff;
        color: black;
        font-weight: bold;
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
    st.session_state.dtc_db = DTCDatabase()
    st.session_state.vehicle_db = VehicleDatabase()
    st.session_state.connected = False
    st.session_state.sgw_unlocked = False
    st.session_state.current_page = "dashboard"
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
    st.session_state.assinatura_pontos = []
    st.session_state.orcamento_atual = None

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
                st.session_state.log.append("> Conectado ao veículo")
                st.rerun()
    else:
        if st.button("🔌 DESCONECTAR", key="disconnect_btn"):
            st.session_state.connected = False
            st.session_state.sgw_unlocked = False
            st.session_state.dtcs = []
            st.session_state.diagnosis_result = None
            st.session_state.log.append("> Desconectado")
            st.rerun()

# =============================================
# SGW AUTO-PASS (Executa automaticamente quando conecta)
# =============================================
if st.session_state.connected and not st.session_state.sgw_unlocked:
    with st.spinner("🔄 Desbloqueando Security Gateway..."):
        time.sleep(2)
        # Simula desbloqueio bem-sucedido
        st.session_state.sgw_unlocked = True
        st.session_state.log.append("✅ SGW desbloqueado com sucesso")
        st.balloons()

# =============================================
# MENU DE NAVEGAÇÃO
# =============================================
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Visualizador 3D", "Modo Cliente", "Diagnóstico IA", "Orçamentos"],
    icons=["speedometer2", "cube", "person", "robot", "cash-coin"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1a1d24", "border-radius": "50px", "margin": "0 20px 20px 20px"},
        "icon": {"color": "#00ffff", "font-size": "14px"},
        "nav-link": {"font-size": "12px", "text-align": "center", "margin": "0px", "color": "#888", "font-family": "Roboto Mono"},
        "nav-link-selected": {"background-color": "#00ffff", "color": "black", "font-weight": "bold"},
    }
)

st.session_state.current_page = selected.lower()

# =============================================
# DASHBOARD PRINCIPAL
# =============================================
if st.session_state.current_page == "dashboard":
    st.markdown("## 🎯 PAINEL DE DIAGNÓSTICO")
    
    col1, col2, col3 = st.columns([1.2, 2, 1.2])
    
    # COLUNA ESQUERDA - Círculo de Saúde e Estatísticas
    with col1:
        st.markdown("### 🩺 SAÚDE DO VEÍCULO")
        
        # Calcula percentual de saúde baseado nas falhas
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
        
        # Status do SGW
        sgw_status_text = "🔓 DESBLOQUEADO" if st.session_state.sgw_unlocked else "🔒 BLOQUEADO"
        sgw_color = "#00ff00" if st.session_state.sgw_unlocked else "#ff0000"
        
        st.markdown(f"""
        <div style="background: #1a1d24; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 3px solid {sgw_color};">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #888;">Security Gateway</span>
                <span style="color: {sgw_color}; font-weight: bold;">{sgw_status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # COLUNA CENTRAL - Dados em Tempo Real e Sistemas
    with col2:
        st.markdown("### 📊 DADOS EM TEMPO REAL")
        
        data = st.session_state.live_data
        
        # Grid de dados
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
        
        # Parâmetros adicionais
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
        
        # Gráfico de tendência
        if len(st.session_state.live_history) > 5:
            hist_df = pd.DataFrame(st.session_state.live_history[-30:])
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=hist_df['rpm'], 
                name='RPM', 
                line=dict(color='#00ffff', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 255, 255, 0.1)'
            ))
            fig.update_layout(
                height=150,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='#1a1d24',
                plot_bgcolor='#1a1d24',
                font=dict(color='white'),
                showlegend=False,
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=True, gridcolor='#333')
            )
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # COLUNA DIREITA - Co-Piloto e DTCs
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
                    st.session_state.log.append("> Escaneamento concluído - 3 falhas encontradas")
        
        with col_btn2:
            if st.button("✅ LIMPAR", key="clear_dtc", use_container_width=True):
                st.session_state.dtcs = []
                st.session_state.diagnosis_result = None
                st.session_state.log.append("> Códigos de falha limpos")
                st.success("Códigos limpos com sucesso!")
        
        # Lista de DTCs
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
                        with st.spinner("IA analisando dados em tempo real..."):
                            time.sleep(2)
                            live_data_for_ia = {
                                'short_term_fuel_trim': st.session_state.live_data.get('short_term_fuel_trim', 0),
                                'long_term_fuel_trim': st.session_state.live_data.get('long_term_fuel_trim', 0),
                                'o2_voltage': st.session_state.live_data.get('o2', 0),
                                'maf': st.session_state.live_data.get('maf', 0),
                                'rpm': st.session_state.live_data.get('rpm', 0),
                                'engine_load': st.session_state.live_data.get('engine_load', 0)
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
        
        # Resultado do Co-Piloto
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
            
            if res['final_recommendation']['action_plan']:
                st.markdown(f"""
                <div style="margin-top:12px; padding-top:8px; border-top:1px solid #00ffff;">
                    <div style="color:#00ffff; font-size:11px; margin-bottom:3px;">✅ RECOMENDAÇÃO:</div>
                    <div style="font-size:11px;">{res['final_recommendation']['action_plan'][0]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Botão para ver em 3D
            if st.button("🔍 VER COMPONENTE EM 3D", key="view_3d", use_container_width=True):
                st.session_state.current_page = "visualizador 3d"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# VISUALIZADOR 3D
# =============================================
elif st.session_state.current_page == "visualizador 3d":
    st.markdown("## 🔍 VISUALIZADOR 3D DE COMPONENTES")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="viewer-3d">', unsafe_allow_html=True)
        
        # Simulação de visualizador 3D
        st.markdown("""
        <div class="engine-3d" style="position: relative;">
            <svg width="100%" height="400" viewBox="0 0 800 400" style="background: #222; border-radius: 8px;">
                <!-- Bloco do motor -->
                <rect x="200" y="100" width="400" height="200" fill="#444" stroke="#00ffff" stroke-width="2" rx="10"/>
                
                <!-- Cilindros -->
                <rect x="250" y="50" width="300" height="50" fill="#555" stroke="#888" stroke-width="1" rx="5"/>
                
                <!-- Cilindro 1 (destacado) -->
                <rect id="cilindro1" x="280" y="130" width="50" height="80" fill="#666" stroke="#ffff00" stroke-width="3" rx="3"/>
                <text x="295" y="175" fill="#ffff00" font-size="12">C1</text>
                
                <!-- Cilindro 2 -->
                <rect x="360" y="130" width="50" height="80" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
                <text x="375" y="175" fill="white" font-size="12">C2</text>
                
                <!-- Cilindro 3 -->
                <rect x="440" y="130" width="50" height="80" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
                <text x="455" y="175" fill="white" font-size="12">C3</text>
                
                <!-- Cilindro 4 -->
                <rect x="520" y="130" width="50" height="80" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
                <text x="535" y="175" fill="white" font-size="12">C4</text>
                
                <!-- Bobina destacada (se houver componente selecionado) -->
                <circle cx="305" cy="70" r="15" fill="#ffaa00" stroke="#ffff00" stroke-width="3" filter="url(#glow)"/>
                <text x="298" y="75" fill="black" font-size="10">BOB</text>
                
                <!-- Seta indicadora -->
                <line x1="305" y1="70" x2="250" y2="30" stroke="#ffff00" stroke-width="2" stroke-dasharray="5,3"/>
                <text x="200" y="20" fill="#ffff00" font-size="12">Componente afetado</text>
                
                <!-- Efeito de brilho -->
                <defs>
                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
                        <feMerge>
                            <feMergeNode in="offsetblur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        # Botões de controle 3D
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
            
            # Informações do componente
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
                
                <div>
                    <div style="color:#888; font-size:11px; margin-bottom:5px;">📊 VALORES DE REFERÊNCIA</div>
                    <div style="font-size:12px;">• Resistência primária: 0.5-1.5Ω</div>
                    <div style="font-size:12px;">• Tensão de alimentação: 12V</div>
                    <div style="font-size:12px;">• Forma de onda: Quadrada 0-5V</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📷 VER ESQUEMA ELÉTRICO", use_container_width=True):
                st.session_state.log.append("> Exibindo esquema elétrico")
        else:
            st.info("Selecione um componente no diagnóstico para visualização 3D")

# =============================================
# MODO CLIENTE
# =============================================
elif st.session_state.current_page == "modo cliente":
    st.markdown("## 👤 MODO CLIENTE - INFORMAÇÕES SIMPLIFICADAS")
    
    if not st.session_state.dtcs:
        st.warning("Nenhum diagnóstico disponível. Execute um escaneamento primeiro.")
    else:
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("### 🚗 RESUMO DO DIAGNÓSTICO")
            
            severidade_max = 0
            
            for dtc in st.session_state.dtcs:
                # Tradução para leigo
                if dtc['code'] == 'P0301':
                    titulo = "🔥 Problema na Queima de Combustível"
                    desc = "O motor está tendo dificuldade para queimar o combustível no cilindro 1, causando perda de potência e aumento no consumo."
                    severidade = 0.8
                elif dtc['code'] == 'P0420':
                    titulo = "🌫️ Sistema de Filtragem de Poluição Comprometido"
                    desc = "O catalisador não está filtrando os gases corretamente, o que pode aumentar a emissão de poluentes."
                    severidade = 0.6
                elif dtc['code'] == 'P0171':
                    titulo = "⚡ Mistura de Ar e Combustível Desregulada"
                    desc = "O motor está recebendo ar demais ou combustível de menos, causando marcha lenta irregular."
                    severidade = 0.5
                else:
                    titulo = f"⚠️ Problema no Sistema {dtc['system']}"
                    desc = dtc['desc']
                    severidade = 0.7
                
                severidade_max = max(severidade_max, severidade)
                
                # Cor baseada na severidade
                cor_titulo = "#ff0000" if severidade > 0.7 else "#ffaa00" if severidade > 0.4 else "#00ff00"
                
                st.markdown(f"""
                <div class="cliente-card">
                    <h4 style="color:{cor_titulo};">{titulo}</h4>
                    <p style="color:#ccc; font-size:13px;">{desc}</p>
                    <div style="margin-top:10px; padding:8px; background:#000; border-radius:5px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                            <span style="color:#888;">Urgência:</span>
                            <span style="color:{cor_titulo};">{'ALTA' if severidade > 0.7 else 'MÉDIA' if severidade > 0.4 else 'BAIXA'}</span>
                        </div>
                        <div class="severidade-bar">
                            <div class="severidade-indicator" style="width:{severidade * 100}%;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Barra de urgência geral
            st.markdown("### ⏰ URGÊNCIA DE REPARO")
            st.markdown(f"""
            <div style="background:#1a1d24; padding:20px; border-radius:15px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="color:#888;">Nível de urgência:</span>
                    <span style="color:#ff0000; font-weight:bold;">{'CRÍTICO' if severidade_max > 0.7 else 'ATENÇÃO' if severidade_max > 0.4 else 'NORMAL'}</span>
                </div>
                <div class="severidade-bar">
                    <div class="severidade-indicator" style="width:{severidade_max * 100}%; background:rgba(255,255,255,0.5);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📝 AUTORIZAÇÃO DE REPARO")
            
            # Resumo do orçamento
            total_pecas = sum([850, 450])
            mao_obra = 3.5 * 120
            total_geral = total_pecas + mao_obra
            
            st.markdown(f"""
            <div style="background:#1a1d24; padding:20px; border-radius:15px; margin-bottom:20px;">
                <h4 style="color:#00ffff; margin-bottom:15px;">ORÇAMENTO ESTIMADO</h4>
                
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="color:#888;">Peças:</span>
                    <span style="color:white;">R$ {total_pecas:.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="color:#888;">Mão de obra (3.5h):</span>
                    <span style="color:white;">R$ {mao_obra:.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-top:15px; padding-top:10px; border-top:1px solid #00ffff;">
                    <span style="color:#00ffff; font-weight:bold;">TOTAL:</span>
                    <span style="color:#00ffff; font-size:20px; font-weight:bold;">R$ {total_geral:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Área de assinatura
            st.markdown("### ✍️ ASSINATURA DIGITAL")
            
            # Simulação de canvas de assinatura
            assinatura_html = """
            <div class="assinatura-area" id="assinaturaCanvas">
                <canvas class="assinatura-canvas" width="300" height="120" style="width:100%; height:120px;"></canvas>
            </div>
            """
            
            st.markdown(assinatura_html, unsafe_allow_html=True)
            
            if st.button("✍️ ASSINAR E AUTORIZAR", use_container_width=True):
                st.session_state.assinatura = True
                st.session_state.log.append("> Cliente autorizou reparo via assinatura digital")
                st.success("✅ Autorização registrada com sucesso!")
                
                # Gerar orçamento automático
                if st.session_state.diagnosis_result:
                    part_info = st.session_state.orcamento.consultar_peca(
                        st.session_state.vehicle_info['vin'],
                        st.session_state.diagnosis_result['probabilities'][0]['component'],
                        st.session_state.diagnosis_result['probabilities'][0].get('part_number', '')
                    )
                    
                    orcamento = st.session_state.orcamento.gerar_orcamento(
                        st.session_state.vehicle_info['vin'],
                        st.session_state.vehicle_info,
                        st.session_state.diagnosis_result,
                        part_info
                    )
                    st.session_state.orcamento_atual = orcamento
            
            if st.session_state.assinatura:
                st.markdown("""
                <div style="background:#004400; padding:10px; border-radius:8px; margin-top:10px; text-align:center;">
                    <span style="color:#00ff00;">✓ Assinatura registrada em 02/03/2026 15:23</span>
                </div>
                """, unsafe_allow_html=True)

# =============================================
# DIAGNÓSTICO IA
# =============================================
elif st.session_state.current_page == "diagnóstico ia":
    st.markdown("## 🤖 DIAGNÓSTICO AVANÇADO COM IA")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔍 ANALISADOR PREDITIVO")
        
        if st.session_state.dtcs:
            dtc_options = [dtc['code'] for dtc in st.session_state.dtcs]
            selected_dtc = st.selectbox("Selecione o DTC para análise detalhada", dtc_options)
            
            if st.button("🔮 EXECUTAR ANÁLISE COMPLETA", use_container_width=True):
                with st.spinner("IA analisando padrões históricos e dados em tempo real..."):
                    time.sleep(3)
                    dtc_atual = next((d for d in st.session_state.dtcs if d['code'] == selected_dtc), None)
                    
                    live_data_for_ia = {
                        'short_term_fuel_trim': st.session_state.live_data.get('short_term_fuel_trim', 0),
                        'long_term_fuel_trim': st.session_state.live_data.get('long_term_fuel_trim', 0),
                        'o2_voltage': st.session_state.live_data.get('o2', 0),
                        'maf': st.session_state.live_data.get('maf', 0),
                        'rpm': st.session_state.live_data.get('rpm', 0),
                        'engine_load': st.session_state.live_data.get('engine_load', 0)
                    }
                    
                    resultado = st.session_state.copiloto.diagnose(
                        selected_dtc,
                        live_data_for_ia,
                        st.session_state.live_history[-20:] if st.session_state.live_history else [],
                        st.session_state.vehicle_info
                    )
                    st.session_state.diagnosis_result = resultado
                    
            if st.session_state.diagnosis_result:
                res = st.session_state.diagnosis_result
                
                st.markdown(f"""
                <div class="copilot-card-modern" style="margin-top:20px;">
                    <div class="copilot-title-modern">📊 RESULTADO DA ANÁLISE</div>
                    <div style="margin:15px 0;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                            <span>DTC:</span>
                            <span style="color:#00ffff;">{res['dtc']}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between;">
                            <span>Confiança:</span>
                            <span style="color:#00ff00;">{res['confidence_score']}%</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Execute um escaneamento primeiro para obter DTCs")
    
    with col2:
        st.markdown("### 📈 CORRELAÇÃO DE DADOS")
        
        if st.session_state.live_history:
            hist_df = pd.DataFrame(st.session_state.live_history[-30:])
            
            fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                                subplot_titles=('RPM', 'STFT', 'O2 Sensor'))
            
            fig.add_trace(go.Scatter(y=hist_df['rpm'], line=dict(color='#00ffff')), row=1, col=1)
            fig.add_trace(go.Scatter(y=hist_df.get('short_term_fuel_trim', [0]*len(hist_df)), 
                                     line=dict(color='#ffff00')), row=2, col=1)
            fig.add_trace(go.Scatter(y=hist_df.get('o2', [0]*len(hist_df)), 
                                     line=dict(color='#ff0000')), row=3, col=1)
            
            fig.update_layout(height=400, showlegend=False,
                             paper_bgcolor='#1a1d24',
                             plot_bgcolor='#1a1d24',
                             font=dict(color='white'))
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aguardando dados em tempo real...")

# =============================================
# ORÇAMENTOS
# =============================================
elif st.session_state.current_page == "orçamentos":
    st.markdown("## 💰 ORÇAMENTOS E PEÇAS")
    
    if st.session_state.diagnosis_result and st.session_state.dtcs:
        res = st.session_state.diagnosis_result
        primary = res['probabilities'][0] if res['probabilities'] else None
        
        if primary:
            st.markdown(f"### 🛒 Consultando peça: {primary['component']}")
            
            with st.spinner("Consultando distribuidores..."):
                time.sleep(1.5)
                part_info = st.session_state.orcamento.consultar_peca(
                    st.session_state.vehicle_info['vin'],
                    primary['component'],
                    primary.get('part_number', '')
                )
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏭 FORNECEDORES")
                
                for supplier in part_info['suppliers'][:3]:
                    st.markdown(f"""
                    <div style="background:#1a1d24; padding:15px; border-radius:10px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:#00ffff;">{supplier['name'].upper()}</span>
                            <span style="color:white;">R$ {supplier['price']:.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:5px; font-size:12px;">
                            <span style="color:#888;">Frete: R$ {supplier['shipping']:.2f}</span>
                            <span style="color:#888;">Total: R$ {supplier['total_price']:.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:5px; font-size:11px;">
                            <span style="color:#00ff00;">✓ {supplier['availability']}</span>
                            <span>Garantia: {supplier['warranty']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 📄 GERAR ORÇAMENTO")
                
                # Seleciona fornecedor recomendado
                if part_info['recommended_supplier']:
                    rec = part_info['recommended_supplier']
                    
                    st.markdown(f"""
                    <div style="background:#004400; padding:20px; border-radius:15px; margin-bottom:20px;">
                        <h4 style="color:#00ff00;">🏆 MELHOR OFERTA</h4>
                        <div style="margin:15px 0;">
                            <div style="font-size:24px; color:#00ff00; font-weight:bold;">R$ {rec['total_price']:.2f}</div>
                            <div style="color:#888;">{rec['name']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("📝 GERAR ORÇAMENTO COMPLETO", use_container_width=True):
                    orcamento = st.session_state.orcamento.gerar_orcamento(
                        st.session_state.vehicle_info['vin'],
                        st.session_state.vehicle_info,
                        res,
                        part_info,
                        labor_hour_rate=120.0
                    )
                    st.session_state.orcamento_atual = orcamento
                    st.success("✅ Orçamento gerado com sucesso!")
                
                if st.session_state.orcamento_atual:
                    st.markdown("### 📋 RESUMO DO ORÇAMENTO")
                    orc = st.session_state.orcamento_atual
                    
                    st.markdown(f"""
                    <div style="background:#1a1d24; padding:20px; border-radius:15px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                            <span style="color:#888;">Peças:</span>
                            <span>R$ {orc['resumo']['total_pecas']:.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                            <span style="color:#888;">Mão de obra:</span>
                            <span>R$ {orc['resumo']['total_mao_obra']:.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:15px; padding-top:10px; border-top:1px solid #00ffff;">
                            <span style="color:#00ffff; font-weight:bold;">TOTAL:</span>
                            <span style="color:#00ffff; font-size:20px; font-weight:bold;">R$ {orc['resumo']['total']:.2f}</span>
                        </div>
                        <div style="margin-top:15px;">
                            <div style="color:#888;">Válido até: {orc['validade']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("📱 ENVIAR VIA WHATSAPP", use_container_width=True):
                        st.session_state.log.append(f"> Orçamento {orc['numero']} enviado via WhatsApp")
                        st.success("✅ Orçamento enviado com sucesso!")
    else:
        st.info("Execute um diagnóstico primeiro para gerar orçamentos")

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
# ATUALIZAÇÃO DE DADOS EM TEMPO REAL
# =============================================
if st.session_state.connected:
    # Atualiza dados com variação realista
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
    
    time.sleep(1)
    st.rerun()
