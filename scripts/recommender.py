"""
Recommends mutual funds matching an investor's risk appetite (Low, Moderate, High) 
based on their annualized Sharpe ratio.
"""
from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

# Ensure scripts path is in system path so we can import _common
sys.path.append(str(Path(__file__).resolve().parent))
from _common import PROCESSED_DIR, get_logger

logger = get_logger("recommender")

def recommend_funds(risk_appetite: str) -> pd.DataFrame:
    """
    Recommends the top 3 mutual funds based on the investor's risk appetite.
    
    Parameters
    ----------
    risk_appetite : str
        The risk appetite of the investor, must be 'Low', 'Moderate', or 'High'.
        
    Returns
    -------
    pd.DataFrame
        A DataFrame containing the top 3 recommended schemes with their details.
    """
    risk_appetite = risk_appetite.strip().capitalize()
    if risk_appetite not in ['Low', 'Moderate', 'High']:
        raise ValueError("risk_appetite must be 'Low', 'Moderate', or 'High'")
        
    # Load scorecard (which contains Sharpe Ratio and CAGR)
    scorecard_path = PROCESSED_DIR / "fund_scorecard.csv"
    master_path = PROCESSED_DIR / "clean_fund_master.csv"
    
    if not scorecard_path.exists() or not master_path.exists():
        logger.error("Required data files do not exist. Please run performance_analytics first.")
        return pd.DataFrame()
        
    scorecard = pd.read_csv(scorecard_path)
    master = pd.read_csv(master_path)
    
    # Merge on amfi_code to get risk categories
    df = scorecard.merge(master[['amfi_code', 'risk_category', 'category', 'sub_category']], on='amfi_code')
    
    # Map risk appetite to SEBI risk categories
    # Unique values in clean_fund_master.csv: 'Low', 'Moderate', 'Moderately High', 'High', 'Very High'
    if risk_appetite == 'Low':
        target_risks = ['Low', 'Moderate']
    elif risk_appetite == 'Moderate':
        target_risks = ['Moderately High', 'High']
    else: # High
        target_risks = ['Very High']
        
    # Filter matching funds
    filtered_df = df[df['risk_category'].isin(target_risks)]
    
    # Rank by Sharpe Ratio (descending) and select top 3
    recommended = filtered_df.sort_values(by='sharpe_ratio', ascending=False).head(3)
    
    # Select columns to return
    columns_to_return = [
        'scorecard_rank', 'scheme_name', 'category', 'sub_category',
        'risk_category', 'cagr_3yr_pct', 'sharpe_ratio', 'alpha'
    ]
    return recommended[columns_to_return]

def main() -> None:
    """Command line handler for testing the recommender."""
    print("Testing Fund Recommender Module...")
    print("=" * 40)
    for risk in ['Low', 'Moderate', 'High']:
        print(f"\nRecommended Funds for {risk} Risk Appetite:")
        recs = recommend_funds(risk)
        if not recs.empty:
            for idx, row in recs.iterrows():
                print(f"  Rank #{row['scorecard_rank']}: {row['scheme_name']}")
                print(f"    Category: {row['category']} ({row['sub_category']}) | Risk: {row['risk_category']}")
                print(f"    3Yr CAGR: {row['cagr_3yr_pct']:.2f}% | Sharpe: {row['sharpe_ratio']:.2f} | Alpha: {row['alpha']:.2f}%")
        else:
            print("  No recommendations found.")
    print("=" * 40)

if __name__ == "__main__":
    main()
