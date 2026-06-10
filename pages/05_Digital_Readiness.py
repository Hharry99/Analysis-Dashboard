# ==========================================================
# DIGITAL READINESS ANALYSIS
# Sprint 3B - Page 5
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
    page_title="Digital Readiness Analysis",
    page_icon="💻",
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

ORG_COL = "Q1. What agency do you work for?"

# ==========================================================
# PREPARE DATA
# ==========================================================

analysis_df = pd.concat(
    [
        master_df[[ORG_COL]],
        indices_df[["DRI"]]
    ],
    axis=1
)

analysis_df["DRI"] = pd.to_numeric(
    analysis_df["DRI"],
    errors="coerce"
)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("💻 Digital Readiness Analysis")

st.markdown("""
This section evaluates the adoption of digital
technologies, databases, analytics platforms,
decision-support systems and digital transformation
capabilities across participating organizations.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_dri = round(
    analysis_df["DRI"].mean(),
    1
)

highest_dri = round(
    analysis_df["DRI"].max(),
    1
)

lowest_dri = round(
    analysis_df["DRI"].min(),
    1
)

agencies = analysis_df[
    ORG_COL
].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average DRI", avg_dri)
c2.metric("Highest DRI", highest_dri)
c3.metric("Lowest DRI", lowest_dri)
c4.metric("Organizations", agencies)

# ==========================================================
# DRI DISTRIBUTION
# ==========================================================

st.markdown("## DRI Distribution")

fig_hist = px.histogram(
    analysis_df,
    x="DRI",
    nbins=10,
    title="Distribution of Digital Readiness Scores"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# DRI BY ORGANIZATION
# ==========================================================

st.markdown("## DRI by Organization")

agency_dri = (
    analysis_df
    .groupby(ORG_COL)["DRI"]
    .mean()
    .reset_index()
)

agency_dri = agency_dri.sort_values(
    "DRI",
    ascending=False
)

fig_agency = px.bar(
    agency_dri,
    x=ORG_COL,
    y="DRI",
    title="Average Digital Readiness Index by Organization"
)

st.plotly_chart(
    fig_agency,
    use_container_width=True
)

# ==========================================================
# AGENCY RANKING
# ==========================================================

st.markdown("## Agency Ranking")

ranking_df = agency_dri.copy()

ranking_df["Rank"] = range(
    1,
    len(ranking_df) + 1
)

ranking_df = ranking_df[
    ["Rank", ORG_COL, "DRI"]
]

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================================
# DRI HEATMAP
# ==========================================================

st.markdown("## Digital Readiness Heatmap")

fig_heatmap = px.imshow(
    agency_dri[["DRI"]].T,
    labels=dict(color="DRI"),
    x=agency_dri[ORG_COL],
    y=["DRI"],
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

The average Digital Readiness Index (DRI)
was **{avg_dri}**.

This reflects the extent to which organizations
have adopted digital technologies,
electronic databases,
decision-support tools,
analytics platforms and digital workflows.

The results indicate moderate progress towards
digital transformation.

Organizations with higher DRI scores are better
positioned to leverage data-driven pavement
management and predictive maintenance practices.

The variation across agencies highlights
opportunities for digital modernization,
system integration and technology adoption.
""")
