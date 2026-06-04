# PROGRESS LOG — Bluestock Mutual Fund Analytics Capstone

_Last updated: 2026-06-04_

## Project Overview
This capstone project involves building an end-to-end data pipeline, analytical database, exploratory analysis, and performance scorecard for Indian mutual funds.

GitHub Repository: [Srujan4812/bluestock-mf-capstone](https://github.com/Srujan4812/bluestock-mf-capstone)

---

## Day-by-Day Progress Summary

### 📅 DAY 1 — Project Setup + Data Ingestion (ETL)
- **Folder Structure**: Set up folders: `data/raw`, `data/processed`, `notebooks/`, `sql/`, `dashboard/`, `reports/`, `scripts/`, `logs/`.
- **Dependencies**: Configured virtual environment `.venv` and generated `requirements.txt` containing standard Python data science libraries.
- **Data Ingestion**: Wrote `scripts/data_ingestion.py` which loads all 10 raw CSV datasets, checking shapes, dtypes, missing values, duplicates, and datatypes. Writes a summary report to `reports/data_quality_report.txt`.
- **Live NAV Fetch**: Created `scripts/live_nav_fetch.py` to retrieve up-to-date NAV history for 6 schemes from `mfapi.in` and saved them to `data/processed/live_nav.csv`.
- **AMFI Validation**: Checked AMFI scheme codes between `fund_master` and `nav_history`, achieving a perfect 40/40 match.

### 📅 DAY 2 — Data Cleaning + SQL Database Design
- **Data Cleaning**: Created `scripts/data_cleaning.py` to parse dates to ISO strings, sort by code and date, forward-fill missing NAVs (for holidays/weekends), normalize transaction types (SIP/Lumpsum/Redemption), and validate ranges. Outputs are saved to `data/processed/clean_*.csv`.
- **Star Schema SQLite DB**: Wrote `sql/schema.sql` defining relational tables with explicit primary and foreign keys. Created `scripts/build_database.py` to load clean CSV files into `data/processed/bluestock.db` in a foreign-key-safe order. Programmatic integrity checks were saved to `reports/day2_validation_report.txt`.
- **Queries & Dictionary**: Created `sql/queries.sql` (11 analytical and validation queries) and wrote `reports/data_dictionary.md` mapping column schemas.

### 📅 DAY 3 — Exploratory Data Analysis (EDA)
- **EDA Notebook**: Created `notebooks/EDA_Analysis.ipynb` running comprehensive analysis of NAV trends (2022–2026), AUM growth, SIP inflow trends, category net inflows, investor demographics, folio counts, returns correlation, and sector weights.
- **EDA Charts**: Generated 17 charts saved as high-resolution PNGs to `reports/charts/`.
- **Optimization**: Cleared extra Plotly notebook metadata and downsampled chart data to optimize render times on GitHub.

### 📅 DAY 4 — Fund Performance Analytics (Today)
- **Return & Risk Metric Calculations**: Created `scripts/performance_analytics.py` to compute:
  - Daily NAV returns and validated distribution (Mean: 0.0631%, Std Dev: 1.0290%).
  - CAGR returns for 1yr, 3yr, and 5yr (using max period 4.4 years as a proxy).
  - Annualized Sharpe Ratio (Rf = 6.5% proxy, 252 trading days).
  - Sortino Ratio (downside standard deviation of negative return days only).
  - Alpha & Beta (OLS regression vs Nifty 100 returns).
  - Maximum Drawdown (and worst peak-to-trough date ranges).
- **Composite Scorecard**: Built a scorecard ranking all 40 funds using a weighted rank combination:
  - 30% * 3yr CAGR Return Rank
  - 25% * Sharpe Rank
  - 20% * Alpha Rank
  - 15% * Expense Ratio Rank (inverse)
  - 10% * Max Drawdown Rank (inverse)
  Saved results to `data/processed/fund_scorecard.csv` and `data/processed/alpha_beta.csv`.
- **Benchmark Line Chart**: Plotted the top 5 funds vs Nifty 50 and Nifty 100 over a 3-year period (2023-05-29 to 2026-05-29) and computed tracking errors relative to both indices. Saved plot to `reports/charts/benchmark_comparison.png` and validations to `reports/day4_performance_report.txt`.
- **Notebook & Execution**: Compiled calculations into `notebooks/Performance_Analytics.ipynb` and executed it in-place to preserve outputs.

---

## Top 5 Performing Funds (Scorecard Results)

1. **Mirae Asset Large Cap Fund - Regular - Growth** (AMFI: 148567) | Score: 86.25
   - 3Yr CAGR: 34.00% | Sharpe: 1.45 | Alpha: 26.98% | Expense Ratio: 1.46% | Max Drawdown: -11.27%
2. **ICICI Pru Midcap Fund - Regular - Growth** (AMFI: 120505) | Score: 82.25
   - 3Yr CAGR: 31.78% | Sharpe: 1.18 | Alpha: 29.26% | Expense Ratio: 1.36% | Max Drawdown: -18.19%
3. **Kotak Flexicap Fund - Regular - Growth** (AMFI: 120843) | Score: 82.00
   - 3Yr CAGR: 29.58% | Sharpe: 1.31 | Alpha: 27.33% | Expense Ratio: 1.45% | Max Drawdown: -12.97%
4. **HDFC Mid-Cap Opportunities Fund - Regular - Growth** (AMFI: 100033) | Score: 80.75
   - 3Yr CAGR: 32.44% | Sharpe: 1.09 | Alpha: 27.20% | Expense Ratio: 1.38% | Max Drawdown: -16.22%
5. **ICICI Pru Bluechip Fund - Direct - Growth** (AMFI: 120504) | Score: 80.00
   - 3Yr CAGR: 32.49% | Sharpe: 1.03 | Alpha: 21.19% | Expense Ratio: 0.80% | Max Drawdown: -12.59%

---

## Current Project Folder Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/                 # 10 raw CSV datasets
│   └── processed/           # cleaned CSVs + bluestock.db + fund_scorecard.csv + alpha_beta.csv
├── notebooks/
│   ├── EDA_Analysis.ipynb
│   └── Performance_Analytics.ipynb
├── sql/
│   ├── schema.sql
│   └── star_schema.sql
├── reports/
│   ├── charts/              # 17 EDA charts + benchmark comparison chart
│   ├── data_quality_report.txt
│   ├── day2_validation_report.txt
│   ├── day4_performance_report.txt
│   └── data_dictionary.md
├── scripts/
│   ├── data_ingestion.py
│   ├── live_nav_fetch.py
│   ├── data_cleaning.py
│   ├── build_database.py
│   ├── performance_analytics.py
│   ├── generate_notebook.py
│   └── _common.py
├── PROGRESS.md
├── README.md
├── requirements.txt
└── .gitignore
```