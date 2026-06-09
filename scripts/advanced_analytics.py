"""
Computes portfolio analytics and risk metrics including Value at Risk (VaR), 
Conditional VaR (CVaR), rolling Sharpe ratio, investor cohort metrics, 
SIP churn rates, sector concentration (HHI), Monte Carlo NAV forecasts, 
and Markowitz portfolio optimization.
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

# Ensure scripts path is in system path so we can import _common
sys.path.append(str(Path(__file__).resolve().parent))
from _common import PROCESSED_DIR, REPORTS_DIR, get_logger

logger = get_logger("advanced_analytics")

# Output Paths
VAR_CVAR_PATH = PROCESSED_DIR / "var_cvar_report.csv"
COHORT_PATH = PROCESSED_DIR / "cohort_analysis.csv"
CONTINUITY_PATH = PROCESSED_DIR / "sip_continuity.csv"
SECTOR_HHI_PATH = PROCESSED_DIR / "sector_hhi.csv"
SCORECARD_PATH = PROCESSED_DIR / "fund_scorecard.csv"

CHARTS_DIR = REPORTS_DIR / "charts"
ROLLING_SHARPE_CHART = CHARTS_DIR / "rolling_sharpe_chart.png"
SECTOR_HHI_CHART = CHARTS_DIR / "sector_concentration.png"

def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load datasets required for advanced analytics."""
    logger.info("Loading cleaned datasets for advanced analytics...")
    nav_df = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv")
    tx_df = pd.read_csv(PROCESSED_DIR / "clean_investor_transactions.csv")
    holdings_df = pd.read_csv(PROCESSED_DIR / "clean_portfolio_holdings.csv")
    master_df = pd.read_csv(PROCESSED_DIR / "clean_fund_master.csv")
    
    scorecard_df = pd.DataFrame()
    if SCORECARD_PATH.exists():
        scorecard_df = pd.read_csv(SCORECARD_PATH)
    
    # Parse dates
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])
    
    return nav_df, tx_df, holdings_df, master_df, scorecard_df

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

