# ==========================================================
# FORECASTING QUESTION ANALYTICS
# Sprint 3B.5A
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Forecasting Questions",
    page_icon="🔮",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/clean_master.csv"
    )

master_df = load_data()
master_df = clean_master_dataset(master_df)

ORG_COL = "Q1. What agency do you work for?"

# ==========================================================
# QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Forecasting Method (Q16)":
        [c for c in master_df.columns if c.startswith("Q16")][0],

    "Forecast Confidence (Q17)":
        [c for c in master_df.columns if c.startswith("Q17")][0],

    "Forecasting Barriers (Q18)":
        [c for c in master_df.columns if c.startswith("Q18")][0],

    "Budgeting Decisions":
        [c for c in master_df.columns
         if "Multi-year budgeting" in c][0],

    "Treatment Timing":
        [c for c in master_df.columns
         if "Treatment timing decisions" in c][0],

    "Network Optimisation":
        [c for c in master_df.columns
         if "Network-level optimisation" in c][0],

    "Risk Prioritisation":
        [c for c in master_df.columns
         if "Risk-based prioritisation" in c][0],

    "Funding Justification":
        [c for c in master_df.columns
         if "Justification of funding requests" in c][0]
}

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🔮 Forecasting Question Analytics")

st.markdown("""
This page explores forecasting practices,
confidence levels and decision-support
applications that contribute to Forecasting Maturity.
""")

# ==========================================================
# FILTERS
# ==========================================================

agencies = sorted(
    master_df[ORG_COL].dropna().unique()
)

selected_agencies = st.multiselect(
    "Filter Organization",
    agencies,
    default=agencies
)

analysis_df = master_df[
    master_df[ORG_COL].isin(
        selected_agencies
    )
]

selected_question = st.selectbox(
    "Select Forecasting Question",
    list(QUESTION_MAP.keys())
)

question_col = QUESTION_MAP[
    selected_question
]

# ==========================================================
# KPI SECTION
# ==========================================================

responses = analysis_df[
    question_col
].dropna()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Responses",
    len(responses)
)

c2.metric(
    "Organizations",
    analysis_df[ORG_COL].nunique()
)

c3.metric(
    "Unique Answers",
    responses.nunique()
)

# ==========================================================
# DISTRIBUTION
# ==========================================================

freq_df = (
    responses
    .value_counts()
    .reset_index()
)

freq_df.columns = [
    "Response",
    "Count"
]

fig = px.bar(
    freq_df,
    x="Count",
    y="Response",
    orientation="h",
    title=f"{selected_question}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# ORGANIZATION HEATMAP
# ==========================================================

cross_df = pd.crosstab(
    analysis_df[ORG_COL],
    analysis_df[question_col]
)

fig2 = px.imshow(
    cross_df,
    aspect="auto",
    title="Agency Comparison Heatmap"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# TABLE
# ==========================================================

st.markdown("## Response Summary")

st.dataframe(
    freq_df,
    use_container_width=True
)

# ==========================================================
# INTERPRETATION
# ==========================================================

top_response = (
    freq_df.iloc[0]["Response"]
    if len(freq_df) > 0
    else "N/A"
)

st.info(f"""
### Executive Interpretation

Question analyzed:

**{selected_question}**

Most common response:

**{top_response}**

The findings provide insight into
forecasting maturity, confidence in
deterioration modelling, and the role
of forecasting in maintenance planning.

Variations between agencies highlight
opportunities for improved analytical
capacity and evidence-based planning.
""")
