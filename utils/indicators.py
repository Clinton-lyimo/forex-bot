import pandas as pd
import os
import yaml
import ta  # Technical Analysis library

# Load config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

RAW_PATH = config["paths"]["raw_data"]
PROCESSED_PATH = config["paths"]["processed_data"]

def calculate_indicators(file_name):
    file_path = os.path.join(RAW_PATH, file_name)
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # Ensure numeric types
    df = df.astype(float)

    # Add indicators
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"]).rsi()
    macd = ta.trend.MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    bollinger = ta.volatility.BollingerBands(close=df["close"])
    df["bb_high"] = bollinger.bollinger_hband()
    df["bb_low"] = bollinger.bollinger_lband()
    df["atr"] = ta.volatility.AverageTrueRange(high=df["high"], low=df["low"], close=df["close"]).average_true_range()

    # Save processed data
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    processed_file = os.path.join(PROCESSED_PATH, file_name)
    df.to_csv(processed_file)
    print(f"✅ Processed indicators saved to {processed_file}")

def process_all():
    for file_name in os.listdir(RAW_PATH):
        if file_name.endswith(".csv"):
            calculate_indicators(file_name)

if __name__ == "__main__":
    process_all()
