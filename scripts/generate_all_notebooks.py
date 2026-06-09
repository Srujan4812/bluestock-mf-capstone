"""
Generate and execute all 5 Jupyter Notebooks.
"""
from __future__ import annotations

import shutil
from pathlib import Path
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"
SCRIPTS_DIR = ROOT / "scripts"

def copy_existing_notebooks():
    print("Copying existing analysis notebooks to numbered formats...")
    # 03_eda_analysis.ipynb
    eda_src = NOTEBOOKS_DIR / "EDA_Analysis.ipynb"
    eda_dst = NOTEBOOKS_DIR / "03_eda_analysis.ipynb"
    if eda_src.exists():
        shutil.copy(eda_src, eda_dst)
        print(f"Copied to {eda_dst.name}")
        
    # 04_performance_analytics.ipynb
    perf_src = NOTEBOOKS_DIR / "Performance_Analytics.ipynb"
    perf_dst = NOTEBOOKS_DIR / "04_performance_analytics.ipynb"
    if perf_src.exists():
        shutil.copy(perf_src, perf_dst)
        print(f"Copied to {perf_dst.name}")
        
    # 05_advanced_analytics.ipynb
    adv_src = NOTEBOOKS_DIR / "Advanced_Analytics.ipynb"
    adv_dst = NOTEBOOKS_DIR / "05_advanced_analytics.ipynb"
    if adv_src.exists():
        shutil.copy(adv_src, adv_dst)
        print(f"Copied to {adv_dst.name}")

