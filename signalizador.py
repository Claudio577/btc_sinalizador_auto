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
        "filter": "hot"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [item['title'] for item in data['results']]
    else:
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
# 3. Simulação da volatilidade
# ====================================
def obter_volatilidade_real():
    # Volatilidade simulada: entre 0.01 e 0.10
    return np.random.uniform(0.01, 0.10)

# ====================================
# 4. Classificação de risco
# ====================================
def classificar_risco(sentimentos, volatilidade, volume):
    media_sentimento = np.mean(sentimentos)

    if media_sentimento < -1 or volatilidade > 0.07:
        return "Alerta Vermelho - Mercado em risco", "🔴"
    elif media_sentimento < 1 or volatilidade > 0.04:
        return "Cuidado - Mercado instável", "🟡"
    else:
        return "Seguro - Ambiente favorável", "🟢"

