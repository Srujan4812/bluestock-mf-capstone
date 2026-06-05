import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
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

# Path definitions
ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

# Helper function to load cleaned CSVs
@st.cache_data
def load_csv_data(filename):
    path = PROCESSED_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

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
    ["Industry Overview", "Fund Performance", "Investor Analytics", "SIP & Market Trends"],
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
        if not scheme_perf.empty:
            plot_data = plot_data.merge(scheme_perf[['amfi_code', 'std_dev_ann_pct']], on='amfi_code')
            
        if not plot_data.empty:
            fig_scatter = px.scatter(
                plot_data,
                x="cagr_3yr_pct",
                y="std_dev_ann_pct",
                color="category",
                hover_name="scheme_name",
                size="sharpe_ratio",
                color_discrete_sequence=px.colors.qualitative.Bold,
                labels={
                    "cagr_3yr_pct": "3-Year CAGR Return (%)",
                    "std_dev_ann_pct": "Annualized Standard Deviation (%)",
                    "sharpe_ratio": "Sharpe Ratio"
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
        }), use_container_width=True, hide_index=True)
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
                
                # Show key stats
                kcol1, kcol2, kcol3, kcol4 = st.columns(4)
                kcol1.metric("3Yr CAGR Return", f"{fund_row['cagr_3yr_pct']:.2f}%")
                kcol2.metric("Sharpe Ratio", f"{fund_row['sharpe_ratio']:.2f}")
                kcol3.metric("Alpha (vs Nifty 100)", f"{fund_row['alpha']:.2f}%")
                kcol4.metric("Maximum Drawdown", f"{fund_row['max_drawdown_pct']:.2f}%")
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
