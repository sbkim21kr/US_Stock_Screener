import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# 🧮 Pearl Score formula
def calculate_pearl_score(eps, pe):
    return round((eps / pe) * 100, 2) if pe else 0

# 📥 Load tickers from tickers.csv
def get_tickers_from_csv():
    return pd.read_csv("tickers.csv")["Symbol"].dropna().tolist()

# 📊 Collect data
tickers = get_tickers_from_csv()
data = []

for ticker in tickers:
    try:
        info = yf.Ticker(ticker).info
        eps = info.get("trailingEps", 0)
        pe = info.get("trailingPE", 0)
        score = calculate_pearl_score(eps, pe)
        name = info.get("shortName", ticker)
        sector = info.get("sector", "Unknown")
        industry = info.get("industry", "Unknown")

        data.append({
            "Ticker": ticker,
            "Name": name,
            "EPS": eps,
            "PE": pe,
            "Pearl Score": score,
            "Sector": sector,
            "Industry": industry
        })
    except Exception as e:
        print(f"⚠️ Error fetching {ticker}: {e}")

# 🗂 Save to CSV
df = pd.DataFrame(data)
today = datetime.today().strftime("%Y-%m-%d")
os.makedirs("data", exist_ok=True)
df.to_csv(f"data/pearl_scores_{today}.csv", index=False)
print(f"✅ Saved: data/pearl_scores_{today}.csv")