def compute_monte_carlo(nav_df: pd.DataFrame, scorecard_df: pd.DataFrame) -> None:
    """Project 5-year NAV growth for the top scorecard fund using Monte Carlo simulation."""
    logger.info("Computing Monte Carlo 5-Year NAV Projections...")
    
    if scorecard_df.empty:
        logger.warning("Scorecard dataframe is empty. Cannot determine top fund.")
        return
        
    # Get the top scorecard fund
    top_fund_code = int(scorecard_df.iloc[0]['amfi_code'])
    top_fund_name = scorecard_df.iloc[0]['scheme_name']
    
    fund_navs = nav_df[nav_df['amfi_code'] == top_fund_code].sort_values('date')
    if fund_navs.empty:
        logger.warning("No NAV history found for top scorecard fund.")
        return
        
    # Compute daily returns
    fund_returns = fund_navs['nav'].pct_change().dropna()
    mu = fund_returns.mean()
    sigma = fund_returns.std()
    last_nav = fund_navs.iloc[-1]['nav']
    
    # 5 years projection (5 * 252 trading days = 1260 days)
    n_days = 5 * 252
    n_sims = 1000
    
    # Geometric Brownian Motion
    drift = mu - 0.5 * (sigma ** 2)
    rand_shocks = np.random.normal(0, 1, (n_days, n_sims))
    sim_daily_returns = np.exp(drift + sigma * rand_shocks)
    
    paths = np.zeros((n_days + 1, n_sims))
    paths[0] = last_nav
    for t in range(1, n_days + 1):
        paths[t] = paths[t - 1] * sim_daily_returns[t - 1]
        
    # Percentiles
    p5 = np.percentile(paths, 5, axis=1)
    p25 = np.percentile(paths, 25, axis=1)
    p50 = np.percentile(paths, 50, axis=1)
    p75 = np.percentile(paths, 75, axis=1)
    p95 = np.percentile(paths, 95, axis=1)
    
    # Save a CSV of the percentiles over time
    steps = np.arange(n_days + 1)
    percentiles_df = pd.DataFrame({
        'step': steps,
        'p5': p5,
        'p25': p25,
        'p50': p50,
        'p75': p75,
        'p95': p95
    })
    mc_path = PROCESSED_DIR / "monte_carlo_projections.csv"
    percentiles_df.to_csv(mc_path, index=False)
    logger.info("Saved Monte Carlo projections to %s", mc_path)
    
    # Save a plot
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    plt.plot(steps, p50, label="Median (50th percentile)", color="#4F46E5", linewidth=2)
    plt.fill_between(steps, p25, p75, color="#6366F1", alpha=0.3, label="Interquartile Range (25th - 75th)")
    plt.fill_between(steps, p5, p95, color="#6366F1", alpha=0.1, label="90% Confidence Interval (5th - 95th)")
    
    plt.title(f"Monte Carlo 5-Year NAV Projection: {top_fund_name.split(' - ')[0]}", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Trading Days")
    plt.ylabel("Projected NAV (INR)")
    plt.legend(loc="upper left", frameon=True, shadow=True)
    plt.tight_layout()
    
    mc_chart = CHARTS_DIR / "monte_carlo_simulation.png"
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(mc_chart, dpi=300)
    plt.close()
    logger.info("Saved Monte Carlo simulation chart to %s", mc_chart)

def compute_portfolio_optimization(nav_df: pd.DataFrame, scorecard_df: pd.DataFrame, Rf_annual: float = 0.065) -> None:
    """Perform Markowitz portfolio optimization for the top 5 scorecard funds."""
    logger.info("Computing Markowitz Efficient Frontier Portfolio Optimization...")
    
    if scorecard_df.empty:
        logger.warning("Scorecard dataframe is empty. Cannot perform portfolio optimization.")
        return
        
    # Select top 5 scorecard funds
    top_5 = scorecard_df.head(5)
    selected_codes = top_5['amfi_code'].tolist()
    selected_names = [name.split(" - ")[0] for name in top_5['scheme_name'].tolist()]
    
    # Filter 3 year period daily returns
    start_date = pd.Timestamp("2023-05-29")
    end_date = pd.Timestamp("2026-05-29")
    
    # Build pivoted returns
    returns_list = []
    for code, name in zip(selected_codes, selected_names):
        fund_data = nav_df[(nav_df['amfi_code'] == code) & (nav_df['date'] >= start_date) & (nav_df['date'] <= end_date)].sort_values('date').copy()
        fund_data['returns'] = fund_data['nav'].pct_change()
        fund_data = fund_data.dropna(subset=['returns'])
        fund_data = fund_data.rename(columns={'returns': name})
        returns_list.append(fund_data[['date', name]])
        
    # Merge returns
    merged_returns = returns_list[0]
    for r in returns_list[1:]:
        merged_returns = pd.merge(merged_returns, r, on='date', how='inner')
        
    merged_returns = merged_returns.drop(columns=['date'])
    
    # Mean and Covariance
    mean_daily = merged_returns.mean()
    cov_daily = merged_returns.cov()
    
    # Annualize (252 trading days)
    ann_returns = mean_daily * 252
    ann_cov = cov_daily * 252
    
    # Monte Carlo simulation of portfolios
    n_portfolios = 2000
    results = np.zeros((3 + len(selected_names), n_portfolios))
    
    # Seed for deterministic results
    np.random.seed(42)
    
    for i in range(n_portfolios):
        # Generate random weights
        weights = np.random.random(len(selected_names))
        weights /= np.sum(weights)
        
        # Portfolio return and volatility
        p_return = np.sum(weights * ann_returns)
        p_volatility = np.sqrt(np.dot(weights.T, np.dot(ann_cov, weights)))
        p_sharpe = (p_return - Rf_annual) / p_volatility
        
        results[0, i] = p_return
        results[1, i] = p_volatility
        results[2, i] = p_sharpe
        for j in range(len(weights)):
            results[3 + j, i] = weights[j]
            
    # Convert results to DataFrame
    columns = ['Return', 'Volatility', 'Sharpe'] + selected_names
    results_df = pd.DataFrame(results.T, columns=columns)
    
    # Find MSR and MVP portfolios
    msr_idx = results_df['Sharpe'].idxmax()
    mvp_idx = results_df['Volatility'].idxmin()
    
    msr_portfolio = results_df.iloc[msr_idx]
    mvp_portfolio = results_df.iloc[mvp_idx]
    
    # Save results to CSV
    opt_path = PROCESSED_DIR / "efficient_frontier_results.csv"
    results_df.to_csv(opt_path, index=False)
    logger.info("Saved portfolio optimization results to %s", opt_path)
    
    # Save a plot of the Efficient Frontier
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Plot random portfolios colored by Sharpe
    sc = plt.scatter(
        results_df['Volatility'] * 100, 
        results_df['Return'] * 100, 
        c=results_df['Sharpe'], 
        cmap='viridis_r', 
        marker='o', 
        s=10, 
        alpha=0.3
    )
    plt.colorbar(sc, label='Sharpe Ratio')
    
    # Plot MSR
    plt.scatter(
        msr_portfolio['Volatility'] * 100, 
        msr_portfolio['Return'] * 100, 
        color='red', 
        marker='*', 
        s=200, 
        label='Max Sharpe Ratio Portfolio'
    )
    
    # Plot MVP
    plt.scatter(
        mvp_portfolio['Volatility'] * 100, 
        mvp_portfolio['Return'] * 100, 
        color='blue', 
        marker='*', 
        s=200, 
        label='Minimum Variance Portfolio'
    )
    
    plt.title("Markowitz Efficient Frontier (Top 5 Scorecard Funds)", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Annualized Volatility / Risk (%)")
    plt.ylabel("Annualized Expected Return (%)")
    plt.legend(loc="upper left", frameon=True, shadow=True)
    plt.tight_layout()
    
    ef_chart = CHARTS_DIR / "efficient_frontier.png"
    plt.savefig(ef_chart, dpi=300)
    plt.close()
    logger.info("Saved Efficient Frontier chart to %s", ef_chart)

def main() -> None:
    nav_df, tx_df, holdings_df, master_df, scorecard_df = load_data()
    
    # Run computations
    compute_var_cvar(nav_df, master_df)
    plot_rolling_sharpe(nav_df, master_df)
    investor_cohort_analysis(tx_df, master_df)
    sip_continuation_analysis(tx_df)
    sector_concentration_analysis(holdings_df, master_df)
    
    # Run forecasts and portfolio optimization
    compute_monte_carlo(nav_df, scorecard_df)
    compute_portfolio_optimization(nav_df, scorecard_df)
    
    logger.info("Advanced Analytics run completed successfully!")

if __name__ == "__main__":
    main()
