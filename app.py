import streamlit as st
from datetime import datetime
import numpy as np
from PIL import Image
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from signalizador import (
    buscar_noticias,
    analisar_sentimentos,
    classificar_risco,
    obter_volatilidade_real,
    obter_tendencia_btc
)

st.set_page_config(page_title="Sinalizador BTC", layout="centered")
st.title("🚦 Sinalizador de Risco - Bitcoin")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Botão para modo iniciante
modo_iniciante = st.checkbox("👶 Ativar Modo Iniciante", value=True)

# Campo da API
api_key = st.text_input("🔑 Insira sua API Key do CryptoPanic:", type="password")

if api_key:
    st_autorefresh(interval=60000, key="auto_refresh")

    with st.spinner("🔍 Coletando e analisando..."):
        noticias = buscar_noticias(api_key)
        sentimentos = analisar_sentimentos(noticias)
        volatilidade_real = obter_volatilidade_real()
        tendencia_pct = obter_tendencia_btc()
        volume = len(sentimentos)
        mensagem, emoji = classificar_risco(sentimentos, volatilidade_real, volume)

    # Escolher imagem do semáforo
    if "🔴" in emoji:
        imagem_risco = "images/semaforo_vermelho.jpeg"
    elif "🟡" in emoji:
        imagem_risco = "images/semaforo_amarelo.jpeg"
    elif "🟢" in emoji:
        imagem_risco = "images/semaforo_verde.jpeg"
    else:
        imagem_risco = "images/semaforo_verde.jpeg"

    image = Image.open(imagem_risco)
    st.image(image, caption="Status de Risco", use_container_width=True)

    # Explicação educativa (modo iniciante)
    if modo_iniciante:
        st.subheader("📘 Orientação para você")
        if "🔴" in emoji:
            st.warning("Evite operar agora. Notícias negativas e mercado instável.")
        elif "🟡" in emoji:
            st.info("Cautela. Espere confirmação da tendência antes de operar.")
        elif "🟢" in emoji:
            st.success("Ambiente favorável. Operar com disciplina e gerenciamento.")
        else:
            st.info("Análise inconclusiva. Acompanhe novas atualizações.")

    # Exibir métricas em colunas
    col1, col2 = st.columns(2)
    col1.metric("📊 Sentimento Médio", f"{np.mean(sentimentos):.2f}")
    col1.metric("📈 Tendência (2h)", f"{tendencia_pct*100:.2f}%")
    col2.metric("📉 Volatilidade Estimada", f"{volatilidade_real:.2%}")
    col2.metric("📰 Volume de Notícias", volume)

    # Mostrar últimas notícias
    st.subheader("📰 Últimas Notícias")
    for i, noticia in enumerate(noticias[:10], 1):
        st.markdown(f"**{i:02d}.** {noticia}")

    # Salvar histórico do sinal
    sinal = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risco": mensagem,
        "emoji": emoji,
        "sentimento": round(np.mean(sentimentos), 2),
        "volatilidade": round(volatilidade_real, 4),
        "tendencia": round(tendencia_pct, 4)
    }
    df = pd.DataFrame([sinal])
    try:
        df_antigo = pd.read_csv("sinais.csv")
        df_total = pd.concat([df_antigo, df], ignore_index=True)
    except:
        df_total = df
    df_total.to_csv("sinais.csv", index=False)

else:
    st.info("Para começar, insira sua chave da API do CryptoPanic.")


