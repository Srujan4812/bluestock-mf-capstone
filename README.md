# Bluestock Mutual Fund Analytics Platform
### End-to-End Data Engineering, ETL Pipeline & Interactive Dashboard
**Prepared By: Srujan / Data Analyst Intern**  
**Date: June 2026**

---

## Project Overview
This repository contains the complete implementation for the **Bluestock Mutual Fund Analytics Platform** capstone project. The platform is designed to ingest daily NAVs, industry inflows, portfolio holdings, and investor transactions, transform them through a robust Python ETL pipeline, store them in a normalized SQLite database, perform mathematical risk-return analytics, and serve insights via an interactive, premium Streamlit dashboard.

### Core Business Objectives Solved:
- **P1: Data Fragmentation**: Consolidated NAV, AUM, SIP flows, and holdings from disparate sources into a single normalized SQLite database.
- **P2: Performance Evaluation**: Computed annualized risk-adjusted return ratios (Sharpe, Sortino, Alpha, Beta) to evaluate active fund efficiency.
- **P3: Index Benchmarking**: Evaluated rolling active alpha and tracking errors against Nifty 50 and Nifty 100 indices.
- **P4: Investor Behavior**: Analyzed demographic and geographic trends, including acquisition cohorts and SIP churn risks.
- **P5: Dynamic Reporting**: Deployed a modern, self-service Streamlit dashboard replacing static reporting processes.

---

