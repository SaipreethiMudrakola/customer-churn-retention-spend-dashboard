"""
Customer Churn & Retention Spend Dashboard
Simple dark-theme Streamlit UI · SQL cohort analysis
Made by Sai Preethi
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_analysis import TENURE_BAND_ORDER, analyze_dataframe, build_analysis

st.set_page_config(
    page_title="Churn & Retention Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Polished dark theme (still simple)
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
    .stApp {
        background:
            radial-gradient(900px 420px at 0% -10%, rgba(56, 132, 255, 0.16), transparent 55%),
            radial-gradient(700px 380px at 100% 0%, rgba(168, 85, 247, 0.12), transparent 50%),
            #0b1220;
        color: #eaf0ff;
    }
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #121a2b 0%, #0d1422 100%);
        border-right: 1px solid #243047;
    }
    [data-testid="stSidebar"] * {
        color: #d7e3f4;
    }
    h1, h2, h3, h4 {
        color: #f4f7ff !important;
        letter-spacing: -0.02em;
    }
    .stMarkdown, p, label, span {
        color: #b7c5d8;
    }
    div[data-testid="stMetricValue"] {
        color: #f4f7ff !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8fa0b8 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #7dd3fc !important;
    }
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(30, 41, 64, 0.95), rgba(17, 24, 39, 0.92));
        border: 1px solid #2b3b55;
        border-radius: 14px;
        padding: 0.85rem 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }
    /* Tabs */
    button[data-baseweb="tab"] {
        color: #9db0c9 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #8ec5ff !important;
        border-bottom-color: #3b82f6 !important;
    }
    /* Inputs / buttons */
    .stButton > button {
        background: linear-gradient(180deg, #2563eb, #1d4ed8);
        color: #fff;
        border: 1px solid #3b82f6;
        border-radius: 10px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #3b82f6, #2563eb);
        border-color: #60a5fa;
    }
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        color: #eaf0ff !important;
        background: #1a2438 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    hr, [data-testid="stDecorator"] {
        border-color: #2a3a52;
    }
    /* Soft header strip */
    .app-header {
        background: linear-gradient(120deg, rgba(37, 99, 235, 0.18), rgba(147, 51, 234, 0.12));
        border: 1px solid #2b3b55;
        border-radius: 16px;
        padding: 1.1rem 1.25rem 0.95rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    }
    .app-header h1 {
        margin: 0 0 0.25rem 0 !important;
        font-size: 1.7rem !important;
        background: linear-gradient(90deg, #f8fbff, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .app-header p {
        margin: 0;
        color: #9db0c9;
        font-size: 0.92rem;
    }
    .pill-row { margin-top: 0.7rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }
    .pill {
        display: inline-block;
        padding: 0.22rem 0.65rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #334155;
        background: rgba(15, 23, 42, 0.55);
        color: #dbe7f7;
    }
    .pill.blue { border-color: rgba(59,130,246,0.55); color: #93c5fd; }
    .pill.red { border-color: rgba(248,113,113,0.5); color: #fda4a4; }
    .pill.amber { border-color: rgba(251,191,36,0.5); color: #fcd34d; }
    .pill.green { border-color: rgba(52,211,153,0.45); color: #6ee7b7; }
    .footer-note {
        margin-top: 1.25rem;
        padding: 0.85rem 1rem;
        border-radius: 12px;
        border: 1px solid #2b3b55;
        background: rgba(17, 24, 39, 0.7);
        color: #9db0c9;
        font-size: 0.86rem;
        text-align: center;
    }
    .footer-note strong { color: #eaf0ff; }
</style>
""",
    unsafe_allow_html=True,
)

DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c5d3e8", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    xaxis=dict(gridcolor="#243247", zerolinecolor="#243247", color="#8fa0b8"),
    yaxis=dict(gridcolor="#243247", zerolinecolor="#243247", color="#8fa0b8"),
    title=dict(font=dict(color="#eaf0ff", size=14)),
)
# Cool blue / teal / violet / amber palette
COLORS = ["#3b82f6", "#22d3ee", "#a78bfa", "#f59e0b", "#f43f5e", "#34d399"]


def style_fig(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(**DARK_LAYOUT, height=height, showlegend=False)
    return fig


def empty_fig(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[dict(text="No data for current filters", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="#8b949e"))],
    )
    return style_fig(fig)


def bar_churn(df: pd.DataFrame, title: str) -> go.Figure:
    if df is None or len(df) == 0:
        return empty_fig(title)
    fig = px.bar(
        df,
        x="segment",
        y="churn_rate_pct",
        title=title,
        text="churn_rate_pct",
        color="segment",
        color_discrete_sequence=COLORS,
    )
    fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside", cliponaxis=False, marker_line_width=0)
    fig.update_layout(yaxis_title="Churn %", xaxis_title="")
    return style_fig(fig)


