CREATE TABLE dim_fund (
    fund_key INTEGER PRIMARY KEY,
    amfi_code INTEGER,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    risk_category TEXT
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER
);

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY,
    fund_key INTEGER,
    date_key INTEGER,
    nav REAL
);

CREATE TABLE fact_transactions (
    txn_id INTEGER PRIMARY KEY,
    fund_key INTEGER,
    date_key INTEGER,
    amount REAL,
    transaction_type TEXT
);

CREATE TABLE fact_performance (
    perf_id INTEGER PRIMARY KEY,
    fund_key INTEGER,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL,
    expense_ratio REAL
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY,
    fund_key INTEGER,
    date_key INTEGER,
    aum REAL
);