# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# SPRINT 1.6 - PRODUCTION FOUNDATION
#
# Research:
# Pavement Performance Management Under Data Constraints
# Perspectives of Practitioners in Kenya
#
# Author: Harrison
# Phase: Pre-Visualization Foundation
#
# Next Sprint:
# - Plotly Charts
# - Donut Charts
# - Gauges
# - Heatmaps
# - Radar Charts
# ==========================================================

# ==========================================================
# IMPORT LIBRARIES
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
# CONFIGURATION
# ==========================================================

DEVELOPER_MODE = False

THEME_DISPLAY_NAMES = {
    "Data_Systems_Databases":
        "Data Systems & Databases",

    "Routine_Data_Collection":
        "Routine Data Collection & Monitoring",

    "Forecasting_AI_Analytics":
        "Forecasting, AI & Analytics",

    "Capacity_Building_Training":
        "Capacity Building & Training",

    "Institutional_Coordination_Policy":
        "Institutional Coordination & Policy",

    "Funding_Resource_Allocation":
        "Funding & Resource Allocation"
}

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* ======================================================
   HERO SECTION
====================================================== */

.hero-badge{
    display:inline-block;
    padding:10px 25px;
    border-radius:30px;
    border:2px solid #D97706;
    color:#D97706;
    font-weight:700;
    letter-spacing:1px;
}

.hero-title{
    font-size:48px;
    font-weight:800;
    text-align:center;
    line-height:1.15;
    margin-top:20px;
}

.hero-subtitle{
    font-size:28px;
    font-weight:600;
    text-align:center;
    color:#D97706;
    margin-top:10px;
}

.hero-description{
    text-align:center;
    color:#6B7280;
    font-size:18px;
    margin-top:10px;
}

/* ======================================================
   KPI CARDS
====================================================== */

div[data-testid="metric-container"]{
    border-radius:16px;
    padding:18px;
    border:1px solid rgba(128,128,128,0.25);
    background:rgba(15,23,42,0.05);
}

/* ======================================================
   FINDINGS BOX
====================================================== */

.findings-box{
    border-left:6px solid #D97706;
    background:rgba(217,119,6,0.08);
    padding:20px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

/* ======================================================
   SECTION TITLES
====================================================== */

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:15px;
}

/* ======================================================
   RESEARCH SCOPE CARD
====================================================== */

.scope-box{
    border-radius:15px;
    padding:20px;
    border:1px solid rgba(128,128,128,0.25);
    margin-top:20px;
    margin-bottom:20px;
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

    (
        master_df,
        multi_df,
        indices_df,
        theme_df,
        benchmark_df
    ) = load_data()

except Exception as e:

    st.error(f"Dataset Loading Error: {e}")
    st.stop()

# ==========================================================
# AUTO-DETECT IMPORTANT COLUMNS
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
# APPLY FILTERS
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
# HELPER FUNCTIONS
# ==========================================================

def safe_mean(df, column):

    try:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if len(values) == 0:
            return 0

        return round(
            values.mean(),
            1
        )

    except:
        return 0


def safe_count(df):

    return len(df)

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

responses = safe_count(filtered_df)

organizations = (
    filtered_df[agency_col].nunique()
    if agency_col else 0
)

dmi = safe_mean(indices_df, "DMI")
fmi = safe_mean(indices_df, "FMI")
rri = safe_mean(indices_df, "RRI")
dri = safe_mean(indices_df, "DRI")

# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown(
"""
<div style='text-align:center'>
<div class='hero-badge'>
📋 DOCTORAL RESEARCH
</div>
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class='hero-title'>
Pavement Performance<br>
Management under Data<br>
Constraints
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class='hero-subtitle'>
Perspectives of Practitioners in Kenya
</div>
""",
unsafe_allow_html=True
)

st.markdown(
f"""
<div class='hero-description'>
Based on {responses} practitioner responses
</div>
""",
unsafe_allow_html=True
)

st.divider()

# ==========================================================
# RESEARCH SCOPE
# ==========================================================

