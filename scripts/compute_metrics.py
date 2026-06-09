"""
Computes fund performance analytics including daily returns, annualized CAGR (1yr, 3yr, 5yr), 
Sharpe and Sortino ratios, risk-adjusted alpha/beta OLS regressions, maximum drawdown, 
and builds a composite scorecard for comparison.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure scripts path is in system path so we can import _common
sys.path.append(str(Path(__file__).resolve().parent))
from _common import PROCESSED_DIR, REPORTS_DIR, get_logger

logger = get_logger("compute_metrics")

# Output Paths
SCORECARD_PATH = PROCESSED_DIR / "fund_scorecard.csv"
ALPHA_BETA_PATH = PROCESSED_DIR / "alpha_beta.csv"
CHARTS_DIR = REPORTS_DIR / "charts"
CHART_PATH = CHARTS_DIR / "benchmark_comparison.png"
REPORT_PATH = REPORTS_DIR / "performance_report.txt"

def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load cleaned datasets required for analysis."""
    logger.info("Loading cleaned datasets...")
    nav_df = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv")
    bench_df = pd.read_csv(PROCESSED_DIR / "clean_benchmark_indices.csv")
    master_df = pd.read_csv(PROCESSED_DIR / "clean_fund_master.csv")
    
    # Parse dates
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    bench_df['date'] = pd.to_datetime(bench_df['date'])
    
    return nav_df, bench_df, master_df

