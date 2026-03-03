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
    
    # COLUNA DIREITA - DTCs (APENAS NO DASHBOARD)
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
            for dtc in st.session_state.dtcs:
                status_class = "critical" if dtc['severity'] == 'critical' else "warning" if dtc['severity'] == 'warning' else ""
                
                st.markdown(f"""
                <div class="system-card {status_class}">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="system-name">{dtc['system']}</span>
                        <span class="dtc-code">{dtc['code']}</span>
                    </div>
                    <div style="font-size:11px; color:#ccc; margin-top:5px;">{dtc['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#1a1d24; padding:20px; border-radius:10px; text-align:center; color:#666;">
                Nenhum código de falha encontrado
            </div>
            """, unsafe_allow_html=True)

# =============================================
# CONTROLE ATIVO (TUNING) - COM PIDs BRASILEIROS E TESTES
# =============================================
elif st.session_state.current_page == "Controle Ativo":
    st.markdown("## ⚡ CONTROLE ATIVO DO MOTOR")
    st.markdown("### Ajuste de Parâmetros em Tempo Real (UDS Service 0x2E)")
    
    # Verifica se está conectado e se o ECU Control existe
    if not st.session_state.connected:
        st.warning("⚠️ Conecte-se a um veículo para usar o Controle Ativo")
    elif st.session_state.ecu_control is None:
        st.error("❌ Módulo ECU Control não disponível")
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
        
        # Métricas em tempo real (TESTES - APENAS NO CONTROLE ATIVO)
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
            lambda_val = st.session_state.ecu_control.live_data.get('lambda', 1.02) if hasattr(st.session_state.ecu_control, 'live_data') else 1.02
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">LAMBDA</div>
                <div class="metric-number">{lambda_val:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">SONDA O2</div>
                <div class="metric-number">{st.session_state.live_data['o2']:.3f}V</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Parâmetros adicionais (STFT, LTFT, MAF - APENAS NO CONTROLE ATIVO)
        col_extra1, col_extra2, col_extra3 = st.columns(3)
        with col_extra1:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:8px; border-radius:5px; text-align:center;">
                <div style="color:#888; font-size:10px;">STFT</div>
                <div style="color:#00ffff; font-size:14px;">{st.session_state.live_data.get('short_term_fuel_trim', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_extra2:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:8px; border-radius:5px; text-align:center;">
                <div style="color:#888; font-size:10px;">LTFT</div>
                <div style="color:#00ffff; font-size:14px;">{st.session_state.live_data.get('long_term_fuel_trim', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_extra3:
            st.markdown(f"""
            <div style="background:#1a1d24; padding:8px; border-radius:5px; text-align:center;">
                <div style="color:#888; font-size:10px;">MAF</div>
                <div style="color:#00ffff; font-size:14px;">{st.session_state.live_data.get('maf', 0)} g/s</div>
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
        
        # =========================================
        # PIDs Brasileiros
        # =========================================
        with st.expander("🇧🇷 COMANDOS ESPECÍFICOS BRASIL"):
            st.markdown("### Comandos exclusivos para veículos nacionais")
            
            tab_vw, tab_fiat, tab_gm = st.tabs(["Volkswagen", "Fiat", "GM"])
            
            with tab_vw:
                st.markdown("#### Motor EA111/EA211 (Gol, Polo, Virtus)")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 RESET FLEX FUEL VW", key="vw_reset_flex", use_container_width=True):
                        with st.spinner("Resetando adaptação flex..."):
                            resp = st.session_state.ecu_control.reset_vw_flex(force=not safety.safe)
                            if resp.success:
                                st.success("✅ Adaptação flex resetada!")
                            else:
                                st.error(f"❌ Falha: {resp.message}")
                
                with col2:
                    if st.button("🔄 RESET MARCHA LENTA", key="vw_reset_idle", use_container_width=True):
                        with st.spinner("Resetando adaptação de marcha lenta..."):
                            resp = st.session_state.ecu_control.write_parameter_brasil(0xF102, 1, force=not safety.safe)
                            if resp.success:
                                st.success("✅ Marcha lenta resetada!")
                            else:
                                st.error(f"❌ Falha: {resp.message}")
            
            with tab_fiat:
                st.markdown("#### Motor Fire/Firefly (Uno, Mobi, Argo)")
                
                idle_rpm_fiat = st.slider(
                    "RPM de Marcha Lenta (Fiat)",
                    min_value=650,
                    max_value=950,
                    value=800,
                    step=10,
                    key="fiat_idle"
                )
                
                if st.button("⚡ APLICAR RPM FIAT", key="fiat_apply", use_container_width=True):
                    with st.spinner("Ajustando marcha lenta..."):
                        resp = st.session_state.ecu_control.adjust_fiat_idle(idle_rpm_fiat, force=not safety.safe)
                        if resp.success:
                            st.success(f"✅ Marcha lenta ajustada para {idle_rpm_fiat} RPM!")
                        else:
                            st.error(f"❌ Falha: {resp.message}")
            
            with tab_gm:
                st.markdown("#### Motor CSS Prime/Ecotec (Onix, Tracker)")
                
                if st.button("🔄 RESET DETONAÇÃO GM", key="gm_reset_knock", use_container_width=True):
                    with st.spinner("Resetando aprendizado de detonação..."):
                        resp = st.session_state.ecu_control.reset_gm_knock(force=not safety.safe)
                        if resp.success:
                            st.success("✅ Aprendizado de detonação resetado!")
                        else:
                            st.error(f"❌ Falha: {resp.message}")
        
        # Otimização Automática
        st.markdown("---")
        st.markdown("### 🎯 OTIMIZAÇÃO AUTOMÁTICA")
        
        lambda_atual = st.session_state.ecu_control.live_data.get('lambda', 1.02) if hasattr(st.session_state.ecu_control, 'live_data') else 1.02
        
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            st.markdown(f"""
            <div style="background:#001a33; padding:10px; border-radius:5px; text-align:center;">
                <span style="color:#888;">Lambda Atual</span><br>
                <span style="color:#00ffff; font-size:28px; font-weight:bold;">{lambda_atual:.3f}</span>
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
        # Container do visualizador 3D com altura fixa
        st.markdown('<div class="viewer-3d-fix">', unsafe_allow_html=True)
        st.markdown('<div class="engine-3d-fix">', unsafe_allow_html=True)
        
        # SVG do motor
        st.markdown("""
        <svg class="engine-svg" viewBox="0 0 800 500" preserveAspectRatio="xMidYMid meet">
            <!-- Bloco do motor -->
            <rect x="200" y="150" width="400" height="200" fill="#444" stroke="#00ffff" stroke-width="2" rx="10"/>
            
            <!-- Tampa do motor -->
            <rect x="250" y="100" width="300" height="50" fill="#555" stroke="#888" stroke-width="1" rx="5"/>
            
            <!-- Cilindros -->
            <rect x="280" y="180" width="50" height="120" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
            <text x="295" y="250" fill="white" font-size="12" font-family="Roboto Mono">C1</text>
            
            <rect x="360" y="180" width="50" height="120" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
            <text x="375" y="250" fill="white" font-size="12">C2</text>
            
            <rect x="440" y="180" width="50" height="120" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
            <text x="455" y="250" fill="white" font-size="12">C3</text>
            
            <rect x="520" y="180" width="50" height="120" fill="#666" stroke="#888" stroke-width="1" rx="3"/>
            <text x="535" y="250" fill="white" font-size="12">C4</text>
            
            <!-- Componente destacado (se houver) -->
            <circle cx="305" cy="120" r="20" fill="#ffaa00" stroke="#ffff00" stroke-width="3" filter="url(#glow)"/>
            <text x="295" y="125" fill="black" font-size="10" font-family="Roboto Mono" text-anchor="middle">BOB</text>
            
            <!-- Seta indicadora -->
            <line x1="305" y1="120" x2="250" y2="80" stroke="#ffff00" stroke-width="2" stroke-dasharray="5,3"/>
            <text x="200" y="70" fill="#ffff00" font-size="12" font-family="Roboto Mono">Componente afetado</text>
            
            <!-- Efeito de brilho -->
            <defs>
                <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceAlpha" stdDeviation="4"/>
                    <feMerge>
                        <feMergeNode in="offsetblur" />
                        <feMergeNode in="SourceGraphic" />
                    </feMerge>
                </filter>
            </defs>
        </svg>
        """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Botões de controle 3D
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            if st.button("🔄 ROTACIONAR", key="rotate_3d", use_container_width=True):
                st.session_state.log.append("> Rotacionando modelo 3D")
        with col_b:
            if st.button("🔍 ZOOM IN", key="zoom_in", use_container_width=True):
                st.session_state.log.append("> Zoom in")
        with col_c:
            if st.button("🔎 ZOOM OUT", key="zoom_out", use_container_width=True):
                st.session_state.log.append("> Zoom out")
        with col_d:
            if st.button("🎯 CENTRALIZAR", key="center", use_container_width=True):
                st.session_state.log.append("> Centralizando visualização")
    
    with col2:
        if st.session_state.selected_component:
            comp = st.session_state.selected_component
            
            # Dicionário de informações por componente
            comp_info = {
                'COIL': {
                    'nome': 'Bobina de Ignição',
                    'localizacao': 'Cabeçote do motor, sobre as velas de ignição',
                    'pinagem': [
                        {'pino': '1', 'funcao': '12V', 'cor': 'Vermelho'},
                        {'pino': '2', 'funcao': 'GND', 'cor': 'Preto'},
                        {'pino': '3', 'funcao': 'Sinal', 'cor': 'Verde'}
                    ]
                },
                'SPARK_PLUG': {
                    'nome': 'Vela de Ignição',
                    'localizacao': 'Cabeçote, dentro dos cilindros',
                    'pinagem': [
                        {'pino': '1', 'funcao': 'Alta tensão', 'cor': '---'}
                    ]
                },
                'INJECTOR': {
                    'nome': 'Injetor de Combustível',
                    'localizacao': 'Trilho de combustível, próximo aos cilindros',
                    'pinagem': [
                        {'pino': '1', 'funcao': '12V', 'cor': 'Azul'},
                        {'pino': '2', 'funcao': 'Sinal', 'cor': 'Marrom'}
                    ]
                },
                'O2_SENSOR': {
                    'nome': 'Sonda Lambda',
                    'localizacao': 'Sistema de escapamento, antes do catalisador',
                    'pinagem': [
                        {'pino': '1', 'funcao': 'Sinal', 'cor': 'Preto'},
                        {'pino': '2', 'funcao': 'GND', 'cor': 'Cinza'},
                        {'pino': '3', 'funcao': '12V', 'cor': 'Vermelho'},
                        {'pino': '4', 'funcao': 'GND', 'cor': 'Marrom'}
                    ]
                },
                'MAF_SENSOR': {
                    'nome': 'Sensor MAF',
                    'localizacao': 'Duto de ar, após o filtro de ar',
                    'pinagem': [
                        {'pino': '1', 'funcao': '5V', 'cor': 'Vermelho'},
                        {'pino': '2', 'funcao': 'Sinal', 'cor': 'Amarelo'},
                        {'pino': '3', 'funcao': 'GND', 'cor': 'Preto'}
                    ]
                },
                'CKP_SENSOR': {
                    'nome': 'Sensor de Rotação',
                    'localizacao': 'Bloco do motor, próximo ao volante do motor',
                    'pinagem': [
                        {'pino': '1', 'funcao': 'Sinal +', 'cor': 'Branco'},
                        {'pino': '2', 'funcao': 'Sinal -', 'cor': 'Cinza'},
                        {'pino': '3', 'funcao': 'Shield', 'cor': 'Transparente'}
                    ]
                },
                'CATALYST': {
                    'nome': 'Catalisador',
                    'localizacao': 'Sistema de escapamento, sob o veículo',
                    'pinagem': [
                        {'pino': 'N/A', 'funcao': 'Componente mecânico', 'cor': '---'}
                    ]
                }
            }
            
            info = comp_info.get(comp, {
                'nome': comp,
                'localizacao': 'Localização não disponível',
                'pinagem': []
            })
            
            # Exibe informações do componente
            st.markdown('<div class="info-panel">', unsafe_allow_html=True)
            st.markdown(f'<div class="info-title">{info["nome"]}</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="info-section">', unsafe_allow_html=True)
            st.markdown('<div class="info-label">📍 LOCALIZAÇÃO</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-content">{info["localizacao"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if info['pinagem']:
                st.markdown('<div class="info-section">', unsafe_allow_html=True)
                st.markdown('<div class="info-label">🔌 PINAGEM</div>', unsafe_allow_html=True)
                st.markdown('<div class="pin-grid">', unsafe_allow_html=True)
                
                for pino in info['pinagem']:
                    st.markdown(f"""
                    <div class="pin-item">
                        <div class="pin-number">{pino['pino']}</div>
                        <div class="pin-function">{pino['funcao']}</div>
                        <div class="pin-wire">{pino['cor']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            # Mensagem quando nenhum componente está selecionado
            st.markdown("""
            <div class="no-component">
                <div class="no-component-icon">
                    <i class="fas fa-cube"></i>
                </div>
                <div class="no-component-title">NENHUM COMPONENTE SELECIONADO</div>
                <div class="no-component-text">
                    Execute um diagnóstico na página "Controle Ativo"<br>
                    ou "Diagnóstico IA" para visualizar componentes
                </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================
# DIAGNÓSTICO IA - COM EXPLICAÇÃO PARA CLIENTE
# =============================================
elif st.session_state.current_page == "Diagnóstico IA":
    st.markdown("## 🤖 DIAGNÓSTICO AVANÇADO COM IA")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.session_state.dtcs:
            dtc_options = [dtc['code'] for dtc in st.session_state.dtcs]
            selected_dtc = st.selectbox("Selecione o DTC para análise", dtc_options)
            
            if st.button("🔮 EXECUTAR ANÁLISE", use_container_width=True):
                with st.spinner("IA analisando dados em tempo real..."):
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
            
            # Resultado técnico
            if st.session_state.diagnosis_result:
                res = st.session_state.diagnosis_result
                st.markdown('<div class="copilot-card-modern">', unsafe_allow_html=True)
                st.markdown(f'<div class="copilot-title-modern">📊 ANÁLISE TÉCNICA - {res["dtc"]}</div>', unsafe_allow_html=True)
                
                for p in res['probabilities'][:3]:
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
        else:
            st.info("Execute um escaneamento primeiro na página Dashboard")
    
    with col2:
        # Explicação para o cliente (sempre visível)
        st.markdown("### 👤 O QUE DIZER AO CLIENTE")
        
        if st.session_state.diagnosis_result and st.session_state.dtcs:
            dtc_atual = st.session_state.diagnosis_result.get('dtc', st.session_state.dtcs[0]['code'])
            explicacao = get_explicacao_cliente(dtc_atual)
            
            st.markdown(f"""
            <div class="explicacao-card">
                <div class="explicacao-titulo">🔍 DIAGNÓSTICO SIMPLIFICADO</div>
                
                <div class="explicacao-subtitulo">⚠️ Problema Detectado:</div>
                <div class="explicacao-texto">{explicacao['problema']}</div>
                
                <div class="explicacao-subtitulo">📝 Explicação para o Cliente:</div>
                <div class="explicacao-texto">{explicacao['explicacao']}</div>
                
                <div class="explicacao-subtitulo">🔧 Possível Causa:</div>
                <div class="explicacao-texto">{explicacao['causa']}</div>
                
                <div class="explicacao-subtitulo">✅ Solução Recomendada:</div>
                <div class="explicacao-texto">{explicacao['solucao']}</div>
                
                <div class="explicacao-orcamento">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #888;">Valor estimado</div>
                            <div class="explicacao-valor">R$ {explicacao['valor_estimado']:.2f}</div>
                            <div style="color: #888; font-size: 12px;">Tempo: {explicacao['tempo_estimado']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: {'#ff0000' if explicacao['urgencia'] == 'ALTA' else '#ffaa00'}; font-weight: bold;">
                                Urgência: {explicacao['urgencia']}
                            </div>
                        </div>
                    </div>
                </div>
                
                <button class="botao-contato" onclick="alert('Contato enviado para a oficina parceira mais próxima!')">
                    📱 ENCAMINHAR PARA OFICINA PARCEIRA
                </button>
                <div style="text-align: center; margin-top: 10px; color: #888; font-size: 11px;">
                    Oficinas parceiras: Auto Mecânica Silva (3km) • Oficina do Zé (5km) • Mecânica Rápida (8km)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="explicacao-card">
                <div class="explicacao-titulo">👋 BEM-VINDO, MECÂNICO!</div>
                <div class="explicacao-texto" style="text-align: center;">
                    Selecione um DTC na coluna ao lado e execute a análise<br>
                    para gerar uma explicação simplificada para o seu cliente.
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <span style="font-size: 48px;">🔧</span>
                </div>
                <div style="color: #888; text-align: center; margin-top: 10px;">
                    Com este recurso, você pode explicar<br>
                    problemas complexos de forma simples
                </div>
            </div>
            """, unsafe_allow_html=True)

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
# BOTTOM BAR (aparece em todas as telas)
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
