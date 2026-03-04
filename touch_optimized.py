# touch_optimized.py - Otimizações para tela touch

import streamlit as st

def apply_touch_optimizations():
    """Aplica otimizações para tela touch de 7" """
    
    st.markdown("""
    <style>
        /* Aumentar tamanho dos botões para touch */
        .stButton > button {
            min-height: 60px !important;
            font-size: 18px !important;
            margin: 5px 0 !important;
        }
        
        /* Aumentar sliders */
        .stSlider > div > div > div {
            height: 40px !important;
        }
        
        /* Aumentar selects */
        .stSelectbox > div > div {
            min-height: 50px !important;
        }
        
        /* Espaçamento entre elementos */
        .element-container {
            margin: 10px 0 !important;
        }
        
        /* Fonte maior para métricas */
        .metric-value {
            font-size: 48px !important;
        }
        
        .metric-label {
            font-size: 16px !important;
        }
        
        /* Botões de navegação maiores */
        .nav-btn {
            padding: 15px 25px !important;
            font-size: 16px !important;
        }
        
        /* Esconder scrollbars (navegação por toque) */
        ::-webkit-scrollbar {
            width: 0px;
            background: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

def create_touch_keyboard():
    """Cria teclado virtual para entrada de dados"""
    
    st.markdown("""
    <div style="background:#1a1d24; padding:20px; border-radius:10px; margin:10px 0;">
        <div style="display:grid; grid-template-columns:repeat(10,1fr); gap:5px;">
            <button style="padding:15px;">1</button>
            <button style="padding:15px;">2</button>
            <button style="padding:15px;">3</button>
            <button style="padding:15px;">4</button>
            <button style="padding:15px;">5</button>
            <button style="padding:15px;">6</button>
            <button style="padding:15px;">7</button>
            <button style="padding:15px;">8</button>
            <button style="padding:15px;">9</button>
            <button style="padding:15px;">0</button>
        </div>
        <div style="display:grid; grid-template-columns:repeat(7,1fr); gap:5px; margin-top:5px;">
            <button style="padding:15px; grid-column:span2;">Q</button>
            <button style="padding:15px;">W</button>
            <button style="padding:15px;">E</button>
            <button style="padding:15px;">R</button>
            <button style="padding:15px;">T</button>
            <button style="padding:15px;">Y</button>
            <button style="padding:15px;">U</button>
            <button style="padding:15px;">I</button>
            <button style="padding:15px;">O</button>
            <button style="padding:15px;">P</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
