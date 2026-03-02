# Dentro da seção "Controle Ativo", adicione:

with st.expander("🇧🇷 COMANDOS ESPECÍFICOS BRASIL"):
    st.markdown("### Comandos exclusivos para veículos nacionais")
    
    tab_vw, tab_fiat, tab_gm = st.tabs(["Volkswagen", "Fiat", "GM"])
    
    with tab_vw:
        st.markdown("#### Motor EA111/EA211 (Gol, Polo, Virtus)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 RESET FLEX FUEL", key="vw_reset_flex", use_container_width=True):
                with st.spinner("Resetando adaptação flex..."):
                    resp = st.session_state.ecu_control.reset_vw_flex()
                    if resp.success:
                        st.success("✅ Adaptação flex resetada!")
                    else:
                        st.error(f"❌ Falha: {resp.message}")
        
        with col2:
            if st.button("🔄 RESET MARCHA LENTA", key="vw_reset_idle", use_container_width=True):
                with st.spinner("Resetando adaptação de marcha lenta..."):
                    resp = st.session_state.ecu_control.write_parameter_brasil(0xF102, 1)
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
        
        if st.button("⚡ APLICAR RPM", key="fiat_apply", use_container_width=True):
            with st.spinner("Ajustando marcha lenta..."):
                resp = st.session_state.ecu_control.adjust_fiat_idle(idle_rpm_fiat)
                if resp.success:
                    st.success(f"✅ Marcha lenta ajustada para {idle_rpm_fiat} RPM!")
                else:
                    st.error(f"❌ Falha: {resp.message}")
    
    with tab_gm:
        st.markdown("#### Motor CSS Prime/Ecotec (Onix, Tracker)")
        
        if st.button("🔄 RESET DETONAÇÃO", key="gm_reset_knock", use_container_width=True):
            with st.spinner("Resetando aprendizado de detonação..."):
                resp = st.session_state.ecu_control.reset_gm_knock()
                if resp.success:
                    st.success("✅ Aprendizado de detonação resetado!")
                else:
                    st.error(f"❌ Falha: {resp.message}")
