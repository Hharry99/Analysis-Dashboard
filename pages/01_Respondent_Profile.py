# ==========================================================
# RESPONDENT PROFILE ANALYSIS
# Sprint 3A - Page 1
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
    page_title="Respondent Profile",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/clean_master.csv")


df = load_data()
df = clean_master_dataset(df)

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

AGENCY_COL = "Q1. What agency do you work for?"
LEVEL_COL = "Q2. At what level do you work?"
POSITION_COL = "Q3. What position do you currently hold?"
EXP_COL = "Q4. How many years of experience do you have in road asset management?"

REQUIRED_COLS = [
    AGENCY_COL,
    LEVEL_COL,
    POSITION_COL,
    EXP_COL
]

# ==========================================================
# VALIDATION
# ==========================================================

missing_cols = [
    col for col in REQUIRED_COLS
    if col not in df.columns
]

if missing_cols:
    st.error(
        f"Missing required columns: {missing_cols}"
    )
    st.stop()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(" Respondent Profile Analysis")

st.markdown("""
This section examines the demographic and professional characteristics
of practitioners who participated in the study.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

total_respondents = len(df)
total_agencies = df[AGENCY_COL].nunique()
total_positions = df[POSITION_COL].nunique()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Respondents",
    total_respondents
)

c2.metric(
    "Agencies",
    total_agencies
)

c3.metric(
    "Positions",
    total_positions
)

# ==========================================================
# AGENCY DISTRIBUTION
# ==========================================================

st.markdown("## Agency Distribution")

agency_counts = (
    df[AGENCY_COL]
    .dropna()
    .value_counts()
    .reset_index()
)

agency_counts.columns = [
    "Agency",
    "Responses"
]

fig_agency = px.pie(
    agency_counts,
    names="Agency",
    values="Responses",
    hole=0.55,
    title="Distribution of Respondents by Agency"
)

fig_agency.update_layout(
    height=500
)

st.plotly_chart(
    fig_agency,
    use_container_width=True
)

# ==========================================================
# WORK LEVEL DISTRIBUTION
# ==========================================================

st.markdown("## Work Level Distribution")

level_counts = (
    df[LEVEL_COL]
    .dropna()
    .value_counts()
    .reset_index()
)

level_counts.columns = [
    "Level",
    "Count"
]

fig_level = px.bar(
    level_counts,
    x="Count",
    y="Level",
    orientation="h",
    title="Respondents by Work Level"
)

fig_level.update_layout(
    xaxis_title="Number of Respondents",
    yaxis_title="Work Level",
    height=450
)

st.plotly_chart(
    fig_level,
    use_container_width=True
)

# ==========================================================
# POSITION DISTRIBUTION
# ==========================================================

st.markdown("## Position Distribution")

position_counts = (
    df[POSITION_COL]
    .dropna()
    .value_counts()
    .head(15)
    .reset_index()
)

position_counts.columns = [
    "Position",
    "Count"
]

fig_position = px.bar(
    position_counts,
    x="Count",
    y="Position",
    orientation="h",
    title="Top Positions Represented"
)

fig_position.update_layout(
    xaxis_title="Number of Respondents",
    yaxis_title="Position",
    height=600
)

st.plotly_chart(
    fig_position,
    use_container_width=True
)

# ==========================================================
# EXPERIENCE PROFILE
# ==========================================================

st.markdown("## Experience Profile")

exp_counts = (
    df[EXP_COL]
    .dropna()
    .value_counts()
    .reset_index()
)

exp_counts.columns = [
    "Experience",
    "Count"
]

fig_exp = px.bar(
    exp_counts,
    x="Experience",
    y="Count",
    text="Count",
    title="Years of Experience Distribution"
)

fig_exp.update_layout(
    xaxis_title="Years of Experience",
    yaxis_title="Number of Respondents",
    height=450
)

fig_exp.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_exp,
    use_container_width=True
)

# ==========================================================
# RESPONDENT SUMMARY TABLE
# ==========================================================

st.markdown("## Respondent Summary")

summary_df = pd.DataFrame({
    "Metric": [
        "Total Respondents",
        "Participating Agencies",
        "Distinct Positions"
    ],
    "Value": [
        total_respondents,
        total_agencies,
        total_positions
    ]
})

st.dataframe(
    summary_df,
    use_container_width=True
)

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Key Insights

A total of **{total_respondents} practitioners** participated in the study.

Respondents were drawn from **{total_agencies} road-sector agencies**.

The survey captured perspectives from **{total_positions} distinct positions**.

The respondent profile provides a diverse representation of stakeholders
involved in pavement management, road asset management, maintenance planning,
technical assessment and institutional decision-making.
""")
