# ==========================================================
# DASHBOARD STYLE UTILITIES
# Safe visual polish only
#
# Save as: utils/dashboard_style.py
# ==========================================================

import streamlit as st


def apply_dashboard_style():
    """
    Safe visual styling only.
    Does not change data logic, calculations, filters, charts, or structure.
    """
    st.markdown("""
<style>

/* Sidebar dark blue theme */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1F3A 0%, #102A4C 55%, #12315A 100%);
    border-right: 1px solid rgba(255,255,255,0.10);
}

section[data-testid="stSidebar"] * {
    color: #E5ECF6 !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin: 0.15rem 0.35rem;
    transition: all 0.2s ease-in-out;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background-color: rgba(255,255,255,0.10);
}

section[data-testid="stSidebar"] [aria-current="page"] {
    background-color: rgba(255,255,255,0.14) !important;
    border-left: 4px solid #60A5FA;
    border-radius: 10px;
    font-weight: 700;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* Sidebar select boxes remain readable */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.96) !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #0F172A !important;
}

/* Main titles */
h1 {
    color: #0F172A !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

h2, h3 {
    color: #163A6B !important;
    font-weight: 750 !important;
}

/* Existing section title class, improved only */
.section-title {
    background: linear-gradient(90deg, #E8F0FE 0%, #F7FAFF 100%);
    border-left: 5px solid #1D4ED8;
    padding: 0.80rem 1rem;
    border-radius: 10px;
    margin-top: 1.35rem !important;
    margin-bottom: 1rem !important;
    color: #163A6B !important;
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFF 100%) !important;
    border: 1px solid #D6E4FF !important;
    padding: 1rem 1rem !important;
    border-radius: 16px !important;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

div[data-testid="metric-container"] label {
    color: #475569 !important;
    font-weight: 700 !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0F172A !important;
    font-weight: 850 !important;
}

/* Existing boxes lightly improved */
.scope-box {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFF 100%);
    border: 1px solid #D6E4FF !important;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
}

.findings-box {
    border-left: 6px solid #D97706 !important;
    background: linear-gradient(180deg, #FFF7ED 0%, #FFFFFF 100%) !important;
    border-top: 1px solid #FED7AA;
    border-right: 1px solid #FED7AA;
    border-bottom: 1px solid #FED7AA;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
}

.note-box {
    border-left: 5px solid #2563EB !important;
    background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 100%) !important;
    border-top: 1px solid #BFDBFE;
    border-right: 1px solid #BFDBFE;
    border-bottom: 1px solid #BFDBFE;
}

.theme-highlight-box {
    border-left: 5px solid #7C3AED !important;
    background: linear-gradient(180deg, #F5F3FF 0%, #FFFFFF 100%) !important;
    border-top: 1px solid #DDD6FE;
    border-right: 1px solid #DDD6FE;
    border-bottom: 1px solid #DDD6FE;
}

/* Chart and table containers */
.stPlotlyChart {
    background: #FFFFFF;
    border: 1px solid #D6E4FF;
    border-radius: 14px;
    padding: 0.50rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

[data-testid="stDataFrame"] {
    border: 1px solid #D6E4FF;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid #D6E4FF;
}

/* Hero light touch */
.hero-badge {
    background: #FFF7ED;
    box-shadow: 0 4px 12px rgba(217,119,6,0.08);
}

.hero-title {
    color: #0F172A;
}

.hero-description {
    color: #475569 !important;
}

</style>
""", unsafe_allow_html=True)
