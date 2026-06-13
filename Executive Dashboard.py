# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# EXECUTIVE DASHBOARD - FULL RESEARCH OVERVIEW POLISHED VERSION
#
# Research:
# Pavement Performance Management Under Data Constraints
# Perspectives of Practitioners in Kenya
#
# Purpose:
# This page provides a high-level overview of the full study:
# respondent profile, maturity indices, survey domains,
# benchmarking, qualitative insights, dataset health and
# strategic priorities.
# ==========================================================

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_cleaning import (
    clean_master_dataset,
    index_diagnostics
)

from utils.theme_coder import build_theme_dataset
from utils.theme_dictionary import THEME_KEYWORDS

from utils.dashboard_style import apply_dashboard_style

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

STRATEGIC_THEME_DISPLAY_NAMES = {
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

Q27_COL = (
    "Q27. What practical improvements in data systems, institutional "
    "approaches, or technical capacity would most strengthen pavement "
    "performance management in Kenya?"
)

Q28_COL = (
    "Q28. Do you have any additional comments or recommendations regarding "
    "forecasting, modelling, or use of condition data in road asset "
    "management and planning?"
)

TEXT_COLUMNS = [
    Q27_COL,
    Q28_COL
]

INDEX_COLS = [
    "DMI",
    "FMI",
    "RRI",
    "DRI"
]

INDEX_LABELS = {
    "DMI": "Data Maturity",
    "FMI": "Forecasting Maturity",
    "RRI": "Reconstruction Readiness",
    "DRI": "Digital Readiness"
}

# ==========================================================
# VISUAL STYLE SETTINGS
# ==========================================================

COLOR_SEQUENCE = px.colors.qualitative.Set2
ALT_COLOR_SEQUENCE = px.colors.qualitative.Pastel
THEME_COLOR_SEQUENCE = px.colors.qualitative.Bold

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

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

div[data-testid="metric-container"]{
    border-radius:16px;
    padding:18px;
    border:1px solid rgba(128,128,128,0.25);
    background:rgba(15,23,42,0.05);
}

.scope-box{
    border-radius:15px;
    padding:20px;
    border:1px solid rgba(128,128,128,0.25);
    margin-top:20px;
    margin-bottom:20px;
}

.findings-box{
    border-left:6px solid #D97706;
    background:rgba(217,119,6,0.08);
    padding:20px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

.note-box{
    border-left:5px solid #2563EB;
    background:rgba(37,99,235,0.08);
    padding:15px;
    border-radius:10px;
    margin-top:10px;
    margin-bottom:20px;
}

.theme-highlight-box{
    border-left:5px solid #7C3AED;
    background:rgba(124,58,237,0.08);
    padding:18px;
    border-radius:12px;
    margin-top:10px;
    margin-bottom:20px;
}

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:15px;
}

</style>
""",
    unsafe_allow_html=True
)

# ==========================================================
# DASHBOARD VISUAL POLISH ADDITIONS
# ==========================================================

apply_dashboard_style()

# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_data():

    master = pd.read_csv(
        "data/clean_master.csv"
    )

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

    return master, multiselect, indices, themes, benchmark


try:

    (
        master_df,
        multi_df,
        indices_df,
        theme_df,
        benchmark_df
    ) = load_data()

except Exception as e:

    st.error(
        f"Dataset Loading Error: {e}"
    )

    st.stop()

master_df = clean_master_dataset(
    master_df
)

# ==========================================================
# COLUMN DETECTION
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

level_col = next(
    (
        c for c in master_df.columns
        if "level" in c.lower()
    ),
    None
)

# ==========================================================
# VALIDATION
# ==========================================================

if agency_col is None:

    st.error(
        "Agency column could not be detected in clean_master.csv."
    )

    st.stop()

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def safe_mean(df, column):

    try:

        if column not in df.columns:
            return 0

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

    except Exception:
        return 0


def safe_numeric(df, columns):

    df = df.copy()

    for col in columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


def comma_list(values):

    clean_values = [
        str(v)
        for v in values
        if pd.notna(v)
    ]

    return ", ".join(
        sorted(clean_values)
    )


def gauge_chart(title, value):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={
                "text": title
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#2563EB"
                },
                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#FEE2E2"
                    },
                    {
                        "range": [40, 60],
                        "color": "#FEF3C7"
                    },
                    {
                        "range": [60, 80],
                        "color": "#DBEAFE"
                    },
                    {
                        "range": [80, 100],
                        "color": "#DCFCE7"
                    }
                ]
            }
        )
    )

    fig.update_layout(
        height=300
    )

    return fig


def round_display_columns(df, columns, decimals=1):

    df = df.copy()

    for col in columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).round(decimals)

    return df

# ==========================================================
# PREPARE ANALYSIS DATA
# ==========================================================

master_df = master_df.reset_index(
    drop=True
)

indices_df = indices_df.reset_index(
    drop=True
)

available_index_cols = [
    col for col in INDEX_COLS
    if col in indices_df.columns
]

indices_df = safe_numeric(
    indices_df,
    available_index_cols
)

analysis_df = pd.concat(
    [
        master_df,
        indices_df[available_index_cols]
    ],
    axis=1
)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header(
    "Dashboard Filters"
)

selected_agencies = st.sidebar.multiselect(
    "Agency",
    sorted(
        analysis_df[agency_col]
        .dropna()
        .unique()
    )
)

selected_positions = []

if position_col:

    selected_positions = st.sidebar.multiselect(
        "Position",
        sorted(
            analysis_df[position_col]
            .dropna()
            .unique()
        )
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = analysis_df.copy()

if selected_agencies:

    filtered_df = filtered_df[
        filtered_df[agency_col]
        .isin(selected_agencies)
    ]

if position_col and selected_positions:

    filtered_df = filtered_df[
        filtered_df[position_col]
        .isin(selected_positions)
    ]

if filtered_df.empty:

    st.warning(
        "No records found for the selected filters."
    )

    st.stop()

# ==========================================================
# CORE KPIs
# ==========================================================

responses = len(
    filtered_df
)

agencies = (
    filtered_df[agency_col]
    .nunique()
)

positions = (
    filtered_df[position_col]
    .nunique()
    if position_col
    else 0
)

agency_names = comma_list(
    master_df[agency_col]
    .dropna()
    .unique()
)

dmi = safe_mean(
    filtered_df,
    "DMI"
)

fmi = safe_mean(
    filtered_df,
    "FMI"
)

rri = safe_mean(
    filtered_df,
    "RRI"
)

dri = safe_mean(
    filtered_df,
    "DRI"
)

maturity_scores = {
    "Data Maturity": dmi,
    "Forecasting Maturity": fmi,
    "Reconstruction Readiness": rri,
    "Digital Readiness": dri
}

strongest_maturity_area = max(
    maturity_scores,
    key=maturity_scores.get
)

weakest_maturity_area = min(
    maturity_scores,
    key=maturity_scores.get
)

# ==========================================================
# BENCHMARK DATA PREPARATION
# ==========================================================

benchmark_df = benchmark_df.copy()

benchmark_numeric_cols = [
    "Overall_Score",
    "DMI",
    "FMI",
    "RRI",
    "DRI"
]

benchmark_df = safe_numeric(
    benchmark_df,
    benchmark_numeric_cols
)

if "Agency" in benchmark_df.columns and "Overall_Score" in benchmark_df.columns:

    benchmark_display_df = (
        benchmark_df
        .dropna(
            subset=[
                "Agency",
                "Overall_Score"
            ]
        )
        .sort_values(
            "Overall_Score",
            ascending=False
        )
        .drop_duplicates(
            subset=[
                "Agency"
            ],
            keep="first"
        )
        .reset_index(drop=True)
    )

    benchmark_display_df["Display_Rank"] = (
        benchmark_display_df.index + 1
    )

    benchmark_display_df = round_display_columns(
        benchmark_display_df,
        benchmark_numeric_cols,
        decimals=1
    )

else:

    benchmark_display_df = pd.DataFrame()

if not benchmark_display_df.empty:

    benchmark_agencies = (
        benchmark_display_df["Agency"]
        .nunique()
    )

    average_overall_score = round(
        benchmark_display_df["Overall_Score"].mean(),
        1
    )

    top_agency = benchmark_display_df.loc[
        benchmark_display_df["Overall_Score"].idxmax(),
        "Agency"
    ]

    top_score = benchmark_display_df["Overall_Score"].max()

    lowest_agency = benchmark_display_df.loc[
        benchmark_display_df["Overall_Score"].idxmin(),
        "Agency"
    ]

    lowest_score = benchmark_display_df["Overall_Score"].min()

else:

    benchmark_agencies = 0
    average_overall_score = 0
    top_agency = "Not Available"
    top_score = 0
    lowest_agency = "Not Available"
    lowest_score = 0

# ==========================================================
# STRATEGIC THEME ANALYSIS
# ==========================================================

strategic_theme_results = []

for col in theme_df.columns:

    if col in STRATEGIC_THEME_DISPLAY_NAMES:

        mentions = pd.to_numeric(
            theme_df[col],
            errors="coerce"
        ).fillna(0).sum()

        strategic_theme_results.append({
            "Theme":
                STRATEGIC_THEME_DISPLAY_NAMES[col],
            "Mentions":
                int(mentions)
        })

strategic_theme_summary = pd.DataFrame(
    strategic_theme_results
)

strategic_theme_groups = len(
    STRATEGIC_THEME_DISPLAY_NAMES
)

dominant_strategic_theme = "Not Available"

if not strategic_theme_summary.empty:

    dominant_strategic_theme = (
        strategic_theme_summary
        .sort_values(
            "Mentions",
            ascending=False
        )
        .iloc[0]["Theme"]
    )

# ==========================================================
# OPERATIONAL THEME ANALYSIS
# ==========================================================

operational_theme_count = len(
    THEME_KEYWORDS
)

dominant_operational_theme = "Not Available"

try:

    available_text_columns = [
        col for col in TEXT_COLUMNS
        if col in filtered_df.columns
    ]

    if available_text_columns:

        operational_theme_df = build_theme_dataset(
            df=filtered_df,
            text_columns=available_text_columns,
            agency_column=agency_col
        )

        if not operational_theme_df.empty:

            dominant_operational_theme = (
                operational_theme_df["Theme"]
                .value_counts()
                .idxmax()
            )

except Exception:

    dominant_operational_theme = "Not Available"

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
Based on {responses} practitioner responses from {agencies} road-sector agencies
</div>
""",
    unsafe_allow_html=True
)

