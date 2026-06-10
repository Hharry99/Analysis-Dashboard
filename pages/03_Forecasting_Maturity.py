# ==========================================================
# FORECASTING MATURITY ANALYSIS
# Sprint 3B - Page 3
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
    page_title="Forecasting Maturity Analysis",
    page_icon="🔮",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    master = pd.read_csv("data/clean_master.csv")
    indices = pd.read_csv("data/indices_dataset.csv")

    return master, indices

master_df, indices_df = load_data()

ORG_COL = "Q1. What agency do you work for?"

# ==========================================================
# PREPARE DATA
# ==========================================================

analysis_df = pd.concat(
    [
        master_df[[ORG_COL]],
        indices_df[["FMI"]]
    ],
    axis=1
)

analysis_df["FMI"] = pd.to_numeric(
    analysis_df["FMI"],
    errors="coerce"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🔮 Forecasting Maturity Analysis")

st.markdown("""
This section evaluates forecasting capability,
predictive modelling practices,
future maintenance planning,
and analytical readiness.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_fmi = round(analysis_df["FMI"].mean(),1)
max_fmi = round(analysis_df["FMI"].max(),1)
min_fmi = round(analysis_df["FMI"].min(),1)

agencies = analysis_df[ORG_COL].nunique()

k1,k2,k3,k4 = st.columns(4)

k1.metric("Average FMI",avg_fmi)
k2.metric("Highest FMI",max_fmi)
k3.metric("Lowest FMI",min_fmi)
k4.metric("Organizations",agencies)

# ==========================================================
# FMI DISTRIBUTION
# ==========================================================

st.subheader("Forecasting Maturity Distribution")

fig_hist = px.histogram(
    analysis_df,
    x="FMI",
    nbins=10,
    title="Distribution of Forecasting Maturity Scores"
)

st.plotly_chart(fig_hist,use_container_width=True)

if analysis_df["FMI"].nunique() <= 1:

    st.warning("""
    FMI contains only one unique value.

    This suggests the index may have been
    reconstructed as a constant rather than
    calculated per respondent.

    Review indices_dataset.csv.
    """)

# ==========================================================
# FMI BY AGENCY
# ==========================================================

agency_scores = (
    analysis_df
    .groupby(ORG_COL)["FMI"]
    .mean()
    .reset_index()
    .sort_values("FMI",ascending=False)
)

fig_bar = px.bar(
    agency_scores,
    x=ORG_COL,
    y="FMI",
    title="Average FMI by Organization"
)

st.plotly_chart(fig_bar,use_container_width=True)

# ==========================================================
# AGENCY RANKING
# ==========================================================

st.subheader("Agency Ranking")

ranking_df = agency_scores.copy()
ranking_df["Rank"] = range(
    1,
    len(ranking_df)+1
)

st.dataframe(
    ranking_df[
        ["Rank",ORG_COL,"FMI"]
    ],
    use_container_width=True
)

# ==========================================================
# FMI HEATMAP
# ==========================================================

st.subheader("Forecasting Heatmap")

fig_heatmap = px.imshow(
    agency_scores[["FMI"]].T,
    labels=dict(color="FMI"),
    x=agency_scores[ORG_COL],
    y=["FMI"],
    aspect="auto"
)

st.plotly_chart(fig_heatmap,use_container_width=True)

# ==========================================================
# INTERPRETATION
# ==========================================================

st.info(f"""
### Interpretation

The average Forecasting Maturity Index (FMI)
was **{avg_fmi}**.

The findings indicate the extent to which
organizations utilise forecasting tools,
predictive models and future maintenance
planning in pavement management.

Lower scores suggest opportunities to
strengthen analytical capability,
forecasting techniques,
and evidence-based planning.
""")
