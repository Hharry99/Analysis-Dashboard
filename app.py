# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# SPRINT 1 - FINAL STABLE VERSION
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Pavement Performance Management Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:38px;
    font-weight:700;
    margin-bottom:5px;
}

.sub-title{
    text-align:center;
    color:#7A7A7A;
    margin-bottom:30px;
}

div[data-testid="metric-container"]{
    border:1px solid rgba(128,128,128,0.25);
    padding:15px;
    border-radius:12px;
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
# LOAD DATA
# ==========================================================

try:

    (
        master_df,
        multi_df,
        indices_df,
        theme_df,
        benchmark_df
    ) = load_data()

except Exception as e:

    st.error(f"Dataset loading error: {e}")
    st.stop()

# ==========================================================
# FIND IMPORTANT COLUMNS
# ==========================================================

agency_col = next(
    (
        c for c in master_df.columns
        if "agency" in c.lower()
    ),
    None
)

position_col = next(
    (
        c for c in master_df.columns
        if "position" in c.lower()
    ),
    None
)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div class='main-title'>
    Pavement Performance Management Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
    Pavement Performance Management Under Data Constraints:
    Perspectives of Practitioners in Kenya
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Dashboard Filters")

selected_orgs = []

if agency_col:

    selected_orgs = st.sidebar.multiselect(
        "Organization",
        sorted(
            master_df[agency_col]
            .dropna()
            .unique()
        )
    )

selected_positions = []

if position_col:

    selected_positions = st.sidebar.multiselect(
        "Position",
        sorted(
            master_df[position_col]
            .dropna()
            .unique()
        )
    )

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = master_df.copy()

if agency_col and selected_orgs:

    filtered_df = filtered_df[
        filtered_df[agency_col]
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

def safe_mean(df, col):

    if col not in df.columns:
        return 0

    return round(
        pd.to_numeric(
            df[col],
            errors="coerce"
        )
        .fillna(0)
        .mean(),
        1
    )

kpi_responses = len(filtered_df)

if agency_col:

    kpi_orgs = filtered_df[
        agency_col
    ].nunique()

else:

    kpi_orgs = 0

dmi = safe_mean(indices_df, "DMI")
fmi = safe_mean(indices_df, "FMI")
rri = safe_mean(indices_df, "RRI")
dri = safe_mean(indices_df, "DRI")

# ==========================================================
# KPI DISPLAY
# ==========================================================

st.subheader("Executive KPI Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Respondents",
        kpi_responses
    )

with c2:
    st.metric(
        "Organizations",
        kpi_orgs
    )

with c3:
    st.metric(
        "Data Maturity Index",
        dmi
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Forecasting Maturity",
        fmi
    )

with c5:
    st.metric(
        "Reconstruction Readiness",
        rri
    )

with c6:
    st.metric(
        "Digital Readiness",
        dri
    )

# ==========================================================
# THEME SUMMARY
# ==========================================================

st.subheader("Theme Frequency Summary")

theme_cols = []

for col in theme_df.columns:

    if col not in [
        "Response_ID",
        "Agency"
    ]:

        theme_cols.append(col)

if len(theme_cols) > 0:

    theme_summary = pd.DataFrame({

        "Theme": theme_cols,

        "Mentions": [
            theme_df[col].sum()
            for col in theme_cols
        ]

    })

    st.dataframe(
        theme_summary.sort_values(
            "Mentions",
            ascending=False
        ),
        use_container_width=True
    )

else:

    st.warning(
        "No theme columns found."
    )

# ==========================================================
# BENCHMARK TABLE
# ==========================================================

st.subheader(
    "Organization Benchmark Ranking"
)

if not benchmark_df.empty:

    st.dataframe(
        benchmark_df,
        use_container_width=True
    )

else:

    st.info(
        "Benchmark dataset is empty."
    )

# ==========================================================
# DATASET DIAGNOSTICS
# REMOVE AFTER TESTING
# ==========================================================

with st.expander(
    "Dataset Diagnostics"
):

    st.write(
        "MASTER DATASET COLUMNS"
    )

    st.write(
        list(master_df.columns)
    )

    st.write(
        "INDICES DATASET COLUMNS"
    )

    st.write(
        list(indices_df.columns)
    )

    st.write(
        "THEME DATASET COLUMNS"
    )

    st.write(
        list(theme_df.columns)
    )

    st.write(
        "BENCHMARK DATASET COLUMNS"
    )

    st.write(
        list(benchmark_df.columns)
    )

# ==========================================================
# FOOTER
# ==========================================================

st.success(
    "Sprint 1 Completed Successfully"
)

st.info(
    "Ready for Sprint 2: Executive Dashboard Visualizations"
)
