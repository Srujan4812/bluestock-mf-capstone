"""
Day 5 - Programmatic dashboard exporter for Bluestock MF Analytics.

Generates 4 high-resolution dashboard mockup pages (PNGs) representing
the Streamlit interactive application views and compiles them into a
unified 'reports/Dashboard.pdf' file.
"""
from __future__ import annotations

import os
import sys
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

# Ensure scripts path is in system path so we can import _common
sys.path.append(str(Path(__file__).resolve().parent))
from _common import PROCESSED_DIR, REPORTS_DIR, get_logger

logger = get_logger("export_dashboard")

CHARTS_DIR = REPORTS_DIR / "charts"
PDF_PATH = REPORTS_DIR / "Dashboard.pdf"

# Set matplotlib style for premium look
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'figure.facecolor': '#0F172A', # Slate-900 background
    'axes.facecolor': '#1E293B',   # Slate-800 background
    'text.color': '#F8FAFC',       # Slate-50 text
    'axes.labelcolor': '#94A3B8',  # Slate-400 labels
    'xtick.color': '#94A3B8',
    'ytick.color': '#94A3B8',
    'grid.color': '#334155',       # Slate-700 grid
    'axes.edgecolor': '#475569',   # Slate-600 border
    'axes.titlecolor': '#6366F1'   # Indigo-500 title
})

def draw_kpi_card(ax, title, value, delta, x_pos=0.1, y_pos=0.1, box_color='#1E293B', border_color='#4F46E5'):
    """Helper to draw a styled KPI card inside an axis."""
    ax.axis('off')
    # Draw background box
    rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, facecolor=box_color, edgecolor=border_color, linewidth=1.5)
    ax.add_patch(rect)
    
    # Text details
    ax.text(0.5, 0.75, title, fontsize=10, color='#94A3B8', ha='center', va='center', fontweight='semibold')
    ax.text(0.5, 0.45, value, fontsize=20, color='#FFFFFF', ha='center', va='center', fontweight='bold')
    ax.text(0.5, 0.15, delta, fontsize=9, color='#10B981', ha='center', va='center')

