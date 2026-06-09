"""
Data cleaning pipeline.

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
    "portfolio_holdings": ["amfi_code"],
}

# rows null in any of these columns are dropped
CRITICAL_COLS: dict[str, list[str]] = {
    "fund_master": ["amfi_code"],
    "nav_history": ["amfi_code", "date", "nav"],
    "aum_by_fund_house": ["date", "fund_house"],
    "monthly_sip_inflows": ["month"],
    "category_inflows": ["month", "category"],
    "industry_folio_count": ["month"],
    "scheme_performance": ["amfi_code"],
    "investor_transactions": ["investor_id", "amfi_code", "transaction_date", "amount_inr"],
    "portfolio_holdings": ["amfi_code", "stock_symbol"],
    "benchmark_indices": ["date", "index_name"],
}


def clean_frame(name: str, df: pd.DataFrame) -> pd.DataFrame:
    """Apply the standard cleaning steps to a single dataset."""
    start = len(df)
    df.columns = [c.strip() for c in df.columns]

    # trim string columns, turn blanks into NA
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().replace("", pd.NA)

    # integer coercion (nullable Int64)
    for col in INT_COLS.get(name, []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df = df.drop_duplicates()
    df = df.dropna(subset=CRITICAL_COLS.get(name, []))

    # normalise parsed dates to ISO strings for stable CSV/SQLite storage
    for col in DATE_COLS.get(name, []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

    if name == "nav_history":
        # Handle weekends/holidays in NAV: reindex each group to full calendar daily range and ffill()
        df['date'] = pd.to_datetime(df['date'])
        min_date = df['date'].min()
        max_date = df['date'].max()
        full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        
        reindexed_dfs = []
        for code, group in df.groupby('amfi_code'):
            group_reindexed = group.set_index('date').reindex(full_date_range)
            group_reindexed['amfi_code'] = code
            group_reindexed['nav'] = group_reindexed['nav'].ffill()
            group_reindexed = group_reindexed.reset_index().rename(columns={'index': 'date'})
            reindexed_dfs.append(group_reindexed)
            
        df = pd.concat(reindexed_dfs, ignore_index=True)
        df['date'] = df['date'].dt.strftime("%Y-%m-%d")
        df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

    logger.info("%s: %d -> %d rows (removed %d)", name, start, len(df), start - len(df))
    return df


def run() -> dict[str, Path]:
    """Clean every dataset and write cleaned CSVs. Returns name -> output path."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}
    for name, fname in RAW_FILES.items():
        try:
            df = pd.read_csv(RAW_DIR / fname, parse_dates=DATE_COLS.get(name) or None)
            cleaned = clean_frame(name, df)
            out_path = PROCESSED_DIR / f"clean_{name}.csv"
            cleaned.to_csv(out_path, index=False)
            outputs[name] = out_path
        except Exception:
            logger.exception("Failed to clean %s", name)
            raise
    logger.info("Cleaning complete: %d datasets written to %s", len(outputs), PROCESSED_DIR)
    return outputs


if __name__ == "__main__":
    run()