## Project Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/                 # Original flat CSV datasets (87K+ transaction rows)
│   └── processed/           # Cleansed CSVs, bluestock.db, fund_scorecard.csv, etc.
├── sql/
│   ├── schema.sql           # SQLite Star Schema DDL definitions
│   ├── star_schema.sql      # Star Schema documentation/references
│   └── queries.sql          # 11 validation and analytical SQL queries
├── notebooks/
│   ├── EDA_Analysis.ipynb          # Day 3 Exploratory Data Analysis
│   ├── Performance_Analytics.ipynb # Day 4 Return & Performance calculations
│   └── Advanced_Analytics.ipynb    # Day 6 Risk, Cohort & Concentration reports
├── dashboard/
│   └── app.py               # Day 5 Multi-page Interactive Streamlit Application
├── reports/
│   ├── charts/              # Generated high-res visualization PNG files
│   ├── data_dictionary.md   # Mapping of tables, data types, and primary/foreign keys
│   ├── data_quality_report.txt     # Day 1 Data Ingestion Profile
│   ├── day2_validation_report.txt  # Day 2 DB Schema Validation Report
│   ├── day4_performance_report.txt # Day 4 Performance Stats & Rankings
│   ├── Dashboard.pdf        # Day 5 Landscaped Dashboard mockup PDF
│   └── Final_Report.pdf     # Day 7 Comprehensive 16-page Executive Report
├── scripts/
│   ├── _common.py            # Logger & shared Path configs
│   ├── data_ingestion.py     # Day 1 Raw data ingestion
│   ├── live_nav_fetch.py     # Day 1 Live NAV mfapi.in API fetcher
│   ├── data_cleaning.py      # Day 2 Programmatic Pandas cleaning
│   ├── build_database.py     # Day 2 SQLite database builder & validation
│   ├── performance_analytics.py # Day 4 CAGR, Sharpe, Sortino, Alpha/Beta computation
│   ├── advanced_analytics.py # Day 6 VaR, Cohort, Churn, HHI calculation & Jupyter builder
│   ├── recommender.py        # Day 6 Risk-appetite rule-based recommender model
│   ├── export_dashboard.py   # Day 5 Programmatic dashboard screen exporter
│   ├── generate_presentation.py # Day 7 PowerPoint Slide Deck compiler
│   └── generate_final_report.py # Day 7 Executive PDF report compiler (ReportLab)
├── logs/                     # Script run logs
├── requirements.txt         # Package dependencies
├── .gitignore               # Configured gitignore (git-ignores large database files)
├── run_pipeline.py          # Master Orchestrator script to run entire pipeline
└── README.md                # Main project documentation
```

---

## Technical Stack Details
- **Language**: Python 3.10+
- **Data Manipulation**: Pandas 2.2+, NumPy 1.26+
- **Database**: SQLite3, SQLAlchemy 2.0+
- **Scientific Computations**: SciPy 1.14+ (OLS regression for Beta/Alpha)
- **Visualizations**: Matplotlib 3.9+, Seaborn 0.13+, Plotly 5.24+
- **Interactive Web App**: Streamlit 1.58+
- **Reporting**: ReportLab 4.5+ (PDF generator), Python-pptx 1.0+ (PPTX generator)

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Srujan4812/bluestock-mf-capstone.git
   cd bluestock-mf-capstone
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Execution Guide

### 1. Run the Entire Project (Orchestrated Pipeline)
You can run the entire pipeline—from raw data cleaning and database creation up to report, slide, and notebook generation—with a single command:
```bash
python run_pipeline.py
```
This executes all daily steps sequentially, verifying that every output is mathematically consistent and matches database updates.

### 2. Run the Interactive Dashboard
To launch the interactive Streamlit dashboard locally:
```bash
streamlit run dashboard/app.py
```
The dashboard features four interactive pages:
1. **Industry Overview**: Traces industry AUM growth trends, folio breakdowns, and AMC assets.
2. **Fund Performance**: Displays return-risk scatter profiles, a sortable scorecard table, and individual fund NAV vs. Benchmark comparisons.
3. **Investor Analytics**: Segments transaction state volumes, transaction types split, ticket sizes, and volume trends.
4. **SIP & Market Trends**: Correlates monthly SIP inflows with the Nifty 50 close price, category inflows, and heatmap distributions.

### 3. Run Standalone Script Modules
You can run individual pipeline segments directly:
- **Clean data**: `python scripts/data_cleaning.py`
- **Build database**: `python scripts/build_database.py`
- **Performance Analytics**: `python scripts/performance_analytics.py`
- **Advanced Analytics**: `python scripts/advanced_analytics.py`
- **Dashboard Screenshots**: `python scripts/export_dashboard.py`
- **PowerPoint Presentation**: `python scripts/generate_presentation.py`
- **PDF Report**: `python scripts/generate_final_report.py`
- **Fund Recommender CLI**: `python scripts/recommender.py`

---

## Core Calculations & Ratios

- **CAGR Return**:
  $$\text{CAGR} = \left(\frac{\text{NAV}_{\text{end}}}{\text{NAV}_{\text{start}}}\right)^{\frac{1}{N_{\text{years}}}} - 1$$
- **Sharpe Ratio (Annualized)**:
  $$\text{Sharpe} = \frac{R_p - R_f}{\sigma_p} \times \sqrt{252}$$  
  *(where $R_f = 6.5\%$ proxy, and daily excess returns are annualized)*
- **Sortino Ratio**:
  $$\text{Sortino} = \frac{R_p - R_f}{\sigma_{\text{downside}}} \times \sqrt{252}$$  
  *(where $\sigma_{\text{downside}}$ uses only negative return trading days)*
- **Alpha & Beta**: Computed via Ordinary Least Squares (OLS) regression of daily fund returns against daily Nifty 100 returns. Alpha intercept is annualized ($\times 252$).
- **Maximum Drawdown**:
  $$\text{Max Drawdown} = \min \left(\frac{\text{NAV}_t}{\text{Running Max NAV}} - 1\right)$$
- **Value at Risk (VaR 95%)**: Computed as the 5th percentile of the daily return distribution (multiplied by $-1$ to represent loss magnitude).
- **Herfindahl-Hirschman Index (HHI)**:
  $$\text{HHI} = \sum_{i} (\text{Sector Weight}_i)^2$$
