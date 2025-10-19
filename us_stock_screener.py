import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time
from io import StringIO
from datetime import datetime, timedelta

st.set_page_config(page_title="U.S. Pearl Finder", layout="wide")

# -----------------------------
# Static Ticker List (Top 50 S&P 500)
# -----------------------------
@st.cache_data
def get_sp500_tickers():
    return [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "BRK.B", "UNH", "JNJ",
        "V", "PG", "JPM", "MA", "HD", "XOM", "LLY", "MRK", "ABBV", "PEP",
        "KO", "AVGO", "ADBE", "COST", "MCD", "WMT", "CRM", "BAC", "TMO", "ACN",
        "CVX", "NFLX", "TXN", "ABT", "INTC", "LIN", "AMD", "NEE", "NKE", "DHR",
        "QCOM", "HON", "UNP", "PM", "AMGN", "LOW", "UPS", "MS", "ORCL", "SBUX"
    ]

# -----------------------------
# Stock Data Fetching Function
# -----------------------------
@st.cache_data
def fetch_stock_data(tickers):
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            eps = info.get("trailingEps", 0)
            volume = info.get("averageVolume", 0)
            pe = info.get("trailingPE", 0)
            sector = info.get("sector", "Unknown")
            industry = info.get("industry", "Unknown")
            market_cap = info.get("marketCap", 0)
            dividend_yield = info.get("dividendYield", 0)
            name = info.get("longName", ticker)

            if eps and pe:
                pearl_score = round((eps / (pe + 1)) * (1e8 / (volume + 1)), 2)
                results.append({
                    "ticker": ticker,
                    "name": name,
                    "eps": round(eps, 2),
                    "volume": volume,
                    "pe": round(pe, 2),
                    "sector": sector,
                    "industry": industry,
                    "market_cap": market_cap,
                    "dividend_yield": round(dividend_yield * 100, 2) if dividend_yield else 0,
                    "pearl_score": pearl_score,
                    "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
    return results

# -----------------------------
# Title and Description
# -----------------------------
st.markdown("<h2 style='text-align: center;'>💎 U.S. Pearl Finder: Discover Hidden Value Stocks</h2>", unsafe_allow_html=True)
st.caption("This dashboard helps you uncover 'pearls in the mud' — undervalued, overlooked U.S. stocks with strong fundamentals. Filter by earnings, valuation, volume, sector, and more to find companies quietly outperforming beneath the surface.")

# -----------------------------
# Weekly Display
# -----------------------------
today = datetime.today()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=4)
st.caption(f"📅 Week: {start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}")

# -----------------------------
# Load and Filter
# -----------------------------
tickers = get_sp500_tickers()
data = fetch_stock_data(tickers)
df = pd.DataFrame(data)

with st.expander("🔧 Tap to adjust filters", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        min_eps = st.number_input("Min EPS", value=2.0, step=0.1)
        selected_sector = st.selectbox("Sector", ["All"] + sorted(df["sector"].unique()))
    with col2:
        max_pe = st.number_input("Max P/E", value=25.0, step=1.0)
        selected_industry = st.selectbox("Industry", ["All"] + sorted(df["industry"].unique()))
    with col3:
        max_volume_input = st.text_input("Max Volume", value="100,000,000")
        try:
            max_volume = int(max_volume_input.replace(",", ""))
        except ValueError:
            st.error("Please enter a valid number for volume (e.g., 10,000,000)")
            max_volume = None

# -----------------------------
# Apply Filters
# -----------------------------
if max_volume is not None:
    filtered_df = df[
        (df["eps"] >= min_eps) &
        (df["pe"] <= max_pe) &
        (df["volume"] <= max_volume)
    ]
    if selected_sector != "All":
        filtered_df = filtered_df[filtered_df["sector"] == selected_sector]
    if selected_industry != "All":
        filtered_df = filtered_df[filtered_df["industry"] == selected_industry]

    filtered_df = filtered_df.sort_values(by="pearl_score", ascending=False)

    # -----------------------------
    # Display Results
    # -----------------------------
    st.markdown("### 📋 Filtered Stocks (Ranked by Pearl Score)")
    if not filtered_df.empty:
        for _, stock in filtered_df.iterrows():
            st.markdown(f"""
                <div style='padding: 8px; border-bottom: 1px solid #ddd;'>
                    <strong>{stock['name']}</strong> <span style='font-size: 0.85em;'>({stock['ticker']})</span><br>
                    EPS: {stock['eps']} | P/E: {stock['pe']} | Volume: {int(stock['volume']):,}<br>
                    Sector: {stock['sector']} | Industry: {stock['industry']}<br>
                    Market Cap: ${int(stock['market_cap']):,} | Dividend Yield: {stock['dividend_yield']}%<br>
                    Pearl Score: <strong>{stock['pearl_score']}</strong><br>
                    Fetched at: {stock['fetched_at']}
                </div>
            """, unsafe_allow_html=True)

        # 📥 Export CSV
        st.markdown("#### 📄 Preview CSV")
        st.dataframe(filtered_df)

        csv_buffer = StringIO()
        filtered_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download filtered results as CSV",
            data=csv_buffer.getvalue(),
            file_name=f"us_pearl_finder_{start_of_week.strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No stocks matched your filter criteria!!!")

