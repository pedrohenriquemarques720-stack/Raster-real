# app.py - RASTHER JPO - Sistema Profissional de Diagnóstico Automotivo
# Versão completa e autônoma - Sem dependências externas

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime
import json

# =============================================
# INICIALIZAÇÃO DA SESSÃO (DEVE SER A PRIMEIRA COISA)
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
        'ecu': '---',
        'protocol': '---',
        'version': '---',
        'km': '---'
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
        'maf': 0,
        'o2': 0.78
    }
    st.session_state.log = []
    st.session_state.diagnosis_result = None
    st.session_state.analysis_result = None

# Configuração da página
st.set_page_config(
    page_title="RASTHER JPO - Scanner Profissional",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    
    /* Connection Bar */
    .connection-bar {
        background: #1a1d24;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ff6600;
        margin-bottom: 20px;
        display: flex;
        gap: 30px;
        flex-wrap: wrap;
    }
    
    .conn-item {
        display: flex;
        flex-direction: column;
    }
    
    .conn-label {
        color: #888;
        font-size: 10px;
        text-transform: uppercase;
    }
    
    .conn-value {
        color: #ff6600;
        font-size: 14px;
        font-weight: bold;
        font-family: monospace;
    }
    
    /* Cards de dados */
    .metric-card {
        background: #1a1d24;
        border: 1px solid #ff6600;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 5px 0;
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
        transition: 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 20px rgba(255,102,0,0.3) !important;
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
        font-family: monospace;
    }
    
    .dtc-desc {
        color: #ccc;
        font-size: 12px;
        margin-left: 10px;
    }
    
    /* Cards de diagnóstico IA */
    .ia-card {
        background: linear-gradient(135deg, #001a33, #002244);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00ffff;
        margin: 10px 0;
    }
    
    .ia-title {
        color: #00ffff;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 1px solid #00ffff;
        padding-bottom: 5px;
    }
    
    .ia-prob {
        margin: 10px 0;
    }
    
    .prob-bar {
        height: 6px;
        background: #333;
        border-radius: 3px;
        margin-top: 3px;
    }
    
    .prob-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff00, #ffff00, #ff0000);
        border-radius: 3px;
    }
    
    /* Cards de orientação ao cliente */
    .cliente-card {
        background: #1a2a33;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00ffff;
    }
    
    .cliente-titulo {
        color: #00ffff;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .cliente-sub {
        color: #ffaa00;
        font-size: 14px;
        font-weight: bold;
        margin: 10px 0 5px 0;
    }
    
    .cliente-texto {
        color: #ccc;
        font-size: 13px;
        line-height: 1.5;
    }
    
    .orcamento-box {
        background: #004400;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
    }
    
    .orcamento-valor {
        color: #00ff00;
        font-size: 24px;
        font-weight: bold;
    }
    
    .orcamento-detalhe {
        color: #888;
        font-size: 12px;
    }
    
    /* Menu de navegação */
    .nav-menu {
        display: flex;
        gap: 10px;
        margin: 0 0 20px 0;
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
        transition: 0.3s;
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
    
    /* Info row */
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
        font-weight: bold;
        font-family: monospace;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# =============================================
# FUNÇÕES AUXILIARES
# =============================================

def get_explicacao_cliente(dtc_code):
    """Retorna explicação em linguagem simples para o cliente"""
    explicacoes = {
        'P0301': {
            'problema': 'Falha de ignição no cilindro 1',
            'explicacao': 'O motor está com problema na queima de combustível no primeiro cilindro. Isso causa perda de potência, aumento no consumo e pode danificar o catalisador.',
            'causa': 'Velas desgastadas, bobina com defeito ou bicos injetores sujos.',
            'solucao': 'Substituir a bobina de ignição e as velas do cilindro 1.',
            'urgencia': 'ALTA',
            'valor': 450.00,
            'tempo': '1.5 horas',
            'componentes': ['Bobina', 'Vela', 'Injetor'],
            'probs': [85, 45, 20]
        },
        'P0420': {
            'problema': 'Catalisador ineficiente',
            'explicacao': 'O sistema de filtragem de poluição não está funcionando corretamente, aumentando a emissão de gases poluentes.',
            'causa': 'Catalisador entupido ou sondas lambda com defeito.',
            'solucao': 'Substituir o catalisador e verificar as sondas lambda.',
            'urgencia': 'MÉDIA',
            'valor': 1850.00,
            'tempo': '3 horas',
            'componentes': ['Catalisador', 'Sonda O2'],
            'probs': [70, 30]
        },
        'P0171': {
            'problema': 'Mistura pobre de combustível',
            'explicacao': 'O motor está recebendo ar demais ou combustível de menos, causando marcha lenta irregular e perda de desempenho.',
            'causa': 'Vazamento de vácuo, sensor MAF sujo ou pressão de combustível baixa.',
            'solucao': 'Limpar sensor MAF e verificar mangueiras de vácuo.',
            'urgencia': 'MÉDIA',
            'valor': 380.00,
            'tempo': '1 hora',
            'componentes': ['Sensor MAF', 'Vazamento', 'Pressão'],
            'probs': [60, 30, 10]
        }
    }
    return explicacoes.get(dtc_code, {
        'problema': 'Falha detectada',
        'explicacao': 'O scanner detectou uma anomalia que requer diagnóstico.',
        'causa': 'Pode ser sensor com defeito ou problema elétrico.',
        'solucao': 'Realizar diagnóstico detalhado.',
        'urgencia': 'MÉDIA',
        'valor': 250.00,
        'tempo': '1 hora',
        'componentes': ['Geral'],
        'probs': [100]
    })

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
    vehicle_display = f"{st.session_state.vehicle_info.get('model', '---')} {st.session_state.vehicle_info.get('year', '')}"
    protocol_display = st.session_state.vehicle_info.get('protocol', '---')
    ecu_display = st.session_state.vehicle_info.get('ecu', '---')
    
    st.markdown(f"""
    <div class="connection-bar">
        <div class="conn-item">
            <span class="conn-label">VEÍCULO</span>
            <span class="conn-value">{vehicle_display}</span>
        </div>
        <div class="conn-item">
            <span class="conn-label">PROTOCOLO</span>
            <span class="conn-value">{protocol_display}</span>
        </div>
        <div class="conn-item">
            <span class="conn-label">ECU</span>
            <span class="conn-value">{ecu_display}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not st.session_state.connected:
        if st.button("🔌 CONECTAR", key="connect_btn"):
            with st.spinner("Conectando ao veículo..."):
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
        if st.button("🔌 DESCONECTAR", key="disconnect_btn"):
            st.session_state.connected = False
            st.session_state.dtcs = []
            st.session_state.diagnosis_result = None
            st.session_state.analysis_result = None
            st.session_state.log.append("❌ Desconectado")
            st.rerun()

# =============================================
# MENU DE NAVEGAÇÃO
# =============================================
pages = ["Dashboard", "Diagnóstico IA", "Controle Ativo", "Visualizador 3D", "Relatórios"]

st.markdown('<div class="nav-menu">', unsafe_allow_html=True)
for page in pages:
    active_class = "active" if st.session_state.current_page == page else ""
    if st.button(page, key=f"nav_{page}"):
        st.session_state.current_page = page
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# ATUALIZA DADOS SIMULADOS (se conectado)
# =============================================
if st.session_state.connected:
    st.session_state.live_data = {
        'rpm': random.randint(750, 3500),
        'speed': random.randint(0, 120),
        'temp': random.randint(82, 98),
        'battery': round(12 + random.random() * 2, 1),
        'engine_load': random.randint(15, 55),
        'stft': round(random.uniform(-5, 15), 1),
        'ltft': round(random.uniform(-8, 18), 1),
        'maf': round(2.5 + random.random() * 3, 1),
        'o2': round(0.7 + random.random() * 0.2, 2)
    }

# =============================================
# CONTEÚDO DAS PÁGINAS
# =============================================

if st.session_state.current_page == "Dashboard":
    st.markdown("## 📊 PAINEL PRINCIPAL")
    
    # Métricas principais
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-row"><span class="info-label">Fabricante:</span> <span class="info-value">{st.session_state.vehicle_info['manufacturer']}</span></div>
        <div class="info-row"><span class="info-label">Modelo:</span> <span class="info-value">{st.session_state.vehicle_info['model']}</span></div>
        <div class="info-row"><span class="info-label">Ano:</span> <span class="info-value">{st.session_state.vehicle_info['year']}</span></div>
        <div class="info-row"><span class="info-label">Motor:</span> <span class="info-value">{st.session_state.vehicle_info['engine']}</span></div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-row"><span class="info-label">VIN:</span> <span class="info-value">{st.session_state.vehicle_info['vin']}</span></div>
        <div class="info-row"><span class="info-label">ECU:</span> <span class="info-value">{st.session_state.vehicle_info['ecu']}</span></div>
        <div class="info-row"><span class="info-label">Protocolo:</span> <span class="info-value">{st.session_state.vehicle_info['protocol']}</span></div>
        <div class="info-row"><span class="info-label">KM:</span> <span class="info-value">{st.session_state.vehicle_info['km']}</span></div>
        """, unsafe_allow_html=True)
    
    # Códigos de falha
    st.markdown("### ⚠️ CÓDIGOS DE FALHA")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔍 ESCANEAR FALHAS", use_container_width=True):
            with st.spinner("Escaneando sistemas..."):
                time.sleep(2)
                st.session_state.dtcs = [
                    {'code': 'P0301', 'desc': 'Falha de ignição no cilindro 1', 'system': 'Motor', 'severity': 'critical'},
                    {'code': 'P0420', 'desc': 'Catalisador ineficiente', 'system': 'Emissões', 'severity': 'warning'},
                    {'code': 'P0171', 'desc': 'Mistura pobre', 'system': 'Combustível', 'severity': 'warning'}
                ]
                st.session_state.log.append("🔍 Escaneamento concluído")
    
    with col_btn2:
        if st.button("✅ LIMPAR FALHAS", use_container_width=True):
            st.session_state.dtcs = []
            st.session_state.diagnosis_result = None
            st.session_state.log.append("✅ Falhas limpas")
    
    if st.session_state.dtcs:
        for dtc in st.session_state.dtcs:
            color = "#ff0000" if dtc['severity'] == 'critical' else "#ffaa00"
            st.markdown(f"""
            <div class="dtc-card" style="border-left-color: {color};">
                <span class="dtc-code">{dtc['code']}</span>
                <span class="dtc-desc">{dtc['desc']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum código de falha encontrado")

elif st.session_state.current_page == "Diagnóstico IA":
    st.markdown("## 🤖 DIAGNÓSTICO INTELIGENTE")
    
    # Layout em duas colunas para análise técnica e orientação
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 ANÁLISE TÉCNICA")
        
        if st.session_state.dtcs:
            dtc_options = [dtc['code'] for dtc in st.session_state.dtcs]
            selected_dtc = st.selectbox("Selecione o código de falha", dtc_options)
            
            if st.button("🔮 ANALISAR COM IA", use_container_width=True):
                with st.spinner("IA analisando dados em tempo real..."):
                    time.sleep(2)
                    explicacao = get_explicacao_cliente(selected_dtc)
                    st.session_state.analysis_result = {
                        'dtc': selected_dtc,
                        'componentes': explicacao['componentes'],
                        'probs': explicacao['probs'],
                        'valor': explicacao['valor'],
                        'tempo': explicacao['tempo'],
                        'urgencia': explicacao['urgencia'],
                        'problema': explicacao['problema'],
                        'causa': explicacao['causa'],
                        'solucao': explicacao['solucao'],
                        'explicacao': explicacao['explicacao']
                    }
            
            if st.session_state.get('analysis_result'):
                res = st.session_state.analysis_result
                
                st.markdown('<div class="ia-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="ia-title">📊 ANÁLISE - {res["dtc"]}</div>', unsafe_allow_html=True)
                
                for i, comp in enumerate(res['componentes']):
                    prob = res['probs'][i] if i < len(res['probs']) else 50
                    st.markdown(f"""
                    <div class="ia-prob">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:white;">{comp}</span>
                            <span style="color:#00ffff;">{prob}%</span>
                        </div>
                        <div class="prob-bar">
                            <div class="prob-fill" style="width:{prob}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Execute um escaneamento primeiro na página Dashboard")
    
    with col2:
        st.markdown("### 👤 ORIENTAÇÃO AO CLIENTE")
        
        if st.session_state.get('analysis_result'):
            res = st.session_state.analysis_result
            cor_urgencia = "#ff0000" if res['urgencia'] == 'ALTA' else "#ffaa00"
            
            st.markdown(f"""
            <div class="cliente-card">
                <div class="cliente-titulo">🔍 DIAGNÓSTICO SIMPLIFICADO</div>
                
                <div class="cliente-sub">⚠️ Problema Detectado:</div>
                <div class="cliente-texto">{res['problema']}</div>
                
                <div class="cliente-sub">📝 Explicação:</div>
                <div class="cliente-texto">{res['explicacao']}</div>
                
                <div class="cliente-sub">🔧 Causa Provável:</div>
                <div class="cliente-texto">{res['causa']}</div>
                
                <div class="cliente-sub">✅ Solução:</div>
                <div class="cliente-texto">{res['solucao']}</div>
                
                <div class="orcamento-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="orcamento-valor">R$ {res['valor']:.2f}</div>
                            <div class="orcamento-detalhe">Tempo: {res['tempo']}</div>
                        </div>
                        <div style="color:{cor_urgencia}; font-weight:bold;">
                            {res['urgencia']}
                        </div>
                    </div>
                </div>
                
                <!-- BOTÕES HORIZONTAIS (CORRIGIDO) -->
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button style="flex: 1; background: #25D366; color: white; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;" 
                            onclick="alert('Contato enviado para oficina parceira!')">
                        📱 WHATSAPP
                    </button>
                    <button style="flex: 1; background: #ff6600; color: white; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;" 
                            onclick="alert('Orçamento gerado com sucesso!')">
                        💰 ORÇAMENTO
                    </button>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 10px;">
                    <button style="flex: 1; background: #0047ab; color: white; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;" 
                            onclick="alert('Agendamento realizado!')">
                        📅 AGENDAR
                    </button>
                    <button style="flex: 1; background: #00ff00; color: black; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;" 
                            onclick="alert('Relatório enviado por e-mail!')">
                        📧 ENVIAR
                    </button>
                </div>
                
                <div style="text-align: center; margin-top: 15px; color: #888; font-size: 11px;">
                    Oficinas parceiras próximas:
                </div>
                <div style="display: flex; gap: 10px; margin-top: 5px; font-size: 11px; color: #00ffff; justify-content: center;">
                    <span>Auto Silva (3km)</span>
                    <span>•</span>
                    <span>Oficina do Zé (5km)</span>
                    <span>•</span>
                    <span>Mecânica Rápida (8km)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="cliente-card">
                <div class="cliente-titulo">👋 BEM-VINDO</div>
                <div class="cliente-texto" style="text-align:center;">
                    Selecione um código de falha e execute a análise<br>
                    para gerar uma orientação para seu cliente.
                </div>
                <div style="text-align:center; margin-top:20px;">
                    <span style="font-size:48px;">🔧</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Execute um escaneamento primeiro na página Dashboard")
    
    with col2:
        st.markdown("### 👤 ORIENTAÇÃO AO CLIENTE")
        
        if st.session_state.get('analysis_result'):
            res = st.session_state.analysis_result
            cor_urgencia = "#ff0000" if res['urgencia'] == 'ALTA' else "#ffaa00"
            
            st.markdown(f"""
            <div class="cliente-card">
                <div class="cliente-titulo">🔍 DIAGNÓSTICO SIMPLIFICADO</div>
                
                <div class="cliente-sub">⚠️ Problema Detectado:</div>
                <div class="cliente-texto">{res['problema']}</div>
                
                <div class="cliente-sub">📝 Explicação:</div>
                <div class="cliente-texto">{res['explicacao']}</div>
                
                <div class="cliente-sub">🔧 Causa Provável:</div>
                <div class="cliente-texto">{res['causa']}</div>
                
                <div class="cliente-sub">✅ Solução:</div>
                <div class="cliente-texto">{res['solucao']}</div>
                
                <div class="orcamento-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="orcamento-valor">R$ {res['valor']:.2f}</div>
                            <div class="orcamento-detalhe">Tempo: {res['tempo']}</div>
                        </div>
                        <div style="color:{cor_urgencia}; font-weight:bold;">
                            {res['urgencia']}
                        </div>
                    </div>
                </div>
                
                <button style="width:100%; background:#25D366; color:white; padding:12px; border:none; border-radius:8px; margin-top:15px; font-weight:bold; cursor:pointer;" onclick="alert('Contato enviado para oficina parceira!')">
                    📱 ENCAMINHAR PARA OFICINA
                </button>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="cliente-card">
                <div class="cliente-titulo">👋 BEM-VINDO</div>
                <div class="cliente-texto" style="text-align:center;">
                    Selecione um código de falha e execute a análise<br>
                    para gerar uma orientação para seu cliente.
                </div>
                <div style="text-align:center; margin-top:20px;">
                    <span style="font-size:48px;">🔧</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Controle Ativo":
    st.markdown("## ⚡ CONTROLE ATIVO DO MOTOR")
    
    if not st.session_state.connected:
        st.warning("⚠️ Conecte-se a um veículo para usar o Controle Ativo")
    else:
        # Métricas em tempo real (STFT, LTFT, MAF)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:10px; border-radius:5px; text-align:center;">
                <div style="color:#888;">STFT</div>
                <div style="color:#00ffff; font-size:24px;">{st.session_state.live_data['stft']}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:10px; border-radius:5px; text-align:center;">
                <div style="color:#888;">LTFT</div>
                <div style="color:#00ffff; font-size:24px;">{st.session_state.live_data['ltft']}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:10px; border-radius:5px; text-align:center;">
                <div style="color:#888;">MAF</div>
                <div style="color:#00ffff; font-size:24px;">{st.session_state.live_data['maf']} g/s</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 Ajustes Manuais")
            
            fuel_trim = st.slider("Ajuste de Mistura (%)", -25.0, 25.0, 0.0, 0.5)
            if st.button("APLICAR AJUSTE DE MISTURA", use_container_width=True):
                st.success(f"✅ Ajuste aplicado: {fuel_trim}%")
                st.session_state.log.append(f"⚡ Ajuste de mistura: {fuel_trim}%")
            
            idle_rpm = st.slider("RPM de Marcha Lenta", 600, 1200, 800, 10)
            if st.button("APLICAR RPM", use_container_width=True):
                st.success(f"✅ RPM ajustado para {idle_rpm}")
                st.session_state.log.append(f"⚡ RPM ajustado: {idle_rpm}")
        
        with col2:
            st.markdown("### ⚙️ Ajustes Avançados")
            
            inj_time = st.slider("Tempo de Injeção (ms)", 1.5, 8.0, 3.5, 0.1)
            if st.button("APLICAR INJEÇÃO", use_container_width=True):
                st.success(f"✅ Injeção ajustada: {inj_time}ms")
                st.session_state.log.append(f"⚡ Injeção ajustada: {inj_time}ms")
            
            if st.button("🔄 RESET FLEX FUEL", use_container_width=True):
                st.success("✅ Flex Fuel resetado com sucesso")
                st.session_state.log.append("🔄 Reset Flex Fuel")

elif st.session_state.current_page == "Visualizador 3D":
    st.markdown("## 🔍 VISUALIZADOR 3D DE COMPONENTES")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background:#111; border:1px solid #00ffff; border-radius:10px; padding:20px; height:450px; display:flex; align-items:center; justify-content:center;">
            <div style="text-align:center;">
                <svg width="500" height="400" viewBox="0 0 500 400">
                    <rect x="150" y="100" width="200" height="150" fill="#333" stroke="#00ffff" stroke-width="2" rx="10"/>
                    <circle cx="250" cy="150" r="20" fill="#ffaa00" stroke="#ffff00" stroke-width="3"/>
                    <text x="235" y="155" fill="black" font-size="12">BOB</text>
                    <line x1="250" y1="150" x2="300" y2="80" stroke="#ffff00" stroke-width="2" stroke-dasharray="5,3"/>
                    <text x="310" y="70" fill="#ffff00" font-size="12">Componente</text>
                </svg>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.get('analysis_result'):
            st.markdown("""
            <div class="info-panel" style="background:#1a1d24; padding:15px; border-radius:10px; border:1px solid #00ffff;">
                <h4 style="color:#00ffff;">Informações</h4>
                <p><strong>Localização:</strong> Cabeçote do motor</p>
                <p><strong>Função:</strong> Ignição</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Execute um diagnóstico para ver componentes")

elif st.session_state.current_page == "Relatórios":
    st.markdown("## 📋 RELATÓRIOS E LOGS")
    
    st.markdown("### 📄 Últimas atividades")
    
    if st.session_state.log:
        for i, log_entry in enumerate(st.session_state.log[-15:]):
            st.code(log_entry)
    else:
        st.info("Nenhum registro encontrado")
    
    if st.button("📥 EXPORTAR RELATÓRIO", use_container_width=True):
        st.success("✅ Relatório exportado com sucesso!")

# =============================================
# BOTTOM BAR
# =============================================
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.session_state.log:
        st.caption(f"📌 Último: {st.session_state.log[-1]}")
    else:
        st.caption("📌 Sistema pronto")

with col2:
    st.caption(f"⏱️ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} • RASTHER JPO v1.0")

# =============================================
# ATUALIZAÇÃO AUTOMÁTICA
# =============================================
if st.session_state.connected:
    time.sleep(1)
    st.rerun()

