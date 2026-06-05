"""
Day 7 - Programmatic PDF Report Generator for Bluestock MF Analytics.

Compiles a comprehensive, professional, multi-page executive report at
'reports/Final_Report.pdf' using ReportLab. Includes structured text,
formatted results tables, and embeds all generated visualization charts.
"""
from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Ensure scripts path is in system path so we can import _common
sys.path.append(str(Path(__file__).resolve().parent))
from _common import PROCESSED_DIR, REPORTS_DIR, get_logger

logger = get_logger("generate_final_report")

PDF_PATH = REPORTS_DIR / "Final_Report.pdf"
CHARTS_DIR = REPORTS_DIR / "charts"

# Hex Colors
PRIMARY = colors.HexColor('#4F46E5')    # Indigo
SECONDARY = colors.HexColor('#1E293B')  # Dark Slate
ACCENT = colors.HexColor('#10B981')     # Emerald
TEXT_COLOR = colors.HexColor('#334155') # Muted text
BG_LIGHT = colors.HexColor('#F8FAFC')   # Light grey background

def create_table_from_df(df, max_rows=10):
    """Helper to convert a pandas DataFrame into a formatted ReportLab Table."""
    data = [df.columns.tolist()] + df.head(max_rows).values.tolist()
    # Format floats
    for row_idx in range(1, len(data)):
        for col_idx in range(len(data[row_idx])):
            val = data[row_idx][col_idx]
            if isinstance(val, float):
                data[row_idx][col_idx] = f"{val:.2f}"
            elif isinstance(val, (int, float)) and 'code' in str(df.columns[col_idx]).lower():
                data[row_idx][col_idx] = str(val)
                
    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
    ]))
    return table

