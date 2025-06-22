import streamlit as st
from datetime import datetime
import numpy as np
from PIL import Image
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt

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

modo_iniciante = st.checkbox("👶 Ativar Modo Iniciante", value=True)
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

    col1, col2 = st.columns(2)
    col1.metric("📊 Sentimento Médio", f"{np.mean(sentimentos):.2f}")
    col1.metric("📈 Tendência (2h)", f"{tendencia_pct*100:.2f}%")
    col2.metric("📉 Volatilidade Estimada", f"{volatilidade_real:.2%}")
    col2.metric("📰 Volume de Notícias", volume)

    # Exibir as últimas 20 notícias
    st.subheader("📰 Últimas Notícias")
    for i, noticia in enumerate(noticias, 1):
        st.markdown(f"**{i:02d}.** {noticia}")

    # Salvar histórico de sinais
    sinal = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risco": mensagem,
        "emoji": emoji,
        "sentimento": round(np.mean(sentimentos), 2),
        "volatilidade": round(volatilidade_real, 4),
        "tendencia": round(tendencia_pct, 4)
    }

    df = pd.DataFrame([sinal])
    historico_path = "sinais.csv"

    try:
        df_antigo = pd.read_csv(historico_path)
        df_total = pd.concat([df_antigo, df], ignore_index=True)
    except:
        df_total = df

    df_total.to_csv(historico_path, index=False)

    # Mostrar últimos 5 sinais
    st.subheader("📅 Últimos 5 Sinais")
    ultimos = df_total.tail(5).iloc[::-1]
    for _, row in ultimos.iterrows():
        st.markdown(f"{row['emoji']} **{row['risco']}** - {row['timestamp']}")

    # Gráfico de tendência
    try:
        emoji_map = {"🔴": 0, "🟡": 1, "🟢": 2}
        df_total["valor_risco"] = df_total["emoji"].map(emoji_map)

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(df_total["timestamp"].tail(30), df_total["valor_risco"].tail(30), marker="o")
        ax.set_title("Tendência dos Sinais")
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(["🔴", "🟡", "🟢"])
        ax.set_xticks(df_total["timestamp"].tail(30)[::5])  # reduz ticks
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        plt.tight_layout()
        st.image(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e}")

else:
    st.info("Para começar, insira sua chave da API do CryptoPanic.")