def bar_revenue(df: pd.DataFrame, title: str) -> go.Figure:
    if df is None or len(df) == 0:
        return empty_fig(title)
    fig = px.bar(
        df,
        x="segment",
        y="revenue_at_risk",
        title=title,
        text="revenue_at_risk",
        color="segment",
        color_discrete_sequence=COLORS,
    )
    fig.update_traces(texttemplate="$%{y:,.0f}", textposition="outside", cliponaxis=False, marker_line_width=0)
    fig.update_layout(yaxis_title="Revenue at risk ($)", xaxis_title="")
    return style_fig(fig)


def pd_notna(v) -> bool:
    return bool(pd.notna(v))


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_base():
    return build_analysis()


base = load_base()
base_df = base["df"]
all_contracts = sorted(base_df["Contract"].dropna().unique().tolist())
all_internets = sorted(base_df["InternetService"].dropna().unique().tolist())
all_payments = sorted(base_df["payment_group"].dropna().unique().tolist())
all_tenures = [b for b in TENURE_BAND_ORDER if b in set(base_df["tenure_band"].unique())]

# Session defaults
for key, default in {
    "flt_contracts": all_contracts,
    "flt_internets": all_internets,
    "flt_payments": all_payments,
    "flt_tenures": all_tenures,
}.items():
    if key not in st.session_state:
        st.session_state[key] = list(default)

# ---------------------------------------------------------------------------
# Sidebar filters (simple)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    st.caption("Made by Sai Preethi")

    if st.button("↺ Reset filters", use_container_width=True):
        st.session_state["flt_contracts"] = list(all_contracts)
        st.session_state["flt_internets"] = list(all_internets)
        st.session_state["flt_payments"] = list(all_payments)
        st.session_state["flt_tenures"] = list(all_tenures)
        st.rerun()

    contracts = st.multiselect("Contract", options=all_contracts, key="flt_contracts")
    internets = st.multiselect("Internet service", options=all_internets, key="flt_internets")
    payments = st.multiselect("Payment group", options=all_payments, key="flt_payments")
    tenure_bands = st.multiselect("Tenure band", options=all_tenures, key="flt_tenures")

    st.divider()
    st.markdown("**Formulas**")
    st.code("Churn % = Churned / Total × 100\nRisk $ = Σ MonthlyCharges (churned)")
    st.caption("Use the top-left arrow to open/close this sidebar.")

# Apply filters
mask = (
    base_df["Contract"].isin(contracts or [])
    & base_df["InternetService"].isin(internets or [])
    & base_df["payment_group"].isin(payments or [])
    & base_df["tenure_band"].isin(tenure_bands or [])
)
filtered_df = base_df.loc[mask].copy()
analysis = analyze_dataframe(filtered_df)

kpis = analysis["kpis"]
by_contract = analysis["by_contract"]
by_tenure = analysis["by_tenure"]
by_internet = analysis["by_internet"]
by_payment = analysis["by_payment"]
by_payment_detail = analysis["by_payment_detail"]
heatmap = analysis["heatmap"]
stories = analysis["stories"]
df = analysis["df"]

# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------
filter_active = len(filtered_df) != len(base_df)
st.markdown(
    f"""
<div class="app-header">
  <h1>📡 Customer Churn & Retention Spend</h1>
  <p>SQL cohort analysis for telecom retention decisions · Made by Sai Preethi</p>
  <div class="pill-row">
    <span class="pill blue">Showing {len(filtered_df):,} / {len(base_df):,}</span>
    <span class="pill red">Churn {kpis['churn_rate_pct']}%</span>
    <span class="pill amber">Risk ${kpis['revenue_at_risk']:,.0f}/mo</span>
    <span class="pill {'amber' if filter_active else 'green'}">{'Filters on' if filter_active else 'Full base'}</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

if len(filtered_df) == 0:
    st.warning("No customers match the current filters. Reset or widen selections in the sidebar.")

# KPI row
k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers", f"{kpis['total_customers']:,}", f"{kpis['churned_customers']:,} churned")
k2.metric("Churn rate", f"{kpis['churn_rate_pct']}%")
k3.metric("Revenue at risk / mo", f"${kpis['revenue_at_risk']:,.0f}")
k4.metric("Revenue at risk / yr", f"${kpis['annual_revenue_at_risk']:,.0f}")

s1, s2, s3, s4 = st.columns(4)
s1.metric("Month-to-month churn", f"{kpis['m2m_churn_pct']}%")
s2.metric("3–6 mo danger zone", f"{kpis['danger_zone_churn_pct']}%")
s3.metric("Electronic check churn", f"{kpis['echeck_churn_pct']}%")
s4.metric("Autopay churn", f"{kpis['autopay_churn_pct']}%")

st.markdown("")
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Overview", "🧮 SQL Cohorts", "🔥 Heatmap", "📖 Story & Decisions", "📁 Customers"]
)

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(bar_churn(by_contract, "Churn rate by contract"), use_container_width=True)
        st.plotly_chart(bar_revenue(by_contract, "Revenue at risk by contract"), use_container_width=True)
    with c2:
        st.plotly_chart(bar_churn(by_tenure, "Churn rate by tenure band"), use_container_width=True)
        st.plotly_chart(bar_revenue(by_tenure, "Revenue at risk by tenure band"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(bar_churn(by_internet, "Churn rate by internet service"), use_container_width=True)
    with c4:
        st.plotly_chart(bar_churn(by_payment, "Churn rate by payment group"), use_container_width=True)

    st.info(
        f"**Takeaway:** Month-to-month churn is **{kpis['m2m_churn_pct']}%**, "
        f"3–6 month danger zone is **{kpis['danger_zone_churn_pct']}%**, "
        f"electronic check is **{kpis['echeck_churn_pct']}%** vs autopay **{kpis['autopay_churn_pct']}%**. "
        f"Monthly revenue at risk: **${kpis['revenue_at_risk']:,.0f}** "
        f"(~${kpis['annual_revenue_at_risk']:,.0f}/year)."
    )

with tab2:
    st.markdown("SQL cohort metrics: `Churn % = Churned ÷ Total × 100` · `Revenue at Risk = Σ MonthlyCharges of churned`")
    st.subheader("Contract")
    st.dataframe(by_contract, use_container_width=True, hide_index=True)
    st.subheader("Tenure band")
    st.dataframe(by_tenure, use_container_width=True, hide_index=True)
    st.subheader("Internet service")
    st.dataframe(by_internet, use_container_width=True, hide_index=True)
    st.subheader("Payment group")
    st.dataframe(by_payment, use_container_width=True, hide_index=True)
    st.subheader("Payment method (detail)")
    st.dataframe(by_payment_detail, use_container_width=True, hide_index=True)
    st.plotly_chart(bar_revenue(by_payment_detail, "Revenue at risk by payment method"), use_container_width=True)

with tab3:
    st.subheader("Contract × tenure churn heatmap")
    hm = heatmap.copy() if heatmap is not None else pd.DataFrame()
    if hm.empty:
        st.info("No heatmap data for current filters.")
    else:
        fig = go.Figure(
            data=go.Heatmap(
                z=hm.values,
                x=list(hm.columns),
                y=list(hm.index),
                colorscale=[
                    [0.0, "#0f172a"],
                    [0.25, "#1e3a5f"],
                    [0.5, "#2563eb"],
                    [0.75, "#f59e0b"],
                    [1.0, "#f43f5e"],
                ],
                text=[[f"{v:.1f}%" if pd_notna(v) else "" for v in row] for row in hm.values],
                texttemplate="%{text}",
                textfont=dict(color="#f0f6fc", size=12),
                colorbar=dict(title="Churn %"),
                hovertemplate="Contract: %{y}<br>Tenure: %{x}<br>Churn: %{z:.1f}%<extra></extra>",
            )
        )
        fig.update_layout(xaxis_title="Tenure band", yaxis_title="Contract")
        st.plotly_chart(style_fig(fig, height=400), use_container_width=True)
        st.caption("Hotter cells = higher churn. Focus retention on month-to-month × early tenure.")

with tab4:
    st.subheader("Findings")
    col_a, col_b, col_c = st.columns(3)
    col_a.write(f"**Month-to-month** contracts churn highest at **{kpis['m2m_churn_pct']}%**.")
    col_b.write(f"**3–6 month** tenure is a danger zone at **{kpis['danger_zone_churn_pct']}%**.")
    col_c.write(f"**Electronic check** churns at **{kpis['echeck_churn_pct']}%** vs autopay **{kpis['autopay_churn_pct']}%**.")

    st.subheader("Customer examples")
    if stories is None or len(stories) == 0:
        st.info("No churned-customer examples for current filters.")
    else:
        for _, row in stories.iterrows():
            st.write(f"- {row['story']}")

    st.subheader("Story example")
    st.write(
        "Customer A churned in month 4 with a **$70** monthly charge → **$840** annual revenue at risk. "
        "A $90 contract-upgrade incentive that saves them is roughly **9×** ROI on that account."
    )

    st.subheader("Decisions enabled")
    st.markdown(
        """
1. **Contract upgrade incentives** for month-to-month customers  
2. **Focus retention spend** on early tenure (especially 3–6 months)  
3. **Promote autopay** among electronic-check users  
"""
    )

with tab5:
    cols = [
        c
        for c in [
            "customerID",
            "gender",
            "tenure",
            "tenure_band",
            "Contract",
            "InternetService",
            "PaymentMethod",
            "payment_group",
            "MonthlyCharges",
            "TotalCharges",
            "Churn",
            "AnnualRisk",
        ]
        if c in df.columns
    ]
    view = df.loc[:, cols] if len(df) and cols else pd.DataFrame(columns=cols)
    st.caption(f"{len(view):,} rows")
    st.dataframe(view, use_container_width=True, hide_index=True, height=420)
    st.download_button(
        "Download filtered CSV",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="filtered_customers.csv",
        mime="text/csv",
        disabled=len(view) == 0,
    )

st.markdown(
    """
<div class="footer-note">
  <strong>Made by Sai Preethi</strong> · SQL cohorts · Pandas · Plotly · Streamlit
</div>
""",
    unsafe_allow_html=True,
)
