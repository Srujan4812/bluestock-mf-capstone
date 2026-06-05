"""Shared paths and logging configuration for Bluestock MF Analytics."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
RAW_DIR: Path = ROOT / "data" / "raw"
PROCESSED_DIR: Path = ROOT / "data" / "processed"
REPORTS_DIR: Path = ROOT / "reports"
SQL_DIR: Path = ROOT / "sql"
LOGS_DIR: Path = ROOT / "logs"
DB_DIR: Path = ROOT / "data" / "db"
DB_PATH: Path = DB_DIR / "bluestock_mf.db"


def get_logger(name: str) -> logging.Logger:
    """Return a logger that writes to both the console and ``logs/<name>.log``."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:  # already configured
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler = logging.FileHandler(LOGS_DIR / f"{name}.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
