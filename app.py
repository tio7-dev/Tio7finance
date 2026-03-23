import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO MOBILE ---
st.set_page_config(page_title="Tio 7 Mobile", layout="centered", page_icon="💰")

# --- LINK DA SUA PLANILHA (Cole o link do CSV aqui) ---
URL_SHEET = "COLE_AQUI_O_LINK_DO_CSV_PUBLICADO"

def carregar_dados():
    try:
        df = pd.read_csv(URL_SHEET)
        # Limpeza de nomes de colunas para evitar erros de síntese
        df.columns = [c.strip().capitalize() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Data', 'Categoria', 'Ticker', 'Valor_pago', 'Qtd', 'Tipo'])

# --- LOGIN ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 Cofre Tio 7</h2>", unsafe_allow_html=True)
    st.image("https://wikimedia.org", width=100)
    user = st.text_input("Usuário")
    pw = st.text_input("Senha", type="password")
    if st.button("ACESSAR COFRE", use_container_width=True):
        if user == "admin" and pw == "123":
            st.session_state.auth = True
            st.rerun()
else:
    # --- INTERFACE DO APP ---
    menu = st.tabs(["💰 Carteira", "📈 Mercado", "💡 Dicas"])
    
    with menu[0]:
        st.subheader("Meu Patrimônio")
        df = carregar_dados()
        
        if not df.empty:
            # Cálculo de Lucro Realizado
            resumo = []
            for t in df['Ticker'].unique():
                try:
                    p_atual = yf.Ticker(str(t)).fast_info['last_price']
                    dados = df[df['Ticker'] == t]
                    p_medio = (dados['Valor_pago'] * dados['Qtd']).sum() / dados['Qtd'].sum()
                    lucro = (p_atual - p_medio) * dados['Qtd'].sum()
                    resumo.append({"Ativo": t, "Preço": f"{p_atual:,.2f}", "Lucro": f"{lucro:,.2f}"})
                except: continue
            
            st.table(pd.DataFrame(resumo))
            
        st.info("📲 Para adicionar dados, abra o app Google Sheets no celular.")

    with menu[1]:
        st.subheader("Preços em Tempo Real")
        ativos = ["BTC-USD", "GC=F", "SI=F", "USDBRL=X", "EURBRL=X"]
        for a in ativos:
            try:
                val = yf.Ticker(a).fast_info['last_price']
                st.metric(a, f"{val:,.2f}")
            except: pass

    with menu[2]:
        st.success("💎 Dica Expert 2026")
        st.write("Mantenha o foco em **Solana** e **Ouro** este mês. O mercado está volátil, proteja seu capital!")

    if st.button("SAIR"):
        st.session_state.auth = False
        st.rerun()
