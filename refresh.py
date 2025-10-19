import yfinance as yf
import pandas as pd
from datetime import datetime

# Load tickers from CSV
tickers_df = pd.read_csv("tickers.csv")
tickers = tickers_df["Ticker"].dropna().unique().tolist()

results = []

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        eps = info.get("forwardEps", 0)
        pe = info.get("forwardPE", 0)
        pearl_score = eps / pe if pe else 0

        results.append({
            "Ticker": ticker,
            "Pearl Score": round(pearl_score, 2),
            "EPS": eps,
            "PE": pe
        })

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

# Save with timestamp
filename = f"pearl_scores_{datetime.today().strftime('%Y-%m-%d')}.csv"
df = pd.DataFrame(results)
df.to_csv(filename, index=False)
