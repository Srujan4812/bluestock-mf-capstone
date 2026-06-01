"""
Day 1 - Live NAV fetch for Bluestock Mutual Fund Analytics.

Fetches the latest NAV for a fixed set of AMFI scheme codes from the public
AMFI-backed API (api.mfapi.in, keyed by AMFI scheme code) and saves the result
to data/processed/live_nav.csv.
"""
from pathlib import Path
from datetime import datetime
import csv
import requests

AMFI_CODES = [125497, 119551, 120503, 118632, 119092, 120841]
API_URL = "https://api.mfapi.in/mf/{}"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "live_nav.csv"
FIELDS = ["amfi_code", "scheme_name", "fund_house", "nav", "nav_date", "fetched_at"]


def fetch_nav(code):
    resp = requests.get(API_URL.format(code), timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    meta = payload.get("meta") or {}
    series = payload.get("data") or []
    latest = series[0] if series else {}
    return {
        "amfi_code": code,
        "scheme_name": meta.get("scheme_name", ""),
        "fund_house": meta.get("fund_house", ""),
        "nav": latest.get("nav", ""),
        "nav_date": latest.get("date", ""),
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
    }


def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for code in AMFI_CODES:
        try:
            row = fetch_nav(code)
            rows.append(row)
            print(f"OK   {code}: NAV {row['nav']} on {row['nav_date']}  ({row['scheme_name']})")
        except Exception as exc:
            print(f"FAIL {code}: {exc}")

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} NAV rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
