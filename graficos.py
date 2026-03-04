# graficos.py - Gráficos em tempo real para diagnóstico

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from collections import deque
import time

class GraficosTempoReal:
    """
    Gráficos em tempo real para diagnóstico automotivo
    - RPM, temperatura, pressão
    - Histórico de falhas
    - Tendências
    """
    
    def __init__(self, max_points=100):
        self.max_points = max_points
        self.historico = {
            'rpm': deque(maxlen=max_points),
            'temp': deque(maxlen=max_points),
            'stft': deque(maxlen=max_points),
            'ltft': deque(maxlen=max_points),
            'maf': deque(maxlen=max_points),
            'timestamps': deque(maxlen=max_points)
        }
    
    def add_reading(self, rpm, temp, stft, ltft, maf):
        """Adiciona uma leitura ao histórico"""
        self.historico['rpm'].append(rpm)
        self.historico['temp'].append(temp)
        self.historico['stft'].append(stft)
        self.historico['ltft'].append(ltft)
        self.historico['maf'].append(maf)
        self.historico['timestamps'].append(time.time())
    
    def render_dashboard_graficos(self):
        """Renderiza dashboard completo de gráficos"""
        
        st.markdown("## 📊 DASHBOARD DE DIAGNÓSTICO")
        
        # Grid de gráficos
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'RPM em Tempo Real',
                'Temperatura do Motor',
                'Short Term Fuel Trim',
                'Long Term Fuel Trim',
                'Fluxo de Ar (MAF)',
                'Correlação STFT/LTFT'
            ),
            specs=[
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": True}]
            ]
        )
        
        if len(self.historico['timestamps']) > 10:
            # Converter timestamps para segundos relativos
            t0 = self.historico['timestamps'][0]
            times = [t - t0 for t in self.historico['timestamps']]
            
            # RPM
            fig.add_trace(
                go.Scatter(
                    x=times,
                    y=list(self.historico['rpm']),
                    mode='lines',
                    name='RPM',
                    line=dict(color='#00ffff', width=2)
                ),
                row=1, col=1
            )
            
            # Temperatura
            fig.add_trace(
                go.Scatter(
                    x=times,
                    y=list(self.historico['temp']),
                    mode='lines',
                    name='Temperatura',
                    line=dict(color='#ff6600', width=2)
                ),
                row=1, col=2
            )
            
            # STFT
            fig.add_trace(
                go.Scatter(
                    x=times,
                    y=list(self.historico['stft']),
                    mode='lines',
                    name='STFT',
                    line=dict(color='#00ff00', width=2)
                ),
                row=2, col=1
            )
            
            # Adicionar linha de referência STFT
            fig.add_hline(y=0, line_dash="dash", line_color="#888", row=2, col=1)
            fig.add_hline(y=10, line_dash="dash", line_color="#ff0000", row=2, col=1)
            fig.add_hline(y=-10, line_dash="dash", line_color="#ff0000", row=2, col=1)
            
            # LTFT
            fig.add_trace(
                go.Scatter(
                    x=times,
                    y=list(self.historico['ltft']),
                    mode='lines',
                    name='LTFT',
                    line=dict(color='#ffff00', width=2)
                ),
                row=2, col=2
            )
            
            # Adicionar linha de referência LTFT
            fig.add_hline(y=0, line_dash="dash", line_color="#888", row=2, col=2)
            fig.add_hline(y=15, line_dash="dash", line_color="#ff0000", row=2, col=2)
            fig.add_hline(y=-15, line_dash="dash", line_color="#ff0000", row=2, col=2)
            
            # MAF
            fig.add_trace(
                go.Scatter(
                    x=times,
                    y=list(self.historico['maf']),
                    mode='lines',
                    name='MAF',
                    line=dict(color='#ff00ff', width=2)
                ),
                row=3, col=1
            )
            
            # Correlação STFT x LTFT (scatter)
            fig.add_trace(
                go.Scatter(
                    x=list(self.historico['stft']),
                    y=list(self.historico['ltft']),
                    mode='markers',
                    name='Correlação',
                    marker=dict(
                        color=list(self.historico['rpm']),
                        colorscale='Viridis',
                        showscale=True,
                        size=8
                    ),
                    text=[f"RPM: {rpm}" for rpm in self.historico['rpm']],
                    hoverinfo='text'
                ),
                row=3, col=2
            )
            
            # Linha de referência para correlação ideal
            fig.add_shape(
                type="line",
                x0=-20, y0=-20, x1=20, y1=20,
                line=dict(color="#888", dash="dash"),
                row=3, col=2
            )
        
        fig.update_layout(
            height=900,
            showlegend=True,
            paper_bgcolor='#0a0c10',
            plot_bgcolor='#1a1d24',
            font=dict(color='white'),
            legend=dict(font=dict(color='white'))
        )
        
        fig.update_xaxes(gridcolor='#333', gridwidth=1)
        fig.update_yaxes(gridcolor='#333', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas rápidas
        if len(self.historico['rpm']) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div style="background:#1a1d24; padding:15px; border-radius:5px;">
                    <span style="color:#888;">RPM Médio</span><br>
                    <span style="color:#00ffff; font-size:24px;">{np.mean(list(self.historico['rpm'])):.0f}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background:#1a1d24; padding:15px; border-radius:5px;">
                    <span style="color:#888;">Temp. Média</span><br>
                    <span style="color:#ff6600; font-size:24px;">{np.mean(list(self.historico['temp'])):.1f}°C</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background:#1a1d24; padding:15px; border-radius:5px;">
                    <span style="color:#888;">STFT Médio</span><br>
                    <span style="color:#00ff00; font-size:24px;">{np.mean(list(self.historico['stft'])):.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="background:#1a1d24; padding:15px; border-radius:5px;">
                    <span style="color:#888;">LTFT Médio</span><br>
                    <span style="color:#ffff00; font-size:24px;">{np.mean(list(self.historico['ltft'])):.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
