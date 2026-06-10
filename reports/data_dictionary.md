# Mutual Fund Analytics - Data Dictionary

This document outlines the data schema definitions for the key relational tables stored in `bluestock_mf.db` and their source datasets.

## 01_fund_master

| Column | Type | Description |
| :--- | :--- | :--- |
| amfi_code | INTEGER (PK) | Unique scheme identifier code assigned by AMFI |
| fund_house | TEXT | Asset Management Company (AMC) name |
| scheme_name | TEXT | Full name of the mutual fund scheme |
| category | TEXT | Asset class category (Equity / Debt) |
| sub_category | TEXT | Detailed category classification (Large Cap, Small Cap, Gilt, etc.) |
| plan | TEXT | Plan type (Direct or Regular) |
| launch_date | DATE | Inception/Launch date of the scheme |
| benchmark | TEXT | Benchmark index assigned to the scheme |
| expense_ratio_pct| REAL | Fund expense ratio in percentage points |
| exit_load_pct | REAL | Exit load percentage applied on redemptions |
| fund_manager | TEXT | Primary manager of the fund |
| risk_category | TEXT | SEBI risk category label (Low, Moderate, High, etc.) |
| sebi_category_code| TEXT | Internal regulatory classification code |

---

## 02_nav_history

| Column | Type | Description |
| :--- | :--- | :--- |
| amfi_code | INTEGER (FK) | Reference code linking to `01_fund_master` |
| date | DATE | Trading date of the NAV (Business days only) |
| nav | REAL | Net Asset Value per unit in INR |

---

## 03_aum_by_fund_house

| Column | Type | Description |
| :--- | :--- | :--- |
| fund_house | TEXT (PK) | AMC name |
| date | DATE (PK) | Reporting quarter-end date |
| aum_lakh_crore | REAL | Total Assets Under Management in lakh crores |
| aum_crore | INTEGER | Total Assets Under Management in crores |
| num_schemes | INTEGER | Number of active schemes offered |

---

## 04_monthly_sip_inflows

| Column | Type | Description |
| :--- | :--- | :--- |
| month | TEXT (PK) | Calendar month in YYYY-MM format |
| sip_inflow_crore | INTEGER | Total monthly SIP inflows in INR crores |
| active_sip_accounts_crore | REAL | Total number of active SIP accounts in crores |
| new_sip_accounts_lakh | REAL | New SIP accounts registered during the month in lakhs |
| sip_aum_lakh_crore | REAL | Total SIP Assets Under Management in lakh crores |
| yoy_growth_pct | REAL | Calculated year-on-year growth rate of inflows |

---

## 05_category_inflows

| Column | Type | Description |
| :--- | :--- | :--- |
| month | TEXT (PK) | Calendar month in YYYY-MM format |
| category | TEXT (PK) | Detailed category class (Large Cap, Mid Cap, ELSS, etc.) |
| net_inflow_crore | REAL | Net monthly inflows/outflows in INR crores |

---

## 06_industry_folio_count

| Column | Type | Description |
| :--- | :--- | :--- |
| month | TEXT (PK) | Reporting month in YYYY-MM format |
| total_folios_crore | REAL | Total mutual fund folios in crores |
| equity_folios_crore | REAL | Total equity-oriented folios in crores |
| debt_folios_crore | REAL | Total debt-oriented folios in crores |
| hybrid_folios_crore | REAL | Total hybrid-oriented folios in crores |
| others_folios_crore | REAL | Total other category folios in crores |

---

## 07_scheme_performance

| Column | Type | Description |
| :--- | :--- | :--- |
| amfi_code | INTEGER (FK) | Reference code linking to `01_fund_master` |
| scheme_name | TEXT | Scheme name |
| fund_house | TEXT | Asset Management Company (AMC) name |
| category | TEXT | Asset class category (Equity / Debt) |
| plan | TEXT | Plan type (Direct or Regular) |
| return_1yr_pct | REAL | Annual absolute return rate |
| return_3yr_pct | REAL | 3-year CAGR percentage |
| return_5yr_pct | REAL | 5-year CAGR percentage |
| benchmark_3yr_pct | REAL | Calculated 3-year CAGR of the benchmark index |
| alpha | REAL | Outperformance return above the benchmark |
| beta | REAL | Calculated market volatility sensitivity |
| sharpe_ratio | REAL | Annualized Sharpe risk-adjusted return ratio |
| sortino_ratio | REAL | Annualized Sortino downside risk-adjusted return ratio |
| std_dev_ann_pct | REAL | Annualized volatility of returns |
| max_drawdown_pct | REAL | Maximum peak-to-trough value drop in percentage |
| aum_crore | INTEGER | Scheme-specific Assets Under Management in crores |
| expense_ratio_pct | REAL | Scheme expense ratio |
| morningstar_rating | INTEGER | Numerical rating score (1-5 stars) |
| risk_grade | TEXT | Relative risk label based on metrics |

---

## 08_investor_transactions

| Column | Type | Description |
| :--- | :--- | :--- |
| investor_id | TEXT | Unique identifier for the investor |
| transaction_date | DATE | Execution date of the transaction |
| amfi_code | INTEGER (FK) | Scheme identifier |
| transaction_type | TEXT | Transaction category (SIP / Lumpsum / Redemption) |
| amount_inr | INTEGER | Transaction value in INR |
| state | TEXT | State of residence of the investor |
| city | TEXT | City of residence of the investor |
| city_tier | TEXT | City classification (T30 / B30) |
| age_group | TEXT | Investor age demographic band |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Declared annual income in lakhs |
| payment_mode | TEXT | Mode of transaction (UPI, Net Banking, Cheque, Mandate) |
| kyc_status | TEXT | Investor verification status (Verified / Pending) |

---

## 09_portfolio_holdings

| Column | Type | Description |
| :--- | :--- | :--- |
| amfi_code | INTEGER (FK) | Scheme identifier code |
| stock_symbol | TEXT | Trading ticker symbol of the held stock |
| stock_name | TEXT | Corporate company name |
| sector | TEXT | Economic sector classification |
| weight_pct | REAL | Portfolio weight of the holding in percentage points |
| market_value_cr | REAL | Total value of holding in INR crores |
| current_price_inr | REAL | Latest share price of the holding stock in INR |
| portfolio_date | DATE | Valuation date of the portfolio holdings |

---

## 10_benchmark_indices

| Column | Type | Description |
| :--- | :--- | :--- |
| date | DATE | Market trading day |
| index_name | TEXT | Index identifier (NIFTY50, NIFTY100, BSE_SMALLCAP, etc.) |
| close_value | REAL | Closing value of the index |
