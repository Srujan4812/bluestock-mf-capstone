"""
Bonus B5 - Weekly Performance HTML Email Report Generator.

Reads the latest cleaned CSVs and scorecard, compiles the key KPIs and risk metrics,
and renders a styled, responsive, dark-indigo themed HTML email report at
'reports/weekly_performance_report.html'.
"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add scripts directory to path
sys.path.append(str(Path(__file__).resolve().parent))
from _common import PROCESSED_DIR, REPORTS_DIR, get_logger

logger = get_logger("email_report")
HTML_OUT_PATH = REPORTS_DIR / "weekly_performance_report.html"

def generate_html_report() -> None:
    logger.info("Assembling weekly HTML email performance summary...")
    
    # 1. Load latest stats
    scorecard_df = pd.read_csv(PROCESSED_DIR / "fund_scorecard.csv")
    monthly_sip = pd.read_csv(PROCESSED_DIR / "clean_monthly_sip_inflows.csv")
    folios = pd.read_csv(PROCESSED_DIR / "clean_industry_folio_count.csv")
    cohort_df = pd.read_csv(PROCESSED_DIR / "cohort_analysis.csv")
    continuity_df = pd.read_csv(PROCESSED_DIR / "sip_continuity.csv")
    
    # KPIs
    latest_sip = monthly_sip.iloc[-1]
    latest_folio = folios.iloc[-1]
    top_fund = scorecard_df.iloc[0]
    
    total_folios = f"{latest_folio['total_folios_crore']:.2f} Cr"
    active_sip = f"{latest_sip['active_sip_accounts_crore']:.2f} Cr"
    sip_inflow = f"Rs. {latest_sip['sip_inflow_crore']:,.0f} Cr"
    
    churn_risk = "N/A"
    if not continuity_df.empty:
        at_risk = continuity_df['is_at_risk'].sum()
        pct = at_risk / len(continuity_df) * 100
        churn_risk = f"{at_risk} ({pct:.1f}%)"
        
    # Table of Top 5 funds
    top_5_rows = ""
    for idx, row in scorecard_df.head(5).iterrows():
        top_5_rows += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #E2E8F0;">#{row['scorecard_rank']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #FFFFFF; font-weight: bold;">{row['scheme_name'].split(" - ")[0]}</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #10B981; font-weight: bold;">{row['cagr_3yr_pct']:.2f}%</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #6366F1;">{row['sharpe_ratio']:.2f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #10B981;">{row['alpha']:.2f}%</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #F59E0B; font-weight: bold;">{row['score']:.2f}</td>
        </tr>
        """
        
    # Table of Cohorts
    cohort_rows = ""
    for idx, row in cohort_df.iterrows():
        cohort_rows += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #FFFFFF; font-weight: bold;">{row['cohort']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #E2E8F0;">{row['total_investors']:,}</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #6366F1; font-weight: bold;">Rs. {row['total_net_investment_cr']:.2f} Cr</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #E2E8F0;">Rs. {row['avg_sip_amount_inr']:.2f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #2D3748; color: #A78BFA;">{row['top_fund_category']}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bluestock Weekly Wealth Summary</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0B0F19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #F1F5F9;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 40px auto; background-color: #0E1322; border: 1px solid #1E293B; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
        <!-- HEADER -->
        <tr>
            <td style="padding: 40px 30px; text-align: center; border-bottom: 1px solid #1E293B; background: linear-gradient(135deg, #4F46E5 0%, #10B981 100%); border-top-left-radius: 12px; border-top-right-radius: 12px;">
                <h1 style="margin: 0; font-size: 26px; font-weight: 800; color: #FFFFFF; letter-spacing: 2px; text-transform: uppercase;">BLUESTOCK</h1>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #E2E8F0; text-transform: uppercase; letter-spacing: 3px;">Weekly Wealth & Performance Analytics</p>
            </td>
        </tr>
        
        <!-- INTRO -->
        <tr>
            <td style="padding: 30px;">
                <p style="margin: 0 0 20px 0; font-size: 15px; line-height: 1.6; color: #94A3B8;">
                    Hello Advisor, here is the automated weekly report for the Bluestock Mutual Fund Analytics Platform. All daily return calculations, risk metrics, and scorecard rankings have been updated as of <b>{datetime.now().strftime('%Y-%m-%d')}</b>.
                </p>
            </td>
        </tr>
        
        <!-- KPI CARDS -->
        <tr>
            <td style="padding: 0 30px 20px 30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td width="31%" style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 15px; text-align: center;">
                            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: bold; margin-bottom: 5px;">Total Folios</div>
                            <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">{total_folios}</div>
                        </td>
                        <td width="3%">&nbsp;</td>
                        <td width="31%" style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 15px; text-align: center;">
                            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: bold; margin-bottom: 5px;">Active SIPs</div>
                            <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">{active_sip}</div>
                        </td>
                        <td width="3%">&nbsp;</td>
                        <td width="31%" style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 15px; text-align: center;">
                            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: bold; margin-bottom: 5px;">SIP Inflow</div>
                            <div style="font-size: 20px; font-weight: bold; color: #10B981;">{sip_inflow}</div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <!-- SCORECARD TABLE -->
        <tr>
            <td style="padding: 10px 30px;">
                <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 700; color: #FFFFFF; border-left: 4px solid #4F46E5; padding-left: 10px;">Top 5 Scorecard Funds</h3>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: left; font-size: 13px;">
                    <thead>
                        <tr style="background-color: #1E293B; color: #94A3B8; font-weight: bold;">
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Rank</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Scheme Name</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">3Yr CAGR</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Sharpe</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Alpha</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {top_5_rows}
                    </tbody>
                </table>
            </td>
        </tr>
        
        <!-- COHORT TABLE -->
        <tr>
            <td style="padding: 30px 30px 10px 30px;">
                <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 700; color: #FFFFFF; border-left: 4px solid #10B981; padding-left: 10px;">Investor Cohort Activity</h3>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: left; font-size: 13px;">
                    <thead>
                        <tr style="background-color: #1E293B; color: #94A3B8; font-weight: bold;">
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Cohort</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Investors</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Net Inv (Cr)</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Avg SIP</th>
                            <th style="padding: 10px; border-bottom: 2px solid #334155;">Preference</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cohort_rows}
                    </tbody>
                </table>
            </td>
        </tr>
        
        <!-- RISK METRICS & CHURN SUMMARY -->
        <tr>
            <td style="padding: 20px 30px 30px 30px;">
                <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 700; color: #FFFFFF; border-left: 4px solid #F59E0B; padding-left: 10px;">Risk & Retention Alert</h3>
                <table border="0" cellpadding="12" cellspacing="0" width="100%" style="background-color: #1E293B; border-radius: 8px; font-size: 14px; line-height: 1.5;">
                    <tr>
                        <td style="color: #94A3B8; width: 50%;">At-Risk SIP Investors:</td>
                        <td style="color: #EF4444; font-weight: bold; text-align: right;">{churn_risk}</td>
                    </tr>
                    <tr>
                        <td style="color: #94A3B8; width: 50%;">Top Scorecard Fund:</td>
                        <td style="color: #10B981; font-weight: bold; text-align: right;">{top_fund['scheme_name'].split(" - ")[0]}</td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <!-- FOOTER -->
        <tr>
            <td style="padding: 30px; text-align: center; border-top: 1px solid #1E293B; font-size: 11px; color: #64748B; background-color: #0E1322; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;">
                <p style="margin: 0 0 10px 0;">This email summary is automatically generated by the Bluestock MF Analytics Pipeline daemon scheduler.</p>
                <p style="margin: 0;">&copy; 2026 Bluestock Fintech Pvt. Ltd. | Confidential Financial Data Report</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    HTML_OUT_PATH.write_text(html_content, encoding="utf-8")
    logger.info("Weekly HTML email report generated successfully at %s!", HTML_OUT_PATH)

if __name__ == "__main__":
    generate_html_report()
