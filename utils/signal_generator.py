import pandas as pd
import os
import yaml
import json

# Load config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

PROCESSED_PATH = config["paths"]["processed_data"]
SIGNAL_PATH = config["paths"]["signals"]

def generate_signals(file_name):
    try:
        file_path = os.path.join(PROCESSED_PATH, file_name)
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)

        if df.empty or df.iloc[-1].isnull().any():
            raise ValueError(f"Data in {file_name} is incomplete or contains NaNs in the latest row.")

        latest = df.iloc[-1]

        # Extract needed values
        close_price = latest["close"]
        atr = latest["atr"]
        rsi = latest["rsi"]
        macd = latest["macd"]
        macd_signal = latest["macd_signal"]

        signal = {}

        # Basic signal logic
        if rsi < 30 and macd > macd_signal:
            signal["action"] = "buy"
        elif rsi > 70 and macd < macd_signal:
            signal["action"] = "sell"
        else:
            signal["action"] = "hold"

        # Risk management
        signal["entry"] = round(close_price, 5)
        signal["stop_loss"] = round(
            close_price - atr if signal["action"] == "buy" else close_price + atr, 5
        )
        signal["take_profit"] = round(
            close_price + 2 * atr if signal["action"] == "buy" else close_price - 2 * atr, 5
        )

        # Metadata
        signal["pair"] = file_name.replace(".csv", "")
        signal["rsi"] = round(rsi, 2)
        signal["macd"] = round(macd, 5)
        signal["macd_signal"] = round(macd_signal, 5)
        signal["atr"] = round(atr, 5)

        return signal

    except Exception as e:
        print(f"❌ Failed to generate signal for {file_name}: {e}")
        return None

def generate_all():
    if not os.path.exists(PROCESSED_PATH):
        print(f"⚠️ Processed data path does not exist: {PROCESSED_PATH}")
        return

    signals = []
    for file_name in os.listdir(PROCESSED_PATH):
        if file_name.endswith(".csv"):
            signal = generate_signals(file_name)
            if signal:
                signals.append(signal)

    if not signals:
        print("⚠️ No valid signals generated.")
        return

    os.makedirs(os.path.dirname(SIGNAL_PATH), exist_ok=True)
    with open(SIGNAL_PATH, "w") as f:
        json.dump(signals, f, indent=4)
    print(f"✅ Signals saved to {SIGNAL_PATH}")

if __name__ == "__main__":
    generate_all()