st.markdown(f"""
<div class='scope-box'>

<h3>Research Scope</h3>

<ul>
<li><b>Survey Responses:</b> {responses}</li>
<li><b>Organizations Represented:</b> {organizations}</li>
<li><b>Open-ended Questions Analysed:</b> Q27 & Q28</li>
<li><b>Themes Identified:</b> 6</li>
<li><b>Study Focus:</b> Pavement Performance Management Under Data Constraints</li>
</ul>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# EXECUTIVE FINDINGS
# ==========================================================

theme_totals = {}

for col in theme_df.columns:

    if col in THEME_DISPLAY_NAMES:

        theme_totals[col] = pd.to_numeric(
            theme_df[col],
            errors="coerce"
        ).fillna(0).sum()

top_theme = "Not Available"

if len(theme_totals) > 0:

    top_theme_key = max(
        theme_totals,
        key=theme_totals.get
    )

    top_theme = THEME_DISPLAY_NAMES[
        top_theme_key
    ]

st.markdown(
f"""
<div class='findings-box'>

<h4>Executive Findings</h4>

<ul>

<li>
<b>{responses}</b> practitioners participated in the survey.
</li>

<li>
<b>{organizations}</b> organizations were represented.
</li>

<li>
Most frequently cited theme:
<b>{top_theme}</b>
</li>

<li>
Average Digital Readiness Index:
<b>{dri}</b>
</li>

<li>
Respondents emphasized stronger data systems,
forecasting capability and institutional capacity.
</li>

</ul>

</div>
""",
unsafe_allow_html=True
)

# ==========================================================
# KPI SECTION
# ==========================================================

st.markdown(
"<div class='section-title'>Executive KPI Summary</div>",
unsafe_allow_html=True
)

k1, k2, k3 = st.columns(3)

with k1:
    st.metric(
        "Respondents",
        responses
    )

with k2:
    st.metric(
        "Organizations",
        organizations
    )

with k3:
    st.metric(
        "Data Maturity Index (DMI)",
        dmi
    )

k4, k5, k6 = st.columns(3)

with k4:
    st.metric(
        "Forecasting Maturity Index (FMI)",
        fmi
    )

with k5:
    st.metric(
        "Reconstruction Readiness Index (RRI)",
        rri
    )

with k6:
    st.metric(
        "Digital Readiness Index (DRI)",
        dri
    )

# ==========================================================
# THEME FREQUENCY SUMMARY
# ==========================================================

st.markdown(
"<div class='section-title'>Theme Frequency Summary</div>",
unsafe_allow_html=True
)

theme_results = []

for col in theme_df.columns:

    if col in THEME_DISPLAY_NAMES:

        total = pd.to_numeric(
            theme_df[col],
            errors="coerce"
        ).fillna(0).sum()

        theme_results.append({

            "Theme":
                THEME_DISPLAY_NAMES[col],

            "Mentions":
                int(total)

        })

theme_summary = pd.DataFrame(
    theme_results
)

if not theme_summary.empty:

    theme_summary = theme_summary.sort_values(
        "Mentions",
        ascending=False
    )

    st.dataframe(
        theme_summary,
        use_container_width=True
    )

else:

    st.warning(
        "Theme dataset not populated."
    )

# ==========================================================
# ORGANIZATION BENCHMARK SUMMARY
# ==========================================================

st.markdown(
"<div class='section-title'>Organization Benchmark Summary</div>",
unsafe_allow_html=True
)

benchmark_columns = [
    "Agency",
    "DMI",
    "FMI",
    "RRI",
    "DRI",
    "Overall_Rank"
]

available_columns = [

    col for col in benchmark_columns

    if col in benchmark_df.columns
]

if len(available_columns) > 0:

    st.dataframe(
        benchmark_df[
            available_columns
        ],
        use_container_width=True
    )

else:

    st.info(
        "Benchmark scores not yet available."
    )

# ==========================================================
# DATASET HEALTH
# ==========================================================

with st.expander("Dataset Health"):

    health_df = pd.DataFrame({

        "Dataset": [

            "Master Dataset",
            "Theme Dataset",
            "Benchmark Dataset",
            "Indices Dataset"

        ],

        "Records": [

            len(master_df),
            len(theme_df),
            len(benchmark_df),
            len(indices_df)

        ]

    })

    st.dataframe(
        health_df,
        use_container_width=True
    )

# ==========================================================
# DEVELOPER DIAGNOSTICS
# ==========================================================

if DEVELOPER_MODE:

    with st.expander(
        "Developer Diagnostics"
    ):

        st.write("MASTER DATASET")
        st.write(
            list(master_df.columns)
        )

        st.write("THEME DATASET")
        st.write(
            list(theme_df.columns)
        )

        st.write("INDICES DATASET")
        st.write(
            list(indices_df.columns)
        )

        st.write("BENCHMARK DATASET")
        st.write(
            list(benchmark_df.columns)
        )

# ==========================================================
# FOOTER
# ==========================================================

st.success(
    "Sprint 1.6 Production Foundation Completed Successfully"
)

st.info(
    "Ready for Sprint 2: Executive Visualizations and Interactive Analytics"
)
