import streamlit as st
import pandas as pd
import os

# 📁 Load the latest CSV file from the data folder
def get_latest_csv():
    data_dir = "data"
    files = [f for f in os.listdir(data_dir) if f.startswith("pearl_scores_") and f.endswith(".csv")]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(data_dir, files[0])

# 🔄 Load data
latest_file = get_latest_csv()
if latest_file:
    df = pd.read_csv(latest_file)
    st.set_page_config(page_title="Pearl Finder Dashboard", layout="wide")
    st.title("📈 Pearl Finder: Sector-Aware Screener")
    st.caption(f"📆 Showing data from: {os.path.basename(latest_file).replace('pearl_scores_', '').replace('.csv', '')}")

    # 📌 Pearl Score Formula
    st.markdown("### 🧮 Pearl Score Formula")
    st.latex(r"\text{Pearl Score} = \left( \frac{\text{EPS}}{\text{PE}} \right) \times 100")

    # 🔍 Filter by EPS and PE
    st.subheader("🔎 Filter Stocks by EPS and PE")
    col1, col2 = st.columns(2)
    with col1:
        eps_min = st.number_input("Minimum EPS", min_value=0.0, value=1.0, format="%.2f")
    with col2:
        pe_max = st.number_input("Maximum PE", min_value=0.0, value=60.0, format="%.2f")

    # Apply filters
    filtered_df = df[
        (df["EPS"] >= eps_min) &
        (df["PE"] <= pe_max)
    ]

    # 🏭 Sector-level Pearl Score
    st.subheader("🏭 Average Pearl Score by Sector")
    sector_scores = filtered_df.groupby("Sector")["Pearl Score"].mean().sort_values(ascending=False)
    st.bar_chart(sector_scores)

    # 🏆 Top 50 stocks from high-scoring sectors
    st.subheader("🏆 Top 50 Stocks from High-Scoring Sectors")
    top_df = filtered_df.sort_values(by="Pearl Score", ascending=False).head(50)
    columns_to_show = ["Name", "Ticker", "Pearl Score", "EPS", "PE", "Sector", "Industry"]
    chunks = [top_df.iloc[i:i+10] for i in range(0, 50, 10)]

    for i, chunk in enumerate(chunks):
        st.markdown(f"### 🔹 Stocks {i*10+1}–{i*10+10}")
        st.dataframe(chunk[columns_to_show])

    # 📋 Metrics View for Top 10
    st.subheader("📋 Metrics for Top 10 Stocks")
    chart_df = top_df.head(10)
    for _, row in chart_df.iterrows():
        with st.expander(f"{row['Name']} ({row['Ticker']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Pearl Score", row["Pearl Score"])
                st.metric("EPS", row["EPS"])
                st.metric("PE", row["PE"])
            with col2:
                st.write(f"🏭 Sector: {row['Sector']}")
                st.write(f"🏢 Industry: {row['Industry']}")

    # 📥 Download filtered top 50
    st.download_button("📥 Download Filtered Top 50 CSV", top_df.to_csv(index=False), "filtered_top_50.csv", "text/csv")
else:
    st.warning("No weekly CSV found in the data folder. Please run refresh.py or wait for GitHub Actions to update.")
