import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pearl Finder", layout="wide")

# 📦 Load latest data with caching
@st.cache_data
def load_latest_data():
    data_folder = "data"
    files = sorted([f for f in os.listdir(data_folder) if f.endswith(".csv")])
    latest_file = os.path.join(data_folder, files[-1])
    return pd.read_csv(latest_file)

df = load_latest_data()

# 🧮 Calculate sector averages
sector_avg = df.groupby("Sector")["Pearl Score"].mean().reset_index()
df = df.merge(sector_avg, on="Sector", suffixes=("", "_SectorAvg"))
df["Above Sector Avg"] = df["Pearl Score"] > df["Pearl Score_SectorAvg"]

# 🔍 Identify top 3 performers per sector
top_by_sector = df.groupby("Sector").apply(lambda x: x.nlargest(3, "Pearl Score")).reset_index(drop=True)

# 💎 Detect outliers (Hidden Gems)
threshold = df["Pearl Score"].quantile(0.95)
hidden_gems = df[df["Pearl Score"] > threshold]

# 🎨 Dashboard layout
st.title("📈 Pearl Finder: Sector-Aware Stock Screener")
st.markdown("This dashboard ranks stocks using the Pearl Score and highlights sector insights.")

tabs = st.tabs(["Top 50 Overall", "Top by Sector", "Hidden Gems", "Sector Averages"])

with tabs[0]:
    st.subheader("🏆 Top 50 Stocks by Pearl Score")
    top_50 = df.sort_values("Pearl Score", ascending=False).head(50)
    st.dataframe(top_50, use_container_width=True)

with tabs[1]:
    st.subheader("🥇 Top 3 Performers per Sector")
    st.dataframe(top_by_sector, use_container_width=True)

with tabs[2]:
    st.subheader("💎 Hidden Gems (Top 5%)")
    st.dataframe(hidden_gems, use_container_width=True)

with tabs[3]:
    st.subheader("📊 Sector Average Pearl Scores")
    st.dataframe(sector_avg, use_container_width=True)

# 📥 Download filtered data
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Full Data as CSV", csv, "pearl_scores.csv", "text/csv")

st.markdown("---")
st.caption("Built by Sangbum Kim • Pearl Score = (EPS / PE) × 100")