st.caption(
    "🔵 INTERIM DATASET · 🟢 FRAMEWORK ALIGNED · 🟠 FINAL REFRESH PENDING · 🟣 EXECUTIVE OVERVIEW"
)

st.divider()

# ==========================================================
# RESEARCH OVERVIEW
# ==========================================================

st.markdown(
    f"""
<div class='scope-box'>

<h3>Research Overview</h3>

<ul>
<li><b>Survey Responses:</b> {responses}</li>
<li><b>Agencies Represented:</b> {agency_names}</li>
<li><b>Respondent Positions Captured:</b> {positions}</li>
<li><b>Main Survey Domains:</b> Data Practices, Forecasting, Reconstruction & Modelling, Digital Readiness, and Open-Ended Insights</li>
<li><b>Open-ended Questions Analysed:</b> Q27 and Q28</li>
<li><b>Study Focus:</b> Pavement Performance Management Under Data Constraints</li>
</ul>

</div>
""",
    unsafe_allow_html=True
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
<b>{responses}</b> practitioners participated across
<b>{agencies}</b> road-sector agencies.
</li>

<li>
The weakest maturity area is
<b>{weakest_maturity_area}</b>, indicating the need to strengthen
data systems, data quality and institutional data practices.
</li>

<li>
The strongest maturity area is
<b>{strongest_maturity_area}</b>, suggesting relatively stronger
readiness in that dimension.
</li>

<li>
The current benchmark leader is
<b>{top_agency}</b> with an overall score of
<b>{top_score:.1f}</b>.
</li>

<li>
Qualitative responses show that the dominant operational theme is
<b>{dominant_operational_theme}</b>.
</li>

<li>
The overall strategic priority is to improve data systems,
forecasting capability, digital transformation, institutional capacity
and evidence-based road asset management.
</li>

</ul>

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# EXECUTIVE KPI SUMMARY
# ==========================================================

st.markdown(
    "<div class='section-title'>Executive KPI Summary</div>",
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Respondents",
    responses
)

k2.metric(
    "Agencies",
    agencies
)

k3.metric(
    "Positions",
    positions
)

k4.metric(
    "Average Overall Score",
    average_overall_score
)

k5, k6, k7, k8 = st.columns(4)

k5.metric(
    "DMI",
    dmi
)

k6.metric(
    "FMI",
    fmi
)

k7.metric(
    "RRI",
    rri
)

k8.metric(
    "DRI",
    dri
)

# ==========================================================
# MATURITY OVERVIEW
# ==========================================================

st.markdown(
    "<div class='section-title'>Maturity Overview</div>",
    unsafe_allow_html=True
)

maturity_df = pd.DataFrame({
    "Maturity Dimension": list(
        maturity_scores.keys()
    ),
    "Score": list(
        maturity_scores.values()
    )
})

fig_maturity = px.bar(
    maturity_df.sort_values(
        "Score",
        ascending=True
    ),
    x="Score",
    y="Maturity Dimension",
    orientation="h",
    text="Score",
    color="Maturity Dimension",
    color_discrete_sequence=COLOR_SEQUENCE,
    title="National Maturity Overview"
)

fig_maturity.update_layout(
    xaxis_title="Average Score",
    yaxis_title="Maturity Dimension",
    xaxis=dict(
        range=[
            0,
            100
        ]
    ),
    height=450,
    showlegend=False
)

fig_maturity.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_maturity,
    use_container_width=True
)

