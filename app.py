import streamlit as st
from datetime import datetime
import numpy as np
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Importa funções do arquivo signalizador.py
from signalizador import (
    buscar_noticias,
    analisar_sentimentos,
    classificar_risco,
    obter_volatilidade_real,
    obter_tendencia_btc
)

# Configurações do app
st.set_page_config(page_title="Sinalizador BTC", layout="centered")
st.title("🚦 Sinalizador de Risco - Bitcoin")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Campo para inserir API key
api_key = st.text_input("🔑 Insira sua API Key do CryptoPanic:", type="password")

# Só executa se a API key for preenchida
if api_key:
    # Atualiza automaticamente a cada 60 segundos
    st_autorefresh(interval=60000, key="auto_refresh")

    with st.spinner("🔍 Coletando e analisando..."):
        # Coleta e análise
        noticias = buscar_noticias(api_key)
        sentimentos = analisar_sentimentos(noticias)
        volatilidade_real = obter_volatilidade_real()
        tendencia_pct = obter_tendencia_btc()
        volume = len(sentimentos)
        mensagem, emoji = classificar_risco(sentimentos, volatilidade_real, volume)

    # Escolher imagem do semáforo com base no emoji
    if "🔴" in emoji:
        imagem_risco = "images/semaforo_vermelho.jpeg"
    elif "🟡" in emoji:
        imagem_risco = "images/semaforo_amarelo.jpeg"
    elif "🟢" in emoji:
        imagem_risco = "images/semaforo_verde.jpeg"
    else:
        imagem_risco = "images/semaforo_verde.jpeg"  # fallback

    # Exibir imagem do semáforo logo após a chave da API
    image = Image.open(imagem_risco)
    st.image(image, caption="Status de Risco", use_container_width=True)

    # Mensagem educativa adaptada ao risco
    st.subheader("📘 Orientação para você")
    if "🔴" in emoji:
        st.warning("Evite operar agora. Notícias negativas e mercado instável.")
    elif "🟡" in emoji:
        st.info("Cautela. Espere confirmação da tendência antes de operar.")
    elif "🟢" in emoji:
        st.success("Ambiente favorável. Operar com disciplina e gerenciamento.")
    else:
        st.info("Análise inconclusiva. Acompanhe novas atualizações.")

    # Mostrar métricas abaixo da orientação
    st.metric("Sentimento Médio", f"{np.mean(sentimentos):.2f}")
    st.metric("Volatilidade Estimada", f"{volatilidade_real:.2%}")
    st.metric("Tendência (2h)", f"{tendencia_pct*100:.2f}%")
    st.metric("Volume de Notícias", volume)

    # Mostrar as últimas notícias
    st.subheader("📰 Últimas Notícias")
    for i, noticia in enumerate(noticias[:10], 1):
        st.markdown(f"**{i:02d}.** {noticia}")
else:
    st.info("Para começar, insira sua chave da API do CryptoPanic.")


