"""
Day 1 - Live NAV fetch for Bluestock Mutual Fund Analytics.

Fetches NAV data for a fixed set of AMFI scheme codes from the public
AMFI-backed API (api.mfapi.in, keyed by AMFI scheme code), parses the JSON
response and saves the full NAV history to ``data/raw/live_nav.csv``.

Codes (per the Day 1 brief):
    125497 (HDFC Top 100 Direct), plus 5 key schemes
    119551, 120503, 118632, 119092, 120841
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

AMFI_CODES: list[int] = [125497, 119551, 120503, 118632, 119092, 120841]
API_URL = "https://api.mfapi.in/mf/{}"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "live_nav.csv"


def fetch_history(code: int) -> pd.DataFrame:
    """GET one scheme, parse its JSON response into a NAV-history DataFrame."""
    resp = requests.get(API_URL.format(code), timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    meta = payload.get("meta") or {}
    records = payload.get("data") or []
    df = pd.DataFrame(records)
    if df.empty:
        return df
    df["amfi_code"] = code
    df["scheme_name"] = meta.get("scheme_name", "")
    df["fund_house"] = meta.get("fund_house", "")
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y").dt.strftime("%Y-%m-%d")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    return df[["amfi_code", "scheme_name", "fund_house", "date", "nav"]]


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frames: list[pd.DataFrame] = []
    for code in AMFI_CODES:
        try:
            df = fetch_history(code)
            if df.empty:
                print(f"WARN {code}: no NAV data returned")
                continue
            frames.append(df)
            latest = df.sort_values("date").iloc[-1]
            print(f"OK   {code}: {len(df):>5} rows | latest NAV {latest['nav']} "
                  f"on {latest['date']} ({latest['scheme_name']})")
        except Exception as exc:  # network / parse errors -> skip but report
            print(f"FAIL {code}: {exc}")

    if not frames:
        raise SystemExit("No NAV data fetched; check internet connectivity.")

    out = pd.concat(frames, ignore_index=True)
    out.to_csv(OUT_PATH, index=False)
    print(f"\nSaved {len(out)} NAV rows for {out['amfi_code'].nunique()} schemes -> {OUT_PATH}")


if __name__ == "__main__":
    main()
