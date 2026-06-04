PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> ollama --version
ollama : The term 'ollama' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a 
path was included, verify that the path is correct and try again.
At line:1 char:1
+ ollama --version
+ ~~~~~~
    + CategoryInfo          : ObjectNotFound: (ollama:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> Get-ChildItem "$env:LOCALAPPDATA\Programs\Ollama"


    Directory: C:\Users\madhu\AppData\Local\Programs\Ollama


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        02-06-2026     19:16                lib
-a----        14-05-2026     22:52           7502 app.ico
-a----        14-05-2026     22:57       26191752 ollama app.exe
-a----        14-05-2026     22:57       42560392 ollama.exe
-a----        02-06-2026     19:23         524761 unins000.dat
-a----        02-06-2026     19:16        4353928 unins000.exe
-a----        02-06-2026     19:23          25316 unins000.msg


PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> & "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> [Environment]::SetEnvironmentVariable(
>>     "Path",
>>     $env:Path + ";$env:LOCALAPPDATA\Programs\Ollama",
>>     "User"
>> )
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> ollama --version
ollama : The term 'ollama' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a 
path was included, verify that the path is correct and try again.
At line:1 char:1
+ ollama --version
+ ~~~~~~
    + CategoryInfo          : ObjectNotFound: (ollama:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> & "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" version
Error: unknown command "version" for "ollama"
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> & "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> & "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" help
Large language model runner

Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start Ollama
  create      Create a model
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  signin      Sign in to ollama.com
  signout     Sign out from ollama.com
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  launch      Launch the Ollama menu or an integration
  help        Help about any command

Flags:
  -h, --help         help for ollama
      --nowordwrap   Don't wrap words to the next line automatically
      --verbose      Show timings for response
  -v, --version      Show version information

Use "ollama [command] --help" for more information about a command.
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> & "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
ollama version is 0.24.0
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> & "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull qwen2.5-coder:7b
pulling manifest
pulling 60e05f210007: 100% ▕████████████████████████████████████████████████████████████████████████████████████████████████▏ 4.7 GB
pulling 66b9ea09bd5b: 100% ▕████████████████████████████████████████████████████████████████████████████████████████████████▏   68 B
pulling 1e65450c3067: 100% ▕████████████████████████████████████████████████████████████████████████████████████████████████▏ 1.6 KB
pulling 832dd9e00a68: 100% ▕████████████████████████████████████████████████████████████████████████████████████████████████▏  11 KB
pulling d9bb33f27869: 100% ▕████████████████████████████████████████████████████████████████████████████████████████████████▏  487 B
verifying sha256 digest
writing manifest
success
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> & "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" run qwen2.5-coder:7b
>>> hello
Hello! How can I help you today? Is there anything specific you would like to talk about or any questions you have? I'm here to answer any questions and      
provide information on a wide range of topics. Just let me know what's on your mind.

>>> C:\Users\madhu\Downloads\drive-download-20260601T185428Z-3-001  these are the datasets , C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone\kiro_full_s
... ession.txt this is the progress till now day 1 completed , DAY 2 — Data Cleaning + SQL Database Design
... TODO
... IMPROVEMENT
... HIGH
... Assigned to
... MU
... mugilanm0105
... SA
... sajeedahmed965
... MA
... madhu481208
... PA
... payments
... Due : 03 Jun 2026
... Time estimate: 7–8 hours
...
... Tasks:
...
... Clean nav_history.csv — parse dates to datetime, sort by amfi_code + date, forward-fill missing NAV for holidays/weekends, remove duplicates, validate NAV
...  > 0.
... Clean investor_transactions.csv — standardise transaction_type values (SIP/Lumpsum/Redemption), validate amount > 0, fix date formats, check KYC status en
... um values.
... Clean scheme_performance.csv — validate all return values are numeric, flag anomalies, check expense_ratio range (0.1% – 2.5%).
... Design SQLite star schema — write CREATE TABLE statements for dim_fund, dim_date, fact_nav, fact_transactions, fact_performance, fact_aum. Define primary 
... and foreign keys.
... Load all cleaned datasets into SQLite — use SQLAlchemy create_engine + df.to_sql(). Verify row counts match source CSVs.
... Write 10 analytical SQL queries — top 5 funds by AUM, average NAV per month, SIP YoY growth, transactions by state, funds with expense_ratio < 1%, and 5 m
... ore of your choice.
... Create data dictionary — document all columns, data types, business definitions, and source references in a Markdown file.
... Git commit: "Day 2: Cleaned data + SQLite DB loaded"
... Deliverables: 10 cleaned CSVs in data/processed/, bluestock_mf.db, schema.sql, queries.sql, data_dictionary.md                                            
...                 pls complete day 2 , and update git hub , my git hub account , madhu481208@gmail.com , Srujan4812 , https://github.com/Srujan4812/bluestoc
... k-mf-capstone
Hello Madhu! I'll help you with completing Day 2 of your project, which includes data cleaning and SQLite database design. Let's start by addressing 
each task step-by-step.

### Task: Clean nav_history.csv

1. **Parse Dates to Datetime**
   ```python
   import pandas as pd
   df = pd.read_csv('C:\\Users\\madhu\\Downloads\\drive-download-20260601T185428Z-3-001\\nav_history.csv')
   df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
   ```

2. **Sort by amfi_code + date**
   ```python
   df.sort_values(by=['amfi_code', 'date'], inplace=True)
   ```

3. **Forward-fill Missing NAV for Holidays/Weekends**
   To do this, we need a list of holidays and weekends to exclude from the forward fill.
   ```python
   holidays = pd.date_range(start='2026-01-01', end='2026-12-31', freq='BM').tolist()
   weekend_days = df['date'].dt.dayofweek.isin([5, 6])
   mask = ~df['amfi_code'].duplicated(keep='first') & (df['nav'].isna() | weekend_days)
   df.loc[mask, 'nav'] = df['nav'].ffill().bfill()
   ```

4. **Remove Duplicates**
   ```python
   df.drop_duplicates(subset=['amfi_code', 'date'], keep='first', inplace=True)
   ```

5. **Validate NAV > 0**
   ```python
   df = df[df['nav'] > 0]
   ```

### Task: Clean investor_transactions.csv

1. **Standardize Transaction Type Values (SIP/Lumpsum/Redemption)**
   ```python
   transaction_mapping = {'SIP': 'Systematic Investment Plan', 'Lumpsum': 'Lump Sum', 'Redemption': 'Redemption'}
   df['transaction_type'] = df['transaction_type'].replace(transaction_mapping)
   ```

2. **Validate Amount > 0**
   ```python
   df = df[df['amount'] > 0]
   ```

3. **Fix Date Formats**
   ```python
   df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
   ```

4. **Check KYC Status Enum Values**
   Assuming the KYC status is in a categorical format, you can validate it.
   ```python
   valid_kyc_statuses = ['Approved', 'Pending', 'Rejected']
   df = df[df['kyc_status'].isin(valid_kyc

>>> C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstonecd C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone
>>> 
Use Ctrl + d or /bye to exit.
>>> 
Use Ctrl + d or /bye to exit.
>>> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> mkdir data\processed
mkdir : An item with the specified name C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone\data\processed already exists.
At line:1 char:1
+ mkdir data\processed
+ ~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ResourceExists: (C:\Users\madhu\...\data\processed:String) [New-Item], IOException
    + FullyQualifiedErrorId : DirectoryExist,Microsoft.PowerShell.Commands.NewItemCommand

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> mkdir sql
mkdir : An item with the specified name C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone\sql already exists.
At line:1 char:1
+ mkdir sql
+ ~~~~~~~~~
    + CategoryInfo          : ResourceExists: (C:\Users\madhu\...mf_capstone\sql:String) [New-Item], IOException
    + FullyQualifiedErrorId : DirectoryExist,Microsoft.PowerShell.Commands.NewItemCommand

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> ni clean_data.py


    Directory: C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        02-06-2026     19:44              0 clean_data.py


PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> ni load_to_sqlite.py


    Directory: C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        02-06-2026     19:44              0 load_to_sqlite.py


PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> ni sql\schema.sql
ni : The file 'C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone\sql\schema.sql' already exists.
At line:1 char:1
+ ni sql\schema.sql
+ ~~~~~~~~~~~~~~~~~
    + CategoryInfo          : WriteError: (C:\Users\madhu\...\sql\schema.sql:String) [New-Item], IOException
    + FullyQualifiedErrorId : NewItemIOError,Microsoft.PowerShell.Commands.NewItemCommand

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> ni sql\queries.sql
ni : The file 'C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone\sql\queries.sql' already exists.
At line:1 char:1
+ ni sql\queries.sql
+ ~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : WriteError: (C:\Users\madhu\...sql\queries.sql:String) [New-Item], IOException
    + FullyQualifiedErrorId : NewItemIOError,Microsoft.PowerShell.Commands.NewItemCommand

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> cd C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git pull
Already up to date.
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> tree /f scripts
Folder PATH listing for volume Windows-SSD
Volume serial number is 40F9-801D
C:\USERS\MADHU\ONEDRIVE\DESKTOP\BLUESTOCK_MF_CAPSTONE\SCRIPTS
│   build_database.py
│   data_cleaning.py
│   data_ingestion.py
│   live_nav_fetch.py
│   _common.py
│   _export_session.py
│
└───__pycache__
        data_cleaning.cpython-312.pyc
        _common.cpython-312.pyc

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> tree /f sql
Folder PATH listing for volume Windows-SSD
Volume serial number is 40F9-801D
C:\USERS\MADHU\ONEDRIVE\DESKTOP\BLUESTOCK_MF_CAPSTONE\SQL
    .gitkeep
    queries.sql
    schema.sql

No subfolders exist

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> tree /f reports
Folder PATH listing for volume Windows-SSD
Volume serial number is 40F9-801D
C:\USERS\MADHU\ONEDRIVE\DESKTOP\BLUESTOCK_MF_CAPSTONE\REPORTS
    .gitkeep
    data_quality_report.txt
    day2_validation_report.txt

No subfolders exist

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> tree /f data\processed
Folder PATH listing for volume Windows-SSD
Volume serial number is 40F9-801D
C:\USERS\MADHU\ONEDRIVE\DESKTOP\BLUESTOCK_MF_CAPSTONE\DATA\PROCESSED
    .gitkeep
    bluestock.db
    clean_aum_by_fund_house.csv
    clean_benchmark_indices.csv
    clean_category_inflows.csv
    clean_fund_master.csv
    clean_industry_folio_count.csv
    clean_investor_transactions.csv
    clean_monthly_sip_inflows.csv
    clean_nav_history.csv
    clean_portfolio_holdings.csv
    clean_scheme_performance.csv
    live_nav.csv

No subfolders exist

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> Get-Content scripts\data_cleaning.py -Head 50
"""
Day 2 - Data cleaning pipeline for Bluestock Mutual Fund Analytics.

Reads the 10 raw CSV datasets and applies: column-name normalisation,
whitespace trimming, date parsing (to ISO ``YYYY-MM-DD`` strings), integer
coercion for codes/amounts, exact-duplicate removal and dropping of rows that
are null in business-critical columns. Cleaned files are written to
``data/processed/clean_<name>.csv``.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from _common import RAW_DIR, PROCESSED_DIR, get_logger

logger = get_logger("data_cleaning")

# logical name -> raw filename
RAW_FILES: dict[str, str] = {
    "fund_master": "01_fund_master.csv",
    "nav_history": "02_nav_history.csv",
    "aum_by_fund_house": "03_aum_by_fund_house.csv",
    "monthly_sip_inflows": "04_monthly_sip_inflows.csv",
    "category_inflows": "05_category_inflows.csv",
    "industry_folio_count": "06_industry_folio_count.csv",
    "scheme_performance": "07_scheme_performance.csv",
    "investor_transactions": "08_investor_transactions.csv",
    "portfolio_holdings": "09_portfolio_holdings.csv",
    "benchmark_indices": "10_benchmark_indices.csv",
}

# date columns to parse per table
DATE_COLS: dict[str, list[str]] = {
    "fund_master": ["launch_date"],
    "nav_history": ["date"],
    "aum_by_fund_house": ["date"],
    "investor_transactions": ["transaction_date"],
    "portfolio_holdings": ["portfolio_date"],
    "benchmark_indices": ["date"],
}

# integer columns to coerce
INT_COLS: dict[str, list[str]] = {
    "fund_master": ["amfi_code", "min_sip_amount", "min_lumpsum_amount"],
    "nav_history": ["amfi_code"],
    "aum_by_fund_house": ["num_schemes"],
    "scheme_performance": ["amfi_code", "morningstar_rating"],
    "investor_transactions": ["amfi_code", "amount_inr"],
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> Get-Content scripts\build_database.py -Head 50
"""
Day 2 - Build and validate the SQLite database for Bluestock MF Analytics.

Regenerates the cleaned CSVs, creates ``data/processed/bluestock.db`` from
``sql/schema.sql``, loads every cleaned dataset in foreign-key-safe order, runs
referential-integrity / sanity validation checks and confirms ``sql/queries.sql``
executes. A validation report is written to ``reports/day2_validation_report.txt``.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

import data_cleaning
from _common import DB_PATH, PROCESSED_DIR, REPORTS_DIR, SQL_DIR, get_logger

logger = get_logger("build_database")

REPORT_PATH = REPORTS_DIR / "day2_validation_report.txt"

# foreign-key-safe load order (parent first)
LOAD_ORDER: list[str] = [
    "fund_master", "nav_history", "aum_by_fund_house", "monthly_sip_inflows",
    "category_inflows", "industry_folio_count", "scheme_performance",
    "investor_transactions", "portfolio_holdings", "benchmark_indices",
]
CHILD_TABLES: list[str] = [
    "nav_history", "scheme_performance", "investor_transactions", "portfolio_holdings",
]


def create_schema(conn: sqlite3.Connection) -> None:
    """Execute schema.sql to (re)create all tables."""
    conn.executescript((SQL_DIR / "schema.sql").read_text(encoding="utf-8"))


def load_tables(conn: sqlite3.Connection) -> dict[str, int]:
    """Load each cleaned CSV into its table. Returns table -> source row count."""
    csv_counts: dict[str, int] = {}
    for table in LOAD_ORDER:
        df = pd.read_csv(PROCESSED_DIR / f"clean_{table}.csv")
        df.to_sql(table, conn, if_exists="append", index=False)
        csv_counts[table] = len(df)
        logger.info("Loaded %d rows into %s", len(df), table)
    return csv_counts


def validate(conn: sqlite3.Connection, csv_counts: dict[str, int]) -> list[str]:
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> Get-Content sql\schema.sql -Head 100
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
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> Get-Content sql\queries.sql -Head 100
-- Bluestock Mutual Fund Analytics - validation & analytical queries (Day 2)

-- == VALIDATION ==

-- V1: row count per table
SELECT 'fund_master' AS tbl, COUNT(*) AS rows FROM fund_master
UNION ALL SELECT 'nav_history', COUNT(*) FROM nav_history
UNION ALL SELECT 'aum_by_fund_house', COUNT(*) FROM aum_by_fund_house
UNION ALL SELECT 'monthly_sip_inflows', COUNT(*) FROM monthly_sip_inflows
UNION ALL SELECT 'category_inflows', COUNT(*) FROM category_inflows
UNION ALL SELECT 'industry_folio_count', COUNT(*) FROM industry_folio_count
UNION ALL SELECT 'scheme_performance', COUNT(*) FROM scheme_performance
UNION ALL SELECT 'investor_transactions', COUNT(*) FROM investor_transactions
UNION ALL SELECT 'portfolio_holdings', COUNT(*) FROM portfolio_holdings
UNION ALL SELECT 'benchmark_indices', COUNT(*) FROM benchmark_indices;

-- V2: orphan amfi_codes in child tables (expect 0 rows)
SELECT 'nav_history' AS tbl, amfi_code FROM nav_history
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master)
UNION SELECT 'scheme_performance', amfi_code FROM scheme_performance
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master)
UNION SELECT 'investor_transactions', amfi_code FROM investor_transactions
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master)
UNION SELECT 'portfolio_holdings', amfi_code FROM portfolio_holdings
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master);

-- V3: NAV values must be positive (expect 0)
SELECT COUNT(*) AS bad_nav FROM nav_history WHERE nav <= 0;

-- V4: transaction amounts must be positive (expect 0)
SELECT COUNT(*) AS bad_amount FROM investor_transactions WHERE amount_inr <= 0;

-- == ANALYTICS ==

-- A1: scheme count by category / sub_category
SELECT category, sub_category, COUNT(*) AS schemes
FROM fund_master GROUP BY category, sub_category ORDER BY schemes DESC;

-- A2: latest NAV per scheme
SELECT n.amfi_code, f.scheme_name, n.date, n.nav
FROM nav_history n
JOIN fund_master f ON f.amfi_code = n.amfi_code
JOIN (SELECT amfi_code, MAX(date) AS mx FROM nav_history GROUP BY amfi_code) m
  ON m.amfi_code = n.amfi_code AND m.mx = n.date
ORDER BY f.scheme_name;

-- A3: top 10 fund houses by latest AUM
SELECT fund_house, aum_crore, date
FROM aum_by_fund_house
WHERE date = (SELECT MAX(date) FROM aum_by_fund_house)
ORDER BY aum_crore DESC LIMIT 10;

-- A4: top 10 schemes by 3-year return
SELECT amfi_code, scheme_name, return_3yr_pct, sharpe_ratio, risk_grade
FROM scheme_performance ORDER BY return_3yr_pct DESC LIMIT 10;

-- A5: net investment flow by transaction type
SELECT transaction_type,
       COUNT(*) AS txns,
       SUM(amount_inr) AS total_inr
FROM investor_transactions GROUP BY transaction_type ORDER BY total_inr DESC;

-- A6: total SIP inflow by year
SELECT substr(month, 1, 4) AS yr, ROUND(SUM(sip_inflow_crore), 2) AS sip_crore
FROM monthly_sip_inflows GROUP BY yr ORDER BY yr;

-- A7: top sectors by aggregate holding market value
SELECT sector, ROUND(SUM(market_value_cr), 2) AS mkt_value_cr
FROM portfolio_holdings GROUP BY sector ORDER BY mkt_value_cr DESC LIMIT 10;
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> (
>> tree /f scripts
>> tree /f sql
At line:2 char:16
+ tree /f scripts
+                ~
Missing closing ')' in expression.
At line:3 char:1
+ tree /f sql
+ ~~~~
Unexpected token 'tree' in expression or statement.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : MissingEndParenthesisInExpression

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> tree /f reports
Folder PATH listing for volume Windows-SSD
Volume serial number is 40F9-801D
C:\USERS\MADHU\ONEDRIVE\DESKTOP\BLUESTOCK_MF_CAPSTONE\REPORTS
    .gitkeep
    data_quality_report.txt
    day2_validation_report.txt

No subfolders exist

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> tree /f data\processed
Folder PATH listing for volume Windows-SSD
Volume serial number is 40F9-801D
C:\USERS\MADHU\ONEDRIVE\DESKTOP\BLUESTOCK_MF_CAPSTONE\DATA\PROCESSED
    .gitkeep
    bluestock.db
    clean_aum_by_fund_house.csv
    clean_benchmark_indices.csv
    clean_category_inflows.csv
    clean_fund_master.csv
    clean_industry_folio_count.csv
    clean_investor_transactions.csv
    clean_monthly_sip_inflows.csv
    clean_nav_history.csv
    clean_portfolio_holdings.csv
    clean_scheme_performance.csv
    live_nav.csv

No subfolders exist

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> ) > day2_status.txt
At line:1 char:1
+ ) > day2_status.txt
+ ~
Unexpected token ')' in expression or statement.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : UnexpectedToken

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> notepad day2_status.txt
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> notepad reports\data_dictionary.md
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> notepad sql\star_schema.sql
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git add .
warning: in the working copy of 'PROGRESS.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'scripts/_export_session.py', LF will be replaced by CRLF the next time Git touches it
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git commit -m "Day 2: Cleaned data + SQLite DB loaded"
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'madhu@Srujan.(none)')
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git push
Everything up-to-date
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   PROGRESS.md
        new file:   clean_data.py
        new file:   day2_status.txt
        new file:   kiro_full_session.txt
        new file:   load_to_sqlite.py
        new file:   scripts/_export_session.py
        new file:   sql/star_schema.sql

PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git config user.name "Bluestock Capstone"
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git config user.email "madhu481208@gmail.com"
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git config user.name "Srujan4812"            
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git config user.email "madhu481208@gmail.com"
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git commit -m "Day 2: Cleaned data + SQLite DB loaded"
[main 683eb0c] Day 2: Cleaned data + SQLite DB loaded
 7 files changed, 3001 insertions(+)
 create mode 100644 PROGRESS.md
 create mode 100644 clean_data.py
 create mode 100644 day2_status.txt
 create mode 100644 kiro_full_session.txt
 create mode 100644 load_to_sqlite.py
 create mode 100644 scripts/_export_session.py
 create mode 100644 sql/star_schema.sql
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git push origin main
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 12 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 65.88 KiB | 876.00 KiB/s, done.
Total 8 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/Srujan4812/bluestock-mf-capstone.git
   76ccf50..683eb0c  main -> main
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
PS C:\Users\madhu\OneDrive\Desktop\bluestock_mf_capstone> 