c1, c2 = st.columns(2)

with c1:

    st.success(
        f"Strongest Maturity Area: {strongest_maturity_area} ({maturity_scores[strongest_maturity_area]:.1f})"
    )

with c2:

    st.error(
        f"Priority Improvement Area: {weakest_maturity_area} ({maturity_scores[weakest_maturity_area]:.1f})"
    )

# ==========================================================
# INDEX GAUGES
# ==========================================================

st.markdown(
    "### Maturity Index Gauges"
)

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
# SURVEY DOMAIN OVERVIEW
# ==========================================================

st.markdown(
    "<div class='section-title'>Survey Domain Overview</div>",
    unsafe_allow_html=True
)

domain_df = pd.DataFrame({
    "Survey Domain": [
        "Respondent Profile",
        "Data Practices",
        "Forecasting Practices",
        "Reconstruction & Modelling",
        "Digital Readiness",
        "Open-Ended Insights"
    ],
    "Main Questions": [
        "Q1–Q4",
        "Q5–Q15",
        "Q16–Q19",
        "Q20–Q22",
        "Q23–Q26",
        "Q27–Q28"
    ],
    "Purpose": [
        "Establishes respondent and agency background.",
        "Assesses data availability, collection, storage, governance and use.",
        "Assesses forecasting methods, confidence, barriers and decision support.",
        "Assesses readiness to use reconstructed or model-estimated condition data.",
        "Assesses familiarity with databases, AI, analytics and MCDA tools.",
        "Captures practitioner priorities, constraints and recommendations."
    ]
})

