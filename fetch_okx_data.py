import requests
import json

BASE_URL = "https://www.okx.com/api/v5/market/ticker"


def fetch_ticker(inst_id):
    params = {"instId": inst_id}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["data"][0]
    else:
        print("Error:", response.status_code)
        return None


def display_market_data(symbol):
    data = fetch_ticker(symbol)

    if data:
        print(f"\n=== {symbol} ===")
        print("Last Price:", data["last"])
        print("24h High:", data["high24h"])
        print("24h Low:", data["low24h"])
        print("24h Volume:", data["vol24h"])


if __name__ == "__main__":
    display_market_data("BTC-USDT")
    display_market_data("ETH-USDT")
