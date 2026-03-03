# app.py - RASTHER JPO - Sistema Profissional de Diagnóstico Automotivo

import streamlit as st
import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime
import json
import os

# Configuração da página (DEVE SER A PRIMEIRA COISA)
st.set_page_config(
    page_title="RASTHER JPO - Scanner Profissional",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# VERIFICAÇÃO DE SESSÃO (CORRIGE O NameError)
# =============================================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_page = "Dashboard"
    st.session_state.connected = False
    st.session_state.vehicle_info = {
        'manufacturer': '---',
        'model': '---',
        'year': '---',
        'engine': '---',
        'vin': '---',
        'protocol': '---'
    }
    st.session_state.dtcs = []
    st.session_state.live_data = {
        'rpm': 0,
        'speed': 0,
        'temp': 0,
        'battery': 12.5,
        'engine_load': 0,
        'stft': 0,
        'ltft': 0,
        'maf': 0
    }
    st.session_state.log = []
    st.session_state.scanning = False
    st.session_state.ecu_connected = False

# =============================================
# IMPORTAÇÕES (APÓS INICIALIZAÇÃO)
# =============================================
try:
    from core.scanner import ScannerProfissional
    from core.diagnostic import DiagnosticAI
    from core.tuning import TuningControl
    from core.pids_br import PIDsBrasil
    from hardware.can_interface import CANInterface
except ImportError as e:
    st.error(f"⚠️ Erro ao carregar módulos: {e}")
    st.info("O sistema funcionará em modo simulação")

# =============================================
# CSS PROFISSIONAL (TEMA AUTOMOTIVO)
# =============================================
st.markdown("""
<style>
    /* Tema automotivo profissional */
    .stApp {
        background: #0a0c10;
    }
    
    /* Header com gradiente */
    .header {
        background: linear-gradient(135deg, #002b5c, #0047ab);
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-left: 5px solid #ff6600;
    }
    
    .logo h1 {
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 0;
    }
    
    .logo p {
        color: #00ffff;
        font-size: 12px;
        margin: 0;
    }
    
    .status {
        background: black;
        padding: 8px 20px;
        border-radius: 30px;
        border: 1px solid #00ffff;
        color: #00ff00;
        font-family: monospace;
    }
    
    /* Cards de dados */
    .metric-card {
        background: #1a1d24;
        border: 1px solid #ff6600;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #00ffff;
        font-family: monospace;
    }
    
    .metric-label {
        color: #888;
        font-size: 12px;
        text-transform: uppercase;
    }
    
    /* Botões profissionais */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff6600, #ff8533) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px !important;
    }
    
    /* Cards de diagnóstico */
    .dtc-card {
        background: #1a1d24;
        border-left: 4px solid #ff0000;
        padding: 10px;
        margin: 5px 0;
        border-radius: 0 5px 5px 0;
    }
    
    .dtc-code {
        color: #ff6666;
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Menu de navegação */
    .nav-menu {
        display: flex;
        gap: 10px;
        margin: 0 20px 20px 20px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .nav-btn {
        background: #1a1d24;
        color: #888;
        padding: 10px 20px;
        border-radius: 30px;
        border: 1px solid #333;
        cursor: pointer;
        font-size: 13px;
        font-weight: bold;
    }
    
    .nav-btn:hover {
        border-color: #ff6600;
        color: #ff6600;
    }
    
    .nav-btn.active {
        background: #ff6600;
        color: black;
        border-color: #ff6600;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# HEADER
# =============================================
status_color = "#00ff00" if st.session_state.connected else "#ff0000"
status_text = "CONECTADO" if st.session_state.connected else "DESCONECTADO"

st.markdown(f"""
<div class="header">
    <div class="logo">
        <h1>🔧 RASTHER JPO</h1>
        <p>DIAGNÓSTICO AUTOMOTIVO PROFISSIONAL</p>
    </div>
    <div class="status">
        <span style="color: {status_color};">●</span> {status_text}
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================
# CONNECTION BAR
# =============================================
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(f"""
    <div style="background:#1a1d24; padding:15px; border-radius:8px; border-left:5px solid #ff6600; margin-bottom:20px;">
        <div style="display:flex; gap:30px;">
            <div><span style="color:#888;">VEÍCULO:</span> <span style="color:#ff6600;">{st.session_state.vehicle_info['model']}</span></div>
            <div><span style="color:#888;">PROTOCOLO:</span> <span style="color:#ff6600;">{st.session_state.vehicle_info['protocol']}</span></div>
            <div><span style="color:#888;">ECU:</span> <span style="color:#ff6600;">{st.session_state.vehicle_info['ecu']}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not st.session_state.connected:
        if st.button("🔌 CONECTAR"):
            with st.spinner("Conectando..."):
                time.sleep(2)
                st.session_state.connected = True
                st.session_state.vehicle_info = {
                    'manufacturer': 'Volkswagen',
                    'model': 'Gol 1.6',
                    'year': '2024',
                    'engine': 'EA211',
                    'vin': '9BWZZZ377VT004251',
                    'ecu': 'BOSCH ME17.9.65',
                    'protocol': 'CAN-BUS',
                    'version': '03H906023AB',
                    'km': '15.234 km'
                }
                st.session_state.log.append("✅ Conectado ao veículo")
                st.rerun()
    else:
        if st.button("🔌 DESCONECTAR"):
            st.session_state.connected = False
            st.session_state.dtcs = []
            st.session_state.log.append("❌ Desconectado")
            st.rerun()

# =============================================
# MENU DE NAVEGAÇÃO
# =============================================
pages = ["Dashboard", "Diagnóstico IA", "Controle Ativo", "Visualizador 3D", "Relatórios"]

nav_cols = st.columns(len(pages))
for i, page in enumerate(pages):
    with nav_cols[i]:
        if st.button(page, key=f"nav_{page}"):
            st.session_state.current_page = page
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# =============================================
# SCANNER SIMULADO (para testes)
# =============================================
if st.session_state.connected:
    # Atualiza dados em tempo real
    st.session_state.live_data = {
        'rpm': np.random.randint(750, 3500),
        'speed': np.random.randint(0, 120),
        'temp': np.random.randint(82, 98),
        'battery': round(12 + np.random.random() * 2, 1),
        'engine_load': np.random.randint(15, 55),
        'stft': round(np.random.uniform(-5, 15), 1),
        'ltft': round(np.random.uniform(-8, 18), 1),
        'maf': round(2.5 + np.random.random() * 3, 1)
    }

# =============================================
# CONTEÚDO DAS PÁGINAS
# =============================================

if st.session_state.current_page == "Dashboard":
    st.markdown("## 📊 PAINEL PRINCIPAL")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RPM</div>
            <div class="metric-value">{st.session_state.live_data['rpm']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">VELOCIDADE</div>
            <div class="metric-value">{st.session_state.live_data['speed']} km/h</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TEMP. MOTOR</div>
            <div class="metric-value">{st.session_state.live_data['temp']}°C</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BATERIA</div>
            <div class="metric-value">{st.session_state.live_data['battery']}V</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Informações do veículo
    st.markdown("### 🚗 INFORMAÇÕES DO VEÍCULO")
    info_cols = st.columns(3)
    info_data = [
        ("Fabricante", st.session_state.vehicle_info['manufacturer']),
        ("Modelo", st.session_state.vehicle_info['model']),
        ("Ano", st.session_state.vehicle_info['year']),
        ("Motor", st.session_state.vehicle_info['engine']),
        ("VIN", st.session_state.vehicle_info['vin']),
        ("KM", st.session_state.vehicle_info['km'])
    ]
    
    for i, (label, value) in enumerate(info_data):
        with info_cols[i % 3]:
            st.markdown(f"**{label}:** {value}")
    
    # Códigos de falha
    st.markdown("### ⚠️ CÓDIGOS DE FALHA")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔍 ESCANEAR FALHAS", use_container_width=True):
            with st.spinner("Escaneando..."):
                time.sleep(2)
                st.session_state.dtcs = [
                    {'code': 'P0301', 'desc': 'Falha de ignição - Cilindro 1', 'severity': 'critical'},
                    {'code': 'P0420', 'desc': 'Catalisador ineficiente', 'severity': 'warning'},
                    {'code': 'P0171', 'desc': 'Mistura pobre', 'severity': 'warning'}
                ]
                st.session_state.log.append("🔍 Escaneamento concluído")
    
    with col_btn2:
        if st.button("✅ LIMPAR FALHAS", use_container_width=True):
            st.session_state.dtcs = []
            st.session_state.log.append("✅ Falhas limpas")
    
    if st.session_state.dtcs:
        for dtc in st.session_state.dtcs:
            color = "#ff0000" if dtc['severity'] == 'critical' else "#ffaa00"
            st.markdown(f"""
            <div class="dtc-card" style="border-left-color: {color};">
                <span class="dtc-code">{dtc['code']}</span>
                <span style="color:#ccc; margin-left:10px;">{dtc['desc']}</span>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Diagnóstico IA":
    st.markdown("## 🤖 DIAGNÓSTICO INTELIGENTE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 ANÁLISE TÉCNICA")
        
        if st.session_state.dtcs:
            dtc_options = [dtc['code'] for dtc in st.session_state.dtcs]
            selected_dtc = st.selectbox("Selecione o código de falha", dtc_options)
            
            if st.button("🔮 ANALISAR COM IA", use_container_width=True):
                with st.spinner("IA analisando..."):
                    time.sleep(2)
                    st.session_state.analysis_result = {
                        'probabilities': [
                            {'component': 'Bobina de Ignição', 'prob': 85},
                            {'component': 'Vela de Ignição', 'prob': 45},
                            {'component': 'Injetor', 'prob': 20}
                        ]
                    }
            
            if st.session_state.get('analysis_result'):
                res = st.session_state.analysis_result
                st.markdown("**Probabilidades:**")
                for p in res['probabilities']:
                    st.progress(p['prob']/100, text=f"{p['component']}: {p['prob']}%")
        else:
            st.info("Execute um escaneamento primeiro")
    
    with col2:
        st.markdown("### 👤 ORIENTAÇÃO AO CLIENTE")
        
        if st.session_state.dtcs:
            st.markdown("""
            <div style="background:#1a2a33; padding:20px; border-radius:10px; border:1px solid #00ffff;">
                <h4 style="color:#00ffff;">🔍 PROBLEMA DETECTADO</h4>
                <p style="color:white;">Falha de ignição no cilindro 1</p>
                
                <h4 style="color:#00ffff;">📝 EXPLICAÇÃO SIMPLES</h4>
                <p style="color:#ccc;">O motor está com problema na queima de combustível no primeiro cilindro, causando perda de potência e aumento no consumo.</p>
                
                <h4 style="color:#00ffff;">🔧 CAUSA PROVÁVEL</h4>
                <p style="color:#ccc;">Bobina de ignição com defeito</p>
                
                <h4 style="color:#00ffff;">✅ SOLUÇÃO</h4>
                <p style="color:#ccc;">Substituir bobina de ignição (R$ 450,00) - 1.5h de serviço</p>
                
                <div style="background:#004400; padding:10px; border-radius:5px; margin-top:15px;">
                    <div style="color:#00ff00; font-size:20px; font-weight:bold;">R$ 450,00</div>
                    <div style="color:#888;">Tempo estimado: 1.5 horas</div>
                </div>
                
                <button style="width:100%; background:#25D366; color:white; padding:10px; border:none; border-radius:5px; margin-top:10px; font-weight:bold;">
                    📱 ENCAMINHAR PARA OFICINA
                </button>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Selecione um código de falha para análise")

elif st.session_state.current_page == "Controle Ativo":
    st.markdown("## ⚡ CONTROLE ATIVO DO MOTOR")
    
    if not st.session_state.connected:
        st.warning("⚠️ Conecte-se a um veículo para usar esta função")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 AJUSTES MANUAIS")
            
            fuel_trim = st.slider("Ajuste de Mistura (%)", -25.0, 25.0, 0.0, 0.5)
            if st.button("APLICAR AJUSTE DE MISTURA"):
                st.success(f"✅ Ajuste aplicado: {fuel_trim}%")
                st.session_state.log.append(f"⚡ Ajuste de mistura: {fuel_trim}%")
            
            idle_rpm = st.slider("RPM de Marcha Lenta", 600, 1200, 800, 10)
            if st.button("APLICAR RPM"):
                st.success(f"✅ RPM ajustado para {idle_rpm}")
                st.session_state.log.append(f"⚡ RPM ajustado: {idle_rpm}")
        
        with col2:
            st.markdown("### ⚙️ AJUSTES AVANÇADOS")
            
            inj_time = st.slider("Tempo de Injeção (ms)", 1.5, 8.0, 3.5, 0.1)
            if st.button("APLICAR INJEÇÃO"):
                st.success(f"✅ Injeção ajustada: {inj_time}ms")
                st.session_state.log.append(f"⚡ Injeção ajustada: {inj_time}ms")
            
            if st.button("🔄 RESET FLEX FUEL"):
                st.success("✅ Flex Fuel resetado")
                st.session_state.log.append("🔄 Reset Flex Fuel")

elif st.session_state.current_page == "Visualizador 3D":
    st.markdown("## 🔍 VISUALIZADOR 3D")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background:#111; border:1px solid #00ffff; border-radius:10px; padding:20px; height:400px;">
            <div style="text-align:center; color:#888; margin-top:150px;">
                <i class="fas fa-cube" style="font-size:48px;"></i>
                <p>Visualização 3D do motor</p>
                <p style="font-size:12px;">(Em desenvolvimento)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.info("Selecione um componente no diagnóstico")

elif st.session_state.current_page == "Relatórios":
    st.markdown("## 📋 RELATÓRIOS")
    
    st.markdown("### 📄 Últimos diagnósticos")
    
    if st.session_state.log:
        for log_entry in st.session_state.log[-10:]:
            st.code(log_entry)
    else:
        st.info("Nenhum registro encontrado")

# =============================================
# BOTTOM BAR
# =============================================
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.session_state.log:
        st.caption(f"📌 {st.session_state.log[-1]}")
    else:
        st.caption("📌 Sistema pronto")

with col2:
    st.caption(f"⏱️ {datetime.now().strftime('%H:%M:%S')} • RASTHER JPO v1.0")
