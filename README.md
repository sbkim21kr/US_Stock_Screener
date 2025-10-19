# 📈 Pearl Finder: Sector-Aware Stock Screener

Pearl Finder is a lightweight stock screener that ranks companies using a custom metric called the **Pearl Score**, calculated from EPS and PE ratio. It includes sector and industry context and displays results in a clean dashboard powered by Streamlit.

---

## 🧮 Pearl Score Formula



\[
\text{Pearl Score} = \left( \frac{\text{EPS}}{\text{PE}} \right) \times 100
\]



This favors companies with strong earnings and reasonable valuations.

---

## 🔧 Features & Adjustments

- ✅ No HTML scraping — replaced `read_html()` with a local `tickers.csv`
- ✅ Manually curated ticker list including Micron (MU) and other key stocks
- ✅ Removed "Exclude Financial Sector" filter — all sectors included
- ✅ Dashboard shows top 50 stocks split into 5 tables of 10
- ✅ Weekly GitHub Actions refresh — auto-generates new CSV every Sunday
- ✅ Downloadable filtered CSV from the dashboard

---

## 📁 Project Structure

