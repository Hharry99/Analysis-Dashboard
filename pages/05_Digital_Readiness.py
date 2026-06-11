# ==========================================================
# DIGITAL READINESS ANALYSIS
# Sprint 3A - Page 5
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
    page_title="Digital Readiness Analysis",
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
INDEX_COL = "DRI"

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
    "Digital Readiness Analysis"
)

st.markdown("""
This section evaluates the adoption of digital technologies, electronic
databases, analytics platforms, decision-support systems and digital
transformation capabilities across participating agencies.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_dri = round(
    analysis_df[INDEX_COL].mean(),
    1
)

highest_dri = round(
    analysis_df[INDEX_COL].max(),
    1
)

lowest_dri = round(
    analysis_df[INDEX_COL].min(),
    1
)

agencies = analysis_df[
    AGENCY_COL
].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average DRI",
    avg_dri
)

c2.metric(
    "Highest DRI",
    highest_dri
)

c3.metric(
    "Lowest DRI",
    lowest_dri
)

c4.metric(
    "Agencies",
    agencies
)

# ==========================================================
# DRI DISTRIBUTION
# ==========================================================

st.markdown(
    "## DRI Distribution"
)

fig_hist = px.histogram(
    analysis_df,
    x=INDEX_COL,
    nbins=10,
    title="Distribution of Digital Readiness Scores"
)

fig_hist.update_layout(
    xaxis_title="Digital Readiness Index",
    yaxis_title="Number of Responses",
    height=450
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# DRI BY AGENCY
# ==========================================================

st.markdown(
    "## DRI by Agency"
)

agency_dri = (
    analysis_df
    .groupby(
        AGENCY_COL
    )[INDEX_COL]
    .mean()
    .reset_index()
)

agency_dri[INDEX_COL] = (
    agency_dri[INDEX_COL]
    .round(1)
)

agency_dri = agency_dri.sort_values(
    INDEX_COL,
    ascending=False
)

fig_agency = px.bar(
    agency_dri,
    x=AGENCY_COL,
    y=INDEX_COL,
    text=INDEX_COL,
    title="Average Digital Readiness Index by Agency"
)

fig_agency.update_layout(
    xaxis_title="Agency",
    yaxis_title="Average DRI",
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

ranking_df = agency_dri.copy()

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
        INDEX_COL: "DRI"
    }
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================================
# DRI HEATMAP
# ==========================================================

st.markdown(
    "## DRI Heatmap"
)

heatmap_df = agency_dri.copy()

fig_heatmap = px.imshow(
    heatmap_df[
        [
            INDEX_COL
        ]
    ].T,
    labels=dict(
        x="Agency",
        y="Index",
        color="DRI"
    ),
    x=heatmap_df[
        AGENCY_COL
    ],
    y=[
        "DRI"
    ],
    aspect="auto",
    title="Digital Readiness Heatmap by Agency"
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

The average Digital Readiness Index (DRI) was **{avg_dri}**.

This reflects the extent to which participating agencies have adopted
digital technologies, electronic databases, decision-support tools,
analytics platforms and digital workflows.

The results indicate moderate progress towards digital transformation.

Agencies with higher DRI scores are better positioned to leverage
data-driven pavement management, predictive maintenance practices
and integrated asset management systems.

Agency-level variation highlights opportunities for digital modernization,
system integration, technology adoption, cybersecurity strengthening and
improved use of digital decision-support platforms.
""")
