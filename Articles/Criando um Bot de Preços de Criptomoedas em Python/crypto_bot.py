import requests
import schedule
import time

def get_crypto_price(crypto):
    try:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd,brl'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[crypto]['usd'], data[crypto]['brl']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter o preço de {crypto}: {e}")
        return None, None

def job():
    cryptos = ['bitcoin', 'ethereum', 'dogecoin']
    for crypto in cryptos:
        price_usd, price_brl = get_crypto_price(crypto)
        if price_usd is not None and price_brl is not None:
            print(f'O preço do {crypto.capitalize()} é ${price_usd:.2f} USD e R${price_brl:.2f} BRL')
    print('-----------------------------------')

# Agendar a tarefa para rodar a cada minuto
schedule.every(1).minutes.do(job)

print("Bot de preços de criptomoedas iniciado...")
while True:
    schedule.run_pending()
    time.sleep(1)