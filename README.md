### 📘 `README.md`

```markdown
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

```
US_Stock_Screener/
├── data/               # Auto-generated CSVs with Pearl Scores
├── tickers.csv         # Manually curated list of stock symbols
├── refresh.py          # Script to fetch data and calculate scores
├── dashboard.py        # Streamlit dashboard
└── .github/workflows/  # GitHub Actions for weekly refresh
```

---

## 🚀 How to Run Locally

1. Clone the repo
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install pandas yfinance streamlit
   ```
4. Run the refresh script:
   ```bash
   python refresh.py
   ```
5. Launch the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

---

## 🗓 GitHub Actions

The workflow in `.github/workflows/weekly_refresh.yml` runs `refresh.py` every Sunday at midnight UTC and commits the updated CSV to the `data/` folder.

---

## 📥 Customize Your Ticker List

Edit `tickers.csv` to include any stocks you want to track. Format:

```csv
Symbol
AAPL
MSFT
MU
NVDA
...
```

---

## 🙌 Credits

Built and maintained by **Sangbum Kim**. Pearl Score concept and dashboard design are custom-built for clarity and performance.
```

---

You can create this file in GitHub by clicking **Add file → Create new file**, naming it `README.md`, and pasting the content above. Let me know if you want to add screenshots or badges!
