# ==========================================================
# DATA MATURITY ANALYSIS
# Sprint 3A - Page 2
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

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

ORG_COL = "Q1. What agency do you work for?"

# ==========================================================
# MERGE DATASETS
# ==========================================================

analysis_df = pd.concat(
    [
        master_df[[ORG_COL]],
        indices_df[["DMI"]]
    ],
    axis=1
)

analysis_df["DMI"] = pd.to_numeric(
    analysis_df["DMI"],
    errors="coerce"
)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("📊 Data Maturity Analysis")

st.markdown("""
This section evaluates the maturity of pavement information systems,
data availability, historical records management, and institutional
data practices across participating agencies.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_dmi = round(
    analysis_df["DMI"].mean(),
    1
)

highest_dmi = round(
    analysis_df["DMI"].max(),
    1
)

lowest_dmi = round(
    analysis_df["DMI"].min(),
    1
)

agencies = analysis_df[
    ORG_COL
].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average DMI", avg_dmi)
c2.metric("Highest DMI", highest_dmi)
c3.metric("Lowest DMI", lowest_dmi)
c4.metric("Organizations", agencies)

# ==========================================================
# DMI DISTRIBUTION
# ==========================================================

st.markdown("## DMI Distribution")

fig_hist = px.histogram(
    analysis_df,
    x="DMI",
    nbins=10,
    title="Distribution of Data Maturity Scores"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# DMI BY AGENCY
# ==========================================================

st.markdown("## DMI by Organization")

agency_dmi = (
    analysis_df
    .groupby(ORG_COL)["DMI"]
    .mean()
    .reset_index()
)

agency_dmi = agency_dmi.sort_values(
    "DMI",
    ascending=False
)

fig_agency = px.bar(
    agency_dmi,
    x=ORG_COL,
    y="DMI",
    title="Average Data Maturity Index by Organization"
)

st.plotly_chart(
    fig_agency,
    use_container_width=True
)

# ==========================================================
# AGENCY RANKING
# ==========================================================

st.markdown("## Agency Ranking")

ranking_df = agency_dmi.copy()

ranking_df["Rank"] = range(
    1,
    len(ranking_df) + 1
)

ranking_df = ranking_df[
    ["Rank", ORG_COL, "DMI"]
]

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================================
# DMI HEATMAP
# ==========================================================

st.markdown("## DMI Heatmap")

heatmap_df = agency_dmi.copy()

fig_heatmap = px.imshow(
    heatmap_df[["DMI"]].T,
    labels=dict(
        color="DMI"
    ),
    x=heatmap_df[ORG_COL],
    y=["DMI"],
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

The average Data Maturity Index (DMI) was **{avg_dmi}**.

This suggests a **low-to-moderate level of data maturity**
across participating organizations.

The results indicate opportunities for:

- Improved data collection systems
- Better historical pavement records
- Stronger data governance
- Enhanced integration of maintenance history with pavement condition information

Agency-level differences suggest that maturity varies across institutions,
highlighting opportunities for benchmarking and knowledge sharing.
""")
