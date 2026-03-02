# rasterapp.py - Versão simplificada para Streamlit Cloud

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="AUTOMOTIVE PRO - Diagnóstico",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    /* Tema automotivo */
    .stApp {
        background-color: #0a0c10;
    }
    
    .main-title {
        background: linear-gradient(135deg, #ff6600, #00b0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    
    .metric-card {
        background: #1a1d24;
        border: 1px solid #ff6600;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255,102,0,0.2);
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #ff6600;
    }
    
    .metric-label {
        color: #9aa4b8;
        font-size: 14px;
    }
    
    .status-online {
        color: #00ff00;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff0000;
        font-weight: bold;
    }
    
    .dtc-card {
        background: #1a1d24;
        border-left: 4px solid #ff3d00;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .dtc-code {
        color: #ff3d00;
        font-weight: bold;
        font-size: 18px;
    }
    
    .button-connect {
        background: #ff6600;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .footer {
        text-align: center;
        color: #666;
        padding: 20px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INICIALIZAÇÃO DO ESTADO
# =============================================
if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.vehicle_info = {}
    st.session_state.dtc_codes = []
    st.session_state.live_data = {
        'rpm': 0,
        'speed': 0,
        'temp': 0,
        'battery': 0,
        'oil_pressure': 0,
        'engine_load': 0,
        'intake_temp': 0,
        'timing_advance': 0,
        'o2_sensor': 0,
        'fuel_pressure': 0,
        'throttle': 0,
        'maf': 0
    }
    st.session_state.history = {
        'rpm': [],
        'temp': [],
        'time': []
    }

# =============================================
# TÍTULO PRINCIPAL
# =============================================
st.markdown('<div class="main-title">🔧 AUTOMOTIVE PRO</div>', unsafe_allow_html=True)
st.markdown("---")

# =============================================
# SIDEBAR - CONFIGURAÇÕES
# =============================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/ff6600/000000?text=AUTOMOTIVE+PRO", use_container_width=True)
    
    st.markdown("## 🔌 CONEXÃO")
    
    # Tipo de conexão
    conn_type = st.radio(
        "Tipo de Conexão",
        ["📱 Bluetooth", "📡 WiFi", "🔌 USB"],
        horizontal=True
    )
    
    # Lista de dispositivos simulados
    devices = {
        "📱 Bluetooth": ["OBDII-ELM327", "OBDII-STN2120", "Scanner Pro BT"],
        "📡 WiFi": ["OBDII-WiFi-01", "OBDII-WiFi-02"],
        "🔌 USB": ["COM3 - USB Serial", "COM4 - USB Serial", "/dev/ttyUSB0"]
    }
    
    selected_type = conn_type.split(" ")[1]
    device_list = devices.get(f"{conn_type}", ["Nenhum dispositivo encontrado"])
    
    device = st.selectbox("Dispositivo", device_list)
    
    # Botão de conexão
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔌 CONECTAR", use_container_width=True):
            st.session_state.connected = True
            st.session_state.vehicle_info = {
                'manufacturer': 'Volkswagen',
                'model': 'Gol 1.6',
                'year': '2024',
                'engine': 'EA211 16V',
                'ecu': 'Bosch ME17.9.65',
                'vin': '9BWZZZ377VT004251',
                'protocol': 'CAN 500kbps'
            }
            st.success("✅ Conectado com sucesso!")
    
    with col2:
        if st.button("❌ DESCONECTAR", use_container_width=True):
            st.session_state.connected = False
            st.warning("Desconectado")
    
    # Status da conexão
    if st.session_state.connected:
        st.markdown("### 🟢 Status: **CONECTADO**")
        st.markdown(f"**Dispositivo:** {device}")
        st.markdown(f"**Protocolo:** {st.session_state.vehicle_info.get('protocol', 'N/A')}")
    else:
        st.markdown("### 🔴 Status: **DESCONECTADO**")
    
    st.markdown("---")
    
    # Ações rápidas
    st.markdown("## ⚡ AÇÕES RÁPIDAS")
    
    if st.button("🔍 ESCANEAR VEÍCULO", use_container_width=True):
        with st.spinner("Escaneando veículo..."):
            time.sleep(2)
            st.success("Veículo identificado!")
    
    if st.button("⚠️ LER FALHAS", use_container_width=True):
        st.session_state.dtc_codes = [
            {'code': 'P0301', 'desc': 'Falha de ignição no cilindro 1', 'system': 'Motor', 'severity': 'Alta'},
            {'code': 'P0420', 'desc': 'Catalisador ineficiente', 'system': 'Emissões', 'severity': 'Média'},
            {'code': 'P0171', 'desc': 'Mistura pobre', 'system': 'Combustível', 'severity': 'Média'}
        ]
        st.warning("3 códigos de falha encontrados!")
    
    if st.button("✅ LIMPAR FALHAS", use_container_width=True):
        st.session_state.dtc_codes = []
        st.success("Códigos de falha limpos!")
    
    if st.button("⚡ REPROGRAMAR ECU", use_container_width=True):
        st.warning("⚠️ ATENÇÃO! Não desligue o veículo durante a reprogramação!")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.05)
            progress_bar.progress(i + 1)
        st.success("✅ Reprogramação concluída!")

# =============================================
# CONTEÚDO PRINCIPAL
# =============================================

if st.session_state.connected:
    # Simulação de dados em tempo real
    st.session_state.live_data = {
        'rpm': random.randint(750, 3500),
        'speed': random.randint(0, 120),
        'temp': random.randint(80, 105),
        'battery': round(12 + random.random() * 2, 1),
        'oil_pressure': round(3 + random.random() * 2, 1),
        'engine_load': random.randint(15, 65),
        'intake_temp': random.randint(25, 45),
        'timing_advance': random.randint(5, 25),
        'o2_sensor': round(0.7 + random.random() * 0.2, 2),
        'fuel_pressure': random.randint(320, 400),
        'throttle': random.randint(5, 40),
        'maf': round(5 + random.random() * 10, 1)
    }
    
    # Atualiza histórico
    st.session_state.history['rpm'].append(st.session_state.live_data['rpm'])
    st.session_state.history['temp'].append(st.session_state.live_data['temp'])
    st.session_state.history['time'].append(datetime.now().strftime("%H:%M:%S"))
    
    # Mantém apenas últimos 50 pontos
    if len(st.session_state.history['rpm']) > 50:
        st.session_state.history['rpm'].pop(0)
        st.session_state.history['temp'].pop(0)
        st.session_state.history['time'].pop(0)

# =============================================
# LINHA 1: MÉTRICAS PRINCIPAIS
# =============================================
st.markdown("## 📊 DADOS EM TEMPO REAL")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">RPM</div>
        <div class="metric-value">{st.session_state.live_data['rpm']}</div>
        <div style="color: #888;">rotações/min</div>
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

st.markdown("---")

# =============================================
# LINHA 2: GRÁFICOS
# =============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 RPM em Tempo Real")
    
    if st.session_state.history['rpm']:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.history['time'],
            y=st.session_state.history['rpm'],
            mode='lines',
            name='RPM',
            line=dict(color='#ff6600', width=2)
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=20),
            paper_bgcolor='#0a0c10',
            plot_bgcolor='#1a1d24',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='#333'),
            yaxis=dict(showgrid=True, gridcolor='#333', range=[0, 7000])
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🌡️ Temperatura do Motor")
    
    if st.session_state.history['temp']:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.history['time'],
            y=st.session_state.history['temp'],
            mode='lines',
            name='Temperatura',
            line=dict(color='#ff3300', width=2),
            fill='tozeroy'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=20),
            paper_bgcolor='#0a0c10',
            plot_bgcolor='#1a1d24',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='#333'),
            yaxis=dict(showgrid=True, gridcolor='#333', range=[70, 120])
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =============================================
# LINHA 3: DADOS DO VEÍCULO
# =============================================
if st.session_state.connected:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚗 INFORMAÇÕES DO VEÍCULO")
        info_data = {
            "Fabricante": st.session_state.vehicle_info.get('manufacturer', 'N/A'),
            "Modelo": st.session_state.vehicle_info.get('model', 'N/A'),
            "Ano": st.session_state.vehicle_info.get('year', 'N/A'),
            "Motor": st.session_state.vehicle_info.get('engine', 'N/A'),
            "ECU": st.session_state.vehicle_info.get('ecu', 'N/A'),
            "VIN": st.session_state.vehicle_info.get('vin', 'N/A')
        }
        
        for key, value in info_data.items():
            st.markdown(f"**{key}:** {value}")
    
    with col2:
        st.subheader("📊 DADOS DO MOTOR")
        motor_data = {
            "Pressão do Óleo": f"{st.session_state.live_data['oil_pressure']} bar",
            "Carga do Motor": f"{st.session_state.live_data['engine_load']}%",
            "Temp. Ar Admissão": f"{st.session_state.live_data['intake_temp']}°C",
            "Avanço Ignição": f"{st.session_state.live_data['timing_advance']}°",
            "Sonda Lambda": f"{st.session_state.live_data['o2_sensor']} V",
            "Pressão Combustível": f"{st.session_state.live_data['fuel_pressure']} kPa",
            "Posição Acelerador": f"{st.session_state.live_data['throttle']}%",
            "Fluxo de Ar": f"{st.session_state.live_data['maf']} g/s"
        }
        
        for key, value in motor_data.items():
            st.markdown(f"**{key}:** {value}")

st.markdown("---")

# =============================================
# CÓDIGOS DE FALHA
# =============================================
st.subheader("⚠️ CÓDIGOS DE FALHA (DTC)")

if st.session_state.dtc_codes:
    for dtc in st.session_state.dtc_codes:
        severity_color = {
            'Alta': '#ff3d00',
            'Média': '#ffb300',
            'Baixa': '#00c853'
        }.get(dtc['severity'], '#888')
        
        st.markdown(f"""
        <div class="dtc-card" style="border-left-color: {severity_color};">
            <div class="dtc-code">{dtc['code']}</div>
            <div style="color: white;">{dtc['desc']}</div>
            <div style="color: #888; font-size: 12px;">Sistema: {dtc['system']} | Gravidade: {dtc['severity']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Nenhum código de falha encontrado.")

# =============================================
# RODAPÉ
# =============================================
st.markdown("---")
st.markdown("""
<div class="footer">
    🔧 AUTOMOTIVE PRO v2.0 | Desenvolvido para diagnóstico profissional<br>
    © 2026 - Todos os direitos reservados
</div>
""", unsafe_allow_html=True)

# Atualização automática a cada 2 segundos
if st.session_state.connected:
    time.sleep(2)
    st.rerun()
