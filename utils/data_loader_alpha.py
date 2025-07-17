import requests
import yaml
import os
import pandas as pd

# Load Config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

API_KEY = config["api"]["key"]
PAIRS = config["trading"]["pairs"]
RAW_PATH = config["paths"]["raw_data"]

def fetch_forex_data(pair):
    try:
        from_symbol, to_symbol = pair.strip().split("/")
    except ValueError:
        print(f"Invalid pair format: {pair}")
        return

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=FX_DAILY"
        f"&from_symbol={from_symbol}&to_symbol={to_symbol}"
        f"&apikey={API_KEY}&outputsize=compact"
    )

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "Time Series FX (Daily)" in data:
                df = pd.DataFrame.from_dict(data["Time Series FX (Daily)"], orient="index")
                df = df.rename(columns={
                    "1. open": "open",
                    "2. high": "high",
                    "3. low": "low",
                    "4. close": "close"
                })
                df.index = pd.to_datetime(df.index)
                df = df.sort_index()
                os.makedirs(RAW_PATH, exist_ok=True)
                filename = f"{from_symbol}_{to_symbol}.csv"
                file_path = os.path.join(RAW_PATH, filename)
                df.to_csv(file_path)
                print(f"✅ Saved {pair} data to {file_path}")
            elif "Note" in data:
                print(f"🔁 API limit reached: {data['Note']}")
            elif "Error Message" in data:
                print(f"❌ Error from API: {data['Error Message']}")
            else:
                print(f"⚠️ Unexpected response for {pair}: {data}")
        else:
            print(f"❌ Failed to fetch data for {pair}: HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching data for {pair}: {e}")


def fetch_all():
    for pair in PAIRS:
        fetch_forex_data(pair)

if __name__ == "__main__":
    fetch_all()
