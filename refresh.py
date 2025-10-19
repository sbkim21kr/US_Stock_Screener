import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# 📁 Load tickers from tickers.csv
def load_tickers():
    try:
        df = pd.read_csv("tickers.csv")
        return df["Ticker"].dropna().tolist()
    except Exception as e:
        print(f"Error loading tickers.csv: {e}")
        return []

# 📊 Define Pearl Score logic
def calculate_pearl_score(eps, pe):
    if pd.isna(eps) or pd.isna(pe) or pe == 0:
        return 0
    return round((eps / pe) * 10, 2)

# 📥 Fetch stock data
def fetch_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            eps = info.get("trailingEps")
            pe = info.get("trailingPE")
            sector = info.get("sector", "N/A")
            score = calculate_pearl_score(eps, pe)
            data.append({
                "Ticker": ticker,
                "Sector": sector,
                "EPS": eps,
                "PE": pe,
                "Pearl Score": score
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
    return pd.DataFrame(data)

# 🗂️ Ensure data folder exists
os.makedirs("data", exist_ok=True)

# 🗓️ Generate filename
today = datetime.utcnow().strftime("%Y-%m-%d")
filename = f"data/pearl_scores_{today}.csv"

# 🚀 Run refresh
tickers = load_tickers()
if tickers:
    df = fetch_stock_data(tickers)
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
else:
    print("⚠️ No tickers found in tickers.csv")
