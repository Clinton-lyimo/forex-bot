# forex-bot

An AI-Powered Forex trading bot that analyzes market data, generates trading signals (entry, stop loss, take profit), and executes trades via MetaTrader 5.

## Features
- Real-Time Forex data fetching
- Technical Indicator analysis
- Machine Learning-based signal generation
- Automated trade execution

## Projet Structure
see `main.py` for orchestration logic. Each module is organized for clarity and scalability.

## setup
1. Install dependencies `pip install -r requirements.txt`
2. Configure API Keys in Keys in `config/settings.yaml`
3. Run the bot : `python main.py`

Great question—and you're absolutely right to pause and reflect on how everything we've built so far works together. Here's a clear and accurate breakdown of the **entire system**, what it does, and how you can use it in a real trading context.

---

## 🧠 **What We've Built So Far**

### ✅ 1. **Data Collection Module (`data_loader.py`)**
- **Purpose**: Fetches **daily Forex price data** (open, high, low, close) from **Alpha Vantage**.
- **How it works**:
  - You specify currency pairs (e.g., `EUR/USD`) in `settings.yaml`.
  - The script calls Alpha Vantage’s API and saves the data as CSV files in `data/raw/`.

---

### ✅ 2. **Indicator Calculation Module (`indicators.py`)**
- **Purpose**: Enhances raw price data with **technical indicators**.
- **Indicators used**:
  - **RSI**: Measures momentum (overbought/oversold).
  - **MACD & MACD Signal**: Trend-following indicators.
  - **Bollinger Bands**: Volatility and price range.
  - **ATR**: Average True Range for volatility and risk management.
- **Output**: Saves enriched data to `data/processed/`.

---

### ✅ 3. **Signal Generation Module (`signal_generator.py`)**
- **Purpose**: Analyzes the latest indicator values to generate **trading signals**.
- **Logic used**:
  - **Buy**: RSI < 30 and MACD > MACD Signal
  - **Sell**: RSI > 70 and MACD < MACD Signal
  - **Hold**: Otherwise
- **Risk Management**:
  - **Stop Loss**: 1× ATR
  - **Take Profit**: 2× ATR
- **Output**: Saves signals to `signals/latest_signals.json`

---

## 🔁 **How It All Works Together**

1. **Run `data_loader.py`** to fetch fresh market data.
2. **Run `indicators.py`** to calculate indicators on that data.
3. **Run `signal_generator.py`** to generate actionable trading signals.

Each module is **modular and testable**, meaning you can run them independently and inspect their outputs.

---

## 📈 **How You Can Use This in Trading**

### 🔹 Manual Trading
- Open `latest_signals.json`.
- Read the suggested **action**, **entry**, **stop loss**, and **take profit**.
- Place trades manually in your broker platform (e.g., MetaTrader 5).

### 🔹 Automated Trading (Next Step)
- Build an **execution module** (`mt5_bridge.py`) that:
  - Reads the signals.
  - Connects to MetaTrader 5 via its Python API.
  - Places trades automatically based on the signals.

---

## 🧪 Example Workflow

```bash
# Step 1: Fetch market data
python utils/data_loader.py

# Step 2: Calculate indicators
python utils/indicators.py

# Step 3: Generate signals
python utils/signal_generator.py

# Step 4: Review signals
cat signals/latest_signals.json
```

---
