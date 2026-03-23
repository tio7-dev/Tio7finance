    with tab_mercado:
        # ... [Manter códigos anteriores] ...
        
        st.divider()
        st.subheader("🔔 Sentinela Tio 7: Alertas de Preço")
        
        c_alt1, c_alt2, c_alt3 = st.columns(3)
        
        with c_alt1:
            ativo_alerta = st.selectbox("Escolha o Ativo para Alerta", ["BTC-USD", "GC=F (Ouro)", "USDBRL=X"])
        with c_alt2:
            preco_alvo = st.number_input("Preço Alvo (Aviso se atingir)", value=60000.0)
        with c_alt3:
            condicao = st.radio("Avisar quando estiver:", ["Acima de", "Abaixo de"])

        # Lógica de Verificação em Tempo Real
        try:
            ticker_limpo = ativo_alerta.split(" ")[0] # Pega só o código (ex: GC=F)
            preco_agora = yf.Ticker(ticker_limpo).fast_info['last_price']
            
            disparou = False
            if condicao == "Acima de" and preco_agora >= preco_alvo:
                disparou = True
            elif condicao == "Abaixo de" and preco_agora <= preco_alvo:
                disparou = True
            
            if disparou:
                st.error(f"⚠️ **ALERTA DISPARADO!** O {ativo_alerta} está em {preco_agora:,.2f}. Hora de agir no cofre!")
                st.balloons() # Efeito visual de comemoração ou alerta
            else:
                st.info(f"Monitorando... Preço atual do {ativo_alerta}: **{preco_agora:,.2f}**")
        except:
            st.warning("Aguardando conexão com o mercado para validar alerta.")
