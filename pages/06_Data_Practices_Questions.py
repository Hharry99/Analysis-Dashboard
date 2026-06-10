# ==========================================================
# DATA PRACTICES QUESTION ANALYTICS
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
    page_title="Data Practices Questions",
    page_icon="📋",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/clean_master.csv")

master_df = load_data()
master_df = clean_master_dataset(master_df)

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

ORG_COL = "Q1. What agency do you work for?"

QUESTION_MAP = {

    "Q5 - Primary Involvement Areas":
        [c for c in master_df.columns if c.startswith("Q5")][0],

    "Q6 - Condition Data Sources":
        [c for c in master_df.columns if c.startswith("Q6")][0],

    "Q7 - Data Collection Frequency":
        [c for c in master_df.columns if c.startswith("Q7")][0],

    "Q8 - Data Types Collected":
        [c for c in master_df.columns if c.startswith("Q8")][0],

    "Q9 - Data Adequacy":
        [c for c in master_df.columns if c.startswith("Q9")][0],

    "Q10 - Data Quality Assessment":
        [c for c in master_df.columns if c.startswith("Q10")][0],

    "Q11 - Data Storage Methods":
        [c for c in master_df.columns if c.startswith("Q11")][0],

    "Q12 - Data Accessibility":
        [c for c in master_df.columns if c.startswith("Q12")][0],

    "Q13 - Data Management Challenges":
        [c for c in master_df.columns if c.startswith("Q13")][0],

    "Q14 - Data Governance Practices":
        [c for c in master_df.columns if c.startswith("Q14")][0],

    "Q15 - Overall Data Maturity":
        [c for c in master_df.columns if c.startswith("Q15")][0],
}

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("📋 Data Practices Question Analytics")

st.markdown("""
This page explores the underlying survey questions that contribute to
Data Maturity across participating organizations.
""")

# ==========================================================
# FILTERS
# ==========================================================

agencies = sorted(master_df[ORG_COL].dropna().unique())

selected_agencies = st.multiselect(
    "Filter Organization",
    agencies,
    default=agencies
)

analysis_df = master_df[
    master_df[ORG_COL].isin(selected_agencies)
]

selected_question = st.selectbox(
    "Select Question",
    list(QUESTION_MAP.keys())
)

question_col = QUESTION_MAP[selected_question]

# ==========================================================
# VALIDATION
# ==========================================================

if question_col not in analysis_df.columns:

    st.error(
        f"{question_col} not found."
    )

    st.stop()

# ==========================================================
# KPI SECTION
# ==========================================================

responses = analysis_df[
    question_col
].dropna()

# ==========================================================
# MULTI-SELECT QUESTIONS
# ==========================================================

question_code = (
    selected_question
    .split(" - ")[0]
)

MULTISELECT_QUESTIONS = [

    "Q5",
    "Q6",
    "Q8",
    "Q13"

]

if question_code in MULTISELECT_QUESTIONS:

    responses = (
        responses
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
    )

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
# RESPONSE DISTRIBUTION
# ==========================================================

st.markdown("## Response Distribution")

freq_df = (
    responses
    .value_counts()
    .reset_index()
)

freq_df.columns = ["Response", "Count"]
freq_df["Percentage"] = (
    freq_df["Count"]
    /
    freq_df["Count"].sum()
    * 100
).round(1)

fig = px.bar(
    freq_df,
    x="Count",
    y="Response",
    orientation="h",
    title=f"{selected_question} Response Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# ORGANIZATION COMPARISON
# ==========================================================

st.markdown("## Organization Comparison")

top_responses = (
    freq_df
    .head(10)["Response"]
)

heatmap_df = analysis_df.copy()

if question_code in MULTISELECT_QUESTIONS:

    heatmap_df = (
        analysis_df[
            [ORG_COL, question_col]
        ]
        .dropna()
    )

    heatmap_df[question_col] = (
        heatmap_df[question_col]
        .astype(str)
        .str.split(";")
    )

    heatmap_df = (
        heatmap_df
        .explode(question_col)
    )

    heatmap_df[question_col] = (
        heatmap_df[question_col]
        .str.strip()
    )

heatmap_df = heatmap_df[
    heatmap_df[question_col]
    .isin(top_responses)
]

cross_df = pd.crosstab(
    heatmap_df[ORG_COL],
    heatmap_df[question_col]
)

fig2 = px.imshow(
    cross_df,
    aspect="auto",
    title="Response Heatmap by Organization"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# RESPONSE TABLE
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

The distribution illustrates how organizations currently manage
data collection, storage, governance and pavement information
practices.

Differences across agencies may indicate opportunities for
benchmarking and institutional learning.
""")
