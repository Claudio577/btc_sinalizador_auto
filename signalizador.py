import requests
import numpy as np
import re

# ... (demais funções continuam iguais)

# ====================================
# Volatilidade real via CoinGecko
# ====================================
def obter_volatilidade_real():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": "1", "interval": "hourly"}
        response = requests.get(url, params=params)
        dados = response.json()

        # Preços das últimas 2 horas
        precos = [p[1] for p in dados["prices"][-2:]]
        if len(precos) < 2:
            return 0.0  # fallback

        preco_max = max(precos)
        preco_min = min(precos)
        preco_medio = np.mean(precos)

        volatilidade = (preco_max - preco_min) / preco_medio
        return volatilidade
    except:
        return 0.0  # fallback em caso de erro

