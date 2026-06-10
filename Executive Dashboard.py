# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# SPRINT 1.6a - PRODUCTION FOUNDATION
#
# Research:
# Pavement Performance Management Under Data Constraints
# Perspectives of Practitioners in Kenya
#
# Status:
# READY FOR SPRINT 2 VISUALIZATIONS
# ==========================================================

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from utils.data_cleaning import (
    clean_master_dataset,
    index_diagnostics
)

# ==========================================================
# PAGE CONFIG
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

/* HERO */

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

/* KPI CARDS */

div[data-testid="metric-container"]{
    border-radius:16px;
    padding:18px;
    border:1px solid rgba(128,128,128,0.25);
    background:rgba(15,23,42,0.05);
}

/* FINDINGS */

.findings-box{
    border-left:6px solid #D97706;
    background:rgba(217,119,6,0.08);
    padding:20px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

/* SCOPE */

.scope-box{
    border-radius:15px;
    padding:20px;
    border:1px solid rgba(128,128,128,0.25);
    margin-top:20px;
    margin-bottom:20px;
}

/* SECTION TITLE */

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:15px;
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

    st.error(f"Dataset Loading Error: {e}")
    st.stop()

master_df = clean_master_dataset(
    master_df
)

# ==========================================================
# AUTO DETECT COLUMNS
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
# HELPERS
# ==========================================================

def safe_mean(df, column):

    try:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if len(values) == 0:
            return 0

        return round(values.mean(), 1)

    except:
        return 0

# ==========================================================
# KPIs
# ==========================================================

responses = len(filtered_df)

organizations = (
    filtered_df[agency_col].nunique()
    if agency_col else 0
)

dmi = safe_mean(indices_df, "DMI")
fmi = safe_mean(indices_df, "FMI")
rri = safe_mean(indices_df, "RRI")
dri = safe_mean(indices_df, "DRI")

# ==========================================================
# HERO
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
<li><b>Organizations Represented:</b> KeRRA, KURA, KeNHA, KRB and MTRD</li>
<li><b>Open-ended Questions Analysed:</b> Q27 and Q28</li>
<li><b>Themes Identified:</b> 6</li>
<li><b>Study Focus:</b> Pavement Performance Management Under Data Constraints</li>
</ul>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# THEME ANALYSIS
# ==========================================================

theme_results = []

for col in theme_df.columns:

    if col in THEME_DISPLAY_NAMES:

        mentions = pd.to_numeric(
            theme_df[col],
            errors="coerce"
        ).fillna(0).sum()

        theme_results.append({
            "Theme":
                THEME_DISPLAY_NAMES[col],

            "Mentions":
                int(mentions)
        })

theme_summary = pd.DataFrame(theme_results)

top_theme = "Not Available"

if not theme_summary.empty:

    top_theme = (
        theme_summary
        .sort_values(
            "Mentions",
            ascending=False
        )
        .iloc[0]["Theme"]
    )

# ==========================================================
# EXECUTIVE FINDINGS
# ==========================================================

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
Respondents highlighted the need for
improved forecasting capability,
stronger data systems,
capacity building,
and evidence-based pavement management.
</li>

</ul>

</div>
""",
unsafe_allow_html=True
)

# ==========================================================
# KPI SUMMARY
# ==========================================================

st.markdown(
"<div class='section-title'>Executive KPI Summary</div>",
unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Respondents", responses)

with c2:
    st.metric("Organizations", organizations)

with c3:
    st.metric("Data Maturity Index (DMI)", dmi)

c4, c5, c6 = st.columns(3)

with c4:
    st.metric("Forecasting Maturity Index (FMI)", fmi)

with c5:
    st.metric("Reconstruction Readiness Index (RRI)", rri)

with c6:
    st.metric("Digital Readiness Index (DRI)", dri)

# ==========================================================
# SPRINT 2
# EXECUTIVE VISUALIZATIONS & ANALYTICS
# ==========================================================

st.markdown("""
<div class='section-title'>
Executive Analytics Dashboard
</div>
""", unsafe_allow_html=True)

# ==========================================================
# PREPARE THEME DATA
# ==========================================================

theme_results = []

for col in theme_df.columns:

    if col in THEME_DISPLAY_NAMES:

        mentions = pd.to_numeric(
            theme_df[col],
            errors="coerce"
        ).fillna(0).sum()

        theme_results.append({

            "Theme":
                THEME_DISPLAY_NAMES[col],

            "Mentions":
                int(mentions)

        })

theme_summary = pd.DataFrame(
    theme_results
)

# ==========================================================
# ROW 1
# AGENCY DISTRIBUTION + THEME FREQUENCY
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Agency Distribution")

    if agency_col:

        agency_counts = (

            master_df[agency_col]
            .value_counts()
            .reset_index()

        )

        agency_counts.columns = [
            "Agency",
            "Responses"
        ]

        fig_agency = px.pie(

            agency_counts,

            names="Agency",

            values="Responses",

            hole=0.55

        )

        fig_agency.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_agency,
            use_container_width=True
        )

with col2:

    st.markdown("### Theme Frequency Analysis")

    if not theme_summary.empty:

        fig_theme = px.bar(

            theme_summary.sort_values(
                "Mentions",
                ascending=True
            ),

            x="Mentions",

            y="Theme",

            orientation="h"

        )

        fig_theme.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_theme,
            use_container_width=True
        )

# ==========================================================
# ROW 2
# THEME PERCENTAGE DONUT
# ==========================================================

st.markdown("### Theme Distribution")

if not theme_summary.empty:

    total_mentions = theme_summary[
        "Mentions"
    ].sum()

    if total_mentions > 0:

        theme_summary["Percentage"] = (

            theme_summary["Mentions"]

            / total_mentions

        ) * 100

        fig_theme_pct = px.pie(

            theme_summary,

            names="Theme",

            values="Percentage",

            hole=0.60

        )

        fig_theme_pct.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_theme_pct,
            use_container_width=True
        )

# ==========================================================
# GAUGE FUNCTION
# ==========================================================

def gauge_chart(title, value):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=value,

            title={"text": title},

            gauge={

                "axis": {

                    "range": [0, 100]

                }

            }

        )

    )

    fig.update_layout(
        height=300
    )

    return fig

# ==========================================================
# ROW 3
# DMI / FMI
# ==========================================================

g1, g2 = st.columns(2)

with g1:

    st.plotly_chart(

        gauge_chart(
            "Data Maturity Index (DMI)",
            dmi
        ),

        use_container_width=True

    )

with g2:

    st.plotly_chart(

        gauge_chart(
            "Forecasting Maturity Index (FMI)",
            fmi
        ),

        use_container_width=True

    )

# ==========================================================
# ROW 4
# RRI / DRI
# ==========================================================

g3, g4 = st.columns(2)

with g3:

    st.plotly_chart(

        gauge_chart(
            "Reconstruction Readiness Index (RRI)",
            rri
        ),

        use_container_width=True

    )

with g4:

    st.plotly_chart(

        gauge_chart(
            "Digital Readiness Index (DRI)",
            dri
        ),

        use_container_width=True

    )

# ==========================================================
# NATIONAL READINESS SUMMARY
# ==========================================================

st.markdown("""
<div class='section-title'>
National Readiness Summary
</div>
""", unsafe_allow_html=True)

summary_df = pd.DataFrame({

    "Index": [

        "Data Maturity Index",

        "Forecasting Maturity Index",

        "Reconstruction Readiness Index",

        "Digital Readiness Index"

    ],

    "Score": [

        dmi,

        fmi,

        rri,

        dri

    ]

})

st.dataframe(
    summary_df,
    use_container_width=True
)

# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

st.markdown("""
<div class='section-title'>
Executive Insights
</div>
""", unsafe_allow_html=True)

top_theme = "Not Available"

if not theme_summary.empty:

    top_theme = (

        theme_summary

        .sort_values(
            "Mentions",
            ascending=False
        )

        .iloc[0]["Theme"]

    )

st.info(f"""

### Key Findings

• Total Respondents: **{responses}**

• Organizations Represented: **{organizations}**

• Dominant Theme: **{top_theme}**

• Data Maturity Index: **{dmi}**

• Forecasting Maturity Index: **{fmi}**

• Reconstruction Readiness Index: **{rri}**

• Digital Readiness Index: **{dri}**

### Interpretation

The survey findings suggest that practitioners
recognize the importance of forecasting,
data-driven pavement management,
institutional strengthening,
capacity development,
and improved use of pavement condition data.

The relatively moderate DMI and FMI scores
suggest opportunities for strengthening
data collection systems and forecasting
capabilities across road agencies.

""")

# ==========================================================
# THEME FREQUENCY SUMMARY
# ==========================================================

st.markdown(
"<div class='section-title'>Theme Frequency Summary</div>",
unsafe_allow_html=True
)

if not theme_summary.empty:

    st.dataframe(
        theme_summary.sort_values(
            "Mentions",
            ascending=False
        ),
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
    "Overall_Score",
    "Overall_Rank"
]

available_columns = [

    col for col in benchmark_columns

    if col in benchmark_df.columns
]

if available_columns:

    st.dataframe(
        benchmark_df[
            available_columns
        ],
        use_container_width=True
    )

else:

    st.info(
        "Benchmark dataset not available."
    )

# ==========================================================
# DATASET HEALTH
# ==========================================================

with st.expander("Dataset Health"):

    health_df = pd.DataFrame({

        "Dataset": [
            "Clean Master",
            "Multi-Select",
            "Theme Dataset",
            "Benchmark Dataset",
            "Indices Dataset"
        ],

        "Records": [
            len(master_df),
            len(multi_df),
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

        st.write(master_df.columns)
        st.write(theme_df.columns)
        st.write(indices_df.columns)
        st.write(benchmark_df.columns)

