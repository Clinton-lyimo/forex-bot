import MetaTrader5 as mt5
import pandas as pd
import os
import yaml

# Load configuration
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

PAIRS = config["trading"]["pairs"]
RAW_PATH = config["paths"]["raw_data"]
TIMEFRAME = config["trading"].get("timeframe", "H1")
BAR_COUNT = config["trading"].get("bar_count", 100)

# Map timeframe string to MT5 constant
TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1
}

def fetch_mt5_data(pair):
    if not mt5.initialize():
        print(f"❌ Failed to initialize MT5 for {pair}")
        return

    try:
        symbol = pair.replace("/", "")
        if not mt5.symbol_select(symbol, True):
            print(f"⚠️ Failed to select symbol {symbol}. It might not be available in your broker.")
            return

        timeframe = TIMEFRAME_MAP.get(TIMEFRAME.upper(), mt5.TIMEFRAME_H1)
        bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, BAR_COUNT)

        if bars is None or len(bars) == 0:
            print(f"⚠️ No data returned for {pair}")
            return

        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        df = df[['open', 'high', 'low', 'close']]

        os.makedirs(RAW_PATH, exist_ok=True)
        file_path = os.path.join(RAW_PATH, f"{symbol}.csv")
        df.to_csv(file_path)
        print(f"✅ Saved {pair} data to {file_path}")

    except Exception as e:
        print(f"❌ Error fetching data for {pair}: {e}")

    finally:
        mt5.shutdown()

def fetch_all():
    for pair in PAIRS:
        fetch_mt5_data(pair)

if __name__ == "__main__":
    fetch_all()
