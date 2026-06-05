"""
Day 6 - Advanced Analytics and Risk Metrics for Bluestock MF Analytics.

Computes:
1. Historical Value at Risk (VaR 95%) and Conditional VaR (CVaR 95%).
2. Rolling 90-day Sharpe Ratio for 5 selected funds.
3. Investor Cohort Analysis (2024 vs 2025 cohorts).
4. SIP Continuation / Churn Analysis (flagging at-risk investors).
5. Sector Concentration Analysis (HHI of sector weights).
6. Generates and executes the Jupyter notebook notebooks/Advanced_Analytics.ipynb.
"""
from __future__ import annotations

import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat as nbf

# Ensure scripts path is in system path so we can import _common
sys.path.append(str(Path(__file__).resolve().parent))
from _common import PROCESSED_DIR, REPORTS_DIR, get_logger

logger = get_logger("advanced_analytics")

# Output Paths
VAR_CVAR_PATH = PROCESSED_DIR / "var_cvar_report.csv"
COHORT_PATH = PROCESSED_DIR / "cohort_analysis.csv"
CONTINUITY_PATH = PROCESSED_DIR / "sip_continuity.csv"
SECTOR_HHI_PATH = PROCESSED_DIR / "sector_hhi.csv"

CHARTS_DIR = REPORTS_DIR / "charts"
ROLLING_SHARPE_CHART = CHARTS_DIR / "rolling_sharpe_chart.png"
SECTOR_HHI_CHART = CHARTS_DIR / "sector_concentration.png"
NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "notebooks" / "Advanced_Analytics.ipynb"

