# Bluestock Mutual Fund Analytics

End-to-end analytics project on Indian mutual fund data (NAVs, AUM, SIP inflows,
scheme performance, investor transactions and portfolio holdings).

> **Day 1 scope only:** project setup, data ingestion + quality report,
> fund_master exploration, AMFI code validation, and live NAV fetch.

## Project structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/          # 10 source CSV datasets
│   └── processed/    # generated outputs (e.g. live_nav.csv)
├── notebooks/        # exploratory notebooks
├── sql/              # SQL scripts
├── dashboard/        # dashboard assets
├── reports/          # generated reports (data_quality_report.txt)
├── scripts/
│   ├── data_ingestion.py
│   └── live_nav_fetch.py
├── logs/
├── requirements.txt
├── .gitignore
└── README.md
```

## Datasets (`data/raw/`)

| File | Key columns | Grain |
|------|-------------|-------|
| 01_fund_master.csv | amfi_code, fund_house, scheme_name, category, sub_category, plan, launch_date, benchmark, expense_ratio_pct, exit_load_pct, min_sip_amount, min_lumpsum_amount, fund_manager, risk_category, sebi_category_code | one row per scheme (amfi_code) |
| 02_nav_history.csv | amfi_code, date, nav | daily NAV per scheme |
| 03_aum_by_fund_house.csv | date, fund_house, aum_lakh_crore, aum_crore, num_schemes | quarterly AUM per fund house |
| 04_monthly_sip_inflows.csv | month, sip_inflow_crore, active_sip_accounts_crore, new_sip_accounts_lakh, sip_aum_lakh_crore, yoy_growth_pct | monthly industry SIP |
| 05_category_inflows.csv | month, category, net_inflow_crore | monthly net inflow per category |
| 06_industry_folio_count.csv | month, total_folios_crore, equity/debt/hybrid/others_folios_crore | monthly industry folios |
| 07_scheme_performance.csv | amfi_code, returns, alpha, beta, sharpe_ratio, sortino_ratio, std_dev_ann_pct, max_drawdown_pct, aum_crore, morningstar_rating, risk_grade | one row per scheme |
| 08_investor_transactions.csv | investor_id, transaction_date, amfi_code, transaction_type, amount_inr, state, city, city_tier, age_group, gender, annual_income_lakh, payment_mode, kyc_status | one row per transaction |
| 09_portfolio_holdings.csv | amfi_code, stock_symbol, stock_name, sector, weight_pct, market_value_cr, current_price_inr, portfolio_date | one row per holding |
| 10_benchmark_indices.csv | date, index_name, close_value | daily index close |

### Relationships
- `amfi_code` is the primary key in **fund_master** and the foreign key joining
  **nav_history**, **scheme_performance**, **investor_transactions** and
  **portfolio_holdings**.
- `fund_house` links **fund_master** ↔ **aum_by_fund_house**.
- `category` links **fund_master** ↔ **category_inflows**.
- `benchmark` (fund_master) maps loosely to `index_name` in **benchmark_indices**.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Load all datasets, print profiles, explore fund_master, validate AMFI codes,
# and write reports/data_quality_report.txt
python scripts/data_ingestion.py

# Fetch latest NAV for the assigned AMFI codes -> data/processed/live_nav.csv
python scripts/live_nav_fetch.py
```

`live_nav_fetch.py` calls the public AMFI-backed API `https://api.mfapi.in/mf/<amfi_code>`
and requires internet access.
