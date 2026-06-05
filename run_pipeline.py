"""
Master Pipeline Orchestrator for Bluestock Mutual Fund Analytics Platform.

Runs all sequential tasks of the 7-day capstone project:
1. Data cleaning (Day 2)
2. Database building and integrity checks (Day 2)
3. Performance analytics and scorecard calculations (Day 4)
4. Advanced risk analytics, behavioral reports, and Jupyter Notebook (Day 6)
5. Dashboard screenshots and PDF exports (Day 5)
6. PowerPoint presentation slide deck compilation (Day 7)
7. Executive PDF report generation (Day 7)
"""
from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

# Ensure scripts folder is importable
ROOT: Path = Path(__file__).resolve().parent
SCRIPTS_DIR: Path = ROOT / "scripts"

def run_script(script_name: str) -> bool:
    """Execute a python script in the scripts directory using the current interpreter."""
    script_path = SCRIPTS_DIR / script_name
    print(f"\n==================================================")
    print(f"RUNNING: {script_name}...")
    print(f"==================================================")
    
    cmd = [sys.executable, str(script_path)]
    try:
        # Run process and pipe output
        result = subprocess.run(cmd, cwd=str(ROOT), check=True, text=True)
        print(f"SUCCESS: {script_name} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {script_name} failed with exit code {e.returncode}.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred running {script_name}: {e}", file=sys.stderr)
        return False

def main() -> None:
    print("======================================================================")
    print("STARTING BLUESTOCK MUTUAL FUND ANALYTICS PIPELINE ORCHESTRATION")
    print(f"Execution Time : {subprocess.check_output(['powershell', '-Command', 'Get-Date -Format g']).decode().strip()}")
    print("======================================================================")
    
    steps = [
        ("etl_pipeline.py", "ETL Pipeline: Ingestion, Cleaning, and SQLite Load"),
        ("compute_metrics.py", "Computing Returns, Sharpe, Sortino, Alpha, Beta, Max Drawdown, and Scorecard"),
        ("advanced_analytics.py", "Advanced Analytics: VaR, Cohorts, Churn, HHI, Monte Carlo & Markowitz Optimization"),
        ("generate_all_notebooks.py", "Generating and Executing all 5 Jupyter Notebooks"),
        ("email_report.py", "Generating Weekly HTML Email Performance Report Preview"),
        ("export_dashboard.py", "Generating Dashboard Mockups & Dashboard.pdf"),
        ("generate_presentation.py", "Generating PowerPoint Presentation Slide Deck"),
        ("generate_final_report.py", "Generating Executive Final PDF Report")
    ]
    
    success = True
    for script, description in steps:
        print(f"\n>>> Step: {description}")
        if not run_script(script):
            success = False
            print(f"\n!!! PIPELINE BROKEN AT: {script} !!!", file=sys.stderr)
            break
            
    print("\n======================================================================")
    if success:
        print("PIPELINE EXECUTED SUCCESSFULLY! All deliverables are up-to-date.")
        print("Deliverables available under:")
        print(f"  - Database: data/db/bluestock_mf.db")
        print(f"  - Jupyter Notebooks: notebooks/01_data_ingestion.ipynb to 05_advanced_analytics.ipynb")
        print(f"  - Reports: reports/Final_Report.pdf, reports/Dashboard.pdf, reports/weekly_performance_report.html")
        print(f"  - Presentation: reports/Presentation.pptx")
        print(f"  - Cleaned CSVs: data/processed/clean_*.csv")
    else:
        print("PIPELINE EXECUTION FAILED. Please review the errors above.")
    print("======================================================================")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
