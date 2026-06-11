# Mutual Fund Analytics Platform
### End-to-End Data Engineering, ETL Pipeline & Interactive Dashboard
**Prepared By: Srujan / Quantitative Analyst**  
**Date: June 2026**

🚀 **Live Dashboard**: [https://bluestock-mf-capstone-1.onrender.com](https://bluestock-mf-capstone-1.onrender.com)

---

## Project Overview
This repository contains the complete implementation for a production-grade **Mutual Fund Analytics Platform**. The platform is designed to ingest daily Net Asset Values (NAV), quarterly AMC Assets Under Management (AUM), monthly industry SIP inflows, portfolio stock holdings, and investor transactions. It transforms raw data through an automated ETL pipeline, stores it in a normalized SQLite database, computes sophisticated risk-adjusted performance metrics, and serves interactive visualizations via a high-performance Streamlit dashboard.

### Core Business Objectives Addressed:
- **Data Consolidation**: Unified daily NAV values, AMC AUMs, industry inflows, and holdings from disparate sources into a single normalized SQLite database.
- **Risk-Adjusted Performance**: Calculated annualized ratios (Sharpe, Sortino, Alpha, Beta) to evaluate historical fund efficiency.
- **Benchmark Tracking**: Evaluated active alpha and tracking errors against Nifty 50 and Nifty 100 indices.
- **Behavioral Analytics**: Segmented investor demographic habits, registration trends, and identified accounts with potential churn risk.
- **Interactive Reporting**: Developed a self-service analytical dashboard to allow drill-downs and real-time visualization of returns and risk metrics.

---

## Project Structure
```
mutual_fund_analytics/
├── data/
│   ├── raw/                 # Original flat CSV datasets (87K+ transaction rows)
│   ├── processed/           # Cleansed, normalized CSV outputs
│   └── db/                  # Star schema SQLite database (bluestock_mf.db - ignored by git)
├── sql/
│   ├── schema.sql           # SQLite Star Schema DDL definitions
│   ├── star_schema.sql      # Star Schema documentation/references
│   └── queries.sql          # Validation and analytical SQL queries
├── notebooks/
│   ├── 01_data_ingestion.ipynb    # Ingestion & quality profiling checks
│   ├── 02_data_cleaning.ipynb     # Column normalization & standardisation
│   ├── 03_eda_analysis.ipynb      # Exploratory Data Analysis (EDA)
│   ├── 04_performance_analytics.ipynb # Risk & return metric computations
│   └── 05_advanced_analytics.ipynb    # Portfolio optimization & simulations
├── dashboard/
│   └── app.py               # Multi-page Interactive Streamlit Application
├── reports/
│   ├── charts/              # Generated high-resolution visualization plots
│   ├── data_dictionary.md   # Schema mapping of tables, types, and constraints
│   ├── data_quality_report.txt     # Initial data quality profile logs
│   ├── database_validation_report.txt # Database integrity check report
│   ├── performance_report.txt      # Performance statistics validation logs
│   ├── Dashboard.pdf        # Landscaped Dashboard mockup PDF
│   ├── Final_Report.pdf     # Comprehensive Executive Report (PDF)
│   └── Presentation.pptx    # PowerPoint Presentation Slide Deck
├── scripts/
│   ├── _common.py            # Logger & shared path configurations
│   ├── etl_pipeline.py       # Master Ingestion, Cleaning & SQLite Loader
│   ├── data_ingestion.py     # Raw data profiling logic
│   ├── live_nav_fetch.py     # Live NAV mfapi.in API fetcher script
│   ├── data_cleaning.py      # Pandas data cleaning logic
│   ├── build_database.py     # Database builder & integrity check validations
│   ├── compute_metrics.py    # Returns, Sharpe, Sortino, Alpha & Beta metrics
│   ├── advanced_analytics.py # VaR, Cohorts, HHI, Monte Carlo & Markowitz Optimization
│   ├── recommender.py        # Rule-based fund recommendation engine
│   ├── email_report.py       # Automated HTML performance email report generator
│   ├── schedule_etl.py       # Weekday daemon scheduler configuration
│   ├── generate_all_notebooks.py # Programmatic notebook executor
│   ├── export_dashboard.py   # Dashboard screen exporter
│   ├── generate_presentation.py # PowerPoint Slide Deck compiler
│   └── generate_final_report.py # Executive PDF report compiler (ReportLab)
├── logs/                     # Script run execution logs
├── requirements.txt         # Package dependencies
├── .gitignore               # Configured gitignore (excludes large database binary files)
├── run_pipeline.py          # Master Orchestrator script to run entire pipeline
└── README.md                # Main project documentation
```

---

## Technical Stack Details
- **Language**: Python 3.10+
- **Data Processing**: Pandas 2.2+, NumPy 1.26+
- **Database**: SQLite3, SQLAlchemy 2.0+
- **Scientific Computations**: SciPy 1.14+ (OLS regression for Beta/Alpha)
- **Visualizations**: Matplotlib 3.9+, Seaborn 0.13+, Plotly 5.24+
- **Application Web Framework**: Streamlit 1.58+
- **Reporting Engine**: ReportLab 4.5+ (PDF compilation), Python-pptx 1.0+ (PPTX compilation)

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
This executes all processing steps sequentially, verifying that every output is mathematically consistent and matches database updates.

### 2. Run the Interactive Dashboard
To launch the interactive Streamlit dashboard locally:
```bash
streamlit run dashboard/app.py
```
The dashboard features four interactive pages:
1. **Industry Overview**: Traces industry AUM growth trends, folio breakdowns, and AMC assets.
2. **Fund Performance**: Displays return-risk scatter profiles, a sortable scorecard table, and individual fund NAV vs. Benchmark comparisons.
3. **Investor Analytics**: Segments transaction state volumes, transaction types split, ticket sizes, and volume trends.
4. **SIP & Market Trends**: Correlates monthly SIP inflows with the Nifty 50 close index, category inflows, and net inflow heatmaps.

### 3. Run Standalone Script Modules
You can run individual pipeline segments directly:
- **Run Full ETL**: `python scripts/etl_pipeline.py`
- **Clean data only**: `python scripts/data_cleaning.py`
- **Build database only**: `python scripts/build_database.py`
- **Performance metrics**: `python scripts/compute_metrics.py`
- **Advanced analytics & risk engine**: `python scripts/advanced_analytics.py`
- **HTML Email Report**: `python scripts/email_report.py`
- **Dashboard Exports (Mockups)**: `python scripts/export_dashboard.py`
- **PowerPoint Presentation Compiler**: `python scripts/generate_presentation.py`
- **PDF Report Compiler**: `python scripts/generate_final_report.py`
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

---

## Power BI / Tableau Integration Guide

To support standard business intelligence workflows, you can connect tools like **Power BI** or **Tableau** directly to the SQLite analytical database or processed datasets in this project.

### 1. Data Connection Steps
- **Direct Database Import**: Install the SQLite ODBC Driver on your system. Define a DSN pointing to the local SQLite database at `data/db/bluestock_mf.db` to load all relational star schema tables.
- **Flat File Import**: Alternatively, you can use the Power BI "Folder" or "Text/CSV" connectors to read the normalized, cleaned flat files from the `data/processed/` directory.

### 2. Data Model Relationships
In the Power BI Model View, configure the following relationships (ensuring referential integrity):
- `nav_history` (composite `amfi_code` key) ──(Many-to-One)──> `clean_fund_master` (`amfi_code`)
- `clean_investor_transactions` (`amfi_code`) ──(Many-to-One)──> `clean_fund_master` (`amfi_code`)
- `fund_scorecard` (`amfi_code`) ──(One-to-One)──> `clean_fund_master` (`amfi_code`)
- `clean_aum_by_fund_house` (`fund_house`) ──(Many-to-One)──> `clean_fund_master` (`fund_house`)

### 3. Key DAX Calculations
You can define custom metrics using DAX inside your Power BI panels:
- **Scorecard Weighted Score**:
  ```dax
  CompositeScore = 
  (0.30 * RANK.EQ(AVERAGE(fund_scorecard[cagr_3yr_pct]), fund_scorecard[cagr_3yr_pct], DESC)) +
  (0.25 * RANK.EQ(AVERAGE(fund_scorecard[sharpe_ratio]), fund_scorecard[sharpe_ratio], DESC)) +
  (0.20 * RANK.EQ(AVERAGE(fund_scorecard[alpha]), fund_scorecard[alpha], DESC)) +
  (0.15 * RANK.EQ(AVERAGE(fund_scorecard[expense_ratio_pct]), fund_scorecard[expense_ratio_pct], ASC)) +
  (0.10 * RANK.EQ(AVERAGE(fund_scorecard[max_drawdown_pct]), fund_scorecard[max_drawdown_pct], ASC))
  ```
- **Annualized Sharpe Ratio**:
  ```dax
  Sharpe = DIVIDE(AVERAGE(fund_scorecard[cagr_3yr_pct]) - 6.5, AVERAGE(fund_scorecard[std_dev_ann_pct]))
  ```

### 4. Interactive Previews & Export
Mockup snapshots representing pages 1 to 4 of the interactive dashboard are exported at `reports/charts/dashboard_page1.png` through `dashboard_page4.png`. A compiled landscape PDF is available for review at [reports/Dashboard.pdf](file:///c:/Users/madhu/OneDrive/Desktop/bluestock_mf_capstone/reports/Dashboard.pdf).