st.dataframe(
    domain_df,
    use_container_width=True
)

# ==========================================================
# BENCHMARK SNAPSHOT
# ==========================================================

st.markdown(
    "<div class='section-title'>Benchmark Snapshot</div>",
    unsafe_allow_html=True
)

b1, b2, b3, b4 = st.columns(4)

b1.metric(
    "Agencies Benchmarked",
    benchmark_agencies
)

b2.metric(
    "Benchmark Leader",
    top_agency
)

b3.metric(
    "Highest Score",
    round(
        top_score,
        1
    )
)

b4.metric(
    "Lowest Score",
    round(
        lowest_score,
        1
    )
)

if not benchmark_display_df.empty:

    benchmark_summary = benchmark_display_df[
        [
            "Display_Rank",
            "Agency",
            "Overall_Score",
            "DMI",
            "FMI",
            "RRI",
            "DRI"
        ]
    ].copy()

    benchmark_summary = benchmark_summary.rename(
        columns={
            "Display_Rank": "Rank",
            "Overall_Score": "Overall Score"
        }
    )

    st.dataframe(
        benchmark_summary,
        use_container_width=True
    )

    st.caption(
        "Note: Benchmark records will be refreshed after survey closure to ensure one final validated record per agency."
    )

# ==========================================================
# RESPONDENT AND AGENCY OVERVIEW
# ==========================================================

st.markdown(
    "<div class='section-title'>Respondent and Agency Overview</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "### Agency Distribution"
    )

    agency_counts = (
        filtered_df[agency_col]
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
        hole=0.55,
        title="Distribution of Responses by Agency",
        color_discrete_sequence=ALT_COLOR_SEQUENCE
    )

    fig_agency.update_layout(
        height=450
    )

    st.plotly_chart(
        fig_agency,
        use_container_width=True
    )

with col2:

    if level_col:

        st.markdown(
            "### Work Level Distribution"
        )

        level_counts = (
            filtered_df[level_col]
            .value_counts()
            .reset_index()
        )

        level_counts.columns = [
            "Work Level",
            "Responses"
        ]

        fig_level = px.bar(
            level_counts,
            x="Responses",
            y="Work Level",
            orientation="h",
            color="Work Level",
            color_discrete_sequence=COLOR_SEQUENCE,
            title="Respondents by Work Level"
        )

        fig_level.update_layout(
            height=450,
            showlegend=False,
            xaxis_title="Responses",
            yaxis_title="Work Level"
        )

        st.plotly_chart(
            fig_level,
            use_container_width=True
        )

# ==========================================================
# QUALITATIVE INSIGHTS SNAPSHOT
# ==========================================================

