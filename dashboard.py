import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 📁 Load the latest CSV file
def get_latest_csv():
    files = [f for f in os.listdir() if f.startswith("pearl_scores_") and f.endswith(".csv")]
    if not files:
        return None
    files.sort(reverse=True)
    return files[0]

# 🔄 Load data
latest_file = get_latest_csv()
if latest_file:
    df = pd.read_csv(latest_file)
    st.set_page_config(page_title="Pearl Finder Dashboard", layout="wide")
    st.title("📈 Pearl Finder: Weekly Screener")
    st.caption(f"📆 Showing data from: {latest_file.replace('pearl_scores_', '').replace('.csv', '')}")

    # 📊 Preview Table
    st.subheader("📊 Screened Stocks")
    st.dataframe(df)

    # 🔍 Filter by ticker
    selected = st.multiselect("🔎 Filter by ticker", df["Ticker"].tolist())
    if selected:
        filtered_df = df[df["Ticker"].isin(selected)]
    else:
        filtered_df = df

    # 📈 Top Pearl Scores
    st.subheader("🏆 Top 10 Pearl Scores")
    top_df = df.sort_values(by="Pearl Score", ascending=False).head(10)
    st.bar_chart(top_df.set_index("Ticker")["Pearl Score"])

    # 📋 Metrics View
    st.subheader("📋 Metrics for Selected Stocks")
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['Ticker']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Pearl Score", row["Pearl Score"])
                st.metric("EPS", row["EPS"])
                st.metric("PE", row["PE"])
            with col2:
                st.write("📁 Historical data coming soon...")

    # 📥 Download filtered data
    st.download_button("📥 Download filtered CSV", filtered_df.to_csv(index=False), "filtered_stocks.csv", "text/csv")
else:
    st.warning("No weekly CSV found. Please run refresh.py or wait for GitHub Actions to update.")
