import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Setup Page Configuration
st.set_page_config(
    page_title="Bluestock Mutual Fund Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS Injection for Premium Look)
st.markdown("""
<style>
    /* Dark Slate & Indigo Gradient Header */
    .reportview-container {
        background: #0F172A;
        color: #F8FAFC;
    }
    .sidebar .sidebar-content {
        background: #1E293B;
    }
    h1, h2, h3 {
        color: #4F46E5;
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 700;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(79, 70, 229, 0.2);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(79, 70, 229, 0.6);
    }
    .metric-title {
        color: #94A3B8;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: bold;
    }
    .metric-delta {
        color: #10B981;
        font-size: 14px;
        margin-top: 5px;
    }
    /* Style main sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allowed_html=True)

# Path definitions
ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "processed" / "bluestock.db"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

# Helper function to get database connection
def get_db_connection():
    return sqlite3.connect(DB_PATH)

# Helper function to load data
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

# Sidebar Logo & Title
st.sidebar.markdown("<h2 style='text-align: center; color: #6366F1;'>BLUESTOCK</h2>", unsafe_allowed_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94A3B8; font-size: 12px;'>MF Analytics Platform</p>", unsafe_allowed_html=True)
st.sidebar.markdown("---")

# Page Selector
page = st.sidebar.radio(
    "Navigation",
    ["Industry Overview", "Fund Performance", "Investor Analytics", "SIP & Market Trends"]
)

# ----------------- PAGE 1: INDUSTRY OVERVIEW -----------------
if page == "Industry Overview":
    st.title("📈 Industry Overview")
    st.markdown("Monitor Indian Mutual Fund industry assets, inflows, and folio growth over time.")
    st.markdown("---")
    
    # Load raw data for Page 1
    monthly_sip = load_csv_data("clean_monthly_sip_inflows.csv")
    aum_fh = load_csv_data("clean_aum_by_fund_house.csv")
    folios = load_csv_data("clean_industry_folio_count.csv")
    
    # Latest statistics
    latest_sip = monthly_sip.iloc[-1] if not monthly_sip.empty else None
    latest_folio = folios.iloc[-1] if not folios.empty else None
    
    # KPIs Layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Total Industry AUM</div>
            <div class="metric-value">₹81.0 L Cr</div>
            <div class="metric-delta">As of Dec 2025</div>
        </div>
        """, unsafe_allowed_html=True)
    with col2:
        val = f"₹{latest_sip['sip_inflow_crore']:,.0f} Cr" if latest_sip is not None else "₹31,002 Cr"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Monthly SIP Inflow</div>
            <div class="metric-value">{val}</div>
            <div class="metric-delta">₹31,002 Cr Milestone</div>
        </div>
        """, unsafe_allowed_html=True)
    with col3:
        val = f"{latest_folio['total_folios_crore']:.2f} Cr" if latest_folio is not None else "26.12 Cr"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Folio Count</div>
            <div class="metric-value">{val}</div>
            <div class="metric-delta">Equity: 78% Share</div>
        </div>
        """, unsafe_allowed_html=True)
    with col4:
        val = f"{latest_sip['active_sip_accounts_crore']:.2f} Cr" if latest_sip is not None else "9.35 Cr"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Active SIP Accounts</div>
            <div class="metric-value">{val}</div>
            <div class="metric-delta">YoY Growth: +18.4%</div>
        </div>
        """, unsafe_allowed_html=True)
        
    st.markdown("<br>", unsafe_allowed_html=True)
    
    # Industry AUM Growth Trend
    st.subheader("Industry Assets Under Management (AUM) Growth Trend")
    if not monthly_sip.empty:
        # Generate plot
        fig_aum = px.line(
            monthly_sip,
            x="month",
            y="sip_aum_lakh_crore",
            title="Total SIP Assets under Management (Rs. Lakh Crore)",
            labels={"sip_aum_lakh_crore": "SIP AUM (Rs. Lakh Crore)", "month": "Month"},
            template="plotly_dark"
        )
        fig_aum.update_traces(line=dict(color="#6366F1", width=3))
        fig_aum.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        )
        st.plotly_chart(fig_aum, use_container_width=True)
        
    st.markdown("---")
    
    # AUM by Fund House
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Top Fund Houses by AUM (Dec 2025)")
        if not aum_fh.empty:
            # Get latest quarter
            latest_date = aum_fh['date'].max()
            latest_aum = aum_fh[aum_fh['date'] == latest_date].sort_values("aum_crore", ascending=False).head(10)
            
            fig_bar = px.bar(
                latest_aum,
                x="aum_crore",
                y="fund_house",
                orientation="h",
                title=f"Assets Under Management (Rs. Crore) - {latest_date}",
                color="aum_crore",
                color_continuous_scale="Viridis",
                labels={"aum_crore": "AUM (Rs. Crore)", "fund_house": "Fund House"},
                template="plotly_dark"
            )
            fig_bar.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
    with col_right:
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
                title="Folio Count by Category (2022-2025)",
                template="plotly_dark"
            )
            fig_folio.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_folio, use_container_width=True)

# ----------------- PAGE 2: FUND PERFORMANCE -----------------
elif page == "Fund Performance":
    st.title("🏆 Fund Performance & Scorecard")
    st.markdown("Analyze mutual fund returns on a risk-adjusted basis against benchmark indices.")
    st.markdown("---")
    
    # Slicers in sidebar
    st.sidebar.subheader("Filter Schemes")
    selected_amcs = st.sidebar.multiselect("Select AMCs", options=fund_master['fund_house'].unique())
    selected_categories = st.sidebar.multiselect("Select Categories", options=fund_master['category'].unique())
    selected_plans = st.sidebar.multiselect("Select Plans", options=fund_master['plan'].unique())
    
    # Filter Scorecard Data
    filtered_scorecard = scorecard.copy()
    if selected_amcs:
        # Match AMC by joining fund_master
        amfi_codes = fund_master[fund_master['fund_house'].isin(selected_amcs)]['amfi_code']
        filtered_scorecard = filtered_scorecard[filtered_scorecard['amfi_code'].isin(amfi_codes)]
    if selected_categories:
        amfi_codes = fund_master[fund_master['category'].isin(selected_categories)]['amfi_code']
        filtered_scorecard = filtered_scorecard[filtered_scorecard['amfi_code'].isin(amfi_codes)]
    if selected_plans:
        amfi_codes = fund_master[fund_master['plan'].isin(selected_plans)]['amfi_code']
        filtered_scorecard = filtered_scorecard[filtered_scorecard['amfi_code'].isin(amfi_codes)]
        
    # Scatter Plot: Return vs Risk
    st.subheader("Risk-Return Profile (3-Year CAGR vs Standard Deviation)")
    
    # Join filtered scorecard with fund_master to get category for coloring
    plot_data = filtered_scorecard.merge(fund_master[['amfi_code', 'category', 'fund_house']], on='amfi_code')
    
    if not plot_data.empty:
        fig_scatter = px.scatter(
            plot_data,
            x="cagr_3yr_pct",
            y="std_dev_ann_pct",
            color="category",
            hover_name="scheme_name",
            size="sharpe_ratio",
            labels={
                "cagr_3yr_pct": "3-Year CAGR Return (%)",
                "std_dev_ann_pct": "Annualized Std Dev (%)",
                "sharpe_ratio": "Sharpe Ratio (size)"
            },
            title="Fund Performance Scatter Plot (Bubble size = Sharpe Ratio)",
            template="plotly_dark"
        )
        fig_scatter.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No data matches selected filters.")
        
    st.markdown("---")
    
    # Scorecard Table
    st.subheader("Composite Fund Scorecard & Rankings")
    st.markdown("Ranked by weighted composite score: Returns (30%), Sharpe (25%), Alpha (20%), Expense Ratio (15%), and Max Drawdown (10%).")
    if not filtered_scorecard.empty:
        display_cols = ['scorecard_rank', 'scheme_name', 'cagr_3yr_pct', 'sharpe_ratio', 'alpha', 'expense_ratio_pct', 'max_drawdown_pct', 'score']
        # Rename columns for readability
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
        
    st.markdown("---")
    
    # Fund Detail & Benchmark Comparison
    st.subheader("Individual Fund Benchmark Analysis")
    selected_scheme = st.selectbox("Select a Scheme for NAV Analysis", options=scorecard['scheme_name'].unique())
    
    if selected_scheme:
        fund_row = scorecard[scorecard['scheme_name'] == selected_scheme].iloc[0]
        code = int(fund_row['amfi_code'])
        
        # Load NAV and Benchmark daily values from Database
        try:
            with get_db_connection() as conn:
                # Get fund NAV
                fund_nav = pd.read_sql(
                    "SELECT date, nav FROM nav_history WHERE amfi_code = ? ORDER BY date", 
                    conn, params=(code,)
                )
                fund_nav['date'] = pd.to_datetime(fund_nav['date'])
                
                # Get Nifty 50 and Nifty 100 for dates
                benchmarks = pd.read_sql(
                    "SELECT date, index_name, close_value FROM benchmark_indices ORDER BY date",
                    conn
                )
                benchmarks['date'] = pd.to_datetime(benchmarks['date'])
                
            # Filter for overlap dates
            fund_nav = fund_nav[fund_nav['date'] >= '2023-05-29']
            benchmarks = benchmarks[benchmarks['date'] >= '2023-05-29']
            
            # Pivot benchmarks
            bench_pivot = benchmarks.pivot(index='date', columns='index_name', values='close_value').reset_index()
            
            # Merge
            compare_df = pd.merge(fund_nav, bench_pivot, on='date', how='inner').sort_values('date')
            
            # Normalize to 100
            if not compare_df.empty:
                compare_df['Fund Normalized'] = (compare_df['nav'] / compare_df.iloc[0]['nav']) * 100
                compare_df['Nifty 50 Normalized'] = (compare_df['NIFTY50'] / compare_df.iloc[0]['NIFTY50']) * 100
                compare_df['Nifty 100 Normalized'] = (compare_df['NIFTY100'] / compare_df.iloc[0]['NIFTY100']) * 100
                
                # Plot
                fig_nav = go.Figure()
                fig_nav.add_trace(go.Scatter(x=compare_df['date'], y=compare_df['Fund Normalized'], name="Fund (Normalized)", line=dict(color="#6366F1", width=2.5)))
                fig_nav.add_trace(go.Scatter(x=compare_df['date'], y=compare_df['Nifty 50 Normalized'], name="Nifty 50", line=dict(color="#E2E8F0", width=1.5, dash='dash')))
                fig_nav.add_trace(go.Scatter(x=compare_df['date'], y=compare_df['Nifty 100 Normalized'], name="Nifty 100", line=dict(color="#94A3B8", width=1.5, dash='dot')))
                
                fig_nav.update_layout(
                    title=f"{selected_scheme} vs Benchmarks (3-Year Normalized NAV, 2023-05-29 = 100)",
                    xaxis_title="Date",
                    yaxis_title="Normalized Value",
                    template="plotly_dark",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_nav, use_container_width=True)
                
                # Show key stats
                kcol1, kcol2, kcol3, kcol4 = st.columns(4)
                kcol1.metric("3Yr CAGR Return", f"{fund_row['cagr_3yr_pct']:.2f}%")
                kcol2.metric("Sharpe Ratio", f"{fund_row['sharpe_ratio']:.2f}")
                kcol3.metric("Alpha (vs Nifty 100)", f"{fund_row['alpha']:.2f}%")
                kcol4.metric("Maximum Drawdown", f"{fund_row['max_drawdown_pct']:.2f}%")
        except Exception as e:
            st.error(f"Error loading comparison chart: {e}")

# ----------------- PAGE 3: INVESTOR ANALYTICS -----------------
elif page == "Investor Analytics":
    st.title("👥 Investor Analytics & Segmentation")
    st.markdown("Analyze transaction patterns, geographic distributions, and demographic cohorts.")
    st.markdown("---")
    
    # Load transactions
    tx_df = load_csv_data("clean_investor_transactions.csv")
    
    # Filters
    st.sidebar.subheader("Demographic Filters")
    states = st.sidebar.multiselect("Select States", options=tx_df['state'].unique() if not tx_df.empty else [])
    tiers = st.sidebar.multiselect("Select City Tiers", options=tx_df['city_tier'].unique() if not tx_df.empty else [])
    age_groups = st.sidebar.multiselect("Select Age Groups", options=tx_df['age_group'].unique() if not tx_df.empty else [])
    
    # Filter Data
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
            st.subheader("Transaction Amount by State")
            state_amt = filtered_tx.groupby('state')['amount_inr'].sum().reset_index().sort_values('amount_inr', ascending=False)
            fig_state = px.bar(
                state_amt,
                x="amount_inr",
                y="state",
                orientation="h",
                color="amount_inr",
                color_continuous_scale="Plasma",
                labels={"amount_inr": "Total Transaction Volume (INR)", "state": "State"},
                template="plotly_dark"
            )
            fig_state.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_state, use_container_width=True)
            
        with col_t2:
            st.subheader("Transaction Types Split")
            type_split = filtered_tx.groupby('transaction_type')['amount_inr'].sum().reset_index()
            fig_donut = px.pie(
                type_split,
                names="transaction_type",
                values="amount_inr",
                hole=0.4,
                title="Transaction Type Contribution",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template="plotly_dark"
            )
            fig_donut.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_donut, use_container_width=True)
            
        st.markdown("---")
        
        # Monthly transaction volume line chart
        st.subheader("Monthly Transaction Volume Trend")
        filtered_tx['month'] = pd.to_datetime(filtered_tx['transaction_date']).dt.to_period('M').astype(str)
        monthly_vol = filtered_tx.groupby('month')['amount_inr'].sum().reset_index()
        fig_vol = px.line(
            monthly_vol,
            x="month",
            y="amount_inr",
            title="Monthly Invested / Redeemed Amount (INR)",
            labels={"amount_inr": "Total Volume (INR)", "month": "Month"},
            template="plotly_dark"
        )
        fig_vol.update_traces(line=dict(color="#10B981", width=3))
        fig_vol.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_vol, use_container_width=True)
        
        # Age group average SIP box plot
        st.subheader("SIP Transaction Size by Age Group")
        sip_tx = filtered_tx[filtered_tx['transaction_type'] == 'SIP']
        if not sip_tx.empty:
            fig_box = px.box(
                sip_tx,
                x="age_group",
                y="amount_inr",
                color="age_group",
                title="Average SIP Amount Range by Age Group",
                labels={"amount_inr": "SIP Amount (INR)", "age_group": "Age Group"},
                template="plotly_dark"
            )
            fig_box.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("No SIP transaction records found matching the filters.")
    else:
        st.warning("No transactions match the selected filters.")

# ----------------- PAGE 4: SIP & MARKET TRENDS -----------------
elif page == "SIP & Market Trends":
    st.title("📊 SIP & Market Trends")
    st.markdown("Analyze mutual fund SIP inflows in parallel with equity market benchmark index movements.")
    st.markdown("---")
    
    monthly_sip = load_csv_data("clean_monthly_sip_inflows.csv")
    cat_inflows = load_csv_data("clean_category_inflows.csv")
    bench_idx = load_csv_data("clean_benchmark_indices.csv")
    
    # Dual Axis: SIP Inflow vs Nifty 50
    st.subheader("SIP Inflow Growth vs Market Movements")
    if not monthly_sip.empty and not bench_idx.empty:
        # Extract Nifty 50 close price at the end of each month
        n50 = bench_idx[bench_idx['index_name'] == 'NIFTY50'].copy()
        n50['date'] = pd.to_datetime(n50['date'])
        n50['month'] = n50['date'].dt.to_period('M').astype(str)
        # Get monthly end closing value
        n50_monthly = n50.sort_values('date').groupby('month').last().reset_index()[['month', 'close_value']]
        
        # Merge
        merged_trend = pd.merge(monthly_sip, n50_monthly, on='month', how='inner')
        
        if not merged_trend.empty:
            # Create Plotly dual axis chart
            fig_dual = go.Figure()
            # Bar chart for SIP Inflows
            fig_dual.add_trace(go.Bar(
                x=merged_trend['month'],
                y=merged_trend['sip_inflow_crore'],
                name="SIP Inflow (Rs. Crore)",
                marker_color="#4F46E5",
                opacity=0.8,
                yaxis="y1"
            ))
            # Line chart for Nifty 50
            fig_dual.add_trace(go.Scatter(
                x=merged_trend['month'],
                y=merged_trend['close_value'],
                name="Nifty 50 Close Value",
                line=dict(color="#10B981", width=3),
                yaxis="y2"
            ))
            
            fig_dual.update_layout(
                title="Monthly SIP Inflows (Rs. Crore) vs Nifty 50 Closing Level",
                template="plotly_dark",
                xaxis=dict(title="Month"),
                yaxis=dict(
                    title="SIP Inflow (Rs. Crore)",
                    titlefont=dict(color="#4F46E5"),
                    tickfont=dict(color="#4F46E5")
                ),
                yaxis2=dict(
                    title="Nifty 50 Level",
                    titlefont=dict(color="#10B981"),
                    tickfont=dict(color="#10B981"),
                    overlaying="y",
                    side="right"
                ),
                legend=dict(x=0.01, y=0.99),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_dual, use_container_width=True)
            
    st.markdown("---")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("Category-wise Net Inflow In FY 2024-25")
        if not cat_inflows.empty:
            cat_sum = cat_inflows.groupby('category')['net_inflow_crore'].sum().reset_index().sort_values('net_inflow_crore', ascending=False)
            fig_cat = px.bar(
                cat_sum,
                x="category",
                y="net_inflow_crore",
                title="Net Inflow by Fund Category (Rs. Crore)",
                color="net_inflow_crore",
                color_continuous_scale="Sunsetdark",
                labels={"net_inflow_crore": "Net Inflow (Rs. Cr)", "category": "Category"},
                template="plotly_dark"
            )
            fig_cat.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            
    with col_c2:
        st.subheader("Category Inflows Heatmap")
        if not cat_inflows.empty:
            heatmap_data = cat_inflows.pivot(index='category', columns='month', values='net_inflow_crore')
            
            fig_heat = px.imshow(
                heatmap_data,
                labels=dict(x="Month", y="Category", color="Net Inflow (Rs. Cr)"),
                title="Category Inflow (Rs. Crore) Month-wise Heatmap",
                color_continuous_scale="RdBu",
                template="plotly_dark"
            )
            fig_heat.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_heat, use_container_width=True)