def generate_ingestion_notebook():
    print("Generating 01_data_ingestion.ipynb...")
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell(
            "# Data Ingestion & Quality Profiling\n\n"
            "This notebook explores the raw files of the Mutual Fund Analytics project. "
            "It profiles dataset shapes, column datatypes, nulls, duplicates, and checks AMFI codes referential integrity."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "import pandas as pd\n\n"
            "# Configure root paths\n"
            "ROOT = Path(os.getcwd()).parent\n"
            "sys.path.append(str(ROOT / 'scripts'))\n"
            "import data_ingestion\n\n"
            "data_ingestion.main()"
        )
    ]
    nb['cells'] = cells
    out_path = NOTEBOOKS_DIR / "01_data_ingestion.ipynb"
    with open(out_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Ingestion notebook generated.")

def generate_cleaning_notebook():
    print("Generating 02_data_cleaning.ipynb...")
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell(
            "# Data Cleaning & Schema Normalization\n\n"
            "This notebook applies column-name normalisation, whitespace trimming, date parsing, integer coercion, "
            "and ffill() for weekend/holiday NAV gaps."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "import pandas as pd\n\n"
            "# Configure root paths\n"
            "ROOT = Path(os.getcwd()).parent\n"
            "sys.path.append(str(ROOT / 'scripts'))\n"
            "import data_cleaning\n\n"
            "outputs = data_cleaning.run()\n"
            "for name, path in outputs.items():\n"
            "    df = pd.read_csv(path)\n"
            "    print(f\"{name:<24} clean shape: {df.shape[0]:>5} rows x {df.shape[1]} columns\")"
        )
    ]
    nb['cells'] = cells
    out_path = NOTEBOOKS_DIR / "02_data_cleaning.ipynb"
    with open(out_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Cleaning notebook generated.")

def append_advanced_metrics_to_notebook():
    print("Updating 05_advanced_analytics.ipynb with B3, B4 and Advanced Insights...")
    adv_path = NOTEBOOKS_DIR / "05_advanced_analytics.ipynb"
    if not adv_path.exists():
        print("Advanced notebook copy not found. Skipping append.")
        return
        
    with open(adv_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
        
    # Check if Monte Carlo cells already exist
    has_mc = any("## Monte Carlo Simulation" in cell.get("source", "") for cell in nb.cells)
    if not has_mc:
        print("Appending Monte Carlo Simulation to notebook...")
        nb.cells.append(
            nbf.v4.new_markdown_cell(
                "## Monte Carlo Simulation (5-Year NAV Projections)\n\n"
                "Using historical mean returns and volatility to simulate 1,000 potential NAV growth paths over 5 years."
            )
        )
        nb.cells.append(
            nbf.v4.new_code_cell(
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "import seaborn as sns\n"
                "from pathlib import Path\n\n"
                "PROCESSED_DIR = Path('../data/processed')\n"
                "percentiles_df = pd.read_csv(PROCESSED_DIR / 'monte_carlo_projections.csv')\n\n"
                "plt.figure(figsize=(10, 6))\n"
                "sns.set_theme(style='whitegrid')\n"
                "plt.plot(percentiles_df['step'], percentiles_df['p50'], label='Median (50th percentile)', color='#4F46E5', linewidth=2)\n"
                "plt.fill_between(percentiles_df['step'], percentiles_df['p25'], percentiles_df['p75'], color='#6366F1', alpha=0.3, label='Interquartile Range')\n"
                "plt.fill_between(percentiles_df['step'], percentiles_df['p5'], percentiles_df['p95'], color='#6366F1', alpha=0.1, label='90% Confidence Band')\n"
                "plt.title('Monte Carlo 5-Year NAV Price Path Forecast', fontsize=13, fontweight='bold', pad=15)\n"
                "plt.xlabel('Trading Days')\n"
                "plt.ylabel('Projected NAV (INR)')\n"
                "plt.legend(loc='upper left')\n"
                "plt.show()"
            )
        )
        
    # Check if Markowitz optimization exists
    has_markowitz = any("## Markowitz Efficient Frontier" in cell.get("source", "") for cell in nb.cells)
    if not has_markowitz:
        print("Appending Markowitz Optimization to notebook...")
        nb.cells.append(
            nbf.v4.new_markdown_cell(
                "## Markowitz Efficient Frontier Portfolio Optimization\n\n"
                "Simulates expected return and volatility for random allocations among the top 5 scorecard funds."
            )
        )
        nb.cells.append(
            nbf.v4.new_code_cell(
                "results_df = pd.read_csv(PROCESSED_DIR / 'efficient_frontier_results.csv')\n\n"
                "plt.figure(figsize=(10, 6))\n"
                "sns.set_theme(style='whitegrid')\n"
                "sc = plt.scatter(results_df['Volatility'] * 100, results_df['Return'] * 100, c=results_df['Sharpe'], cmap='viridis_r', s=10, alpha=0.3)\n"
                "plt.colorbar(sc, label='Sharpe Ratio')\n\n"
                "msr = results_df.iloc[results_df['Sharpe'].idxmax()]\n"
                "mvp = results_df.iloc[results_df['Volatility'].idxmin()]\n\n"
                "plt.scatter(msr['Volatility'] * 100, msr['Return'] * 100, color='red', marker='*', s=200, label='Max Sharpe Ratio Portfolio')\n"
                "plt.scatter(mvp['Volatility'] * 100, mvp['Return'] * 100, color='blue', marker='*', s=200, label='Minimum Variance Portfolio')\n"
                "plt.title('Markowitz Efficient Frontier - Asset Allocations', fontsize=13, fontweight='bold', pad=15)\n"
                "plt.xlabel('Volatility (Risk %)'), plt.ylabel('Expected Return (%)')\n"
                "plt.legend(loc='upper left')\n"
                "plt.show()\n\n"
                "print('Maximum Sharpe Ratio Portfolio Weights:')\n"
                "print(msr.drop(['Return', 'Volatility', 'Sharpe']).to_frame().T.to_string(index=False))"
            )
        )

    # Check if Advanced Insights already exist
    has_insights = any("## Portfolio Risk & Performance Insights" in cell.get("source", "") for cell in nb.cells)
    if not has_insights:
        print("Appending Portfolio Risk & Performance Insights markdown to notebook...")
        insights_md = (
            "## Portfolio Risk & Performance Insights\n\n"
            "Based on the quantitative analyses executed on the datasets, we have extracted the following five key insights:\n\n"
            "### Insight 1: Small Cap Funds Exhibit Highest Downside Risk (VaR & CVaR)\n"
            "* **Finding**: Aditya Birla Sun Life (ABSL) Small Cap Fund (Regular - Growth) exhibits the highest daily downside risk with a **95% VaR of 2.39%** and a **95% CVaR of 3.03%**, followed closely by Axis Small Cap Fund (VaR: 2.33%, CVaR: 2.97%) and SBI Small Cap Fund (VaR: 2.32%, CVaR: 3.02%).\n"
            "* **Implication**: For a ₹1,00,000 portfolio in ABSL Small Cap, there is a 5% probability of losing more than ₹2,391 on any single trading day. If that threshold is breached, the average expected loss is ₹3,029. High-risk tolerance is mandatory for these schemes.\n\n"
            "### Insight 2: Dramatic Cohort Growth in 2024 vs. 2025 (Inflows & Engagement)\n"
            "* **Finding**: The 2024 investor cohort dominates the platform's user base with **4,803 investors** and a total net investment of **₹102.50 Crores**. Conversely, the 2025 cohort is vastly smaller, with only **197 investors** contributing a net investment of **₹0.75 Crores**.\n"
            "* **Implication**: While client acquisition slowed dramatically in 2025, the 2025 cohort boasts a higher **average SIP contribution of ₹13,505** compared to the 2024 cohort's **₹10,997**, demonstrating that new entrants are more heavily capitalized.\n\n"
            "### Insight 3: Critical SIP Continuity / Churn Risk (99.9% At-Risk)\n"
            "* **Finding**: Out of **1,362 active SIP investors** (with 6+ transactions), **1,361 (99.93%)** are flagged as \"at-risk\" due to transaction gaps exceeding 35 days.\n"
            "* **Implication**: Since standard SIP cycles are monthly (~30 days), gaps exceeding 35 days point to missed payments or billing issues. This highlights an urgent need for automated reminders or platform friction diagnostics to arrest systemic drop-offs.\n\n"
            "### Insight 4: Extreme Portfolio Sector Concentration (Axis Bluechip)\n"
            "* **Finding**: Axis Bluechip Fund (Regular - Growth) exhibits the highest sector concentration with a Herfindahl-Hirschman Index (HHI) of **0.2968**, compared to the average HHI of **0.2029** across all 34 equity funds.\n"
            "* **Implication**: Axis Bluechip's high HHI reflects concentrated exposure (e.g., Financial Services and IT). While offering high conviction, it introduces substantial idiosyncratic sector risk compared to more diversified peers (minimum HHI is 0.1240).\n\n"
            "### Insight 5: Risk-Adjusted Returns Optimize at Moderate/Low Risk Profiles\n"
            "* **Finding**: The Sharpe ratio analysis reveals that the top risk-adjusted performer is currently Mirae Asset Large Cap Fund (Low risk appetite, Sharpe: **1.07**, 3Yr CAGR: 34.00%), followed by Kotak Flexicap Fund (Moderate risk appetite, Sharpe: **0.97**). In contrast, the top high-risk fund (DSP Small Cap) yields a Sharpe ratio of only **0.71**.\n"
            "* **Implication**: High risk has not been rewarded with commensurate returns in this market cycle. Conservative-to-moderate portfolios are delivering superior risk-adjusted premiums."
        )
        nb.cells.append(nbf.v4.new_markdown_cell(insights_md))
        
    with open(adv_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Advanced notebook updated successfully.")

def execute_all_notebooks():
    print("Executing all 5 notebooks...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    for i in range(1, 6):
        name = f"0{i}_data_ingestion.ipynb" if i==1 else f"0{i}_data_cleaning.ipynb" if i==2 else f"0{i}_eda_analysis.ipynb" if i==3 else f"0{i}_performance_analytics.ipynb" if i==4 else f"0{i}_advanced_analytics.ipynb"
        path = NOTEBOOKS_DIR / name
        if not path.exists():
            print(f"Notebook {name} does not exist. Skipping.")
            continue
            
        print(f"Executing {name} in place...")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                nb = nbf.read(f, as_version=4)
            ep.preprocess(nb, {'metadata': {'path': str(NOTEBOOKS_DIR)}})
            with open(path, 'w', encoding='utf-8') as f:
                nbf.write(nb, f)
            print(f"Success: executed {name}")
        except Exception as e:
            print(f"ERROR executing {name}: {e}")

def main():
    NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)
    copy_existing_notebooks()
    generate_ingestion_notebook()
    generate_cleaning_notebook()
    append_advanced_metrics_to_notebook()
    execute_all_notebooks()

if __name__ == "__main__":
    main()