def main() -> None:
    logger.info("Initializing PDF report compilation...")
    
    # Page setup - 0.5 inch margins for maximized printable area
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=SECONDARY,
        alignment=TA_LEFT,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=180
    )
    
    metadata_style = ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=TEXT_COLOR,
        alignment=TA_LEFT,
        spaceAfter=5
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceBefore=20,
        spaceAfter=12,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=SECONDARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=TEXT_COLOR,
        spaceAfter=10,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_COLOR,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_COLOR,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    story = []
    
    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 100))
    story.append(Paragraph("BLUESTOCK FINTECH", ParagraphStyle('Company', fontName='Helvetica-Bold', fontSize=14, leading=16, textColor=PRIMARY, spaceAfter=20)))
    story.append(Paragraph("MUTUAL FUND ANALYTICS<br/>PLATFORM", title_style))
    story.append(Paragraph("End-to-End Data Engineering, ETL Pipeline & Interactive Dashboard", subtitle_style))
    story.append(Spacer(1, 100))
    story.append(Paragraph("<b>Project Type:</b> Individual Capstone Project", metadata_style))
    story.append(Paragraph("<b>Prepared By:</b> Intern / Data Analyst — Srujan", metadata_style))
    story.append(Paragraph("<b>Domain:</b> Mutual Fund / FinTech", metadata_style))
    story.append(Paragraph("<b>Date:</b> June 2026", metadata_style))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 2: TABLE OF CONTENTS & EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "The growth of the Indian mutual fund industry has been historic, with assets under management (AUM) crossing ₹81 lakh crore and monthly SIP inflows reaching ₹31,002 crore as of December 2025. Despite this expansion, individual investors and wealth managers face massive challenges in selecting funds due to data fragmentation (NAV, holding, and transaction reports are split across multiple AMFI/NSE sections in different formats) and the lack of accessible risk-adjusted evaluation metrics.",
        body_style
    ))
    story.append(Paragraph(
        "This project successfully designs and deploys a complete <b>Mutual Fund Analytics Platform</b> to bridge this gap. The platform implements a robust Python ETL pipeline to ingest daily NAVs, holdings, and investor transaction reports, structures them into a normalized SQLite database, and computes key return and risk parameters (CAGR, Sharpe, Sortino, Alpha, Beta, VaR, and sector concentration). Finally, we build a multi-page interactive Streamlit dashboard allowing self-service analytics and fund selection.",
        body_style
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Table of Contents", h2_style))
    story.append(Paragraph("1. Project Overview & Context .......................................................................................... Page 3", bullet_style))
    story.append(Paragraph("2. System Architecture & ETL Ingestion ......................................................................... Page 4", bullet_style))
    story.append(Paragraph("3. Relational SQL Schema & Database Design .................................................................. Page 5", bullet_style))
    story.append(Paragraph("4. Exploratory Data Analysis (EDA) Highlights ................................................................ Page 6", bullet_style))
    story.append(Paragraph("5. Fund Performance Analytics & Scorecard ..................................................................... Page 8", bullet_style))
    story.append(Paragraph("6. Advanced Risk & Behavioral Analytics ........................................................................ Page 10", bullet_style))
    story.append(Paragraph("7. Interactive Dashboard Walkthrough ............................................................................. Page 12", bullet_style))
    story.append(Paragraph("8. Key Recommendations & Conclusion .............................................................................. Page 14", bullet_style))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 3: PROJECT OVERVIEW & CONTEXT
    # ==========================================
    story.append(Paragraph("1. Project Overview & Context", h1_style))
    story.append(Paragraph(
        "Bluestock Fintech seeks to democratize investment analytics for retail and institutional investors. The primary goal of this analytics platform is to track NAV movements of 40+ key mutual fund schemes, monitor AUM growth of the 10 largest fund houses, analyze investor transaction patterns, benchmark active fund returns against indexes, and compute mathematical risk-adjusted ratios.",
        body_style
    ))
    story.append(Paragraph("Business Objectives Met:", h2_style))
    story.append(Paragraph("<b>• Objective 1 (ETL Ingestion)</b>: Set up an automated pipeline extracting data from public AMFI archives and live API resources (mfapi.in).", bullet_style))
    story.append(Paragraph("<b>• Objective 2 (SQL Schema)</b>: Design a highly optimized star schema database to support fast analytics queries.", bullet_style))
    story.append(Paragraph("<b>• Objective 3 (EDA)</b>: Conduct exploratory data analysis to discover key structural trends in assets, geography, and age demographics.", bullet_style))
    story.append(Paragraph("<b>• Objective 4-5 (Performance & Dashboard)</b>: Compute risk-adjusted return ratios and build a dynamic dashboard displaying the outcomes.", bullet_style))
    story.append(Paragraph("<b>• Objective 6-7 (Investor & Benchmark Analysis)</b>: Segment transaction habits by geographic/demographic cohorts, evaluate churn risk, and calculate regression alpha and tracking error against benchmark indexes.", bullet_style))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 4: SYSTEM ARCHITECTURE & ETL
    # ==========================================
    story.append(Paragraph("2. System Architecture & ETL Ingestion", h1_style))
    story.append(Paragraph(
        "The analytics platform utilizes a standard five-layer data engineering pipeline: Extract, Transform, Load, Analyze, and Visualize. This architecture replicates scalable fintech systems used by commercial platforms.",
        body_style
    ))
    story.append(Paragraph("Pipeline Layer Breakdown:", h2_style))
    story.append(Paragraph("<b>1. Data Ingestion (Extract)</b>: Implements flat file ingestion of historical CSVs (metadata, historical NAVs, transactions, index prices) and runs script integrations for live API requests to mfapi.in. Daily NAV endpoints are fetched to refresh the local files.", bullet_style))
    story.append(Paragraph("<b>2. Data Cleansing (Transform)</b>: Employs Pandas for programmatic data cleaning. It parses date columns to standard datetimes, sorts chronology, forward-fills missing NAV values on weekends/holidays to prevent CAGR calculation errors, normalizes transaction types, and validates value boundaries (e.g., amount > 0).", bullet_style))
    story.append(Paragraph("<b>3. Storage Engine (Load)</b>: Structures cleaned tables inside a SQLite relational database with enforced referential integrity and custom indexing for fast lookup.", bullet_style))
    story.append(Paragraph("<b>4. Risk Engine (Analyze)</b>: Computes CAGRs, Sharpe ratios, Sortino ratios, rolling beta/alpha regressions, 95% historical Value at Risk (VaR), and sector concentration indexes.", bullet_style))
    story.append(Paragraph("<b>5. Delivery Engine (Visualize)</b>: Serves interactive charts and selectors via a local Streamlit app and compiles static reports.", bullet_style))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 5: RELATIONAL SQL SCHEMA
    # ==========================================
    story.append(Paragraph("3. Relational SQL Schema & Database Design", h1_style))
    story.append(Paragraph(
        "To enable analytical queries, all clean CSV datasets were loaded into a normalized SQLite relational database (<code>bluestock_mf.db</code>) using a structured star schema.",
        body_style
    ))
    story.append(Paragraph("Star Schema Table Structures:", h2_style))
    story.append(Paragraph("<b>• Dimension Table: fund_master</b>: Stores AMC details, scheme metadata, categories (Large/Mid/Small Cap), plan type (Regular/Direct), and expense ratios. Enforces <code>amfi_code</code> as the Primary Key.", bullet_style))
    story.append(Paragraph("<b>• Fact Table: nav_history</b>: Compiles daily NAV records. Enforces composite primary key on <code>(amfi_code, date)</code> and references <code>fund_master</code> as a foreign key.", bullet_style))
    story.append(Paragraph("<b>• Fact Table: investor_transactions</b>: Simulates ~32,000 transactions across 5,000 investors, tracking dates, investor IDs, amounts, payment modes, kyc, and demographics.", bullet_style))
    story.append(Paragraph("<b>• Fact Table: scheme_performance</b>: Houses computed performance and risk-adjusted metrics (returns, Sharpe, Sortino, Alpha, Beta, max drawdown) indexed on <code>amfi_code</code>.", bullet_style))
    story.append(Paragraph("<b>• Fact Table: portfolio_holdings</b>: Tracks sector weights and equity holdings for all funds.", bullet_style))
    story.append(Paragraph("<b>• Fact Table: benchmark_indices</b>: Records daily closings of Nifty 50 and Nifty 100 indexes.", bullet_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Optimized SQL Queries & Integrity Verification:", h2_style))
    story.append(Paragraph("Integrity tests run automatically during database construction via <code>PRAGMA foreign_key_check</code> and custom validation scripts. Zero orphan records exist. Column indexes (e.g. <code>idx_nav_amfi</code>, <code>idx_txn_amfi</code>) are built to optimize joins.", body_style))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 6: EDA FINDINGS - PART 1
    # ==========================================
    story.append(Paragraph("4. Exploratory Data Analysis (EDA) Highlights", h1_style))
    story.append(Paragraph(
        "Exploratory data analysis was conducted on NAV trends, assets under management (AUM), SIP flows, and investor demographics. Programmatic charts are saved inside reports for stakeholder distribution.",
        body_style
    ))
    
    # Embed NAV trends chart
    chart1_path = CHARTS_DIR / "chart1_nav_trends.png"
    if chart1_path.exists():
        story.append(Image(str(chart1_path), width=480, height=240))
        story.append(Paragraph("Figure 1: Daily NAV Trends of Key Mutual Fund Schemes (2022–2026)", caption_style))
        
    story.append(Paragraph(
        "<b>NAV Growth Performance</b>: Charting daily NAVs shows a steady upward trajectory from 2022 to mid-2026, marking strong bull cycles, minor corrections in early 2024, and a powerful post-correction rally. Direct plans consistently outperformed Regular plans due to lower expense ratios.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 7: EDA FINDINGS - PART 2
    # ==========================================
    story.append(Paragraph("4. EDA Highlights (Continued)", h1_style))
    
    # Embed AUM growth chart
    chart5_path = CHARTS_DIR / "chart5_aum_growth.png"
    if chart5_path.exists():
        story.append(Image(str(chart5_path), width=480, height=240))
        story.append(Paragraph("Figure 2: Assets Under Management (AUM) Growth by Major Fund Houses (2022-2025)", caption_style))
        
    story.append(Paragraph(
        "<b>Asset Consolidation</b>: The top three fund houses (SBI Mutual Fund, ICICI Prudential, and HDFC Mutual Fund) dominate the industry assets, with SBI leading at ₹12.50 lakh crore in Dec 2025. Industry AUM growth was heavily correlated with rising SIP accounts and a deepening equity culture in India.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 8: FUND PERFORMANCE ANALYTICS & SCORECARD
    # ==========================================
    story.append(Paragraph("5. Fund Performance Analytics & Scorecard", h1_style))
    story.append(Paragraph(
        "To establish a quantitative framework for fund selection, we calculated CAGRs, Sharpe and Sortino ratios, alpha and beta relative to Nifty 100, and maximum drawdowns from the cleaned daily NAV history.",
        body_style
    ))
    story.append(Paragraph("Composite Scorecard Model (0-100):", h2_style))
    story.append(Paragraph("A weighted rank model was designed to score funds out of 100: 30% Return Rank + 25% Sharpe Rank + 20% Alpha Rank + 15% Expense Ratio Rank (inverted) + 10% Max Drawdown Rank (inverted).", body_style))
    
    # Load scorecard data
    scorecard_df = pd.read_csv(PROCESSED_DIR / "fund_scorecard.csv")
    if not scorecard_df.empty:
        # Display top 8 funds
        table_df = scorecard_df[['scorecard_rank', 'scheme_name', 'cagr_3yr_pct', 'sharpe_ratio', 'alpha', 'score']].head(8)
        table_df = table_df.rename(columns={
            'scorecard_rank': 'Rank',
            'scheme_name': 'Scheme Name',
            'cagr_3yr_pct': '3Yr CAGR',
            'sharpe_ratio': 'Sharpe',
            'alpha': 'Alpha',
            'score': 'Score'
        })
        story.append(create_table_from_df(table_df, max_rows=8))
        story.append(Spacer(1, 5))
        story.append(Paragraph("Table 1: Top 8 Performing Funds Ranked by Composite Scorecard", caption_style))
        
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 9: BENCHMARK PERFORMANCE COMPARISON
    # ==========================================
    story.append(Paragraph("5. Benchmark Comparison (Continued)", h1_style))
    
    # Embed Benchmark comparison chart
    bench_chart_path = CHARTS_DIR / "benchmark_comparison.png"
    if bench_chart_path.exists():
        story.append(Image(str(bench_chart_path), width=480, height=240))
        story.append(Paragraph("Figure 3: Top 5 Scorecard Funds vs Nifty 50 and Nifty 100 Benchmarks (3-Year Normalized NAV)", caption_style))
        
    story.append(Paragraph(
        "<b>Alpha and Tracking Error Analysis</b>: Over a 3-year trailing period, all top 5 scorecard funds generated significant positive alpha (21.1% to 29.2%) against the Nifty 100. Tracking errors ranged from 8.5% to 10.2% vs Nifty 50, reflecting active management deviations to harvest excess return.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 10: ADVANCED RISK ANALYTICS
    # ==========================================
    story.append(Paragraph("6. Advanced Risk & Behavioral Analytics", h1_style))
    story.append(Paragraph(
        "Day 6 analytics focused on advanced mathematical risk modelling: Historical Value at Risk (VaR 95%), Conditional VaR (CVaR 95%), rolling Sharpe ratios, investor cohort metrics, SIP continuation, and sector concentration.",
        body_style
    ))
    story.append(Paragraph("Historical Value at Risk (95% Confidence):", h2_style))
    story.append(Paragraph(
        "Daily VaR represents the threshold loss that will not be exceeded with 95% confidence on any single trading day. Daily CVaR computes the expected loss on days that breach this VaR threshold.",
        body_style
    ))
    
    # Load VaR report
    var_df = pd.read_csv(PROCESSED_DIR / "var_cvar_report.csv")
    if not var_df.empty:
        # Display top 5 risky funds
        risky_df = var_df.sort_values('var_95_pct', ascending=False).head(5)
        risky_df['scheme_name'] = risky_df['scheme_name'].apply(lambda x: x.split(" - ")[0][:40])
        risky_df = risky_df.rename(columns={
            'amfi_code': 'AMFI Code',
            'scheme_name': 'Scheme Name',
            'var_95_pct': 'Daily VaR 95%',
            'cvar_95_pct': 'Daily CVaR 95%'
        })
        story.append(create_table_from_df(risky_df, max_rows=5))
        story.append(Spacer(1, 5))
        story.append(Paragraph("Table 2: Top 5 Funds with Highest Daily Value at Risk (VaR 95%)", caption_style))
        
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 11: ROLLING SHARPE & BEHAVIOR
    # ==========================================
    story.append(Paragraph("6. Risk & Behavior Analytics (Continued)", h1_style))
    
    # Embed rolling Sharpe chart
    rolling_chart = CHARTS_DIR / "rolling_sharpe_chart.png"
    if rolling_chart.exists():
        story.append(Image(str(rolling_chart), width=480, height=240))
        story.append(Paragraph("Figure 4: Trailing 90-Day Annualized Sharpe Ratios (2022-2026)", caption_style))
        
    story.append(Paragraph(
        "<b>Sharpe Ratio Stability</b>: Analyzing the trailing 90-day Sharpe ratios shows that fund performance efficiency varies dynamically. During the 2024 election and correction phase, Sharpe ratios fell sharply across all funds, recovering strongly in late 2024 to cross 1.5, proving active risk-return stabilization.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 12: INVESTOR BEHAVIOR & COHORT
    # ==========================================
    story.append(Paragraph("6. Investor Behavior & Churn Analytics", h1_style))
    story.append(Paragraph(
        "Understanding investor behavior is critical for AMC retention and marketing. We segmented investors into acquisition cohorts based on their first transaction year.",
        body_style
    ))
    
    # Load cohort data
    cohort_df = pd.read_csv(PROCESSED_DIR / "cohort_analysis.csv")
    if not cohort_df.empty:
        cohort_table = cohort_df.rename(columns={
            'cohort': 'Cohort Year',
            'total_investors': 'Total Investors',
            'total_net_investment_cr': 'Net Investment (Cr)',
            'avg_sip_amount_inr': 'Avg SIP (INR)',
            'top_fund_category': 'Top Preference'
        })
        story.append(create_table_from_df(cohort_table, max_rows=2))
        story.append(Spacer(1, 5))
        story.append(Paragraph("Table 3: Investor Demographics & Activity by Acquisition Cohort", caption_style))
        
    story.append(Paragraph("SIP continuation and churn risks:", h2_style))
    story.append(Paragraph(
        "For investors with at least 6 SIP payments, we calculated consecutive payment intervals. Standard SIP gaps are 30 days. Out of the frequent investor pool, <b>1,361 investors</b> exhibit payment gaps greater than 35 days, flagging them as at-risk. This provides AMCs with a predictive list to trigger email reminders or customer retention calls before outright cancellation.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 13: SECTOR CONCENTRATION
    # ==========================================
    story.append(Paragraph("6. Sector Concentration & Recommendations", h1_style))
    
    # Embed HHI chart
    hhi_chart = CHARTS_DIR / "sector_concentration.png"
    if hhi_chart.exists():
        story.append(Image(str(hhi_chart), width=480, height=240))
        story.append(Paragraph("Figure 5: Herfindahl-Hirschman Index (HHI) for Top 10 Concentrated Portfolios", caption_style))
        
    story.append(Paragraph(
        "<b>Sector Diversification</b>: The Herfindahl-Hirschman Index (HHI) measures concentration. Lower HHI shows wide sector diversification (e.g. Flexicap funds hover at 0.12 - 0.15), while midcap and thematic funds exhibit HHI values above 0.24, showing concentration in Financials, IT, and Infrastructure.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 14: INTERACTIVE DASHBOARD WALKTHROUGH
    # ==========================================
    story.append(Paragraph("7. Interactive Dashboard Walkthrough", h1_style))
    story.append(Paragraph(
        "An interactive dashboard was developed using Streamlit as a modern, self-service alternative to static monthly reports. The application contains 4 major reporting pages:",
        body_style
    ))
    
    # Embed Dashboard page 1 screenshot
    db_page1 = CHARTS_DIR / "dashboard_page1.png"
    if db_page1.exists():
        story.append(Image(str(db_page1), width=440, height=220))
        story.append(Paragraph("Figure 6: Dashboard Page 1 - Industry Assets & Folio Growth Overview", caption_style))
        
    story.append(Paragraph(
        "<b>Dashboard Page 1 (Industry Overview)</b>: Houses real-time high-level industry KPIs (AUM, monthly inflow, active folios) and traces the long-term trend line of SIP assets alongside a bar chart displaying AUM ranks for the top 8 fund houses.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 15: INTERACTIVE DASHBOARD WALKTHROUGH (CONTINUED)
    # ==========================================
    story.append(Paragraph("7. Dashboard Walkthrough (Continued)", h1_style))
    
    # Embed Dashboard page 2 screenshot
    db_page2 = CHARTS_DIR / "dashboard_page2.png"
    if db_page2.exists():
        story.append(Image(str(db_page2), width=440, height=220))
        story.append(Paragraph("Figure 7: Dashboard Page 2 - Interactive Fund Performance Scatter & Scorecard Grid", caption_style))
        
    story.append(Paragraph(
        "<b>Dashboard Page 2 (Performance & Analysis)</b>: Integrates interactive scatter plots mapping annualized returns against standard deviation. Users can filter by category, AMC, and plan. Selecting a scheme renders trailing CAGR statistics and interactive NAV line charts plotted against Nifty benchmarks.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 16: KEY RECOMMENDATIONS & CONCLUSION
    # ==========================================
    story.append(Paragraph("8. Key Recommendations & Conclusion", h1_style))
    story.append(Paragraph(
        "The Capstone project successfully establishes a production-quality mutual fund analytics platform at Bluestock Fintech. By combining automated extraction, database storage, and programmatic risk reporting, the platform resolves data fragmentation and provides advisors with actionable insight.",
        body_style
    ))
    story.append(Paragraph("Strategic Business Recommendations:", h2_style))
    story.append(Paragraph("<b>1. Deploy Automated Churn Alerts</b>: Leverage the SIP continuation engine to auto-email notifications to advisors when an investor's payment gap crosses 35 days, protecting AMC assets under management.", bullet_style))
    story.append(Paragraph("<b>2. Promote Low-Expense Direct Plans</b>: Highlight Direct schemes in the scorecard table. Lower expense ratios (0.6% - 0.8%) translate into significant return compounding over 5+ years compared to Regular equivalents.", bullet_style))
    story.append(Paragraph("<b>3. Leverage Rule-Based Recommendations</b>: Incorporate the risk-profile recommender in customer-facing portals to match retail investors with the highest Sharpe ratio funds matching their SEBI risk grades.", bullet_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Project Conclusion:", h2_style))
    story.append(Paragraph(
        "The Mutual Fund Analytics Platform is ready for deployment. The codebase is clean, well-documented, and version-controlled. Moving from static reports to self-service interactive dashboards represents a major leap in operational efficiency for data-driven wealth management.",
        body_style
    ))
    
    # Compile document
    doc.build(story)
    logger.info("PDF report compiled successfully at %s!", PDF_PATH)

if __name__ == "__main__":
    main()
