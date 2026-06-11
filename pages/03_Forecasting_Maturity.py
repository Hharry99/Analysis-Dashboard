# ==========================================================
# FORECASTING MATURITY ANALYSIS
# Sprint 3A - Page 3
# Framework Aligned Production Version
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
# PREPARE DATA
# ==========================================================

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
# FMI DISTRIBUTION
# ==========================================================

st.markdown(
    "## FMI Distribution"
)

fig_hist = px.histogram(
    analysis_df,
    x=INDEX_COL,
    nbins=10,
    title="Distribution of Forecasting Maturity Scores"
)

fig_hist.update_layout(
    xaxis_title="Forecasting Maturity Index",
    yaxis_title="Number of Responses",
    height=450
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# FMI DATA CHECK
# ==========================================================

if analysis_df[INDEX_COL].nunique() <= 1:

    st.warning("""
    FMI contains only one unique value.

    This suggests the index may have been reconstructed as a constant
    rather than calculated per respondent.

    Review indices_dataset.csv during the final dataset refresh.
    """)

# ==========================================================
# FMI BY AGENCY
# ==========================================================

st.markdown(
    "## FMI by Agency"
)

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

agency_fmi = agency_fmi.sort_values(
    INDEX_COL,
    ascending=False
)

fig_agency = px.bar(
    agency_fmi,
    x=AGENCY_COL,
    y=INDEX_COL,
    text=INDEX_COL,
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
    height=500
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
    "## Agency Ranking"
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
        INDEX_COL
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
    "## FMI Heatmap"
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
    title="Forecasting Maturity Heatmap by Agency"
)

fig_heatmap.update_layout(
    height=450
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Interpretation

The average Forecasting Maturity Index (FMI) was **{avg_fmi}**.

This reflects the extent to which participating agencies use forecasting
tools, predictive models, scenario analysis and future maintenance planning
in pavement management.

The findings suggest that forecasting capability is developing, but there
remain opportunities to strengthen analytical capability, deterioration
modelling, forecasting techniques and evidence-based planning.

Agency-level differences highlight opportunities for targeted capacity
building, improved data availability and stronger integration of forecasting
outputs into maintenance planning and investment decision-making.
""")
