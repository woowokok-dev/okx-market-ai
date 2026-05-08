import requests
import pandas as pd

BASE_URL = "https://www.okx.com/api/v5/market/candles"


def fetch_candles(inst_id="BTC-USDT", bar="1H", limit=100):
    params = {
        "instId": inst_id,
        "bar": bar,
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()["data"]

    df = pd.DataFrame(data, columns=[
        "ts", "open", "high", "low", "close",
        "vol", "volCcy", "volCcyQuote", "confirm"
    ])

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["vol"] = df["vol"].astype(float)

    return df[::-1]


def calculate_ema(df):
    df["EMA20"] = df["close"].ewm(span=20).mean()
    df["EMA50"] = df["close"].ewm(span=50).mean()
    return df


def calculate_rsi(df, period=14):
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df


def calculate_bollinger(df, window=20):
    df["MA20"] = df["close"].rolling(window).mean()
    std = df["close"].rolling(window).std()

    df["Upper"] = df["MA20"] + (2 * std)
    df["Lower"] = df["MA20"] - (2 * std)

    return df


def analyze():
    df = fetch_candles()

    df = calculate_ema(df)
    df = calculate_rsi(df)
    df = calculate_bollinger(df)
    df = calculate_kdj(df)
    df = calculate_support_resistance(df)
    
    latest = df.iloc[-1]

    print("Current Price:", latest["close"])
    print("EMA20:", latest["EMA20"])
    print("EMA50:", latest["EMA50"])
    print("RSI:", latest["RSI"])
    print("Upper Band:", latest["Upper"])
    print("Lower Band:", latest["Lower"])
    print("K:", latest["K"])
    print("D:", latest["D"])
    print("J:", latest["J"])
    print("Support:", latest["Support"])
    print("Resistance:", latest["Resistance"])


if __name__ == "__main__":
    analyze()

def calculate_kdj(df, n=9):
    low_min = df["low"].rolling(n).min()
    high_max = df["high"].rolling(n).max()

    rsv = (df["close"] - low_min) / (high_max - low_min) * 100

    df["K"] = rsv.ewm(com=2).mean()
    df["D"] = df["K"].ewm(com=2).mean()
    df["J"] = 3 * df["K"] - 2 * df["D"]

    return df

def calculate_support_resistance(df, window=20):
    support = df["low"].rolling(window).min()
    resistance = df["high"].rolling(window).max()

    df["Support"] = support
    df["Resistance"] = resistance

    return df
