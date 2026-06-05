"""
Day 5 / Bonus B1 - Weekday 8 PM ETL Scheduler.

Runs continuously in the background, checking every 30 seconds if it is 8:00 PM (20:00)
on a weekday (Monday to Friday), and if so, triggers the ETL pipeline orchestrator.
"""
from __future__ import annotations

import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Resolve base paths
ROOT = Path(__file__).resolve().parents[1]
ETL_SCRIPT = ROOT / "scripts" / "etl_pipeline.py"

def run_scheduler():
    print("======================================================================")
    print("BLUESTOCK ETL SCHEDULER DEAMON ACTIVE")
    print(f"System Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Trigger Target : Weekdays (Mon-Fri) at 20:00 (8:00 PM)")
    print("======================================================================")
    
    last_run_date = None
    
    try:
        while True:
            now = datetime.now()
            # Weekday check: Monday is 0, Sunday is 6
            is_weekday = now.weekday() < 5
            is_8pm = now.hour == 20 and now.minute == 0
            today_str = now.strftime("%Y-%m-%d")
            
            if is_weekday and is_8pm and last_run_date != today_str:
                print(f"\n[{now.strftime('%H:%M:%S')}] Target trigger matched! Launching ETL pipeline...")
                cmd = [sys.executable, str(ETL_SCRIPT)]
                try:
                    # Execute process
                    result = subprocess.run(cmd, cwd=str(ROOT), check=True, text=True)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ETL Pipeline executed successfully.")
                    last_run_date = today_str
                except subprocess.CalledProcessError as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: ETL pipeline failed with exit code {e.returncode}.", file=sys.stderr)
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: Unexpected error running ETL: {e}", file=sys.stderr)
            
            # Check every 30 seconds
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nScheduler daemon stopped by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    run_scheduler()
