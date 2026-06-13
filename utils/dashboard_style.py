# ==========================================================
# DASHBOARD STYLE UTILITIES
# Safe visual polish only - adaptive for light and dark mode
#
# Save as: utils/dashboard_style.py
# ==========================================================

import streamlit as st


def apply_dashboard_style():
    """
    Safe visual styling only.
    This version is adaptive for both Streamlit light mode and dark mode.
    It avoids forcing main-page text colours, so no wording disappears.
    """
    st.markdown("""
<style>

/* ==========================================================
   SIDEBAR DARK BLUE THEME
   ========================================================== */

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

/* ==========================================================
   MAIN CONTENT - DO NOT FORCE TEXT COLOURS
   ========================================================== */

/* Keep native Streamlit theme colours for text. This protects dark mode. */
h1, h2, h3, h4, p, li, label, span {
    color: inherit;
}

/* ==========================================================
   SECTION HEADERS - ADAPTIVE
   ========================================================== */

.section-title {
    background: rgba(37, 99, 235, 0.08);
    border-left: 5px solid #2563EB;
    padding: 0.80rem 1rem;
    border-radius: 10px;
    margin-top: 1.35rem !important;
    margin-bottom: 1rem !important;
    color: inherit !important;
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

/* ==========================================================
   METRIC CARDS - ADAPTIVE
   ========================================================== */

div[data-testid="metric-container"] {
    background: rgba(37, 99, 235, 0.045) !important;
    border: 1px solid rgba(96, 165, 250, 0.30) !important;
    padding: 1rem 1rem !important;
    border-radius: 16px !important;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

div[data-testid="metric-container"] label,
div[data-testid="metric-container"] [data-testid="stMetricLabel"],
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: inherit !important;
}

/* ==========================================================
   EXISTING BOXES - ADAPTIVE
   ========================================================== */

.scope-box {
    background: rgba(37, 99, 235, 0.04) !important;
    border: 1px solid rgba(96, 165, 250, 0.25) !important;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    color: inherit !important;
}

.findings-box {
    border-left: 6px solid #D97706 !important;
    background: rgba(217, 119, 6, 0.08) !important;
    border-top: 1px solid rgba(217,119,6,0.20);
    border-right: 1px solid rgba(217,119,6,0.20);
    border-bottom: 1px solid rgba(217,119,6,0.20);
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    color: inherit !important;
}

.note-box {
    border-left: 5px solid #2563EB !important;
    background: rgba(37, 99, 235, 0.08) !important;
    border-top: 1px solid rgba(37,99,235,0.20);
    border-right: 1px solid rgba(37,99,235,0.20);
    border-bottom: 1px solid rgba(37,99,235,0.20);
    color: inherit !important;
}

.theme-highlight-box {
    border-left: 5px solid #7C3AED !important;
    background: rgba(124, 58, 237, 0.08) !important;
    border-top: 1px solid rgba(124,58,237,0.20);
    border-right: 1px solid rgba(124,58,237,0.20);
    border-bottom: 1px solid rgba(124,58,237,0.20);
    color: inherit !important;
}

/* ==========================================================
   CHART AND TABLE CONTAINERS - ADAPTIVE
   ========================================================== */

.stPlotlyChart {
    background: rgba(37, 99, 235, 0.025);
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-radius: 14px;
    padding: 0.50rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid rgba(96, 165, 250, 0.25);
}

/* ==========================================================
   HERO - ADAPTIVE
   ========================================================== */

.hero-badge {
    background: rgba(217,119,6,0.10);
    box-shadow: 0 4px 12px rgba(217,119,6,0.08);
}

.hero-title,
.hero-subtitle,
.hero-description {
    color: inherit;
}

/* Do not force chart text colour here. Plotly should follow its own theme. */

</style>
""", unsafe_allow_html=True)


def render_status_line():
    """
    Native Streamlit status line. No HTML, so it is safe for PDF export.
    """
    st.caption(
        "🔵 INTERIM DATASET · 🟢 FRAMEWORK ALIGNED · 🟠 FINAL REFRESH PENDING · 🟣 EXECUTIVE OVERVIEW"
    )
