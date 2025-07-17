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
    try:
        file_path = os.path.join(RAW_PATH, file_name)
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)

        # Clean and validate
        required_cols = ["open", "high", "low", "close"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required price columns in {file_name}")

        df = df.dropna(subset=required_cols)
        df[required_cols] = df[required_cols].astype(float)

        # Calculate indicators
        df["rsi"] = ta.momentum.RSIIndicator(close=df["close"]).rsi()

        macd = ta.trend.MACD(close=df["close"])
        df["macd"] = macd.macd()
        df["macd_signal"] = macd.macd_signal()

        bollinger = ta.volatility.BollingerBands(close=df["close"])
        df["bb_high"] = bollinger.bollinger_hband()
        df["bb_low"] = bollinger.bollinger_lband()

        atr = ta.volatility.AverageTrueRange(
            high=df["high"], low=df["low"], close=df["close"]
        )
        df["atr"] = atr.average_true_range()

        # Save processed data
        os.makedirs(PROCESSED_PATH, exist_ok=True)
        output_file = os.path.join(PROCESSED_PATH, file_name)
        df.to_csv(output_file)
        print(f"✅ Processed indicators saved to {output_file}")

    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")

def process_all():
    if not os.path.exists(RAW_PATH):
        print(f"⚠️ Raw data path does not exist: {RAW_PATH}")
        return

    for file_name in os.listdir(RAW_PATH):
        if file_name.endswith(".csv"):
            calculate_indicators(file_name)

if __name__ == "__main__":
    process_all()