st.markdown(
    "<div class='section-title'>Qualitative Insights Snapshot</div>",
    unsafe_allow_html=True
)

q1, q2 = st.columns(2)

q1.metric(
    "Strategic Theme Groups",
    strategic_theme_groups
)

q2.metric(
    "Operational Themes",
    operational_theme_count
)

st.markdown(
    f"""
<div class='theme-highlight-box'>
<b>Dominant Operational Theme:</b>
{dominant_operational_theme}
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class='note-box'>
<b>Theme Framework Note:</b>
The Executive Dashboard summarises qualitative findings using six
strategic theme groups. The Open Ended Insights page provides the
detailed operational theme breakdown from Q27 and Q28.
</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# STRATEGIC THEME FREQUENCY
# ==========================================================

if not strategic_theme_summary.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### Strategic Theme Frequency"
        )

        fig_theme = px.bar(
            strategic_theme_summary.sort_values(
                "Mentions",
                ascending=True
            ),
            x="Mentions",
            y="Theme",
            orientation="h",
            color="Theme",
            color_discrete_sequence=THEME_COLOR_SEQUENCE,
            title="Strategic Theme Group Mentions"
        )

        fig_theme.update_layout(
            height=450,
            xaxis_title="Mentions",
            yaxis_title="Strategic Theme Group",
            showlegend=False
        )

        st.plotly_chart(
            fig_theme,
            use_container_width=True
        )

    with col2:

        st.markdown(
            "### Strategic Theme Distribution"
        )

        total_mentions = strategic_theme_summary[
            "Mentions"
        ].sum()

        if total_mentions > 0:

            strategic_theme_summary["Percentage"] = (
                strategic_theme_summary["Mentions"]
                /
                total_mentions
                *
                100
            )

            fig_theme_pct = px.pie(
                strategic_theme_summary,
                names="Theme",
                values="Percentage",
                hole=0.60,
                title="Strategic Theme Group Share",
                color_discrete_sequence=THEME_COLOR_SEQUENCE
            )

            fig_theme_pct.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_theme_pct,
                use_container_width=True
            )

# ==========================================================
# DATASET HEALTH
# ==========================================================

st.markdown(
    "<div class='section-title'>Dataset Health</div>",
    unsafe_allow_html=True
)

with st.expander(
    "View Dataset Health and Data Quality Summary",
    expanded=False
):

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

    st.markdown(
        "### Data Quality Summary"
    )

    dq_df = pd.DataFrame({
        "Metric": [
            "Unique Agencies",
            "Unique Positions"
        ],
        "Value": [
            master_df[agency_col].nunique(),
            master_df[position_col].nunique()
            if position_col
            else 0
        ]
    })

    st.dataframe(
        dq_df,
        use_container_width=True
    )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.markdown(
    "<div class='section-title'>Executive Interpretation</div>",
    unsafe_allow_html=True
)

st.info(f"""
### Overall Research Interpretation

The survey assessed pavement performance management under data constraints
across **{agencies} participating road-sector agencies** and **{responses}
practitioner responses**.

The quantitative results show that **{weakest_maturity_area}** is the main
priority improvement area, while **{strongest_maturity_area}** is the strongest
maturity dimension.

The benchmarking results currently identify **{top_agency}** as the leading
agency, with an overall benchmark score of **{top_score:.1f}**. Final rankings
will be refreshed after the survey closes and the validated dataset is updated.

The question-level analysis explains the maturity results by examining data
practices, forecasting practices, reconstruction and modelling readiness, and
digital readiness across agencies.

The qualitative findings from Q27 and Q28 provide additional context by showing
that practitioners emphasize digital transformation, stronger data systems,
forecasting capability, capacity building, funding, institutional coordination
and evidence-based road asset management.

Overall, the dashboard provides a decision-support framework for identifying
sector-wide maturity gaps, agency-level priorities and practical improvement
pathways for pavement performance management in Kenya.
""")

# ==========================================================
# DEVELOPER DIAGNOSTICS
# ==========================================================

if DEVELOPER_MODE:

    with st.expander(
        "Developer Diagnostics"
    ):

        st.write(
            "Master Columns",
            master_df.columns
        )

        st.write(
            "Theme Columns",
            theme_df.columns
        )

        st.write(
            "Indices Columns",
            indices_df.columns
        )

        st.write(
            "Benchmark Columns",
            benchmark_df.columns
        )

        st.markdown(
            "### Index Diagnostics"
        )

        diag_df = index_diagnostics(
            indices_df
        )

        st.dataframe(
            diag_df,
            use_container_width=True
        )
