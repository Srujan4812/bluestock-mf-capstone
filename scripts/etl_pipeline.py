"""
Master ETL Pipeline Orchestrator for Bluestock MF Analytics.

Runs sequentially:
1. Ingestion profiling & validation (data_ingestion.py)
2. Cleaning raw files & SQLite DB Loading (build_database.py)
"""
from __future__ import annotations
import sys
from pathlib import Path

# Add scripts path to system path
sys.path.append(str(Path(__file__).resolve().parent))

import data_ingestion
import build_database
from _common import get_logger

logger = get_logger("etl_pipeline")

def run():
    logger.info("Executing Ingestion & Profiling step...")
    data_ingestion.main()
    logger.info("Executing Cleaning & DB Loading step...")
    build_database.main()
    logger.info("ETL Pipeline Execution Complete!")

if __name__ == "__main__":
    run()
