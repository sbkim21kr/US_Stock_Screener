# US Stock Screener 📈

This project automatically screens U.S. stocks and generates a weekly CSV file with updated scores.

## 🔧 Features
- Weekly refresh of stock data
- Generates `pearl_scores_YYYY-MM-DD.csv`
- GitHub Actions workflow for automation
- Easy integration with data analysis tools

## 🗓️ Workflow
The GitHub Actions workflow runs every Sunday and:
1. Fetches updated stock data
2. Calculates scores
3. Commits the new CSV file to the repository

## 📁 Output
- `pearl_scores_2025-10-19.csv` (example)
- Located in the root of the repository

## 🚀 Getting Started
To run locally:
```bash
git clone https://github.com/sbkim21kr/US_Stock_Screener.git
cd US_Stock_Screener
python screener.py