def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load datasets required for advanced analytics."""
    logger.info("Loading cleaned datasets for advanced analytics...")
    nav_df = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv")
    tx_df = pd.read_csv(PROCESSED_DIR / "clean_investor_transactions.csv")
    holdings_df = pd.read_csv(PROCESSED_DIR / "clean_portfolio_holdings.csv")
    master_df = pd.read_csv(PROCESSED_DIR / "clean_fund_master.csv")
    
    # Parse dates
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])
    
    return nav_df, tx_df, holdings_df, master_df

def compute_var_cvar(nav_df: pd.DataFrame, master_df: pd.DataFrame) -> pd.DataFrame:
    """Compute 95% Historical VaR and CVaR for all 40 funds."""
    logger.info("Computing Historical VaR (95%) and CVaR...")
    
    # Sort nav_df and calculate daily returns
    nav_df = nav_df.sort_values(['amfi_code', 'date']).copy()
    nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()
    
    records = []
    codes = nav_df['amfi_code'].unique()
    
    for code in codes:
        fund_returns = nav_df[(nav_df['amfi_code'] == code) & (nav_df['daily_return'].notna())]['daily_return']
        if fund_returns.empty:
            continue
            
        # 95% VaR is the 5th percentile of daily returns
        var_5th = np.percentile(fund_returns, 5)
        # Convert to positive loss representation
        var_95 = -var_5th * 100
        
        # CVaR is the mean of returns below or equal to VaR threshold
        below_var = fund_returns[fund_returns <= var_5th]
        cvar_95 = -below_var.mean() * 100 if not below_var.empty else var_95
        
        records.append({
            'amfi_code': code,
            'var_95_pct': var_95,
            'cvar_95_pct': cvar_95
        })
        
    var_cvar_df = pd.DataFrame(records)
    # Join with master for names
    var_cvar_df = var_cvar_df.merge(master_df[['amfi_code', 'scheme_name']], on='amfi_code')
    # Reorder columns
    var_cvar_df = var_cvar_df[['amfi_code', 'scheme_name', 'var_95_pct', 'cvar_95_pct']]
    var_cvar_df.to_csv(VAR_CVAR_PATH, index=False)
    logger.info("Saved VaR/CVaR report to %s", VAR_CVAR_PATH)
    return var_cvar_df

def plot_rolling_sharpe(nav_df: pd.DataFrame, master_df: pd.DataFrame, Rf_annual: float = 0.065) -> None:
    """Compute and plot Rolling 90-day Sharpe Ratio for 5 selected funds."""
    logger.info("Plotting Rolling 90-day Sharpe Ratio for 5 key funds...")
    
    # Selected funds
    selected_codes = [119551, 125497, 120503, 118632, 120841]
    
    # Calculate daily returns
    nav_df = nav_df.sort_values(['amfi_code', 'date']).copy()
    nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()
    
    Rf_daily = Rf_annual / 252
    
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    
    for code in selected_codes:
        fund_name = master_df[master_df['amfi_code'] == code]['scheme_name'].iloc[0].split(" - ")[0]
        fund_data = nav_df[(nav_df['amfi_code'] == code) & (nav_df['date'] >= '2022-06-01')].sort_values('date')
        
        # Daily return and excess return
        fund_data = fund_data.dropna(subset=['daily_return']).copy()
        fund_data['excess_return'] = fund_data['daily_return'] - Rf_daily
        
        # Rolling 90-day Sharpe
        rolling_mean = fund_data['excess_return'].rolling(90).mean()
        rolling_std = fund_data['daily_return'].rolling(90).std()
        fund_data['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(252)
        
        plt.plot(fund_data['date'], fund_data['rolling_sharpe'], label=fund_name, linewidth=1.5)
        
    plt.title("Rolling 90-Day Sharpe Ratio Over Time (Rf = 6.5%)", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("Annualized Sharpe Ratio")
    plt.legend(loc="upper left", fontsize=9, frameon=True, shadow=True)
    plt.tight_layout()
    
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ROLLING_SHARPE_CHART, dpi=300)
    plt.close()
    logger.info("Saved rolling Sharpe chart to %s", ROLLING_SHARPE_CHART)

def investor_cohort_analysis(tx_df: pd.DataFrame, master_df: pd.DataFrame) -> pd.DataFrame:
    """Investor cohort analysis: Group by first transaction year (2024 vs 2025)."""
    logger.info("Performing investor cohort analysis...")
    
    # Get first transaction date for each investor
    first_tx = tx_df.groupby('investor_id')['transaction_date'].min().reset_index()
    first_tx['cohort'] = first_tx['transaction_date'].dt.year
    
    # Merge cohort back to transactions
    tx_cohort = tx_df.merge(first_tx[['investor_id', 'cohort']], on='investor_id')
    
    records = []
    cohorts = [2024, 2025]
    
    for yr in cohorts:
        cohort_tx = tx_cohort[tx_cohort['cohort'] == yr]
        total_investors = cohort_tx['investor_id'].nunique()
        
        # Net investment = (SIP + Lumpsum) - Redemption
        sip_lump = cohort_tx[cohort_tx['transaction_type'].isin(['SIP', 'Lumpsum'])]['amount_inr'].sum()
        redemp = cohort_tx[cohort_tx['transaction_type'] == 'Redemption']['amount_inr'].sum()
        net_inv = sip_lump - redemp
        
        # Avg SIP Amount
        avg_sip = cohort_tx[cohort_tx['transaction_type'] == 'SIP']['amount_inr'].mean()
        
        # Top fund category preference (merge fund_master)
        cohort_details = cohort_tx.merge(master_df[['amfi_code', 'category']], on='amfi_code')
        top_cat = cohort_details['category'].mode().iloc[0] if not cohort_details.empty else "N/A"
        
        records.append({
            'cohort': f"{yr} Cohort",
            'total_investors': total_investors,
            'total_net_investment_cr': net_inv / 1e7,
            'avg_sip_amount_inr': avg_sip,
            'top_fund_category': top_cat
        })
        
    cohort_df = pd.DataFrame(records)
    cohort_df.to_csv(COHORT_PATH, index=False)
    logger.info("Saved cohort analysis to %s", COHORT_PATH)
    return cohort_df

def sip_continuation_analysis(tx_df: pd.DataFrame) -> pd.DataFrame:
    """For each investor with 6+ SIPs, compute transaction gap and flag 'at-risk'."""
    logger.info("Performing SIP continuation analysis...")
    
    # Filter for SIP transactions
    sip_tx = tx_df[tx_df['transaction_type'] == 'SIP'].copy()
    sip_counts = sip_tx.groupby('investor_id').size().reset_index(name='sip_count')
    
    # Filter investors with 6+ SIP transactions
    frequent_investors = sip_counts[sip_counts['sip_count'] >= 6]['investor_id']
    sip_frequent = sip_tx[sip_tx['investor_id'].isin(frequent_investors)].sort_values(['investor_id', 'transaction_date'])
    
    records = []
    
    for inv_id, group in sip_frequent.groupby('investor_id'):
        # Date differences in days
        diffs = group['transaction_date'].diff().dropna().dt.days
        avg_gap = diffs.mean()
        max_gap = diffs.max()
        
        # Flag as at-risk if max gap > 35 days (Standard monthly SIP gap should be ~30 days)
        is_at_risk = int(max_gap > 35)
        
        records.append({
            'investor_id': inv_id,
            'sip_count': len(group),
            'avg_gap_days': avg_gap,
            'max_gap_days': max_gap,
            'is_at_risk': is_at_risk
        })
        
    continuity_df = pd.DataFrame(records)
    continuity_df.to_csv(CONTINUITY_PATH, index=False)
    logger.info("Saved SIP continuation analysis to %s (At-Risk Count: %d)", CONTINUITY_PATH, continuity_df['is_at_risk'].sum())
    return continuity_df

def sector_concentration_analysis(holdings_df: pd.DataFrame, master_df: pd.DataFrame) -> pd.DataFrame:
    """Compute Herfindahl-Hirschman Index (HHI) of sector weights for each fund."""
    logger.info("Performing sector concentration analysis (HHI)...")
    
    # Group holdings by fund and sector
    sector_weights = holdings_df.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()
    
    records = []
    codes = sector_weights['amfi_code'].unique()
    
    for code in codes:
        fund_weights = sector_weights[sector_weights['amfi_code'] == code]['weight_pct']
        # Convert weight_pct to ratio (0 to 1)
        ratios = fund_weights / 100.0
        # HHI is sum of squared weights
        hhi = np.sum(ratios ** 2)
        
        records.append({
            'amfi_code': code,
            'sector_hhi': hhi
        })
        
    hhi_df = pd.DataFrame(records)
    hhi_df = hhi_df.merge(master_df[['amfi_code', 'scheme_name']], on='amfi_code')
    hhi_df = hhi_df.sort_values(by='sector_hhi', ascending=False)
    
    # Reorder columns
    hhi_df = hhi_df[['amfi_code', 'scheme_name', 'sector_hhi']]
    hhi_df.to_csv(SECTOR_HHI_PATH, index=False)
    logger.info("Saved HHI sector concentration report to %s", SECTOR_HHI_PATH)
    
    # Plot top 10 concentrated funds
    plt.figure(figsize=(10, 5))
    sns.set_theme(style="whitegrid")
    
    top_concentrated = hhi_df.head(10).copy()
    top_concentrated['scheme_name'] = top_concentrated['scheme_name'].apply(lambda x: x.split(" - ")[0][:28])
    
    sns.barplot(data=top_concentrated, x='sector_hhi', y='scheme_name', palette="flare", hue='scheme_name', legend=False)
    plt.title("Top 10 Most Concentrated Funds by Sector (HHI Index)", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Herfindahl-Hirschman Index (HHI) - Sector Weights")
    plt.ylabel("")
    plt.tight_layout()
    
    plt.savefig(SECTOR_HHI_CHART, dpi=300)
    plt.close()
    logger.info("Saved sector concentration chart to %s", SECTOR_HHI_CHART)
    
    return hhi_df

def generate_notebook() -> None:
    """Generate the notebooks/Advanced_Analytics.ipynb notebook using nbformat."""
    logger.info("Generating notebook at %s...", NOTEBOOK_PATH)
    nb = nbf.v4.new_notebook()
    
    cells = [
        nbf.v4.new_markdown_cell(
            "# DAY 6 — Advanced Analytics & Risk Metrics\n\n"
            "This notebook implements advanced analytics on mutual fund NAV history, portfolio holdings, "
            "and investor transactions. It covers the following details:\n"
            "1. **Historical Value at Risk (VaR 95%) & Conditional VaR (CVaR 95%)**\n"
            "2. **Rolling 90-day Sharpe Ratio** for selected funds\n"
            "3. **Investor Cohort Analysis** (2024 vs 2025 cohorts)\n"
            "4. **SIP Continuation Analysis** (identifying at-risk investors)\n"
            "5. **Sector Concentration Analysis** using Herfindahl-Hirschman Index (HHI)\n\n"
            "## Setup & Load Data"
        ),
        nbf.v4.new_code_cell(
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n\n"
            "nav_df = pd.read_csv('../data/processed/clean_nav_history.csv')\n"
            "tx_df = pd.read_csv('../data/processed/clean_investor_transactions.csv')\n"
            "holdings_df = pd.read_csv('../data/processed/clean_portfolio_holdings.csv')\n"
            "master_df = pd.read_csv('../data/processed/clean_fund_master.csv')\n\n"
            "nav_df['date'] = pd.to_datetime(nav_df['date'])\n"
            "tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])\n\n"
            "print(f\"Data loaded successfully.\")"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Compute Historical VaR & CVaR (95%)\n\n"
            "Historical Value at Risk (VaR) measures the potential loss in value of a fund over a daily horizon "
            "with a 95% confidence level. Conditional VaR (CVaR) measures the expected loss on days when the loss exceeds the VaR."
        ),
        nbf.v4.new_code_cell(
            "nav_df = nav_df.sort_values(['amfi_code', 'date'])\n"
            "nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()\n\n"
            "var_records = []\n"
            "for code in nav_df['amfi_code'].unique():\n"
            "    fund_returns = nav_df[(nav_df['amfi_code'] == code) & (nav_df['daily_return'].notna())]['daily_return']\n"
            "    if fund_returns.empty:\n"
            "        continue\n"
            "    var_5th = np.percentile(fund_returns, 5)\n"
            "    var_95 = -var_5th * 100\n"
            "    below_var = fund_returns[fund_returns <= var_5th]\n"
            "    cvar_95 = -below_var.mean() * 100 if not below_var.empty else var_95\n"
            "    var_records.append({\n"
            "        'amfi_code': code,\n"
            "        'var_95_pct': var_95,\n"
            "        'cvar_95_pct': cvar_95\n"
            "    })\n"
            "var_df = pd.DataFrame(var_records).merge(master_df[['amfi_code', 'scheme_name']], on='amfi_code')\n"
            "var_df = var_df[['amfi_code', 'scheme_name', 'var_95_pct', 'cvar_95_pct']]\n"
            "print(\"Top 5 Funds with Highest Daily VaR 95% (Highest Potential Loss):\")\n"
            "print(var_df.sort_values('var_95_pct', ascending=False).head(5).to_string(index=False))"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Rolling 90-day Sharpe Ratio\n\n"
            "Rolling Sharpe ratio tracks the risk-adjusted returns of 5 key funds over a 90-day window to evaluate performance stability."
        ),
        nbf.v4.new_code_cell(
            "selected_codes = [119551, 125497, 120503, 118632, 120841]\n"
            "Rf_annual = 0.065\n"
            "Rf_daily = Rf_annual / 252\n\n"
            "plt.figure(figsize=(12, 6))\n"
            "sns.set_theme(style=\"whitegrid\")\n\n"
            "for code in selected_codes:\n"
            "    fund_name = master_df[master_df['amfi_code'] == code]['scheme_name'].iloc[0].split(' - ')[0]\n"
            "    fund_data = nav_df[(nav_df['amfi_code'] == code) & (nav_df['date'] >= '2022-06-01')].sort_values('date')\n"
            "    fund_data = fund_data.dropna(subset=['daily_return']).copy()\n"
            "    fund_data['excess_return'] = fund_data['daily_return'] - Rf_daily\n"
            "    rolling_mean = fund_data['excess_return'].rolling(90).mean()\n"
            "    rolling_std = fund_data['daily_return'].rolling(90).std()\n"
            "    fund_data['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(252)\n"
            "    plt.plot(fund_data['date'], fund_data['rolling_sharpe'], label=fund_name, linewidth=1.5)\n\n"
            "plt.title(\"Rolling 90-Day Sharpe Ratio Over Time (Rf = 6.5%)\", fontsize=13, fontweight='bold', pad=15)\n"
            "plt.xlabel(\"Date\")\n"
            "plt.ylabel(\"Annualized Sharpe Ratio\")\n"
            "plt.legend(loc=\"upper left\")\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Investor Cohort Analysis\n\n"
            "Analyzes investor demographics and transaction activity by their acquisition year cohort (2024 vs 2025)."
        ),
        nbf.v4.new_code_cell(
            "first_tx = tx_df.groupby('investor_id')['transaction_date'].min().reset_index()\n"
            "first_tx['cohort'] = first_tx['transaction_date'].dt.year\n"
            "tx_cohort = tx_df.merge(first_tx[['investor_id', 'cohort']], on='investor_id')\n\n"
            "cohort_records = []\n"
            "for yr in [2024, 2025]:\n"
            "    cohort_tx = tx_cohort[tx_cohort['cohort'] == yr]\n"
            "    total_investors = cohort_tx['investor_id'].nunique()\n"
            "    sip_lump = cohort_tx[cohort_tx['transaction_type'].isin(['SIP', 'Lumpsum'])]['amount_inr'].sum()\n"
            "    redemp = cohort_tx[cohort_tx['transaction_type'] == 'Redemption']['amount_inr'].sum()\n"
            "    net_inv = sip_lump - redemp\n"
            "    avg_sip = cohort_tx[cohort_tx['transaction_type'] == 'SIP']['amount_inr'].mean()\n"
            "    cohort_details = cohort_tx.merge(master_df[['amfi_code', 'category']], on='amfi_code')\n"
            "    top_cat = cohort_details['category'].mode().iloc[0] if not cohort_details.empty else 'N/A'\n"
            "    cohort_records.append({\n"
            "        'cohort': f\"{yr} Cohort\",\n"
            "        'total_investors': total_investors,\n"
            "        'total_net_investment_cr': net_inv / 1e7,\n"
            "        'avg_sip_amount_inr': avg_sip,\n"
            "        'top_fund_category': top_cat\n"
            "    })\n"
            "cohort_df = pd.DataFrame(cohort_records)\n"
            "print(cohort_df.to_string(index=False))"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. SIP Continuation / Churn Analysis\n\n"
            "Identifies at-risk investors based on transaction intervals. If the maximum gap between consecutive "
            "SIP transactions exceeds 35 days, the investor is flagged as 'at-risk' for churn."
        ),
        nbf.v4.new_code_cell(
            "sip_tx = tx_df[tx_df['transaction_type'] == 'SIP'].copy()\n"
            "sip_counts = sip_tx.groupby('investor_id').size().reset_index(name='sip_count')\n"
            "frequent_investors = sip_counts[sip_counts['sip_count'] >= 6]['investor_id']\n"
            "sip_frequent = sip_tx[sip_tx['investor_id'].isin(frequent_investors)].sort_values(['investor_id', 'transaction_date'])\n\n"
            "continuity_records = []\n"
            "for inv_id, group in sip_frequent.groupby('investor_id'):\n"
            "    diffs = group['transaction_date'].diff().dropna().dt.days\n"
            "    avg_gap = diffs.mean()\n"
            "    max_gap = diffs.max()\n"
            "    is_at_risk = int(max_gap > 35)\n"
            "    continuity_records.append({\n"
            "        'investor_id': inv_id,\n"
            "        'sip_count': len(group),\n"
            "        'avg_gap_days': avg_gap,\n"
            "        'max_gap_days': max_gap,\n"
            "        'is_at_risk': is_at_risk\n"
            "    })\n"
            "continuity_df = pd.DataFrame(continuity_records)\n"
            "at_risk_count = continuity_df['is_at_risk'].sum()\n"
            "print(f\"Analyzed {len(continuity_df)} investors with >= 6 SIP transactions.\")\n"
            "print(f\"Flagged {at_risk_count} at-risk investors ({at_risk_count/len(continuity_df):.2%} churn risk).\")\n"
            "print(continuity_df.head(5).to_string(index=False))"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. Sector Concentration Analysis (HHI)\n\n"
            "Computes Herfindahl-Hirschman Index (HHI) on portfolio sector weights. Higher HHI indicates a highly concentrated sector profile."
        ),
        nbf.v4.new_code_cell(
            "sector_weights = holdings_df.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()\n"
            "hhi_records = []\n"
            "for code in sector_weights['amfi_code'].unique():\n"
            "    fund_weights = sector_weights[sector_weights['amfi_code'] == code]['weight_pct']\n"
            "    ratios = fund_weights / 100.0\n"
            "    hhi = np.sum(ratios ** 2)\n"
            "    hhi_records.append({\n"
            "        'amfi_code': code,\n"
            "        'sector_hhi': hhi\n"
            "    })\n"
            "hhi_df = pd.DataFrame(hhi_records).merge(master_df[['amfi_code', 'scheme_name']], on='amfi_code')\n"
            "hhi_df = hhi_df.sort_values(by='sector_hhi', ascending=False)\n\n"
            "print(\"Top 5 Most Concentrated Funds by Sector:\")\n"
            "print(hhi_df.head(5)[['scheme_name', 'sector_hhi']].to_string(index=False))\n\n"
            "# Bar plot\n"
            "plt.figure(figsize=(10, 5))\n"
            "top_10 = hhi_df.head(10).copy()\n"
            "top_10['scheme_name'] = top_10['scheme_name'].apply(lambda x: x.split(' - ')[0][:28])\n"
            "sns.barplot(data=top_10, x='sector_hhi', y='scheme_name', palette='flare', hue='scheme_name', legend=False)\n"
            "plt.title(\"Top 10 Most Concentrated Funds (Sector HHI Index)\", fontsize=13, fontweight='bold')\n"
            "plt.xlabel(\"HHI Index\")\n"
            "plt.ylabel(\"\")\n"
            "plt.show()"
        )
    ]
    
    nb['cells'] = cells
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    logger.info("Saved notebook file.")

def execute_notebook() -> None:
    """Execute the notebook in place to populate the output cells."""
    logger.info("Executing notebook in place...")
    try:
        import nbformat
        from nbconvert.preprocessors import ExecutePreprocessor
        
        with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': str(NOTEBOOK_PATH.parent)}})
        
        with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
            
        logger.info("Notebook executed successfully programmatically.")
    except Exception as e:
        logger.error("Notebook execution programmatically failed: %s", e)

def main() -> None:
    nav_df, tx_df, holdings_df, master_df = load_data()
    
    # Run computations
    compute_var_cvar(nav_df, master_df)
    plot_rolling_sharpe(nav_df, master_df)
    investor_cohort_analysis(tx_df, master_df)
    sip_continuation_analysis(tx_df)
    sector_concentration_analysis(holdings_df, master_df)
    
    # Generate and execute Jupyter notebook
    generate_notebook()
    execute_notebook()
    
    logger.info("Day 6 - Advanced Analytics run completed successfully!")

if __name__ == "__main__":
    main()
