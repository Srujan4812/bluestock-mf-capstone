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

### 📅 DAY 5 — Interactive Dashboard Development
- **Visual Analytics Hub**: Created `dashboard/app.py` using Streamlit, featuring an Outfit Google Font face, glassmorphism card containers, hover micro-animations, and multi-option sidebar filter controls (AMC, category, and plan type).
- **Core Dashboard Pages**:
  - **Page 1: Industry Overview**: Displays Total Industry AUM (₹81.0 L Cr), Monthly SIP Inflows, folio counts, and AMC asset consolidation.
  - **Page 2: Fund Performance**: Plots Risk-Return profiles (CAGR vs. Std Dev), renders the weighted scorecard ranking table, and shows normalized NAV vs. Benchmark comparisons. Fixed bubble chart sizing for negative Sharpe ratios by scaling values to `sharpe_ratio_size`.
  - **Page 3: Investor Analytics**: State-wise transactions bar charts, ticket size box plots by age, transaction types (SIP vs. Lumpsum vs. Redemption) splits, and monthly volume line trends.
  - **Page 4: SIP & Market Trends**: Dual-axis overlays correlating monthly SIP inflows with the Nifty 50 close index, category inflows, and net inflow heatmaps.
- **Visual Exports**: Developed [scripts/export_dashboard.py](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/scripts/export_dashboard.py) which programmatically snaps pages 1 to 4 as high-res PNG screens and compiles them into a landscaped evaluation deck at [reports/Dashboard.pdf](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/reports/Dashboard.pdf).
- **Zero-Config Cloud Deploy Check**: Configured the dashboard startup block to dynamically compile the database and clean flat files if missing (supporting click-to-deploy on Streamlit Community Cloud).

### 📅 DAY 6 — Advanced Analytics & Risk Modelling
- **Tail Vulnerability Engine**: Computed daily Historical Value at Risk (VaR 95%) and Conditional Value at Risk (CVaR 95%) for all 40 funds. Saved outputs to `data/processed/var_cvar_report.csv`.
- **Rolling Volatility**: Plotted 90-day rolling Sharpe ratios for top funds to evaluate performance stability over time. Saved chart to `reports/charts/rolling_sharpe_chart.png`.
- **Acquisition Segment Cohorts**: Grouped transaction habits to compare 2024 and 2025 investor cohorts on averages, net ticket volumes, and asset class preferences. Saved to `data/processed/cohort_analysis.csv`.
- **SIP Churn Predictor**: Screened transaction intervals to identify and flag investors with maximum payment gaps > 35 days as "at-risk". Saved results to `data/processed/sip_continuity.csv`.
- **Diversification Analysis**: Computed the Herfindahl-Hirschman Index (HHI) of sector weights to evaluate holdings concentration. Saved to `data/processed/sector_hhi.csv` and plotted top concentrated schemes to `reports/charts/sector_concentration.png`.
- **B3 — Monte Carlo Simulation**: Forecasted 1,000 potential NAV growth paths over 5 years (1,260 trading days) using Geometric Brownian Motion (GBM) drift. Saved outputs to `data/processed/monte_carlo_projections.csv` and the chart to `reports/charts/monte_carlo_simulation.png`.
- **B4 — Portfolio Optimization**: Built a Markowitz Efficient Frontier model simulating 2,000 random weight combinations of top scorecard funds. Calculated Expected Return, Volatility, Sharpe ratios, and Maximum Sharpe Ratio (MSR) and Minimum Variance Portfolio (MVP) weights. Saved data to `data/processed/efficient_frontier_results.csv` and the plot to `reports/charts/efficient_frontier.png`.
- **Numbered Notebooks**: Staged and programmatically ran [notebooks/05_advanced_analytics.ipynb](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/notebooks/05_advanced_analytics.ipynb) containing explanations, LaTeX equations, calculations, and chart renders.

### 📅 DAY 7 — Final Reporting & Slide Deck Compilation
- **B5 — Weekly performance email report**: Programmed [scripts/email_report.py](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/scripts/email_report.py) to compile portfolio stats, cohort activity, and scorecard lists into a responsive HTML email summary saved at [reports/weekly_performance_report.html](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/reports/weekly_performance_report.html).
- **PowerPoint Presentation Deck**: Coded [scripts/generate_presentation.py](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/scripts/generate_presentation.py) to compile a 12-slide presentation deck at [reports/Presentation.pptx](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/reports/Presentation.pptx). Features clean slide layouts matching Bluestock Fintech’s brand guidelines.
- **Executive PDF Report**: Wrote [scripts/generate_final_report.py](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/scripts/generate_final_report.py) using ReportLab. Renders the Cover Page, Executive Summary, SQL DDL schema and queries, EDA charts, Scorecard grids, VaR tables, cohort statistics, and dashboard walkthroughs. Saved to [reports/Final_Report.pdf](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/reports/Final_Report.pdf).
- **Master Orchestrator**: Developed [run_pipeline.py](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/run_pipeline.py) to execute all steps sequentially, ensuring complete data consistency across database rows, scorecard files, notebooks, slides, and PDF report pages.

---

## Current Project Folder Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/                 # Original flat CSV datasets (87K+ transaction rows)
│   ├── processed/           # Cleansed, normalized CSV outputs
│   └── db/                  # Star schema SQLite database (bluestock_mf.db - ignored by git)
├── sql/
│   ├── schema.sql           # SQLite Star Schema DDL definitions
│   ├── star_schema.sql      # Star Schema documentation/references
│   └── queries.sql          # 11 validation and analytical SQL queries
├── notebooks/
│   ├── 01_data_ingestion.ipynb    # Day 1 Data Ingestion & Profiling
│   ├── 02_data_cleaning.ipynb     # Day 2 Data Cleaning & Standardisation
│   ├── 03_eda_analysis.ipynb      # Day 3 Exploratory Data Analysis (EDA)
│   ├── 04_performance_analytics.ipynb # Day 4 Return & Performance calculations
│   └── 05_advanced_analytics.ipynb    # Day 6 Risk, Monte Carlo & Portfolio optimization
├── dashboard/
│   └── app.py               # Day 5 Multi-page Interactive Streamlit Application
├── reports/
│   ├── charts/              # Generated high-res visualization PNG files
│   ├── data_dictionary.md   # Mapping of tables, data types, and primary/foreign keys
│   ├── data_quality_report.txt     # Day 1 Data Ingestion Profile
│   ├── day2_validation_report.txt  # Day 2 DB Schema Validation Report
│   ├── day4_performance_report.txt # Day 4 Performance Stats & Scorecard rankings
│   ├── Dashboard.pdf        # Day 5 Landscaped Dashboard mockup PDF
│   ├── Final_Report.pdf     # Day 7 Comprehensive Executive Report
│   └── Presentation.pptx    # Day 7 PowerPoint Presentation Slide Deck
```