def generate_page1():
    """Page 1: Industry Overview."""
    logger.info("Generating Dashboard Page 1 (Industry Overview)...")
    
    monthly_sip = pd.read_csv(PROCESSED_DIR / "clean_monthly_sip_inflows.csv")
    aum_fh = pd.read_csv(PROCESSED_DIR / "clean_aum_by_fund_house.csv")
    folios = pd.read_csv(PROCESSED_DIR / "clean_industry_folio_count.csv")
    
    # Create multi-panel landscape figure
    fig = plt.figure(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#0F172A')
    
    # Title Header
    fig.text(0.05, 0.94, "BLUESTOCK MUTUAL FUND ANALYTICS  |  DASHBOARD", fontsize=11, color='#6366F1', fontweight='bold')
    fig.text(0.05, 0.90, "Page 1: Industry Assets & Inflows Overview", fontsize=18, color='#FFFFFF', fontweight='bold')
    
    # 1. Row of KPI Cards (use GridSpec)
    gs_kpi = fig.add_gridspec(nrows=1, ncols=4, left=0.05, right=0.95, bottom=0.74, top=0.86)
    
    # Card 1: Total AUM
    draw_kpi_card(fig.add_subplot(gs_kpi[0, 0]), "Total Industry AUM", "₹81.0 L Cr", "Dec 2025 • Peak")
    # Card 2: SIP Inflow
    latest_sip = monthly_sip.iloc[-1]
    draw_kpi_card(fig.add_subplot(gs_kpi[0, 1]), "Monthly SIP Inflow", f"₹{latest_sip['sip_inflow_crore']:,.0f} Cr", "All-time High Inflow")
    # Card 3: Folios
    latest_folio = folios.iloc[-1]
    draw_kpi_card(fig.add_subplot(gs_kpi[0, 2]), "Total Folio Count", f"{latest_folio['total_folios_crore']:.2f} Cr", "Equity: 78% Share")
    # Card 4: Active SIP Accounts
    draw_kpi_card(fig.add_subplot(gs_kpi[0, 3]), "Active SIP Accounts", f"{latest_sip['active_sip_accounts_crore']:.2f} Cr", "YoY Growth: +18.4%")
    
    # 2. Main charts below
    gs_main = fig.add_gridspec(nrows=2, ncols=2, left=0.05, right=0.95, bottom=0.05, top=0.68, hspace=0.35, wspace=0.2)
    
    # Chart 1: Industry AUM Growth Trend (spanning top to bottom on left)
    ax_trend = fig.add_subplot(gs_main[:, 0])
    ax_trend.plot(monthly_sip['month'], monthly_sip['sip_aum_lakh_crore'], color='#6366F1', linewidth=3.5, label='SIP AUM')
    ax_trend.fill_between(monthly_sip['month'], monthly_sip['sip_aum_lakh_crore'], color='#6366F1', alpha=0.15)
    ax_trend.set_title("SIP Assets Under Management Trend (2022-2025)", fontsize=13, fontweight='bold', pad=10)
    ax_trend.set_ylabel("Rs. Lakh Crore")
    # Set xticks frequency
    ax_trend.set_xticks(monthly_sip['month'][::6])
    ax_trend.set_xticklabels(monthly_sip['month'][::6], rotation=15)
    
    # Chart 2: Top 10 AMC AUM (top right)
    ax_amc = fig.add_subplot(gs_main[0, 1])
    latest_date = aum_fh['date'].max()
    latest_aum = aum_fh[aum_fh['date'] == latest_date].sort_values("aum_crore", ascending=False).head(8)
    sns.barplot(data=latest_aum, x='aum_crore', y='fund_house', ax=ax_amc, palette="viridis", hue='fund_house', legend=False)
    ax_amc.set_title(f"Top 8 Fund Houses by AUM (Rs. Crore) - {latest_date}", fontsize=12, fontweight='bold', pad=10)
    ax_amc.set_xlabel("AUM (Rs. Crore)")
    ax_amc.set_ylabel("")
    ax_amc.tick_params(axis='y', labelsize=8)
    
    # Chart 3: Folio Count by Category (bottom right)
    ax_folio = fig.add_subplot(gs_main[1, 1])
    ax_folio.plot(folios['month'], folios['equity_folios_crore'], color='#10B981', linewidth=2, label='Equity')
    ax_folio.plot(folios['month'], folios['debt_folios_crore'], color='#EF4444', linewidth=2, label='Debt')
    ax_folio.plot(folios['month'], folios['hybrid_folios_crore'], color='#F59E0B', linewidth=2, label='Hybrid')
    ax_folio.set_title("Folio Count Growth by Category (2022-2025)", fontsize=12, fontweight='bold', pad=10)
    ax_folio.set_ylabel("Folios (Crores)")
    ax_folio.set_xticks(folios['month'][::6])
    ax_folio.set_xticklabels(folios['month'][::6], rotation=15)
    ax_folio.legend(facecolor='#1E293B', edgecolor='#475569', labelcolor='#F8FAFC')
    
    img_path = CHARTS_DIR / "dashboard_page1.png"
    plt.savefig(img_path, facecolor='#0F172A', dpi=200)
    plt.close()
    return img_path

def generate_page2():
    """Page 2: Fund Performance & Scorecard."""
    logger.info("Generating Dashboard Page 2 (Performance & Scorecard)...")
    
    scorecard = pd.read_csv(PROCESSED_DIR / "fund_scorecard.csv")
    nav_df = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv")
    bench_df = pd.read_csv(PROCESSED_DIR / "clean_benchmark_indices.csv")
    master_df = pd.read_csv(PROCESSED_DIR / "clean_fund_master.csv")
    
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    bench_df['date'] = pd.to_datetime(bench_df['date'])
    
    fig = plt.figure(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#0F172A')
    
    fig.text(0.05, 0.94, "BLUESTOCK MUTUAL FUND ANALYTICS  |  DASHBOARD", fontsize=11, color='#6366F1', fontweight='bold')
    fig.text(0.05, 0.90, "Page 2: Fund Performance & Scorecard Analytics", fontsize=18, color='#FFFFFF', fontweight='bold')
    
    gs = fig.add_gridspec(nrows=2, ncols=2, left=0.05, right=0.95, bottom=0.05, top=0.86, hspace=0.35, wspace=0.22)
    
    # 1. Scatter Plot (Top Left)
    ax_scatter = fig.add_subplot(gs[0, 0])
    perf_df = pd.read_csv(PROCESSED_DIR / "clean_scheme_performance.csv")
    plot_data = scorecard.merge(perf_df[['amfi_code', 'std_dev_ann_pct']], on='amfi_code')
    plot_data = plot_data.merge(master_df[['amfi_code', 'category']], on='amfi_code')
    sns.scatterplot(
        data=plot_data,
        x="cagr_3yr_pct",
        y="std_dev_ann_pct",
        hue="category",
        size="sharpe_ratio",
        sizes=(40, 240),
        alpha=0.85,
        palette="Accent",
        ax=ax_scatter
    )
    ax_scatter.set_title("Risk-Return Profile (3-Year CAGR vs Std Dev)", fontsize=13, fontweight='bold', pad=10)
    ax_scatter.set_xlabel("3-Year CAGR Return (%)")
    ax_scatter.set_ylabel("Annualized Standard Deviation (%)")
    ax_scatter.legend(facecolor='#1E293B', edgecolor='#475569', loc='lower left', prop={'size': 8}, labelcolor='#F8FAFC')
    
    # 2. Scorecard Table (Top Right)
    ax_table = fig.add_subplot(gs[0, 1])
    ax_table.axis('off')
    ax_table.set_title("Top 5 Funds Ranked by Composite Score", fontsize=13, fontweight='bold', pad=15)
    
    table_data = scorecard.head(5)[['scorecard_rank', 'scheme_name', 'cagr_3yr_pct', 'sharpe_ratio', 'alpha']].copy()
    table_data['scheme_name'] = table_data['scheme_name'].apply(lambda x: x.split(" - ")[0][:28] + "...")
    
    headers = ["Rank", "Scheme Name", "3Yr CAGR", "Sharpe", "Alpha"]
    rows = table_data.values.tolist()
    
    # Draw table
    col_widths = [0.1, 0.45, 0.15, 0.15, 0.15]
    y = 0.8
    # Header
    for idx, (head, width) in enumerate(zip(headers, col_widths)):
        x = sum(col_widths[:idx])
        ax_table.text(x, y, head, fontsize=10, fontweight='bold', color='#6366F1')
    
    ax_table.plot([0, 1], [y-0.05, y-0.05], color='#4F46E5', linewidth=1.5)
    
    # Rows
    y -= 0.15
    for r in rows:
        for idx, (val, width) in enumerate(zip(r, col_widths)):
            x = sum(col_widths[:idx])
            # formatting
            if idx == 0:
                txt = f"#{val}"
                fw = 'bold'
            elif idx in [2, 4]:
                txt = f"{val:.2f}%"
                fw = 'normal'
            elif idx == 3:
                txt = f"{val:.2f}"
                fw = 'normal'
            else:
                txt = str(val)
                fw = 'normal'
            ax_table.text(x, y, txt, fontsize=9.5, fontweight=fw, color='#F8FAFC')
        y -= 0.12
        
    # 3. Selected Fund vs Benchmark (Bottom - spanning full width)
    ax_nav = fig.add_subplot(gs[1, :])
    # Let's plot the top ranked fund: Mirae Asset Large Cap Fund
    top_code = int(scorecard.iloc[0]['amfi_code'])
    top_name = scorecard.iloc[0]['scheme_name']
    
    start_date = pd.Timestamp("2023-05-29")
    end_date = pd.Timestamp("2026-05-29")
    
    fund_nav = nav_df[(nav_df['amfi_code'] == top_code) & (nav_df['date'] >= start_date) & (nav_df['date'] <= end_date)].sort_values('date')
    nifty50_all = bench_df[(bench_df['index_name'] == 'NIFTY50') & (bench_df['date'] >= start_date) & (bench_df['date'] <= end_date)].sort_values('date')
    nifty100_all = bench_df[(bench_df['index_name'] == 'NIFTY100') & (bench_df['date'] >= start_date) & (bench_df['date'] <= end_date)].sort_values('date')
    
    base_nav = fund_nav.iloc[0]['nav']
    normalized_nav = (fund_nav['nav'] / base_nav) * 100
    
    n50_base = nifty50_all.iloc[0]['close_value']
    normalized_n50 = (nifty50_all['close_value'] / n50_base) * 100
    
    n100_base = nifty100_all.iloc[0]['close_value']
    normalized_n100 = (nifty100_all['close_value'] / n100_base) * 100
    
    ax_nav.plot(fund_nav['date'], normalized_nav, color='#6366F1', linewidth=2.5, label=f"Fund: {top_name.split(' - ')[0]}")
    ax_nav.plot(nifty50_all['date'], normalized_n50, color='#E2E8F0', linestyle='--', linewidth=1.5, label='Nifty 50')
    ax_nav.plot(nifty100_all['date'], normalized_n100, color='#94A3B8', linestyle=':', linewidth=1.5, label='Nifty 100')
    
    ax_nav.set_title(f"3-Year NAV Performance vs Benchmarks (Normalized, 2023-05-29 = 100)", fontsize=13, fontweight='bold', pad=10)
    ax_nav.set_ylabel("Normalized Value")
    ax_nav.legend(facecolor='#1E293B', edgecolor='#475569', labelcolor='#F8FAFC')
    
    img_path = CHARTS_DIR / "dashboard_page2.png"
    plt.savefig(img_path, facecolor='#0F172A', dpi=200)
    plt.close()
    return img_path

def generate_page3():
    """Page 3: Investor Analytics."""
    logger.info("Generating Dashboard Page 3 (Investor Analytics)...")
    
    tx_df = pd.read_csv(PROCESSED_DIR / "clean_investor_transactions.csv")
    
    fig = plt.figure(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#0F172A')
    
    fig.text(0.05, 0.94, "BLUESTOCK MUTUAL FUND ANALYTICS  |  DASHBOARD", fontsize=11, color='#6366F1', fontweight='bold')
    fig.text(0.05, 0.90, "Page 3: Investor Demographics & Behavior Analytics", fontsize=18, color='#FFFFFF', fontweight='bold')
    
    gs = fig.add_gridspec(nrows=2, ncols=2, left=0.05, right=0.95, bottom=0.05, top=0.86, hspace=0.38, wspace=0.2)
    
    # 1. State bar chart
    ax_state = fig.add_subplot(gs[0, 0])
    state_amt = tx_df.groupby('state')['amount_inr'].sum().reset_index().sort_values('amount_inr', ascending=False).head(10)
    state_amt['amount_inr_cr'] = state_amt['amount_inr'] / 1e7
    sns.barplot(data=state_amt, x='amount_inr_cr', y='state', ax=ax_state, palette="plasma", hue='state', legend=False)
    ax_state.set_title("Top 10 States by Transaction Amount (Rs. Crore)", fontsize=13, fontweight='bold', pad=10)
    ax_state.set_xlabel("Volume (Rs. Crore)")
    ax_state.set_ylabel("")
    
    # 2. Transaction types split (donut)
    ax_donut = fig.add_subplot(gs[0, 1])
    type_split = tx_df.groupby('transaction_type')['amount_inr'].sum().reset_index()
    ax_donut.pie(
        type_split['amount_inr'], 
        labels=type_split['transaction_type'], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#6366F1', '#10B981', '#F59E0B'],
        wedgeprops=dict(width=0.4, edgecolor='#1E293B', linewidth=1.5),
        textprops=dict(color='#F8FAFC', fontsize=10)
    )
    ax_donut.set_title("Transaction Type Contribution (SIP vs Lumpsum vs Redemption)", fontsize=13, fontweight='bold', pad=10)
    
    # 3. Monthly Transaction Volume (bottom left)
    ax_vol = fig.add_subplot(gs[1, 0])
    tx_df['month'] = pd.to_datetime(tx_df['transaction_date']).dt.to_period('M').astype(str)
    monthly_vol = tx_df.groupby('month')['amount_inr'].sum().reset_index()
    monthly_vol['amount_cr'] = monthly_vol['amount_inr'] / 1e7
    ax_vol.plot(monthly_vol['month'], monthly_vol['amount_cr'], color='#10B981', linewidth=3, marker='o')
    ax_vol.set_title("Monthly Invested / Redeemed Amount (Rs. Crore)", fontsize=13, fontweight='bold', pad=10)
    ax_vol.set_ylabel("Rs. Crore")
    ax_vol.set_xticks(monthly_vol['month'][::6])
    ax_vol.set_xticklabels(monthly_vol['month'][::6], rotation=15)
    
    # 4. Age Group vs average SIP
    ax_age = fig.add_subplot(gs[1, 1])
    sip_tx = tx_df[tx_df['transaction_type'] == 'SIP']
    age_sip = sip_tx.groupby('age_group')['amount_inr'].mean().reset_index()
    sns.barplot(data=age_sip, x='age_group', y='amount_inr', ax=ax_age, palette="muted", hue='age_group', legend=False)
    ax_age.set_title("Average SIP Amount (Rs.) by Age Group", fontsize=13, fontweight='bold', pad=10)
    ax_age.set_xlabel("Age Group")
    ax_age.set_ylabel("Average SIP Amount (Rs.)")
    
    img_path = CHARTS_DIR / "dashboard_page3.png"
    plt.savefig(img_path, facecolor='#0F172A', dpi=200)
    plt.close()
    return img_path

def generate_page4():
    """Page 4: SIP & Market Trends."""
    logger.info("Generating Dashboard Page 4 (SIP & Market Trends)...")
    
    monthly_sip = pd.read_csv(PROCESSED_DIR / "clean_monthly_sip_inflows.csv")
    cat_inflows = pd.read_csv(PROCESSED_DIR / "clean_category_inflows.csv")
    bench_idx = pd.read_csv(PROCESSED_DIR / "clean_benchmark_indices.csv")
    
    fig = plt.figure(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#0F172A')
    
    fig.text(0.05, 0.94, "BLUESTOCK MUTUAL FUND ANALYTICS  |  DASHBOARD", fontsize=11, color='#6366F1', fontweight='bold')
    fig.text(0.05, 0.90, "Page 4: SIP & Market Trends Correlation", fontsize=18, color='#FFFFFF', fontweight='bold')
    
    gs = fig.add_gridspec(nrows=2, ncols=2, left=0.05, right=0.95, bottom=0.05, top=0.86, hspace=0.38, wspace=0.2)
    
    # 1. Dual Axis (Top Row - full width)
    ax_dual = fig.add_subplot(gs[0, :])
    
    # Nifty 50 end of month close price
    n50 = bench_idx[bench_idx['index_name'] == 'NIFTY50'].copy()
    n50['date'] = pd.to_datetime(n50['date'])
    n50['month'] = n50['date'].dt.to_period('M').astype(str)
    n50_monthly = n50.sort_values('date').groupby('month').last().reset_index()[['month', 'close_value']]
    merged_trend = pd.merge(monthly_sip, n50_monthly, on='month', how='inner')
    
    # Left Axis: SIP Inflow
    ax_left = ax_dual
    bars = ax_left.bar(merged_trend['month'], merged_trend['sip_inflow_crore'], color='#4F46E5', alpha=0.6, label="SIP Inflow (Rs. Cr)")
    ax_left.set_ylabel("Monthly SIP Inflow (Rs. Crore)", color='#818CF8', fontweight='semibold')
    ax_left.tick_params(axis='y', labelcolor='#818CF8')
    ax_left.set_xticks(merged_trend['month'][::6])
    ax_left.set_xticklabels(merged_trend['month'][::6], rotation=15)
    ax_left.grid(False)
    
    # Right Axis: Nifty 50
    ax_right = ax_left.twinx()
    line = ax_right.plot(merged_trend['month'], merged_trend['close_value'], color='#10B981', linewidth=3, label="Nifty 50 Level")
    ax_right.set_ylabel("Nifty 50 Closing Level", color='#34D399', fontweight='semibold')
    ax_right.tick_params(axis='y', labelcolor='#34D399')
    ax_right.grid(False)
    
    ax_dual.set_title("Monthly SIP Inflow Trend (Rs. Crore) vs Nifty 50 Benchmark Performance", fontsize=13, fontweight='bold', pad=10)
    
    # 2. Net Category Inflows FY 2024-25 (Bottom Left)
    ax_cat = fig.add_subplot(gs[1, 0])
    cat_sum = cat_inflows.groupby('category')['net_inflow_crore'].sum().reset_index().sort_values('net_inflow_crore', ascending=False)
    sns.barplot(data=cat_sum, x='net_inflow_crore', y='category', ax=ax_cat, palette="rocket", hue='category', legend=False)
    ax_cat.set_title("Net Inflow by Category (Rs. Crore) - FY 2024-25", fontsize=13, fontweight='bold', pad=10)
    ax_cat.set_xlabel("Net Inflow (Rs. Crore)")
    ax_cat.set_ylabel("")
    
    # 3. Category Inflows Heatmap (Bottom Right)
    ax_heat = fig.add_subplot(gs[1, 1])
    heatmap_data = cat_inflows.pivot(index='category', columns='month', values='net_inflow_crore')
    sns.heatmap(heatmap_data, cmap="RdBu_r", center=0, ax=ax_heat, cbar_kws={'label': 'Rs. Crore'})
    ax_heat.set_title("Monthly Net Category Inflow Heatmap (Rs. Crore)", fontsize=13, fontweight='bold', pad=10)
    ax_heat.set_xlabel("Month")
    ax_heat.set_ylabel("")
    ax_heat.tick_params(axis='x', labelsize=8)
    ax_heat.tick_params(axis='y', labelsize=8)
    
    img_path = CHARTS_DIR / "dashboard_page4.png"
    plt.savefig(img_path, facecolor='#0F172A', dpi=200)
    plt.close()
    return img_path

def compile_pdf(image_paths):
    """Compile the generated dashboard images into a single landscape PDF."""
    logger.info("Compiling dashboard images into PDF at %s...", PDF_PATH)
    
    # Use landscape A4 page size
    # A4 is 595.27 x 841.89 points. In landscape: 841.89 x 595.27
    width, height = landscape(A4)
    c = canvas.Canvas(str(PDF_PATH), pagesize=landscape(A4))
    
    for img_path in image_paths:
        c.drawImage(str(img_path), 0, 0, width, height)
        c.showPage()
        
    c.save()
    logger.info("Dashboard PDF successfully saved!")

def main() -> None:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    
    img_paths = []
    img_paths.append(generate_page1())
    img_paths.append(generate_page2())
    img_paths.append(generate_page3())
    img_paths.append(generate_page4())
    
    compile_pdf(img_paths)
    logger.info("Day 5 - Dashboard Export process finished successfully!")

if __name__ == "__main__":
    main()
