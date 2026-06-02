# PROGRESS LOG — Bluestock Mutual Fund Analytics Capstone

_Last updated: 2026-06-02 (session 1)_

## End goal
Complete the **Bluestock Mutual Fund Analytics Capstone** (7-day roadmap) using the
real datasets in the workspace — no placeholder data. Deliverables span ETL,
SQLite DB, EDA, performance analytics, dashboard, advanced analytics and final docs.

GitHub repo: https://github.com/Srujan4812/bluestock-mf-capstone

## What we completed today

### Environment
- Installed **Python 3.12.10** (via winget) — `C:\Users\madhu\AppData\Local\Programs\Python\Python312\python.exe`
- Created virtual env **`.venv`** in the project root
- Installed all 9 required deps: pandas, numpy, scipy, matplotlib, seaborn,
  plotly, sqlalchemy, requests, jupyter (see `requirements.txt`)
- Installed **Git** (via winget) — `C:\Program Files\Git\cmd\git.exe`

### Day 1 — Project Setup + Data Ingestion (DONE, pushed)
- Folder structure: `data/raw`, `data/processed`, `notebooks`, `sql`, `dashboard`,
  `reports`, `scripts`, `logs`
- Copied all 10 source CSVs into `data/raw/`
- `scripts/data_ingestion.py` — loads 10 CSVs; prints shape/dtypes/head; reports
  missing values, duplicates, datatype issues; explores fund_master (fund houses,
  categories, sub-categories, risk grades); validates AMFI codes
  (fund_master ↔ nav_history = **40/40 matched**); writes
  `reports/data_quality_report.txt`
- `scripts/live_nav_fetch.py` — fetches full NAV history from api.mfapi.in for
  125497, 119551, 120503, 118632, 119092, 120841 → `data/raw/live_nav.csv`
  (**19,792 rows, 6 schemes**)
- `requirements.txt`, `.gitignore`, `README.md` created

### Day 2 — Cleaning + SQLite (DONE locally + pushed; see caveat)
- `scripts/_common.py` — shared paths + logging (logs to console + `logs/*.log`)
- `scripts/data_cleaning.py` — cleans all 10 datasets → `data/processed/clean_*.csv`
  (type coercion, date→ISO, whitespace trim, dedup, critical-null drop).
  **0 rows removed** — source data was already clean
- `sql/schema.sql` — 10 tables, PKs, FKs to `fund_master(amfi_code)`, indexes
- `scripts/build_database.py` — builds `data/processed/bluestock.db`, loads cleaned
  data FK-safe, runs validation → `reports/day2_validation_report.txt`
  (**ALL CHECKS PASSED**: row counts match, 0 FK orphans, 0 bad values), and
  executes all 11 statements in `sql/queries.sql`
- `sql/queries.sql` — 4 validation + 7 analytics queries

### Dataset facts (real, verified)
- 40 schemes; fund_master amfi_code is the PK / FK across nav_history,
  scheme_performance, investor_transactions, portfolio_holdings — **0 orphans** anywhere
- Row counts: nav_history 46,000 · investor_transactions 32,778 ·
  benchmark_indices 8,050 · category_inflows 144 · aum 90 · sip 48 · folio 21 ·
  fund_master / scheme_performance 40 · portfolio_holdings 322 (34 funds w/ holdings)
- Categories: Debt, Equity · Sub-categories (12): ELSS, Flexi Cap, Gilt, Index,
  Index/ETF, Large & Mid Cap, Large Cap, Liquid, Mid Cap, Short Duration, Small Cap, Value
- Risk grades: Low, Moderate, Moderately High, High, Very High
- Note: "risk grade" column is `risk_category` in fund_master but `risk_grade` in scheme_performance
- monthly_sip_inflows.yoy_growth_pct has 12 genuine NULLs (first 12 months — expected)

### Git / GitHub state
- Branch: **main** (renamed from master), remote `origin` → the repo URL above
- Latest commit pushed: **76ccf50** (local == remote, in sync)
- History:
  - 76ccf50 Day 1: complete dependency list + full live NAV history as raw CSV
  - 0218fe3 chore: add *.db and .env to .gitignore
  - e57ecb7 Day 2: data cleaning pipeline, SQLite schema + build/load, validation queries
  - 859e422 Day 1: project setup, data ingestion + quality report, AMFI validation, live NAV fetch
- `.gitignore` excludes: `*.db`, `__pycache__/`, `.ipynb_checkpoints/`, `.env`,
  `.venv/`, `logs/*`, `data/processed/*`, `reports/*` (all keep `.gitkeep`)
- Committed with inline identity (name "Bluestock Capstone", email madhu481208@gmail.com);
  global git config left unchanged

## Open caveats / things to flag
1. **Live scheme names differ from the brief.** mfapi.in maps 125497→"SBI Small Cap",
   119551→"Aditya Birla Banking & PSU Debt" etc., NOT the brief's labels
   (HDFC Top 100 / SBI Bluechip). The capstone dataset amfi_codes are synthetic, so
   they don't line up with the live API. Real API data cannot be changed.
2. **Day 1 commit message** is descriptive, not the literal "Day 1: Data ingestion
   complete" from the brief. Not rewritten (would need a destructive force-push).
3. **DB location vs brief folder spec.** Brief expects `data/db/bluestock_mf.db`;
   we built `data/processed/bluestock.db`. Realign in Day 2 cleanup if the rubric needs it.

## How to resume
```bash
# from project root: C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone
.venv\Scripts\activate            # activate env (or call .venv\Scripts\python.exe directly)

python scripts/data_ingestion.py  # Day 1 ingestion + quality report
python scripts/live_nav_fetch.py  # Day 1 live NAV  (needs internet)
python scripts/data_cleaning.py   # Day 2 clean CSVs
python scripts/build_database.py  # Day 2 build + validate bluestock.db
```
Tools: Python `C:\Users\madhu\AppData\Local\Programs\Python\Python312\python.exe`,
Git `C:\Program Files\Git\cmd\git.exe`. Source datasets also at
`C:\Users\madhu\Downloads\drive-download-20260601T185428Z-3-001`.

## Next phases (NOT started)
- **Phase 3 (D3):** EDA notebook `notebooks/03_eda_analysis.ipynb` — charts + insights
- **Phase 4 (D4):** Performance analytics — CAGR (annualise with 252 trading days),
  Sharpe, Sortino, Alpha, Beta, Max Drawdown → `scripts/compute_metrics.py` + CSVs
- **Phase 5 (D5):** Dashboard (Power BI .pbix or Streamlit) — 4 pages, ≥2 slicers each
- **Phase 6 (D6):** Advanced — VaR, CVaR, cohort analysis, recommender (`recommender.py`)
- **Phase 7 (D7):** Final report (.pdf) + presentation (.pptx)
- Bonus: cron NAV fetch, Streamlit app, Monte Carlo, Markowitz frontier, email report

## Gotchas learned this session
- The shell strips `$_`/`$var` in some inline PowerShell — avoid pipeline vars; call
  `.venv\Scripts\python.exe` directly.
- Git/Python write progress to **stderr**, so PowerShell may report exit code 1 even on
  success — verify by the actual output, not just the code.
- Don't reindex NAV on calendar days; ffill after reindexing to a full date range (future phases).
