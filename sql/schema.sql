-- Bluestock Mutual Fund Analytics - SQLite schema (Day 2)
-- Dates are stored as ISO text (YYYY-MM-DD); months as text (YYYY-MM).

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS investor_transactions;
DROP TABLE IF EXISTS portfolio_holdings;
DROP TABLE IF EXISTS scheme_performance;
DROP TABLE IF EXISTS nav_history;
DROP TABLE IF EXISTS category_inflows;
DROP TABLE IF EXISTS aum_by_fund_house;
DROP TABLE IF EXISTS monthly_sip_inflows;
DROP TABLE IF EXISTS industry_folio_count;
DROP TABLE IF EXISTS benchmark_indices;
DROP TABLE IF EXISTS fund_master;

CREATE TABLE fund_master (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT NOT NULL,
    scheme_name         TEXT NOT NULL,
    category            TEXT,
    sub_category        TEXT,
    plan                TEXT,
    launch_date         TEXT,
    benchmark           TEXT,
    expense_ratio_pct   REAL,
    exit_load_pct       REAL,
    min_sip_amount      INTEGER,
    min_lumpsum_amount  INTEGER,
    fund_manager        TEXT,
    risk_category       TEXT,
    sebi_category_code  TEXT
);

CREATE TABLE nav_history (
    amfi_code  INTEGER NOT NULL,
    date       TEXT NOT NULL,
    nav        REAL NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

CREATE TABLE aum_by_fund_house (
    date            TEXT NOT NULL,
    fund_house      TEXT NOT NULL,
    aum_lakh_crore  REAL,
    aum_crore       REAL,
    num_schemes     INTEGER,
    PRIMARY KEY (date, fund_house)
);

CREATE TABLE monthly_sip_inflows (
    month                      TEXT PRIMARY KEY,
    sip_inflow_crore           REAL,
    active_sip_accounts_crore  REAL,
    new_sip_accounts_lakh      REAL,
    sip_aum_lakh_crore         REAL,
    yoy_growth_pct             REAL
);

CREATE TABLE category_inflows (
    month            TEXT NOT NULL,
    category         TEXT NOT NULL,
    net_inflow_crore REAL,
    PRIMARY KEY (month, category)
);

CREATE TABLE industry_folio_count (
    month                 TEXT PRIMARY KEY,
    total_folios_crore    REAL,
    equity_folios_crore   REAL,
    debt_folios_crore     REAL,
    hybrid_folios_crore   REAL,
    others_folios_crore   REAL
);

CREATE TABLE scheme_performance (
    amfi_code         INTEGER PRIMARY KEY,
    scheme_name       TEXT,
    fund_house        TEXT,
    category          TEXT,
    plan              TEXT,
    return_1yr_pct    REAL,
    return_3yr_pct    REAL,
    return_5yr_pct    REAL,
    benchmark_3yr_pct REAL,
    alpha             REAL,
    beta              REAL,
    sharpe_ratio      REAL,
    sortino_ratio     REAL,
    std_dev_ann_pct   REAL,
    max_drawdown_pct  REAL,
    aum_crore         REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade        TEXT,
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

CREATE TABLE investor_transactions (
    investor_id       TEXT NOT NULL,
    transaction_date  TEXT NOT NULL,
    amfi_code         INTEGER NOT NULL,
    transaction_type  TEXT,
    amount_inr        INTEGER,
    state             TEXT,
    city              TEXT,
    city_tier         TEXT,
    age_group         TEXT,
    gender            TEXT,
    annual_income_lakh REAL,
    payment_mode      TEXT,
    kyc_status        TEXT,
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

CREATE TABLE portfolio_holdings (
    amfi_code         INTEGER NOT NULL,
    stock_symbol      TEXT NOT NULL,
    stock_name        TEXT,
    sector            TEXT,
    weight_pct        REAL,
    market_value_cr   REAL,
    current_price_inr REAL,
    portfolio_date    TEXT,
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

CREATE TABLE benchmark_indices (
    date        TEXT NOT NULL,
    index_name  TEXT NOT NULL,
    close_value REAL,
    PRIMARY KEY (date, index_name)
);

CREATE INDEX IF NOT EXISTS idx_nav_amfi ON nav_history (amfi_code);
CREATE INDEX IF NOT EXISTS idx_txn_amfi ON investor_transactions (amfi_code);
CREATE INDEX IF NOT EXISTS idx_holdings_amfi ON portfolio_holdings (amfi_code);
