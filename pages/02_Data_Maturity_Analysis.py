# ==========================================================
# DATA MATURITY ANALYSIS
# Sprint 3A - Page 2
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
    page_title="Data Maturity Analysis",
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
INDEX_COL = "DMI"

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
# MERGE DATASETS
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
    "Data Maturity Analysis"
)

st.markdown("""
This section evaluates the maturity of pavement information systems,
data availability, historical records management and institutional
data practices across participating agencies.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_dmi = round(
    analysis_df[INDEX_COL].mean(),
    1
)

highest_dmi = round(
    analysis_df[INDEX_COL].max(),
    1
)

lowest_dmi = round(
    analysis_df[INDEX_COL].min(),
    1
)

agencies = analysis_df[
    AGENCY_COL
].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average DMI",
    avg_dmi
)

c2.metric(
    "Highest DMI",
    highest_dmi
)

c3.metric(
    "Lowest DMI",
    lowest_dmi
)

c4.metric(
    "Agencies",
    agencies
)

# ==========================================================
# DMI DISTRIBUTION
# ==========================================================

st.markdown(
    "## DMI Distribution"
)

fig_hist = px.histogram(
    analysis_df,
    x=INDEX_COL,
    nbins=10,
    title="Distribution of Data Maturity Scores"
)

fig_hist.update_layout(
    xaxis_title="Data Maturity Index",
    yaxis_title="Number of Responses",
    height=450
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# DMI BY AGENCY
# ==========================================================

st.markdown(
    "## DMI by Agency"
)

agency_dmi = (
    analysis_df
    .groupby(
        AGENCY_COL
    )[INDEX_COL]
    .mean()
    .reset_index()
)

agency_dmi[INDEX_COL] = (
    agency_dmi[INDEX_COL]
    .round(1)
)

agency_dmi = agency_dmi.sort_values(
    INDEX_COL,
    ascending=False
)

fig_agency = px.bar(
    agency_dmi,
    x=AGENCY_COL,
    y=INDEX_COL,
    text=INDEX_COL,
    title="Average Data Maturity Index by Agency"
)

fig_agency.update_layout(
    xaxis_title="Agency",
    yaxis_title="Average DMI",
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

ranking_df = agency_dmi.copy()

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
        INDEX_COL: "DMI"
    }
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================================
# DMI HEATMAP
# ==========================================================

st.markdown(
    "## DMI Heatmap"
)

heatmap_df = agency_dmi.copy()

fig_heatmap = px.imshow(
    heatmap_df[
        [
            INDEX_COL
        ]
    ].T,
    labels=dict(
        x="Agency",
        y="Index",
        color="DMI"
    ),
    x=heatmap_df[
        AGENCY_COL
    ],
    y=[
        "DMI"
    ],
    aspect="auto",
    title="Data Maturity Heatmap by Agency"
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

The average Data Maturity Index (DMI) was **{avg_dmi}**.

This suggests a **low-to-moderate level of data maturity**
across participating agencies.

The results indicate opportunities for:

• Improved data collection systems

• Better historical pavement records

• Stronger data governance

• Enhanced integration of maintenance history with pavement condition information

Agency-level differences suggest that data maturity varies across institutions,
highlighting opportunities for benchmarking, knowledge sharing and targeted
data management improvements.
""")
