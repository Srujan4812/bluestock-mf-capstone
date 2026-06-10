import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import contextlib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Setup Page Configuration
st.set_page_config(
    page_title="Bluestock Mutual Fund Analytics Workspace",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS Injection for High-End Glassmorphism & Typography)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Background & Typography */
    .stApp {
        background-color: #0B0F19;
        color: #F1F5F9;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Gradient Headers */
    .gradient-header {
        background: linear-gradient(135deg, #6366F1 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 20px;
    }
    
    /* SideBar Custom Style */
    [data-testid="stSidebar"] {
        background-color: #0E1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Interactive Card container */
    .premium-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .premium-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* KPI Card styling */
    .kpi-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.5) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    .kpi-container:hover {
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15);
    }
    .kpi-title {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #FFFFFF;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .kpi-delta {
        font-size: 13px;
        font-weight: 500;
    }
    
    /* Recommender Cards styling */
    .recommender-card {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1.5px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    .recommender-card:hover {
        border-color: rgba(16, 185, 129, 0.6);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);
    }
    .recommender-rank {
        background-color: #6366F1;
        color: white;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
        padding: 2px 8px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .recommender-name {
        font-size: 15px;
        font-weight: 700;
        color: white;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

# Check and dynamically generate processed data files if missing (e.g., when deployed to Streamlit Cloud)
required_files = [
    "clean_fund_master.csv", 
    "fund_scorecard.csv", 
    "alpha_beta.csv", 
    "var_cvar_report.csv", 
    "sector_hhi.csv", 
    "cohort_analysis.csv"
]
missing_files = [f for f in required_files if not (PROCESSED_DIR / f).exists()]
if missing_files:
    import sys
    
    # Ensure directories exist
    (ROOT_DIR / "data" / "db").mkdir(parents=True, exist_ok=True)
    (ROOT_DIR / "reports" / "charts").mkdir(parents=True, exist_ok=True)
    
    # Run pipelines directly in-process
    sys.path.append(str(ROOT_DIR / "scripts"))
    import etl_pipeline
    import compute_metrics
    import advanced_analytics
    
    etl_pipeline.run()
    compute_metrics.main()
    advanced_analytics.main()

# Helper function to load cleaned CSVs
@st.cache_data
def load_csv_data(filename):
    path = PROCESSED_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@contextlib.contextmanager
def get_db_connection():
    db_path = ROOT_DIR / "data" / "db" / "bluestock_mf.db"
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

# Load common datasets
fund_master = load_csv_data("clean_fund_master.csv")
scorecard = load_csv_data("fund_scorecard.csv")
alpha_beta = load_csv_data("alpha_beta.csv")
scheme_perf = load_csv_data("clean_scheme_performance.csv")
var_report = load_csv_data("var_cvar_report.csv")
sector_hhi = load_csv_data("sector_hhi.csv")
cohort_analysis = load_csv_data("cohort_analysis.csv")

# Sidebar Branding
st.sidebar.markdown("<div style='padding: 20px 0; text-align: center;'><h2 style='background: linear-gradient(135deg, #6366F1 0%, #10B981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 26px; margin: 0;'>BLUESTOCK</h2><p style='color: #64748B; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; margin: 5px 0 0 0;'>Mutual Fund Analytics</p></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Page Selector
page = st.sidebar.radio(
    "NAVIGATION HUB",
    ["Industry Overview", "Fund Performance", "Investor Analytics", "SIP & Market Trends", "Monte Carlo Projections", "Portfolio Optimization"],
    key="nav_radio"
)

# Shared plotly formatting helper
def update_plotly_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Outfit',
        font_color='#94A3B8',
        title_font_color='#FFFFFF',
        title_font_size=16,
        title_font_family='Outfit',
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.6)',
            bordercolor='rgba(255,255,255,0.05)',
            borderwidth=1,
            font=dict(size=10, color='#E2E8F0')
        ),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    fig.update_xaxes(showgrid=False, color='#475569', linecolor='rgba(255,255,255,0.05)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', color='#475569', linecolor='rgba(255,255,255,0.05)')
    return fig

# ----------------- PAGE 1: INDUSTRY OVERVIEW -----------------
if page == "Industry Overview":
    st.markdown("<h1 class='gradient-header'>📈 Industry Overview</h1>", unsafe_allow_html=True)
    st.markdown("Track macro-level assets under management (AUM), SIP inflow rates, and mutual fund folio distribution across India.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    monthly_sip = load_csv_data("clean_monthly_sip_inflows.csv")
    aum_fh = load_csv_data("clean_aum_by_fund_house.csv")
    folios = load_csv_data("clean_industry_folio_count.csv")
    
    latest_sip = monthly_sip.iloc[-1] if not monthly_sip.empty else None
    latest_folio = folios.iloc[-1] if not folios.empty else None
    
    # Premium KPI Layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="kpi-container">
            <div class="kpi-title">Total Industry AUM</div>
            <div class="kpi-value">₹81.0 L Cr</div>
            <div class="kpi-delta" style="color: #10B981;">▲ As of Dec 2025</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        val = f"₹{latest_sip['sip_inflow_crore']:,.0f} Cr" if latest_sip is not None else "₹31,002 Cr"
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Monthly SIP Inflow</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta" style="color: #10B981;">▲ Active Record Inflow</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        val = f"{latest_folio['total_folios_crore']:.2f} Cr" if latest_folio is not None else "26.12 Cr"
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Total Folios</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta" style="color: #6366F1;">78% Equity Accounts</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        val = f"{latest_sip['active_sip_accounts_crore']:.2f} Cr" if latest_sip is not None else "9.35 Cr"
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Active SIP Accounts</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta" style="color: #10B981;">▲ YoY: +18.4%</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graph Section
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Industry Assets Under Management (AUM) Growth Trend")
    if not monthly_sip.empty:
        fig_aum = px.area(
            monthly_sip,
            x="month",
            y="sip_aum_lakh_crore",
            labels={"sip_aum_lakh_crore": "SIP AUM (Rs. Lakh Crore)", "month": "Month"},
            template="plotly_dark",
            color_discrete_sequence=["#6366F1"]
        )
        fig_aum.update_traces(line=dict(width=3), fillcolor="rgba(99, 102, 241, 0.15)")
        fig_aum = update_plotly_theme(fig_aum)
        st.plotly_chart(fig_aum, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Top Fund Houses by AUM (Dec 2025)")
        if not aum_fh.empty:
            latest_date = aum_fh['date'].max()
            latest_aum = aum_fh[aum_fh['date'] == latest_date].sort_values("aum_crore", ascending=False).head(8)
            
            fig_bar = px.bar(
                latest_aum,
                x="aum_crore",
                y="fund_house",
                orientation="h",
                color="aum_crore",
                color_continuous_scale="Purples",
                labels={"aum_crore": "AUM (Rs. Crore)", "fund_house": "AMC"},
                template="plotly_dark"
            )
            fig_bar = update_plotly_theme(fig_bar)
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
            
    with col_right:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Folio Count Growth by Category")
        if not folios.empty:
            folios_melted = folios.melt(
                id_vars=["month"],
                value_vars=["equity_folios_crore", "debt_folios_crore", "hybrid_folios_crore"],
                var_name="Category",
                value_name="Folios (Crore)"
            )
            folios_melted['Category'] = folios_melted['Category'].str.replace('_folios_crore', '').str.capitalize()
            
            fig_folio = px.line(
                folios_melted,
                x="month",
                y="Folios (Crore)",
                color="Category",
                color_discrete_map={"Equity": "#10B981", "Debt": "#EF4444", "Hybrid": "#F59E0B"},
                template="plotly_dark"
            )
            fig_folio = update_plotly_theme(fig_folio)
            fig_folio.update_traces(line=dict(width=2.5))
            st.plotly_chart(fig_folio, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- PAGE 2: FUND PERFORMANCE -----------------
elif page == "Fund Performance":
    st.markdown("<h1 class='gradient-header'>🏆 Fund Performance & Risk-Adjusted Scoring</h1>", unsafe_allow_html=True)
    st.markdown("Analyze mutual fund returns on a risk-adjusted basis, evaluate tracking errors against benchmarks, and discover top recommendation models.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dynamic top-level KPIs computed from scorecard
    if not scorecard.empty:
        top_cagr_row = scorecard.loc[scorecard['cagr_3yr_pct'].idxmax()]
        top_sharpe_row = scorecard.loc[scorecard['sharpe_ratio'].idxmax()]
        top_alpha_row = scorecard.loc[scorecard['alpha'].idxmax()]
        lowest_exp_row = scorecard.loc[scorecard['expense_ratio_pct'].idxmin()]
        
        kcol1, kcol2, kcol3, kcol4 = st.columns(4)
        with kcol1:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">Top CAGR Return</div>
                <div class="kpi-value">{top_cagr_row['cagr_3yr_pct']:.1f}%</div>
                <div class="kpi-delta" style="color: #10B981;">🏆 {top_cagr_row['scheme_name'].split(" - ")[0][:28]}</div>
            </div>
            """, unsafe_allow_html=True)
        with kcol2:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">Highest Sharpe Ratio</div>
                <div class="kpi-value">{top_sharpe_row['sharpe_ratio']:.2f}</div>
                <div class="kpi-delta" style="color: #6366F1;">💎 {top_sharpe_row['scheme_name'].split(" - ")[0][:28]}</div>
            </div>
            """, unsafe_allow_html=True)
        with kcol3:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">Max Alpha (vs Bench)</div>
                <div class="kpi-value">+{top_alpha_row['alpha']:.1f}%</div>
                <div class="kpi-delta" style="color: #10B981;">⚡ {top_alpha_row['scheme_name'].split(" - ")[0][:28]}</div>
            </div>
            """, unsafe_allow_html=True)
        with kcol4:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">Lowest Expense Ratio</div>
                <div class="kpi-value">{lowest_exp_row['expense_ratio_pct']:.2f}%</div>
                <div class="kpi-delta" style="color: #6366F1;">🌿 {lowest_exp_row['scheme_name'].split(" - ")[0][:28]}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Sidebar Filters
    st.sidebar.markdown("### FILTER CONTROLS")
    selected_amcs = st.sidebar.multiselect("Select AMC / Fund Houses", options=fund_master['fund_house'].unique())
    selected_categories = st.sidebar.multiselect("Select Asset Categories", options=fund_master['category'].unique())
    selected_plans = st.sidebar.multiselect("Select Plan Types", options=fund_master['plan'].unique())
    
    # Filter Scorecard Data
    filtered_scorecard = scorecard.copy()
    if selected_amcs:
        amfi_codes = fund_master[fund_master['fund_house'].isin(selected_amcs)]['amfi_code']
        filtered_scorecard = filtered_scorecard[filtered_scorecard['amfi_code'].isin(amfi_codes)]
    if selected_categories:
        amfi_codes = fund_master[fund_master['category'].isin(selected_categories)]['amfi_code']
        filtered_scorecard = filtered_scorecard[filtered_scorecard['amfi_code'].isin(amfi_codes)]
    if selected_plans:
        amfi_codes = fund_master[fund_master['plan'].isin(selected_plans)]['amfi_code']
        filtered_scorecard = filtered_scorecard[filtered_scorecard['amfi_code'].isin(amfi_codes)]
        
    # Split layout: Main performance charts and inline recommender
    col_main, col_rec = st.columns([7, 3])
    
    with col_main:
        # Scatter Plot Return vs Risk
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Risk-Return Profile (3-Year CAGR vs Standard Deviation)")
        
        # Merge std_dev_ann_pct and category
        plot_data = filtered_scorecard.merge(fund_master[['amfi_code', 'category', 'fund_house']], on='amfi_code')
        if 'std_dev_ann_pct' not in plot_data.columns and not scheme_perf.empty:
            plot_data = plot_data.merge(scheme_perf[['amfi_code', 'std_dev_ann_pct']], on='amfi_code')
            
        if not plot_data.empty:
            # Map size parameter safely (clip at minimum to prevent Plotly errors on negative Sharpe Ratios)
            plot_data['sharpe_ratio_size'] = plot_data['sharpe_ratio'].clip(lower=0.1) * 10 + 5
            
            fig_scatter = px.scatter(
                plot_data,
                x="cagr_3yr_pct",
                y="std_dev_ann_pct",
                color="category",
                hover_name="scheme_name",
                size="sharpe_ratio_size",
                color_discrete_sequence=px.colors.qualitative.Bold,
                labels={
                    "cagr_3yr_pct": "3-Year CAGR Return (%)",
                    "std_dev_ann_pct": "Annualized Standard Deviation (%)",
                    "sharpe_ratio": "Sharpe Ratio"
                },
                hover_data={
                    "cagr_3yr_pct": ":.2f",
                    "std_dev_ann_pct": ":.2f",
                    "sharpe_ratio": ":.2f",
                    "alpha": ":.2f",
                    "sharpe_ratio_size": False
                },
                template="plotly_dark"
            )
            fig_scatter = update_plotly_theme(fig_scatter)
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No data matches selected filters for scatter plot.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_rec:
        st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.subheader("💡 Fund Recommender")
        st.markdown("Match top-performing funds by Sharpe ratio within SEBI risk grades.")
        
        # Risk Appetite Input
        risk_app = st.selectbox("Select Your Risk Appetite", ["Low", "Moderate", "High"])
        
        if risk_app == 'Low':
            target_risks = ['Low', 'Moderate']
        elif risk_app == 'Moderate':
            target_risks = ['Moderately High', 'High']
        else: # High
            target_risks = ['Very High']
            
        # Recommend Logic
        rec_df = scorecard.merge(fund_master[['amfi_code', 'risk_category', 'category', 'sub_category']], on='amfi_code')
        rec_df = rec_df[rec_df['risk_category'].isin(target_risks)]
        recommended = rec_df.sort_values(by='sharpe_ratio', ascending=False).head(3)
        
        if not recommended.empty:
            for idx, r in recommended.iterrows():
                st.markdown(f"""
                <div class="recommender-card">
                    <span class="recommender-rank">RANK #{r['scorecard_rank']}</span>
                    <div class="recommender-name">{r['scheme_name'].split(" - ")[0]}</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-bottom: 10px;">
                        Category: {r['category']} • Risk: {r['risk_category']}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; color: #F1F5F9;">
                        <span>CAGR: <span style="color: #10B981;">{r['cagr_3yr_pct']:.2f}%</span></span>
                        <span>Sharpe: <span style="color: #6366F1;">{r['sharpe_ratio']:.2f}</span></span>
                        <span>Alpha: <span style="color: #8B5CF6;">{r['alpha']:.2f}%</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recommendations found for this profile.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Scorecard Table
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Composite Fund Scorecard & Ranks")
    st.markdown("Weighted ranking evaluation: CAGR (30%) + Sharpe (25%) + Alpha (20%) + Expense Ratio (15%) + Max Drawdown (10%).")
    if not filtered_scorecard.empty:
        display_cols = ['scorecard_rank', 'scheme_name', 'cagr_3yr_pct', 'sharpe_ratio', 'alpha', 'expense_ratio_pct', 'max_drawdown_pct', 'score']
        table_df = filtered_scorecard[display_cols].rename(columns={
            'scorecard_rank': 'Rank',
            'scheme_name': 'Scheme Name',
            'cagr_3yr_pct': '3Yr CAGR (%)',
            'sharpe_ratio': 'Sharpe Ratio',
            'alpha': 'Alpha (%)',
            'expense_ratio_pct': 'Expense Ratio (%)',
            'max_drawdown_pct': 'Max Drawdown (%)',
            'score': 'Composite Score'
        })
        st.dataframe(table_df.style.format({
            '3Yr CAGR (%)': '{:.2f}%',
            'Sharpe Ratio': '{:.2f}',
            'Alpha (%)': '{:.2f}%',
            'Expense Ratio (%)': '{:.2f}%',
            'Max Drawdown (%)': '{:.2f}%',
            'Composite Score': '{:.2f}'
        }).background_gradient(subset=['Composite Score'], cmap='Purples'), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Fund Detail & Benchmark comparison
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Detailed Benchmark Analysis & Trailing NAV")
    selected_scheme = st.selectbox("Select a Scheme for NAV Analysis", options=scorecard['scheme_name'].sort_values().unique(), key="performance_select")
    
    if selected_scheme:
        fund_row = scorecard[scorecard['scheme_name'] == selected_scheme].iloc[0]
        code = int(fund_row['amfi_code'])
        
        try:
            with get_db_connection() as conn:
                fund_nav = pd.read_sql("SELECT date, nav FROM nav_history WHERE amfi_code = ? ORDER BY date", conn, params=(code,))
                fund_nav['date'] = pd.to_datetime(fund_nav['date'])
                benchmarks = pd.read_sql("SELECT date, index_name, close_value FROM benchmark_indices ORDER BY date", conn)
                benchmarks['date'] = pd.to_datetime(benchmarks['date'])
                
            fund_nav = fund_nav[fund_nav['date'] >= '2023-05-29']
            benchmarks = benchmarks[benchmarks['date'] >= '2023-05-29']
            bench_pivot = benchmarks.pivot(index='date', columns='index_name', values='close_value').reset_index()
            compare_df = pd.merge(fund_nav, bench_pivot, on='date', how='inner').sort_values('date')
            
            if not compare_df.empty:
                compare_df['Fund Normalized'] = (compare_df['nav'] / compare_df.iloc[0]['nav']) * 100
                compare_df['Nifty 50 Normalized'] = (compare_df['NIFTY50'] / compare_df.iloc[0]['NIFTY50']) * 100
                compare_df['Nifty 100 Normalized'] = (compare_df['NIFTY100'] / compare_df.iloc[0]['NIFTY100']) * 100
                
                fig_nav = go.Figure()
                fig_nav.add_trace(go.Scatter(x=compare_df['date'], y=compare_df['Fund Normalized'], name="Fund (Normalized)", line=dict(color="#6366F1", width=3)))
                fig_nav.add_trace(go.Scatter(x=compare_df['date'], y=compare_df['Nifty 50 Normalized'], name="Nifty 50", line=dict(color="#E2E8F0", width=1.5, dash='dash')))
                fig_nav.add_trace(go.Scatter(x=compare_df['date'], y=compare_df['Nifty 100 Normalized'], name="Nifty 100", line=dict(color="#94A3B8", width=1.5, dash='dot')))
                
                fig_nav.update_layout(title=f"{selected_scheme} Normalized Trend vs Benchmarks (2023-05-29 = 100)", template="plotly_dark")
                fig_nav = update_plotly_theme(fig_nav)
                st.plotly_chart(fig_nav, use_container_width=True)
                
                # Fetch beta dynamically
                beta_val = "N/A"
                if not alpha_beta.empty:
                    ab_row = alpha_beta[alpha_beta['amfi_code'] == code]
                    if not ab_row.empty:
                        beta_val = f"{ab_row.iloc[0]['beta']:.2f}"
                
                # Show key stats in glassmorphic cards
                scol1, scol2, scol3, scol4, scol5 = st.columns(5)
                with scol1:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">3Yr CAGR</div>
                        <div class="kpi-value" style="font-size: 24px; color: #10B981;">{fund_row['cagr_3yr_pct']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with scol2:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Sharpe Ratio</div>
                        <div class="kpi-value" style="font-size: 24px; color: #6366F1;">{fund_row['sharpe_ratio']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with scol3:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Alpha (vs Nifty 100)</div>
                        <div class="kpi-value" style="font-size: 24px; color: #10B981;">{fund_row['alpha']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with scol4:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Beta (vs Nifty 100)</div>
                        <div class="kpi-value" style="font-size: 24px; color: #F59E0B;">{beta_val}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with scol5:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Max Drawdown</div>
                        <div class="kpi-value" style="font-size: 24px; color: #EF4444;">{fund_row['max_drawdown_pct']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading comparison chart: {e}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Advanced Risk metrics: VaR & HHI grids side-by-side
    col_var, col_hhi = st.columns(2)
    with col_var:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Value at Risk (VaR 95% & CVaR 95%)")
        st.markdown("95% confidence threshold loss and tail expectation under adverse markets.")
        if not var_report.empty:
            display_var = var_report.sort_values(by='var_95_pct', ascending=False).head(10).rename(columns={
                'scheme_name': 'Scheme Name',
                'var_95_pct': 'Daily VaR (95%)',
                'cvar_95_pct': 'Daily CVaR (95%)'
            })
            st.dataframe(display_var[['Scheme Name', 'Daily VaR (95%)', 'Daily CVaR (95%)']].style.format({
                'Daily VaR (95%)': '{:.2f}%',
                'Daily CVaR (95%)': '{:.2f}%'
            }), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_hhi:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Portfolio Sector HHI Index")
        st.markdown("Herfindahl-Hirschman Index of sector concentration (higher HHI = more concentrated).")
        if not sector_hhi.empty:
            display_hhi = sector_hhi.sort_values(by='sector_hhi', ascending=False).head(10).rename(columns={
                'scheme_name': 'Scheme Name',
                'sector_hhi': 'Sector HHI Index'
            })
            st.dataframe(display_hhi[['Scheme Name', 'Sector HHI Index']].style.format({
                'Sector HHI Index': '{:.4f}'
            }), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Financial Glossary & Formula Guide
    with st.expander("📚 Financial Metrics Glossary & Reference Guide"):
        st.markdown("""
        ### Understanding Risk & Return Metrics
        To help you evaluate mutual funds on our platform, here is a breakdown of the key mathematical formulas and terminology used:
        
        *   **CAGR (Compound Annual Growth Rate)**: The geometric progression ratio that provides a constant rate of return over the 3-year time period.
            $$\\text{CAGR} = \\left( \\frac{\\text{End NAV}}{\\text{Start NAV}} \\right)^{\\frac{1}{3}} - 1$$
        *   **Standard Deviation (Volatility)**: Annualized standard deviation of daily returns, indicating historical fund dispersion. Higher values denote higher pricing instability.
            $$\\sigma_{\\text{ann}} = \\sigma_{\\text{daily}} \\times \\sqrt{252} \\times 100$$
        *   **Sharpe Ratio**: A measure of risk-adjusted excess return per unit of volatility (assuming a risk-free rate $R_f = 6.5\\%$).
            $$\\text{Sharpe} = \\frac{R_p - R_f}{\\sigma_p}$$
        *   **Alpha (OLS Jensen's Alpha)**: The return of the fund in excess of the Nifty 100 index return, after adjusting for market beta risk. Shows fund manager value-add.
            $$\\alpha = R_p - [R_f + \\beta_p (R_m - R_f)]$$
        *   **Beta**: The systematic risk coefficient representing a fund's volatility relative to the broader market index (Nifty 100).
        *   **Max Drawdown**: The maximum peak-to-trough drop in a fund's NAV, highlighting historical capital downside vulnerability.
        *   **Value at Risk (VaR 95%)**: The daily potential portfolio loss that will not be exceeded with 95% statistical confidence.
        *   **Conditional Value at Risk (CVaR 95%)**: The expected loss on days where the VaR threshold is breached (extreme tail loss).
        *   **Sector HHI (Herfindahl-Hirschman Index)**: Measures portfolio concentration across SEBI sectors.
            $$\\text{HHI} = \\sum_{i=1}^{n} s_i^2$$
            *(where $s_i$ is the percentage share of sector $i$. HHI < 0.15 is highly diversified; > 0.25 is concentrated).*
        """, unsafe_allow_html=True)

# ----------------- PAGE 3: INVESTOR ANALYTICS -----------------
elif page == "Investor Analytics":
    st.markdown("<h1 class='gradient-header'>👥 Investor Analytics & Segmentation</h1>", unsafe_allow_html=True)
    st.markdown("Analyze retail transaction amounts, geographical split across states, and acquisition cohorts.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    tx_df = load_csv_data("clean_investor_transactions.csv")
    
    st.sidebar.markdown("### DEMOGRAPHIC FILTERS")
    states = st.sidebar.multiselect("Select State Location", options=tx_df['state'].unique() if not tx_df.empty else [])
    tiers = st.sidebar.multiselect("Select City Tier", options=tx_df['city_tier'].unique() if not tx_df.empty else [])
    age_groups = st.sidebar.multiselect("Select Age Brackets", options=tx_df['age_group'].unique() if not tx_df.empty else [])
    
    filtered_tx = tx_df.copy()
    if states:
        filtered_tx = filtered_tx[filtered_tx['state'].isin(states)]
    if tiers:
        filtered_tx = filtered_tx[filtered_tx['city_tier'].isin(tiers)]
    if age_groups:
        filtered_tx = filtered_tx[filtered_tx['age_group'].isin(age_groups)]
        
    if not filtered_tx.empty:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.subheader("Transaction Volume by State")
            state_amt = filtered_tx.groupby('state')['amount_inr'].sum().reset_index().sort_values('amount_inr', ascending=False)
            state_amt['amount_inr_cr'] = state_amt['amount_inr'] / 1e7
            fig_state = px.bar(
                state_amt,
                x="amount_inr_cr",
                y="state",
                orientation="h",
                color="amount_inr_cr",
                color_continuous_scale="Viridis",
                labels={"amount_inr_cr": "Total volume (Rs. Crore)", "state": "State"},
                template="plotly_dark"
            )
            fig_state = update_plotly_theme(fig_state)
            fig_state.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
            st.plotly_chart(fig_state, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_t2:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.subheader("Transaction Types Split")
            type_split = filtered_tx.groupby('transaction_type')['amount_inr'].sum().reset_index()
            fig_donut = px.pie(
                type_split,
                names="transaction_type",
                values="amount_inr",
                hole=0.45,
                color_discrete_sequence=["#6366F1", "#10B981", "#EF4444"],
                template="plotly_dark"
            )
            fig_donut = update_plotly_theme(fig_donut)
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Monthly Transaction Volume Trend")
        filtered_tx['month'] = pd.to_datetime(filtered_tx['transaction_date']).dt.to_period('M').astype(str)
        monthly_vol = filtered_tx.groupby('month')['amount_inr'].sum().reset_index()
        monthly_vol['amount_cr'] = monthly_vol['amount_inr'] / 1e7
        fig_vol = px.line(
            monthly_vol,
            x="month",
            y="amount_cr",
            labels={"amount_cr": "Total Volume (Rs. Crore)", "month": "Month"},
            template="plotly_dark"
        )
        fig_vol = update_plotly_theme(fig_vol)
        fig_vol.update_traces(line=dict(color="#10B981", width=3))
        st.plotly_chart(fig_vol, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col_box, col_cohort = st.columns([1, 1])
        with col_box:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.subheader("SIP Transaction Size by Age Group")
            sip_tx = filtered_tx[filtered_tx['transaction_type'] == 'SIP']
            if not sip_tx.empty:
                fig_box = px.box(
                    sip_tx,
                    x="age_group",
                    y="amount_inr",
                    color="age_group",
                    labels={"amount_inr": "SIP Amount (INR)", "age_group": "Age Group"},
                    template="plotly_dark"
                )
                fig_box = update_plotly_theme(fig_box)
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("No SIP transaction records found.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_cohort:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.subheader("Acquisition Cohort Metrics")
            st.markdown("Comparison metrics for 2024 vs 2025 investor acquisition cohorts.")
            if not cohort_analysis.empty:
                display_cohort = cohort_analysis.rename(columns={
                    'cohort': 'Cohort',
                    'total_investors': 'Total Investors',
                    'total_net_investment_cr': 'Net Investment (Cr)',
                    'avg_sip_amount_inr': 'Avg SIP (Rs.)',
                    'top_fund_category': 'Top Preference'
                })
                st.dataframe(display_cohort.style.format({
                    'Net Investment (Cr)': '₹{:.2f} Cr',
                    'Avg SIP (Rs.)': '₹{:.2f}'
                }), use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.warning("No transactions match the selected filters.")

# ----------------- PAGE 4: SIP & MARKET TRENDS -----------------
elif page == "SIP & Market Trends":
    st.markdown("<h1 class='gradient-header'>📊 SIP & Market Trends</h1>", unsafe_allow_html=True)
    st.markdown("Analyze industry SIP flows in correlation with Nifty 50 equity benchmarks and category net inflows.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    monthly_sip = load_csv_data("clean_monthly_sip_inflows.csv")
    cat_inflows = load_csv_data("clean_category_inflows.csv")
    bench_idx = load_csv_data("clean_benchmark_indices.csv")
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("SIP Inflow Growth vs Market Movements")
    if not monthly_sip.empty and not bench_idx.empty:
        n50 = bench_idx[bench_idx['index_name'] == 'NIFTY50'].copy()
        n50['date'] = pd.to_datetime(n50['date'])
        n50['month'] = n50['date'].dt.to_period('M').astype(str)
        n50_monthly = n50.sort_values('date').groupby('month').last().reset_index()[['month', 'close_value']]
        merged_trend = pd.merge(monthly_sip, n50_monthly, on='month', how='inner')
        
        if not merged_trend.empty:
            fig_dual = go.Figure()
            fig_dual.add_trace(go.Bar(
                x=merged_trend['month'],
                y=merged_trend['sip_inflow_crore'],
                name="SIP Inflow (Rs. Crore)",
                marker_color="#4F46E5",
                opacity=0.65,
                yaxis="y1"
            ))
            fig_dual.add_trace(go.Scatter(
                x=merged_trend['month'],
                y=merged_trend['close_value'],
                name="Nifty 50 Index Close",
                line=dict(color="#10B981", width=3),
                yaxis="y2"
            ))
            
            fig_dual.update_layout(
                xaxis=dict(title="Month"),
                yaxis=dict(
                    title="SIP Inflow (Rs. Crore)",
                    titlefont=dict(color="#6366F1"),
                    tickfont=dict(color="#6366F1")
                ),
                yaxis2=dict(
                    title="Nifty 50 Level",
                    titlefont=dict(color="#10B981"),
                    tickfont=dict(color="#10B981"),
                    overlaying="y",
                    side="right"
                ),
                legend=dict(x=0.01, y=0.99),
                template="plotly_dark"
            )
            fig_dual = update_plotly_theme(fig_dual)
            st.plotly_chart(fig_dual, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
            
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Category-wise Net Inflow In FY 2024-25")
        if not cat_inflows.empty:
            cat_sum = cat_inflows.groupby('category')['net_inflow_crore'].sum().reset_index().sort_values('net_inflow_crore', ascending=False)
            fig_cat = px.bar(
                cat_sum,
                x="category",
                y="net_inflow_crore",
                color="net_inflow_crore",
                color_continuous_scale="Purples",
                labels={"net_inflow_crore": "Net Inflow (Rs. Cr)", "category": "Category"},
                template="plotly_dark"
            )
            fig_cat = update_plotly_theme(fig_cat)
            fig_cat.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
            
    with col_c2:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("Category Net Inflows Heatmap")
        if not cat_inflows.empty:
            heatmap_data = cat_inflows.pivot(index='category', columns='month', values='net_inflow_crore')
            
            fig_heat = px.imshow(
                heatmap_data,
                labels=dict(x="Month", y="Category", color="Net Inflow (Rs. Cr)"),
                color_continuous_scale="RdBu_r",
                template="plotly_dark"
            )
            fig_heat = update_plotly_theme(fig_heat)
            st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- PAGE 5: MONTE CARLO PROJECTIONS -----------------
elif page == "Monte Carlo Projections":
    st.markdown("<h1 class='gradient-header'>🎲 Monte Carlo Simulation & NAV Projections</h1>", unsafe_allow_html=True)
    st.markdown("Project future price paths over 5 years (1,260 trading days) using Geometric Brownian Motion simulations.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Select Scheme & Simulation Configuration")
    
    selected_scheme = st.selectbox(
        "Select a Scheme to Project", 
        options=scorecard['scheme_name'].sort_values().unique(), 
        key="mc_scheme_select"
    )
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        n_sims = st.slider("Number of Simulations", min_value=100, max_value=2000, value=1000, step=100)
    with col_sim2:
        n_years = st.slider("Projection Horizon (Years)", min_value=1, max_value=10, value=5, step=1)
        
    if selected_scheme:
        fund_row = scorecard[scorecard['scheme_name'] == selected_scheme].iloc[0]
        code = int(fund_row['amfi_code'])
        
        try:
            with get_db_connection() as conn:
                fund_nav = pd.read_sql("SELECT date, nav FROM nav_history WHERE amfi_code = ? ORDER BY date", conn, params=(code,))
                fund_nav['date'] = pd.to_datetime(fund_nav['date'])
                
            if not fund_nav.empty:
                # Calculate daily return parameters
                fund_nav['returns'] = fund_nav['nav'].pct_change()
                returns = fund_nav['returns'].dropna()
                
                mu = returns.mean()
                sigma = returns.std()
                last_nav = fund_nav.iloc[-1]['nav']
                
                # Parameters
                n_days = n_years * 252
                drift = mu - 0.5 * (sigma ** 2)
                
                # Run simulations
                np.random.seed(42)
                rand_shocks = np.random.normal(0, 1, (n_days, n_sims))
                sim_daily_returns = np.exp(drift + sigma * rand_shocks)
                
                paths = np.zeros((n_days + 1, n_sims))
                paths[0] = last_nav
                for t in range(1, n_days + 1):
                    paths[t] = paths[t - 1] * sim_daily_returns[t - 1]
                    
                # Compute percentiles
                steps = np.arange(n_days + 1)
                p5 = np.percentile(paths, 5, axis=1)
                p25 = np.percentile(paths, 25, axis=1)
                p50 = np.percentile(paths, 50, axis=1)
                p75 = np.percentile(paths, 75, axis=1)
                p95 = np.percentile(paths, 95, axis=1)
                
                # Plotly figure
                fig_mc = go.Figure()
                fig_mc.add_trace(go.Scatter(x=steps, y=p50, name="Median (50th %)", line=dict(color="#6366F1", width=3)))
                fig_mc.add_trace(go.Scatter(x=steps, y=p75, name="75th Percentile", line=dict(color="#10B981", width=1.5, dash='dash')))
                fig_mc.add_trace(go.Scatter(x=steps, y=p25, name="25th Percentile", line=dict(color="#F59E0B", width=1.5, dash='dash')))
                fig_mc.add_trace(go.Scatter(x=steps, y=p95, name="95th Percentile (Upper Bound)", line=dict(color="#A78BFA", width=1, dash='dot')))
                fig_mc.add_trace(go.Scatter(x=steps, y=p5, name="5th Percentile (Lower Bound)", line=dict(color="#EF4444", width=1, dash='dot')))
                
                fig_mc.update_layout(
                    title=f"Monte Carlo {n_years}-Year Projection for {selected_scheme.split(' - ')[0]} (Start NAV: ₹{last_nav:.2f})",
                    xaxis_title="Trading Days",
                    yaxis_title="Projected NAV (INR)",
                    template="plotly_dark"
                )
                fig_mc = update_plotly_theme(fig_mc)
                st.plotly_chart(fig_mc, use_container_width=True)
                
                # Show summary statistics
                mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                
                final_median = p50[-1]
                expected_growth = (final_median / last_nav - 1) * 100
                ann_cagr = ((final_median / last_nav) ** (1.0 / n_years) - 1) * 100
                prob_positive = (paths[-1] > last_nav).mean() * 100
                
                with mcol1:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Current NAV</div>
                        <div class="kpi-value">₹{last_nav:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with mcol2:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Projected Median NAV</div>
                        <div class="kpi-value">₹{final_median:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with mcol3:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Projected Ann. CAGR</div>
                        <div class="kpi-value" style="color: #10B981;">{ann_cagr:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with mcol4:
                    st.markdown(f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Prob. of Positive Return</div>
                        <div class="kpi-value" style="color: #6366F1;">{prob_positive:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("No NAV history available for this scheme.")
        except Exception as e:
            st.error(f"Error executing Monte Carlo simulation: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- PAGE 6: PORTFOLIO OPTIMIZATION -----------------
elif page == "Portfolio Optimization":
    st.markdown("<h1 class='gradient-header'>📊 Markowitz Efficient Frontier Portfolio Optimization</h1>", unsafe_allow_html=True)
    st.markdown("Simulate optimal asset allocations among our top-performing mutual funds using Modern Portfolio Theory (MPT).")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check if results exist, otherwise compute or show error
    ef_path = PROCESSED_DIR / "efficient_frontier_results.csv"
    if ef_path.exists():
        results_df = pd.read_csv(ef_path)
        
        # Load top 5 names dynamically
        selected_names = [col for col in results_df.columns if col not in ['Return', 'Volatility', 'Sharpe']]
        
        # MSR and MVP portfolios
        msr = results_df.iloc[results_df['Sharpe'].idxmax()]
        mvp = results_df.iloc[results_df['Volatility'].idxmin()]
        
        col_ef_chart, col_ef_alloc = st.columns([6, 4])
        
        with col_ef_chart:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.subheader("Efficient Frontier Scatter Plot")
            
            # Interactive plot with plotly
            fig_ef = px.scatter(
                results_df,
                x="Volatility",
                y="Return",
                color="Sharpe",
                color_continuous_scale="viridis_r",
                labels={"Volatility": "Annualized Volatility (Risk)", "Return": "Expected Annual Return", "Sharpe": "Sharpe Ratio"},
                template="plotly_dark",
                hover_data={n: ":.2f" for n in selected_names}
            )
            
            # Add MSR marker
            fig_ef.add_trace(go.Scatter(
                x=[msr['Volatility']],
                y=[msr['Return']],
                mode='markers',
                marker=dict(color='red', size=15, symbol='star'),
                name='Max Sharpe Ratio (MSR)',
                showlegend=True
            ))
            
            # Add MVP marker
            fig_ef.add_trace(go.Scatter(
                x=[mvp['Volatility']],
                y=[mvp['Return']],
                mode='markers',
                marker=dict(color='blue', size=15, symbol='star'),
                name='Min Variance (MVP)',
                showlegend=True
            ))
            
            fig_ef = update_plotly_theme(fig_ef)
            st.plotly_chart(fig_ef, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_ef_alloc:
            st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
            st.subheader("💡 Optimal Allocations")
            
            portfolio_choice = st.radio("Select Allocation Model", ["Maximum Sharpe Ratio (MSR)", "Minimum Variance Portfolio (MVP)"])
            
            target_port = msr if portfolio_choice == "Maximum Sharpe Ratio (MSR)" else mvp
            color_theme = "#10B981" if portfolio_choice == "Maximum Sharpe Ratio (MSR)" else "#6366F1"
            
            st.markdown(f"""
            <div style="background-color: rgba(30, 41, 59, 0.6); padding: 15px; border-radius: 8px; border-left: 5px solid {color_theme}; margin-bottom: 20px;">
                <div style="font-size: 13px; color: #94A3B8;">EXPECTED PORTFOLIO RETURN</div>
                <div style="font-size: 28px; font-weight: bold; color: white;">{target_port['Return'] * 100:.2f}%</div>
                <div style="font-size: 12px; color: #94A3B8; margin-top: 10px; display: flex; justify-content: space-between;">
                    <span>Volatility: <b>{target_port['Volatility'] * 100:.2f}%</b></span>
                    <span>Sharpe: <b>{target_port['Sharpe']:.2f}</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("##### Portfolio Weights Allocation")
            weights_data = []
            for name in selected_names:
                weights_data.append({
                    "Scheme / Fund": name,
                    "Allocation Weight (%)": f"{target_port[name] * 100:.2f}%"
                })
            st.table(pd.DataFrame(weights_data))
            
            # Pie Chart
            fig_pie = px.pie(
                values=[target_port[name] for name in selected_names],
                names=selected_names,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Purples_r,
                template="plotly_dark"
            )
            fig_pie = update_plotly_theme(fig_pie)
            fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.info("Efficient Frontier results have not been generated yet. Please run advanced_analytics.py first.")

