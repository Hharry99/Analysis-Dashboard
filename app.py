# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# Sprint 1 - Core Engine & Data Architecture
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Pavement Performance Management Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# Works well in both Light and Dark Mode
# ==========================================================

st.markdown("""
<style>

.main-title {
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    padding: 10px;
}

.section-box {
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(128,128,128,0.3);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_data():

    master = pd.read_csv("data/clean_master.csv")

    multiselect = pd.read_csv(
        "data/multiselect_dataset.csv"
    )

    indices = pd.read_csv(
        "data/indices_dataset.csv"
    )

    themes = pd.read_csv(
        "data/theme_dataset.csv"
    )

    benchmark = pd.read_csv(
        "data/benchmark_dataset.csv"
    )

    return (
        master,
        multiselect,
        indices,
        themes,
        benchmark
    )

# ==========================================================
# LOAD DATASETS
# ==========================================================

try:

    master_df, multi_df, indices_df, theme_df, benchmark_df = load_data()

except Exception as e:

    st.error(f"Error loading datasets: {e}")
    st.stop()

# ==========================================================
# TITLE
# ==========================================================

st.markdown(
    """
    <div class='main-title'>
    Pavement Performance Management Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Pavement Performance Management Under Data Constraints: Perspectives of Practitioners in Kenya"
)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Dashboard Filters")

# Organization Filter

if "Agency" in master_df.columns:

    selected_orgs = st.sidebar.multiselect(
        "Organization",
        options=sorted(
            master_df["Agency"]
            .dropna()
            .unique()
        )
    )

else:
    selected_orgs = []

# Position Filter

position_col = None

for col in master_df.columns:

    if "position" in col.lower():

        position_col = col
        break

if position_col:

    selected_positions = st.sidebar.multiselect(
        "Position",
        options=sorted(
            master_df[position_col]
            .dropna()
            .unique()
        )
    )

else:
    selected_positions = []

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = master_df.copy()

if selected_orgs:

    filtered_df = filtered_df[
        filtered_df["Agency"]
        .isin(selected_orgs)
    ]

if position_col and selected_positions:

    filtered_df = filtered_df[
        filtered_df[position_col]
        .isin(selected_positions)
    ]

# ==========================================================
# KPI ENGINE
# ==========================================================

def calculate_kpis():

    kpis = {}

    kpis["Respondents"] = len(master_df)

    if "Agency" in master_df.columns:
        kpis["Organizations"] = (
            master_df["Agency"]
            .nunique()
        )
    else:
        kpis["Organizations"] = 0

    if "DMI" in indices_df.columns:
        kpis["DMI"] = round(
            indices_df["DMI"].mean(),
            1
        )
    else:
        kpis["DMI"] = 0

    if "FMI" in indices_df.columns:
        kpis["FMI"] = round(
            indices_df["FMI"].mean(),
            1
        )
    else:
        kpis["FMI"] = 0

    if "RRI" in indices_df.columns:
        kpis["RRI"] = round(
            indices_df["RRI"].mean(),
            1
        )
    else:
        kpis["RRI"] = 0

    if "DRI" in indices_df.columns:
        kpis["DRI"] = round(
            indices_df["DRI"].mean(),
            1
        )
    else:
        kpis["DRI"] = 0

    return kpis

# ==========================================================
# DISPLAY KPI CARDS
# ==========================================================

kpis = calculate_kpis()

st.subheader("Executive KPI Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Respondents",
        kpis["Respondents"]
    )

with c2:
    st.metric(
        "Organizations",
        kpis["Organizations"]
    )

with c3:
    st.metric(
        "Data Maturity Index",
        kpis["DMI"]
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Forecasting Maturity",
        kpis["FMI"]
    )

with c5:
    st.metric(
        "Reconstruction Readiness",
        kpis["RRI"]
    )

with c6:
    st.metric(
        "Digital Readiness",
        kpis["DRI"]
    )

# ==========================================================
# THEME ENGINE
# ==========================================================

THEMES = [
    "Data Systems & Databases",
    "Routine Data Collection & Monitoring",
    "Forecasting, AI & Analytics",
    "Capacity Building & Training",
    "Institutional Coordination & Policy",
    "Funding & Resource Allocation"
]

def calculate_theme_frequency():

    results = []

    for theme in THEMES:

        if theme in theme_df.columns:

            count = theme_df[theme].sum()

            results.append({
                "Theme": theme,
                "Mentions": count
            })

    return pd.DataFrame(results)

# ==========================================================
# THEME TABLE
# ==========================================================

st.subheader("Theme Frequency Summary")

theme_summary = calculate_theme_frequency()

if not theme_summary.empty:

    st.dataframe(
        theme_summary,
        use_container_width=True
    )

# ==========================================================
# BENCHMARK ENGINE
# ==========================================================

def organization_rankings():

    if benchmark_df.empty:
        return pd.DataFrame()

    benchmark = benchmark_df.copy()

    required_cols = [
        "DMI",
        "FMI",
        "RRI",
        "DRI"
    ]

    missing = [
        c for c in required_cols
        if c not in benchmark.columns
    ]

    if missing:
        return pd.DataFrame()

    benchmark["Overall Score"] = (

        benchmark["DMI"]
        + benchmark["FMI"]
        + benchmark["RRI"]
        + benchmark["DRI"]

    ) / 4

    benchmark = benchmark.sort_values(
        "Overall Score",
        ascending=False
    )

    return benchmark

# ==========================================================
# BENCHMARK TABLE
# ==========================================================

st.subheader("Organization Benchmark Ranking")

ranking_df = organization_rankings()

if not ranking_df.empty:

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

else:

    st.info(
        "Benchmark dataset not yet populated."
    )

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.success(
    "Sprint 1 Completed Successfully"
)

st.info(
    "Next Step: Build Executive Dashboard Visualizations (Sprint 2)"
)
