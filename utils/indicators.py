import pandas as pd
import os
import yaml
import ta #technical analysis library

#load the config file
with open("config/settings.yaml","r") as f:
    config = yaml.safe_load(f)

RAW_PATH = config["paths"]["raw_data"]
PROCESSED_PATH = config["paths"]["processed_data"]

def calculate_indicators(file_name):
    file_path = os.path.join(RAW_PATH, file_name)
    df = pd.read_csv(file_path,index_col=0,parse_dates=True)

    #Ensure numeric types
    df = df.astype(float)

    #add indicator
    df["rsi"] = ta.momentum.RSIIndicator(clos=df["Close"]).rsi()
    macd = ta.trend.MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"]