def compute_daily_returns(nav_df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily returns for all 40 schemes."""
    logger.info("Computing daily returns...")
    nav_df = nav_df.sort_values(['amfi_code', 'date'])
    nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()
    
    # Simple distribution check printouts
    stats_summary = nav_df.groupby('amfi_code')['daily_return'].describe()
    logger.info("Daily return summary (sample):\n%s", stats_summary.head(3).to_string())
    
    return nav_df

def compute_bench_returns(bench_df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily returns for benchmark indices."""
    logger.info("Computing benchmark returns...")
    bench_df = bench_df.sort_values(['index_name', 'date'])
    bench_df['daily_return'] = bench_df.groupby('index_name')['close_value'].pct_change()
    return bench_df

def compute_cagr_metrics(nav_df: pd.DataFrame) -> pd.DataFrame:
    """Compute CAGR for 1yr, 3yr, and maximum period (4.4 years as 5yr proxy)."""
    logger.info("Computing CAGR returns...")
    
    # Latest date is 2026-05-29
    end_date = pd.Timestamp("2026-05-29")
    start_1yr = pd.Timestamp("2025-05-29")
    start_3yr = pd.Timestamp("2023-05-29")
    start_5yr = pd.Timestamp("2022-01-03") # earliest date in dataset
    
    records = []
    codes = nav_df['amfi_code'].unique()
    
    for code in codes:
        fund_nav = nav_df[nav_df['amfi_code'] == code].set_index('date')
        
        # Get nearest NAVs
        nav_end = fund_nav.loc[end_date, 'nav']
        nav_1yr = fund_nav.loc[start_1yr, 'nav']
        nav_3yr = fund_nav.loc[start_3yr, 'nav']
        nav_5yr = fund_nav.loc[start_5yr, 'nav']
        
        # Calculations
        cagr_1yr = (nav_end / nav_1yr) ** (1 / 1.0) - 1
        cagr_3yr = (nav_end / nav_3yr) ** (1 / 3.0) - 1
        
        # For 5yr CAGR, we have 1607 days = 4.3997 years
        days_5yr = (end_date - start_5yr).days
        years_5yr = days_5yr / 365.25
        cagr_5yr = (nav_end / nav_5yr) ** (1 / years_5yr) - 1
        
        records.append({
            'amfi_code': code,
            'cagr_1yr_pct': cagr_1yr * 100,
            'cagr_3yr_pct': cagr_3yr * 100,
            'cagr_5yr_pct': cagr_5yr * 100
        })
        
    return pd.DataFrame(records)

def compute_risk_adjusted_ratios(nav_df: pd.DataFrame, Rf_annual: float = 0.065) -> pd.DataFrame:
    """Compute annualized Sharpe and Sortino ratios (Rf = 6.5%, 252 trading days)."""
    logger.info("Computing Sharpe and Sortino ratios...")
    Rf_daily = Rf_annual / 252
    records = []
    codes = nav_df['amfi_code'].unique()
    
    for code in codes:
        fund_returns = nav_df[(nav_df['amfi_code'] == code) & (nav_df['daily_return'].notna())]['daily_return']
        
        # Sharpe
        excess_returns = fund_returns - Rf_daily
        mean_excess = excess_returns.mean()
        std_dev = fund_returns.std()
        sharpe = (mean_excess / std_dev) * np.sqrt(252) if std_dev > 0 else np.nan
        
        # Sortino (downside standard deviation of negative return days only)
        downside_returns = fund_returns[fund_returns < 0]
        downside_std = downside_returns.std()
        sortino = (mean_excess / downside_std) * np.sqrt(252) if downside_std > 0 else np.nan
        
        records.append({
            'amfi_code': code,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'std_dev_ann_pct': std_dev * np.sqrt(252) * 100
        })
        
    return pd.DataFrame(records)

def compute_alpha_beta(nav_df: pd.DataFrame, bench_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Beta and Alpha relative to Nifty 100 returns."""
    logger.info("Computing Alpha and Beta (OLS regression vs Nifty 100)...")
    
    nifty100 = bench_df[(bench_df['index_name'] == 'NIFTY100') & (bench_df['daily_return'].notna())][['date', 'daily_return']]
    nifty100 = nifty100.rename(columns={'daily_return': 'bench_return'})
    
    records = []
    codes = nav_df['amfi_code'].unique()
    
    for code in codes:
        fund_ret = nav_df[(nav_df['amfi_code'] == code) & (nav_df['daily_return'].notna())][['date', 'daily_return']]
        merged = pd.merge(fund_ret, nifty100, on='date', how='inner')
        
        # Regress
        slope, intercept, r_val, p_val, std_err = stats.linregress(merged['bench_return'], merged['daily_return'])
        beta = slope
        alpha = intercept * 252 # Annualize the intercept
        
        records.append({
            'amfi_code': code,
            'alpha': alpha * 100, # as a percentage
            'beta': beta
        })
        
    return pd.DataFrame(records)

def compute_max_drawdown(nav_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Maximum Drawdown and find the worst drawdown date range."""
    logger.info("Computing Maximum Drawdown and worst drawdown date range...")
    records = []
    codes = nav_df['amfi_code'].unique()
    
    for code in codes:
        fund_nav = nav_df[nav_df['amfi_code'] == code].sort_values('date').reset_index(drop=True)
        nav_series = fund_nav['nav']
        date_series = fund_nav['date']
        
        running_max = nav_series.cummax()
        drawdowns = nav_series / running_max - 1
        max_dd = drawdowns.min()
        
        trough_idx = drawdowns.idxmin()
        trough_date = date_series.iloc[trough_idx]
        peak_val = running_max.iloc[trough_idx]
        
        # Find peak date before or at trough_idx
        peak_idx = nav_series.iloc[:trough_idx + 1][nav_series.iloc[:trough_idx + 1] == peak_val].index[-1]
        peak_date = date_series.iloc[peak_idx]
        
        records.append({
            'amfi_code': code,
            'max_drawdown_pct': max_dd * 100,
            'drawdown_peak_date': peak_date.strftime('%Y-%m-%d'),
            'drawdown_trough_date': trough_date.strftime('%Y-%m-%d')
        })
        
    return pd.DataFrame(records)

def build_scorecard(
    master_df: pd.DataFrame,
    cagr_df: pd.DataFrame,
    ratios_df: pd.DataFrame,
    alpha_beta_df: pd.DataFrame,
    drawdown_df: pd.DataFrame
) -> pd.DataFrame:
    """Build composite score (0-100) and rank all 40 funds."""
    logger.info("Building Fund Scorecard...")
    
    # Merge all metrics
    df = master_df[['amfi_code', 'scheme_name', 'expense_ratio_pct']].copy()
    df = df.merge(cagr_df, on='amfi_code')
    df = df.merge(ratios_df, on='amfi_code')
    df = df.merge(alpha_beta_df, on='amfi_code')
    df = df.merge(drawdown_df, on='amfi_code')
    
    # Rank components (percentile rank, 0 to 100)
    # Higher 3yr CAGR return is better
    df['rank_3yr'] = df['cagr_3yr_pct'].rank(pct=True) * 100
    # Higher Sharpe is better
    df['rank_Sharpe'] = df['sharpe_ratio'].rank(pct=True) * 100
    # Higher Alpha is better
    df['rank_Alpha'] = df['alpha'].rank(pct=True) * 100
    # Lower expense ratio is better
    df['rank_expense'] = df['expense_ratio_pct'].rank(ascending=False, pct=True) * 100
    # Less negative max drawdown is better
    df['rank_max_dd'] = df['max_drawdown_pct'].rank(ascending=True, pct=True) * 100
    
    # Weighted Score
    df['score'] = (
        0.30 * df['rank_3yr'] +
        0.25 * df['rank_Sharpe'] +
        0.20 * df['rank_Alpha'] +
        0.15 * df['rank_expense'] +
        0.10 * df['rank_max_dd']
    )
    
    # Scorecard Rank (1 is top, 40 is bottom)
    df['scorecard_rank'] = df['score'].rank(ascending=False, method='min').astype(int)
    df = df.sort_values('scorecard_rank')
    
    return df

def generate_benchmark_comparison_chart(
    scorecard_df: pd.DataFrame,
    nav_df: pd.DataFrame,
    bench_df: pd.DataFrame
) -> dict[str, dict[str, float]]:
    """Plot top 5 funds vs Nifty 50 and Nifty 100 over 3 years and calculate tracking errors."""
    logger.info("Generating benchmark comparison chart...")
    
    # Get top 5 funds
    top_5 = scorecard_df.head(5)
    top_5_codes = top_5['amfi_code'].tolist()
    top_5_names = top_5['scheme_name'].tolist()
    
    # 3 year period
    start_date = pd.Timestamp("2023-05-29")
    end_date = pd.Timestamp("2026-05-29")
    
    plt.figure(figsize=(12, 7))
    sns.set_theme(style="whitegrid")
    
    # tracking error calculations store
    tracking_errors = {}
    
    # Benchmark returns for tracking error
    nifty50_all = bench_df[(bench_df['index_name'] == 'NIFTY50') & (bench_df['date'] >= start_date) & (bench_df['date'] <= end_date)].sort_values('date')
    nifty100_all = bench_df[(bench_df['index_name'] == 'NIFTY100') & (bench_df['date'] >= start_date) & (bench_df['date'] <= end_date)].sort_values('date')
    
    # Plot top 5 funds
    for code, name in zip(top_5_codes, top_5_names):
        fund_data = nav_df[(nav_df['amfi_code'] == code) & (nav_df['date'] >= start_date) & (nav_df['date'] <= end_date)].sort_values('date')
        base_nav = fund_data.iloc[0]['nav']
        normalized_nav = (fund_data['nav'] / base_nav) * 100
        
        plt.plot(fund_data['date'], normalized_nav, label=name.split(" - ")[0], linewidth=1.5)
        
        # Calculate tracking errors
        fund_ret = fund_data['daily_return'].values[1:] # Drop first day (NaN)
        n50_ret = nifty50_all['daily_return'].values[1:]
        n100_ret = nifty100_all['daily_return'].values[1:]
        
        # Handle length mismatches if any
        min_len_50 = min(len(fund_ret), len(n50_ret))
        min_len_100 = min(len(fund_ret), len(n100_ret))
        
        te_n50 = np.std(fund_ret[:min_len_50] - n50_ret[:min_len_50], ddof=1) * np.sqrt(252) * 100
        te_n100 = np.std(fund_ret[:min_len_100] - n100_ret[:min_len_100], ddof=1) * np.sqrt(252) * 100
        
        tracking_errors[name] = {
            'TE_Nifty50_pct': te_n50,
            'TE_Nifty100_pct': te_n100
        }
        
    # Plot Nifty 50
    n50_base = nifty50_all.iloc[0]['close_value']
    normalized_n50 = (nifty50_all['close_value'] / n50_base) * 100
    plt.plot(nifty50_all['date'], normalized_n50, label='Nifty 50', color='black', linestyle='--', linewidth=2)
    
    # Plot Nifty 100
    n100_base = nifty100_all.iloc[0]['close_value']
    normalized_n100 = (nifty100_all['close_value'] / n100_base) * 100
    plt.plot(nifty100_all['date'], normalized_n100, label='Nifty 100', color='dimgray', linestyle=':', linewidth=2)
    
    # Format Chart
    plt.title("Top 5 Funds vs Benchmarks - 3 Year Normalized Performance (2023-05-29 = 100)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Date", fontsize=12, labelpad=10)
    plt.ylabel("Normalized NAV / Close Price", fontsize=12, labelpad=10)
    plt.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    plt.tight_layout()
    
    # Ensure charts dir exists
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(CHART_PATH, dpi=300)
    plt.close()
    logger.info("Saved benchmark comparison chart to %s", CHART_PATH)
    
    return tracking_errors

def main() -> None:
    nav_df, bench_df, master_df = load_data()
    
    # Calculations
    nav_df = compute_daily_returns(nav_df)
    bench_df = compute_bench_returns(bench_df)
    cagr_df = compute_cagr_metrics(nav_df)
    ratios_df = compute_risk_adjusted_ratios(nav_df)
    alpha_beta_df = compute_alpha_beta(nav_df, bench_df)
    drawdown_df = compute_max_drawdown(nav_df)
    
    # Scorecard building
    scorecard_df = build_scorecard(master_df, cagr_df, ratios_df, alpha_beta_df, drawdown_df)
    
    # Save Outputs
    SCORECARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    scorecard_df[[
        'amfi_code', 'scheme_name', 'cagr_3yr_pct', 'sharpe_ratio', 'alpha',
        'expense_ratio_pct', 'max_drawdown_pct', 'score', 'scorecard_rank',
        'std_dev_ann_pct'
    ]].to_csv(SCORECARD_PATH, index=False)
    logger.info("Saved scorecard to %s", SCORECARD_PATH)
    
    # Save alpha_beta.csv
    scorecard_df[['amfi_code', 'scheme_name', 'alpha', 'beta']].to_csv(ALPHA_BETA_PATH, index=False)
    logger.info("Saved alpha and beta to %s", ALPHA_BETA_PATH)
    
    # Comparison chart and tracking errors
    tracking_errors = generate_benchmark_comparison_chart(scorecard_df, nav_df, bench_df)
    
    # Write a comprehensive validation report
    report_lines = [
        "======================================================================",
        "Day 4 - Fund Performance Analytics Validation Report",
        f"Generated At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "======================================================================",
        "",
        "1. DAILY RETURNS DISTRIBUTION VALIDATION",
        "----------------------------------------",
        f"Total daily NAV returns calculated: {nav_df['daily_return'].notna().sum()}",
        f"Mean daily return (all funds): {nav_df['daily_return'].mean():.6%}",
        f"Std Dev daily return (all funds): {nav_df['daily_return'].std():.6%}",
        f"Min daily return: {nav_df['daily_return'].min():.6%}",
        f"Max daily return: {nav_df['daily_return'].max():.6%}",
        f"Kurtosis of daily returns: {nav_df['daily_return'].kurtosis():.4f}",
        f"Skewness of daily returns: {nav_df['daily_return'].skew():.4f}",
        "",
        "2. TOP 5 PERFORMING FUNDS (SCORECARD)",
        "-------------------------------------",
    ]
    
    top_5 = scorecard_df.head(5)
    for idx, row in top_5.iterrows():
        report_lines.append(
            f"Rank {row['scorecard_rank']}: {row['scheme_name']} (AMFI: {row['amfi_code']})\n"
            f"  Score: {row['score']:.2f} | 3Yr CAGR: {row['cagr_3yr_pct']:.2f}% | "
            f"Sharpe: {row['sharpe_ratio']:.2f} | Alpha: {row['alpha']:.2f} | "
            f"Expense Ratio: {row['expense_ratio_pct']:.2f}% | Max DD: {row['max_drawdown_pct']:.2f}%"
        )
        
    report_lines.append("\n3. TRACKING ERRORS OF TOP 5 FUNDS (3-YEAR PERIOD)")
    report_lines.append("-------------------------------------------------")
    for name, te_dict in tracking_errors.items():
        report_lines.append(
            f"{name.split(' - ')[0]}:\n"
            f"  Tracking Error vs Nifty 50: {te_dict['TE_Nifty50_pct']:.4f}%\n"
            f"  Tracking Error vs Nifty 100: {te_dict['TE_Nifty100_pct']:.4f}%"
        )
        
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    logger.info("Saved validation report to %s", REPORT_PATH)
    logger.info("Performance analytics run completed successfully!")

if __name__ == "__main__":
    main()
