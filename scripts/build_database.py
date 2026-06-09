"""
Builds and validates the SQLite database.

Creates the SQLite database from ``sql/schema.sql``, loads every cleaned dataset 
in foreign-key-safe order, runs referential-integrity and sanity validation checks, 
and confirms ``sql/queries.sql`` executes. A validation report is written to 
``reports/database_validation_report.txt``.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

import data_cleaning
from _common import DB_PATH, PROCESSED_DIR, REPORTS_DIR, SQL_DIR, get_logger

logger = get_logger("build_database")

REPORT_PATH = REPORTS_DIR / "database_validation_report.txt"

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
    """Run validation checks and return human-readable report lines."""
    lines: list[str] = ["DAY 2 VALIDATION REPORT", "=" * 40, ""]
    ok = True

    lines.append("[Row counts: DB vs cleaned CSV]")
    for table, expected in csv_counts.items():
        actual = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        status = "OK" if actual == expected else "MISMATCH"
        ok &= actual == expected
        lines.append(f"  {table:<24} csv={expected:<6} db={actual:<6} {status}")

    lines.append("\n[Foreign key integrity]")
    fk_violations = conn.execute("PRAGMA foreign_key_check").fetchall()
    ok &= not fk_violations
    lines.append(f"  foreign_key_check violations: {len(fk_violations)}")
    for table in CHILD_TABLES:
        orphans = conn.execute(
            f"SELECT COUNT(*) FROM {table} "
            "WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master)"
        ).fetchone()[0]
        ok &= orphans == 0
        lines.append(f"  {table:<24} orphan amfi_code: {orphans}")

    lines.append("\n[Value sanity checks]")
    bad_nav = conn.execute("SELECT COUNT(*) FROM nav_history WHERE nav <= 0").fetchone()[0]
    bad_amt = conn.execute(
        "SELECT COUNT(*) FROM investor_transactions WHERE amount_inr <= 0"
    ).fetchone()[0]
    ok &= bad_nav == 0 and bad_amt == 0
    lines.append(f"  non-positive NAV rows:        {bad_nav}")
    lines.append(f"  non-positive amount rows:     {bad_amt}")

    lines.append("\n" + ("ALL CHECKS PASSED" if ok else "VALIDATION FAILED"))
    return lines


def run_queries(conn: sqlite3.Connection) -> None:
    """Execute every statement in queries.sql to confirm validity."""
    sql = (SQL_DIR / "queries.sql").read_text(encoding="utf-8")
    for i, chunk in enumerate(sql.split(";"), 1):
        # drop full-line comments, keep the SQL body
        code = "\n".join(
            ln for ln in chunk.splitlines() if not ln.strip().startswith("--")
        ).strip()
        if not code:
            continue
        rows = conn.execute(code).fetchall()
        logger.info("queries.sql statement %d OK -> %d rows", i, len(rows))


def main() -> None:
    data_cleaning.run()  # ensure fresh cleaned CSVs
    if DB_PATH.exists():
        DB_PATH.unlink()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        create_schema(conn)
        csv_counts = load_tables(conn)
        conn.commit()
        report = validate(conn, csv_counts)
        run_queries(conn)
    finally:
        conn.close()

    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    logger.info("Database built at %s; report at %s", DB_PATH, REPORT_PATH)


if __name__ == "__main__":
    main()
