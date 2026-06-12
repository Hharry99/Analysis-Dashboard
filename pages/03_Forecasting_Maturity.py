# ==========================================================
# FORECASTING MATURITY ANALYSIS
# Sprint 3A - Page 3
# Polished Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Forecasting Maturity Analysis",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# VISUAL STYLE SETTINGS
# ==========================================================

COLOR_SEQUENCE = px.colors.qualitative.Set2
BAR_COLOR_SEQUENCE = px.colors.qualitative.Bold
HEATMAP_SCALE = "YlGnBu"

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:15px;
}

.insight-box{
    border-left:6px solid #7C3AED;
    background:rgba(124,58,237,0.08);
    padding:18px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

.warning-note{
    border-left:6px solid #F59E0B;
    background:rgba(245,158,11,0.10);
    padding:16px;
    border-radius:10px;
    margin-top:12px;
    margin-bottom:18px;
}

div[data-testid="metric-container"]{
    border-radius:16px;
    padding:18px;
    border:1px solid rgba(128,128,128,0.25);
    background:rgba(15,23,42,0.05);
}

</style>
""",
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    master = pd.read_csv(
        "data/clean_master.csv"
    )

    indices = pd.read_csv(
        "data/indices_dataset.csv"
    )

    return master, indices


master_df, indices_df = load_data()

master_df = clean_master_dataset(
    master_df
)

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

AGENCY_COL = "Q1. What agency do you work for?"
INDEX_COL = "FMI"

REQUIRED_MASTER_COLS = [
    AGENCY_COL
]

REQUIRED_INDEX_COLS = [
    INDEX_COL
]

# ==========================================================
# VALIDATION
# ==========================================================

missing_master_cols = [
    col for col in REQUIRED_MASTER_COLS
    if col not in master_df.columns
]

missing_index_cols = [
    col for col in REQUIRED_INDEX_COLS
    if col not in indices_df.columns
]

if missing_master_cols:

    st.error(
        f"Missing required master dataset columns: {missing_master_cols}"
    )

    st.stop()

if missing_index_cols:

    st.error(
        f"Missing required indices dataset columns: {missing_index_cols}"
    )

    st.stop()

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def classify_maturity(score):

    if pd.isna(score):
        return "Not Available"

    if score < 40:
        return "Emerging"

    if score < 60:
        return "Developing"

    if score < 80:
        return "Advanced"

    return "Leading"


def add_percentage(df_in, count_col):

    df_out = df_in.copy()

    total = df_out[count_col].sum()

    if total > 0:

        df_out["Percentage"] = (
            df_out[count_col]
            /
            total
            *
            100
        ).round(1)

    else:

        df_out["Percentage"] = 0

    return df_out

# ==========================================================
# PREPARE DATA
# ==========================================================

master_df = master_df.reset_index(
    drop=True
)

indices_df = indices_df.reset_index(
    drop=True
)

analysis_df = pd.concat(
    [
        master_df[
            [
                AGENCY_COL
            ]
        ],
        indices_df[
            [
                INDEX_COL
            ]
        ]
    ],
    axis=1
)

analysis_df[INDEX_COL] = pd.to_numeric(
    analysis_df[INDEX_COL],
    errors="coerce"
)

analysis_df = analysis_df.dropna(
    subset=[
        AGENCY_COL,
        INDEX_COL
    ]
)

if analysis_df.empty:

    st.warning(
        "No valid FMI records were found after cleaning."
    )

    st.stop()

analysis_df["Maturity Band"] = analysis_df[INDEX_COL].apply(
    classify_maturity
)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Forecasting Maturity Analysis"
)

st.markdown("""
This section evaluates forecasting capability, predictive modelling
practices, future maintenance planning and analytical readiness
across participating agencies.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_fmi = round(
    analysis_df[INDEX_COL].mean(),
    1
)

highest_fmi = round(
    analysis_df[INDEX_COL].max(),
    1
)

lowest_fmi = round(
    analysis_df[INDEX_COL].min(),
    1
)

agencies = analysis_df[
    AGENCY_COL
].nunique()

overall_band = classify_maturity(
    avg_fmi
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average FMI",
    avg_fmi
)

c2.metric(
    "Highest FMI",
    highest_fmi
)

c3.metric(
    "Lowest FMI",
    lowest_fmi
)

c4.metric(
    "Agencies",
    agencies
)

# ==========================================================
# AGENCY LEVEL SUMMARY
# ==========================================================

agency_fmi = (
    analysis_df
    .groupby(
        AGENCY_COL
    )[INDEX_COL]
    .mean()
    .reset_index()
)

agency_fmi[INDEX_COL] = (
    agency_fmi[INDEX_COL]
    .round(1)
)

agency_fmi["Maturity Band"] = agency_fmi[INDEX_COL].apply(
    classify_maturity
)

agency_fmi = agency_fmi.sort_values(
    INDEX_COL,
    ascending=False
)

top_agency = (
    agency_fmi.iloc[0][AGENCY_COL]
    if not agency_fmi.empty
    else "Not Available"
)

top_agency_score = (
    agency_fmi.iloc[0][INDEX_COL]
    if not agency_fmi.empty
    else 0
)

lowest_agency = (
    agency_fmi.iloc[-1][AGENCY_COL]
    if not agency_fmi.empty
    else "Not Available"
)

lowest_agency_score = (
    agency_fmi.iloc[-1][INDEX_COL]
    if not agency_fmi.empty
    else 0
)

# ==========================================================
# EXECUTIVE SNAPSHOT
# ==========================================================

st.markdown(
    f"""
<div class="insight-box">

<b>Forecasting Maturity Snapshot:</b><br>
The average Forecasting Maturity Index is <b>{avg_fmi}</b>, placing the
overall forecasting maturity position in the <b>{overall_band}</b> maturity band.

<br><br>
The highest average agency FMI is recorded by <b>{top_agency}</b>
(<b>{top_agency_score}</b>), while the lowest average agency FMI is recorded by
<b>{lowest_agency}</b> (<b>{lowest_agency_score}</b>).

<br><br>
This indicates that forecasting capability is developing, but there is still
need to strengthen deterioration modelling, scenario analysis, historical data
availability and evidence-based maintenance planning.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# FMI DATA CHECK
# ==========================================================

if analysis_df[INDEX_COL].nunique() <= 1:

    st.markdown(
        """
<div class="warning-note">

<b>Data Quality Note:</b>
FMI contains only one unique value. This may suggest that the index was
reconstructed as a constant rather than calculated per respondent. Review
indices_dataset.csv during the final dataset refresh.

</div>
""",
        unsafe_allow_html=True
    )

# ==========================================================
# FMI DISTRIBUTION
# ==========================================================

st.markdown(
    "<div class='section-title'>FMI Distribution</div>",
    unsafe_allow_html=True
)

fig_hist = px.histogram(
    analysis_df,
    x=INDEX_COL,
    color="Maturity Band",
    nbins=10,
    title="Distribution of Forecasting Maturity Scores",
    color_discrete_sequence=COLOR_SEQUENCE
)

fig_hist.update_layout(
    xaxis_title="Forecasting Maturity Index",
    yaxis_title="Number of Responses",
    height=480,
    bargap=0.10,
    legend_title_text="Maturity Band"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# FMI BY AGENCY
# ==========================================================

st.markdown(
    "<div class='section-title'>FMI by Agency</div>",
    unsafe_allow_html=True
)

fig_agency = px.bar(
    agency_fmi,
    x=AGENCY_COL,
    y=INDEX_COL,
    text=INDEX_COL,
    color=AGENCY_COL,
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title="Average Forecasting Maturity Index by Agency"
)

fig_agency.update_layout(
    xaxis_title="Agency",
    yaxis_title="Average FMI",
    yaxis=dict(
        range=[
            0,
            100
        ]
    ),
    height=520,
    showlegend=False
)

fig_agency.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_agency,
    use_container_width=True
)

# ==========================================================
# AGENCY RANKING
# ==========================================================

st.markdown(
    "<div class='section-title'>Agency Ranking</div>",
    unsafe_allow_html=True
)

ranking_df = agency_fmi.copy()

ranking_df["Rank"] = range(
    1,
    len(ranking_df) + 1
)

ranking_df = ranking_df[
    [
        "Rank",
        AGENCY_COL,
        INDEX_COL,
        "Maturity Band"
    ]
]

ranking_df = ranking_df.rename(
    columns={
        AGENCY_COL: "Agency",
        INDEX_COL: "FMI"
    }
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================================
# FMI HEATMAP
# ==========================================================

st.markdown(
    "<div class='section-title'>FMI Heatmap</div>",
    unsafe_allow_html=True
)

heatmap_df = agency_fmi.copy()

fig_heatmap = px.imshow(
    heatmap_df[
        [
            INDEX_COL
        ]
    ].T,
    labels=dict(
        x="Agency",
        y="Index",
        color="FMI"
    ),
    x=heatmap_df[
        AGENCY_COL
    ],
    y=[
        "FMI"
    ],
    aspect="auto",
    title="Forecasting Maturity Heatmap by Agency",
    color_continuous_scale=HEATMAP_SCALE,
    zmin=0,
    zmax=100
)

fig_heatmap.update_layout(
    height=450
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# ==========================================================
# FMI SUMMARY TABLES
# ==========================================================

with st.expander(
    "View Detailed FMI Summary Tables",
    expanded=False
):

    st.markdown(
        "### Agency FMI Summary"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.markdown(
        "### Maturity Band Distribution"
    )

    band_summary = (
        analysis_df["Maturity Band"]
        .value_counts()
        .reset_index()
    )

    band_summary.columns = [
        "Maturity Band",
        "Responses"
    ]

    band_summary = add_percentage(
        band_summary,
        "Responses"
    )

    st.dataframe(
        band_summary,
        use_container_width=True
    )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Interpretation

The average Forecasting Maturity Index (FMI) was **{avg_fmi}**, which indicates
an overall **{overall_band}** level of forecasting maturity across participating
agencies.

This reflects the extent to which agencies use forecasting tools, predictive
models, scenario analysis and future maintenance planning in pavement
management.

The findings suggest that forecasting capability is developing, but there remain
opportunities to strengthen analytical capability, deterioration modelling,
forecasting techniques and evidence-based planning.

Agency-level differences highlight opportunities for targeted capacity building,
improved historical data availability and stronger integration of forecasting
outputs into maintenance planning, budgeting and investment decision-making.
""")
