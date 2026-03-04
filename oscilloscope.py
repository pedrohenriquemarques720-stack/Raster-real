# oscilloscope.py - Osciloscópio automotivo em tempo real

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from collections import deque
from datetime import datetime

class OsciloscopioAutomotivo:
    """
    Osciloscópio profissional para diagnóstico automotivo
    - 4 canais simultâneos
    - Zoom e pan interativos
    - Trigger ajustável
    - Salvar formas de onda
    """
    
    def __init__(self, max_points=1000):
        self.max_points = max_points
        self.data = {
            'CH1': deque(maxlen=max_points),  # Sonda Lambda
            'CH2': deque(maxlen=max_points),  # Sensor de Rotação
            'CH3': deque(maxlen=max_points),  # Injetor
            'CH4': deque(maxlen=max_points),  # Bobina
            'time': deque(maxlen=max_points)
        }
        self.time_base = 0.01  # 10ms por divisão
        self.volts_per_div = {'CH1': 1, 'CH2': 5, 'CH3': 12, 'CH4': 50}
        self.trigger_channel = 'CH1'
        self.trigger_level = 0.5
        self.running = False
        self.sampling_rate = 1000  # Hz
        
    def start_acquisition(self):
        """Inicia aquisição de dados"""
        self.running = True
        self.start_time = time.time()
        
    def stop_acquisition(self):
        """Para aquisição de dados"""
        self.running = False
    
    def add_sample(self, ch1, ch2, ch3, ch4):
        """Adiciona uma amostra aos buffers"""
        current_time = time.time() - self.start_time
        self.data['CH1'].append(ch1)
        self.data['CH2'].append(ch2)
        self.data['CH3'].append(ch3)
        self.data['CH4'].append(ch4)
        self.data['time'].append(current_time)
    
    def simulate_signal(self):
        """Simula sinais para teste (quando não conectado ao veículo)"""
        t = time.time()
        return (
            0.5 + 0.4 * np.sin(2 * np.pi * 5 * t),  # Sonda Lambda
            2.5 + 2.5 * np.sin(2 * np.pi * 50 * t), # Sensor Rotação
            12 * (0.5 + 0.5 * np.sin(2 * np.pi * 100 * t)), # Injetor
            300 * (0.5 + 0.5 * np.sin(2 * np.pi * 20 * t))  # Bobina
        )
    
    def render_oscilloscope(self):
        """Renderiza o osciloscópio no Streamlit"""
        
        st.markdown("## 📈 OSCILOSCÓPIO AUTOMOTIVO (4 CANAIS)")
        
        # Controles
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("### ⏱️ BASE DE TEMPO")
            self.time_base = st.select_slider(
                "ms/div",
                options=[1, 2, 5, 10, 20, 50, 100],
                value=10
            )
        
        with col2:
            st.markdown("### 🎯 TRIGGER")
            self.trigger_channel = st.selectbox(
                "Canal",
                ['CH1', 'CH2', 'CH3', 'CH4', 'AUTO']
            )
            self.trigger_level = st.slider("Nível (V)", -10.0, 10.0, 0.5, 0.1)
        
        with col3:
            st.markdown("### 📊 VOLTS/DIV")
            for ch in ['CH1', 'CH2', 'CH3', 'CH4']:
                self.volts_per_div[ch] = st.number_input(
                    f"{ch} (V/div)",
                    min_value=0.1,
                    max_value=100.0,
                    value=self.volts_per_div[ch],
                    step=0.1,
                    key=f"volts_{ch}"
                )
        
        with col4:
            st.markdown("### 🎮 CONTROLE")
            if st.button("▶️ INICIAR", use_container_width=True):
                self.start_acquisition()
            if st.button("⏹️ PARAR", use_container_width=True):
                self.stop_acquisition()
            if st.button("💾 SALVAR", use_container_width=True):
                self.save_waveform()
            if st.button("🔄 LIMPAR", use_container_width=True):
                self.clear_all_channels()
        
        st.markdown("---")
        
        # Gráfico principal
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(
                'CH1 - Sonda Lambda (0-1V)',
                'CH2 - Sensor de Rotação (0-5V)',
                'CH3 - Sinal de Injeção (0-12V)',
                'CH4 - Bobina de Ignição (0-400V)'
            )
        )
        
        # Cores dos canais
        colors = ['#00ffff', '#ffff00', '#ff6600', '#ff00ff']
        
        if len(self.data['time']) > 10:
            times = list(self.data['time'])
            
            for i, ch in enumerate(['CH1', 'CH2', 'CH3', 'CH4']):
                fig.add_trace(
                    go.Scatter(
                        x=times,
                        y=list(self.data[ch]),
                        mode='lines',
                        name=ch,
                        line=dict(color=colors[i], width=2)
                    ),
                    row=i+1, col=1
                )
                
                # Linha de trigger
                if self.trigger_channel == ch:
                    fig.add_hline(
                        y=self.trigger_level,
                        line_dash="dash",
                        line_color="red",
                        row=i+1, col=1
                    )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            paper_bgcolor='#0a0c10',
            plot_bgcolor='#1a1d24',
            font=dict(color='white')
        )
        
        fig.update_xaxes(gridcolor='#333', gridwidth=1)
        fig.update_yaxes(gridcolor='#333', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Painel de informações
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background:#1a1d24; padding:10px; border-radius:5px; border-left:3px solid #00ffff;">
                <span style="color:#888;">CH1 - Sonda Lambda</span><br>
                <span style="color:#00ffff; font-size:20px;">0.78 V</span><br>
                <span style="color:#888;">Frequência: 5 Hz</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background:#1a1d24; padding:10px; border-radius:5px; border-left:3px solid #ffff00;">
                <span style="color:#888;">CH2 - Sensor Rotação</span><br>
                <span style="color:#ffff00; font-size:20px;">2.45 V</span><br>
                <span style="color:#888;">Frequência: 50 Hz</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background:#1a1d24; padding:10px; border-radius:5px; border-left:3px solid #ff6600;">
                <span style="color:#888;">CH3 - Injeção</span><br>
                <span style="color:#ff6600; font-size:20px;">12.0 V</span><br>
                <span style="color:#888;">Duty Cycle: 45%</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background:#1a1d24; padding:10px; border-radius:5px; border-left:3px solid #ff00ff;">
                <span style="color:#888;">CH4 - Bobina</span><br>
                <span style="color:#ff00ff; font-size:20px;">280 V</span><br>
                <span style="color:#888;">Tempo de carga: 3.5ms</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Modo de aquisição (loop)
        if self.running:
            ch1, ch2, ch3, ch4 = self.simulate_signal()
            self.add_sample(ch1, ch2, ch3, ch4)
            time.sleep(1/self.sampling_rate)
            st.rerun()
    
    def save_waveform(self):
        """Salva a forma de onda atual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"osc_waveform_{timestamp}.csv"
        
        df = pd.DataFrame({
            'time': list(self.data['time']),
            'CH1': list(self.data['CH1']),
            'CH2': list(self.data['CH2']),
            'CH3': list(self.data['CH3']),
            'CH4': list(self.data['CH4'])
        })
        df.to_csv(filename, index=False)
        st.success(f"✅ Forma de onda salva: {filename}")
    
    def clear_all_channels(self):
        """Limpa todos os canais"""
        for ch in ['CH1', 'CH2', 'CH3', 'CH4', 'time']:
            self.data[ch].clear()
        st.success("✅ Todos os canais limpos")
