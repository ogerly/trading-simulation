import requests
import pandas as pd

# Daten-Cache für Preisdaten
price_data_cache = {}

def get_price_history(coin_id, vs_currency='usd', days=90):
    if (coin_id, days) in price_data_cache:
        return price_data_cache[(coin_id, days)]
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {'vs_currency': vs_currency, 'days': days, 'interval': 'daily'}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Daten für {coin_id}: HTTP {response.status_code}")
        return None
    data = response.json()
    if 'prices' not in data:
        print(f"API-Antwort für {coin_id} enthält keine 'prices'-Daten.")
        return None
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', f'{coin_id}_price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    price_data_cache[(coin_id, days)] = df
    return df

def get_top_gainers_and_losers():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'price_change_percentage_24h_desc',
        'per_page': 10,
        'page': 1,
        'price_change_percentage': '24h'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Fehler beim Abrufen der Top Gainers.")
        return [], []
    gainers = response.json()

    params['order'] = 'price_change_percentage_24h_asc'
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Fehler beim Abrufen der Top Losers.")
        return gainers, []
    losers = response.json()

    return gainers, losers
