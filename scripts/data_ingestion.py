"""
Data ingestion & quality report generator.

Loads all 10 raw CSV datasets and reports: shape, dtypes, head, missing values,
duplicates and datatype issues. Also explores fund_master and validates AMFI
codes between fund_master and nav_history. A copy of the report is written to
reports/data_quality_report.txt.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
REPORT_PATH = ROOT / "reports" / "data_quality_report.txt"

# dataset key -> (filename, date columns to parse)
DATASETS = {
    "fund_master":           ("01_fund_master.csv",          ["launch_date"]),
    "nav_history":           ("02_nav_history.csv",          ["date"]),
    "aum_by_fund_house":     ("03_aum_by_fund_house.csv",    ["date"]),
    "monthly_sip_inflows":   ("04_monthly_sip_inflows.csv",  []),
    "category_inflows":      ("05_category_inflows.csv",     []),
    "industry_folio_count":  ("06_industry_folio_count.csv", []),
    "scheme_performance":    ("07_scheme_performance.csv",   []),
    "investor_transactions": ("08_investor_transactions.csv", ["transaction_date"]),
    "portfolio_holdings":    ("09_portfolio_holdings.csv",   ["portfolio_date"]),
    "benchmark_indices":     ("10_benchmark_indices.csv",    ["date"]),
}

_lines = []


def log(msg=""):
    """Print to console and buffer for the report file."""
    print(msg)
    _lines.append(str(msg))


def load_all():
    data = {}
    for key, (fname, dates) in DATASETS.items():
        data[key] = pd.read_csv(RAW_DIR / fname, parse_dates=dates or None)
    return data


def detect_dtype_issues(df):
    """Flag object columns that look numeric or like dates (possible parsing issues)."""
    issues = []
    for col in df.select_dtypes(include="object").columns:
        s = df[col].dropna()
        if s.empty:
            continue
        numeric_ratio = pd.to_numeric(s, errors="coerce").notna().mean()
        if numeric_ratio > 0.95:
            issues.append(f"'{col}' is object but {numeric_ratio:.0%} numeric")
        elif "date" in col.lower() and not pd.api.types.is_datetime64_any_dtype(df[col]):
            issues.append(f"'{col}' looks like a date but stored as object")
    return issues


def profile(key, df):
    log("=" * 70)
    log(f"DATASET: {key}  ({DATASETS[key][0]})")
    log("=" * 70)
    log(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    log("\n-- Dtypes --")
    log(df.dtypes.to_string())

    log("\n-- Head --")
    log(df.head().to_string())

    log("\n-- Missing values (count / %) --")
    miss = df.isna().sum()
    miss_pct = (miss / len(df) * 100).round(2)
    miss_tbl = pd.DataFrame({"missing": miss, "pct": miss_pct})
    miss_tbl = miss_tbl[miss_tbl["missing"] > 0]
    log(miss_tbl.to_string() if not miss_tbl.empty else "None")

    dup = int(df.duplicated().sum())
    log(f"\n-- Duplicate rows: {dup} --")

    issues = detect_dtype_issues(df)
    log("\n-- Datatype issues --")
    log("\n".join(issues) if issues else "None")
    log("")


def explore_fund_master(df):
    log("#" * 70)
    log("FUND MASTER EXPLORATION")
    log("#" * 70)
    log(f"Total schemes: {len(df)}")
    for col, label in [
        ("fund_house", "Fund houses"),
        ("category", "Categories"),
        ("sub_category", "Sub-categories"),
        ("risk_category", "Risk grades"),
    ]:
        vals = sorted(df[col].dropna().unique().tolist())
        log(f"\n{label} ({len(vals)}):")
        log(", ".join(map(str, vals)))
    log("")


def validate_amfi_codes(fund_master, nav_history):
    log("#" * 70)
    log("AMFI CODE VALIDATION: fund_master <-> nav_history")
    log("#" * 70)
    master_codes = set(fund_master["amfi_code"].unique())
    nav_codes = set(nav_history["amfi_code"].unique())

    log(f"Unique AMFI codes in fund_master : {len(master_codes)}")
    log(f"Unique AMFI codes in nav_history : {len(nav_codes)}")
    log(f"Matched codes                    : {len(master_codes & nav_codes)}")

    no_nav = sorted(master_codes - nav_codes)
    orphan_nav = sorted(nav_codes - master_codes)
    log(f"\nIn fund_master but NO NAV history ({len(no_nav)}):")
    log(", ".join(map(str, no_nav)) if no_nav else "None")
    log(f"\nIn nav_history but NOT in fund_master ({len(orphan_nav)}):")
    log(", ".join(map(str, orphan_nav)) if orphan_nav else "None")
    log("")


def main():
    data = load_all()
    log(f"Loaded {len(data)} datasets from {RAW_DIR}\n")

    for key, df in data.items():
        profile(key, df)

    explore_fund_master(data["fund_master"])
    validate_amfi_codes(data["fund_master"], data["nav_history"])

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(_lines), encoding="utf-8")
    print(f"\nData quality report saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()
