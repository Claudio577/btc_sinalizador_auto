import requests
import numpy as np
import re

# ============================
# 1. Buscar notícias da API
# ============================
def buscar_noticias(api_key):
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": api_key,
        "currencies": "BTC",
        "kind": "news",
        "public": "true"  # evita filtragem de resultados para usuários gratuitos
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [item['title'] for item in data.get('results', [])]
    else:
        print("Erro ao buscar notícias:", response.status_code, response.text)
        return ["Erro ao buscar notícias. Verifique sua API key."]

# ====================================
# 2. Analisar sentimentos simples
# ====================================
def analisar_sentimentos(noticias):
    palavras_positivas = ["alta", "subiu", "valorizou", "ganhou", "recorde", "positivo"]
    palavras_negativas = ["queda", "caiu", "desvalorizou", "perdeu", "baixa", "negativo"]

    sentimentos = []
    for noticia in noticias:
        texto = noticia.lower()
        score = 0
        for p in palavras_positivas:
            score += len(re.findall(rf"\b{p}\b", texto))
        for n in palavras_negativas:
            score -= len(re.findall(rf"\b{n}\b", texto))
        sentimentos.append(score)

    return sentimentos if sentimentos else [0]

# ====================================
# 3. Volatilidade real via CoinGecko
# ====================================
def obter_volatilidade_real():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": "2"}
        response = requests.get(url, params=params)
        dados = response.json()

        precos = [p[1] for p in dados["prices"][-24:]]  # últimas ~2h

        if len(precos) < 2:
            return 0.0

        preco_max = max(precos)
        preco_min = min(precos)
        preco_medio = np.mean(precos)

        volatilidade = (preco_max - preco_min) / preco_medio
        return round(volatilidade, 4)
    except Exception as e:
        print("Erro na volatilidade:", e)
        return 0.0

# ====================================
# 4. Tendência de curto prazo (~2h)
# ====================================
def obter_tendencia_btc():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": "2"}
        response = requests.get(url, params=params)
        dados = response.json()

        precos = [p[1] for p in dados["prices"][-24:]]  # últimas ~2h

        if len(precos) < 2:
            return 0.0

        preco_inicial = precos[0]
        preco_final = precos[-1]
        variacao = (preco_final - preco_inicial) / preco_inicial
        return round(variacao, 4)
    except Exception as e:
        print("Erro na tendência:", e)
        return 0.0

# ====================================
# 5. Classificação de risco
# ====================================
def classificar_risco(sentimentos, volatilidade, volume):
    media_sentimento = np.mean(sentimentos)

    if media_sentimento < -1 or volatilidade > 0.07:
        return "Alerta Vermelho - Mercado em risco", "🔴"
    elif media_sentimento < 1 or volatilidade > 0.04:
        return "Cuidado - Mercado instável", "🟡"
    else:
        return "Seguro - Ambiente favorável", "🟢"



