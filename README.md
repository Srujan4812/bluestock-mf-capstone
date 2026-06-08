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
├── scripts/
│   ├── _common.py            # Logger & shared Path configs
│   ├── etl_pipeline.py       # Master Ingestion, Cleaning & SQLite Loader
│   ├── data_ingestion.py     # Raw data ingestion profile logic
│   ├── live_nav_fetch.py     # Live NAV mfapi.in API fetcher script
│   ├── data_cleaning.py      # Programmatic Pandas data cleaning logic
│   ├── build_database.py     # SQLite database builder & validation checks
│   ├── compute_metrics.py    # Return calculations, Sharpe, Sortino, Alpha & Beta
│   ├── advanced_analytics.py # VaR, Cohorts, Churn, HHI, Monte Carlo & Markowitz Optimization
│   ├── recommender.py        # Rule-based risk-appetite mutual fund recommender
│   ├── email_report.py       # B5 automated HTML performance email report generator
│   ├── schedule_etl.py       # B1 weekday 8 PM daemon ETL scheduler script
│   ├── generate_all_notebooks.py # Programmatic notebook executor & builder
│   ├── export_dashboard.py   # Programmatic dashboard screen exporter
│   ├── generate_presentation.py # PowerPoint Slide Deck compiler
│   └── generate_final_report.py # Executive PDF report compiler (ReportLab)
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

## Day 5: Power BI / Tableau Integration Guide

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

