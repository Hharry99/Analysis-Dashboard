# ==========================================================
# RECONSTRUCTION READINESS ANALYSIS
# Sprint 3B - Page 4
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_cleaning import (
    clean_master_dataset
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Reconstruction Readiness Analysis",
    page_icon="🛣",
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

ORG_COL = "Q1. What agency do you work for?"

# ==========================================================
# PREPARE DATA
# ==========================================================

analysis_df = pd.concat(
    [
        master_df[[ORG_COL]],
        indices_df[["RRI"]]
    ],
    axis=1
)

analysis_df["RRI"] = pd.to_numeric(
    analysis_df["RRI"],
    errors="coerce"
)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🛣 Reconstruction Readiness Analysis")

st.markdown("""
This section evaluates organizational readiness
for pavement rehabilitation and reconstruction
planning, prioritization and implementation.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_rri = round(
    analysis_df["RRI"].mean(),
    1
)

highest_rri = round(
    analysis_df["RRI"].max(),
    1
)

lowest_rri = round(
    analysis_df["RRI"].min(),
    1
)

agencies = analysis_df[
    ORG_COL
].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average RRI", avg_rri)
c2.metric("Highest RRI", highest_rri)
c3.metric("Lowest RRI", lowest_rri)
c4.metric("Organizations", agencies)

# ==========================================================
# RRI DISTRIBUTION
# ==========================================================

st.markdown("## RRI Distribution")

fig_hist = px.histogram(
    analysis_df,
    x="RRI",
    nbins=10,
    title="Distribution of Reconstruction Readiness Scores"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# RRI BY ORGANIZATION
# ==========================================================

st.markdown("## RRI by Organization")

agency_rri = (
    analysis_df
    .groupby(ORG_COL)["RRI"]
    .mean()
    .reset_index()
)

agency_rri = agency_rri.sort_values(
    "RRI",
    ascending=False
)

fig_agency = px.bar(
    agency_rri,
    x=ORG_COL,
    y="RRI",
    title="Average Reconstruction Readiness Index by Organization"
)

st.plotly_chart(
    fig_agency,
    use_container_width=True
)

# ==========================================================
# AGENCY RANKING
# ==========================================================

st.markdown("## Agency Ranking")

ranking_df = agency_rri.copy()

ranking_df["Rank"] = range(
    1,
    len(ranking_df) + 1
)

ranking_df = ranking_df[
    ["Rank", ORG_COL, "RRI"]
]

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================================
# RRI HEATMAP
# ==========================================================

st.markdown("## Reconstruction Readiness Heatmap")

fig_heatmap = px.imshow(
    agency_rri[["RRI"]].T,
    labels=dict(color="RRI"),
    x=agency_rri[ORG_COL],
    y=["RRI"],
    aspect="auto"
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

The average Reconstruction Readiness Index (RRI)
was **{avg_rri}**.

This reflects the extent to which participating
organizations are prepared for pavement
rehabilitation and reconstruction decision-making.

The relatively high readiness score suggests
that reconstruction planning practices are
more mature than data maturity and forecasting
capabilities.

However, differences across organizations indicate
opportunities for improved prioritization,
investment planning and evidence-based
reconstruction programming.
""")
