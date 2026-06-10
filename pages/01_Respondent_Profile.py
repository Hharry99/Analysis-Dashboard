# ==========================================================
# RESPONDENT PROFILE ANALYSIS
# Sprint 3A - Page 1
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
    page_title="Respondent Profile",
    page_icon="👥",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/clean_master.csv")

df = load_data()

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

ORG_COL = "Q1. What agency do you work for?"
LEVEL_COL = "Q2. At what level do you work?"
POSITION_COL = "Q3. What position do you currently hold?"
EXP_COL = "Q4. How many years of experience do you have in road asset management?"

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("👥 Respondent Profile Analysis")
st.markdown("""
This section examines the demographic and professional characteristics
of practitioners who participated in the study.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

total_respondents = len(df)
total_agencies = df[ORG_COL].nunique()
total_positions = df[POSITION_COL].nunique()

c1, c2, c3 = st.columns(3)

c1.metric("Respondents", total_respondents)
c2.metric("Organizations", total_agencies)
c3.metric("Positions", total_positions)

# ==========================================================
# ORGANIZATION DISTRIBUTION
# ==========================================================

st.markdown("## Organization Distribution")

org_counts = (
    df[ORG_COL]
    .value_counts()
    .reset_index()
)

org_counts.columns = ["Agency", "Responses"]

fig_org = px.pie(
    org_counts,
    names="Agency",
    values="Responses",
    hole=0.55,
    title="Distribution of Respondents by Organization"
)

st.plotly_chart(fig_org, use_container_width=True)

# ==========================================================
# WORK LEVEL DISTRIBUTION
# ==========================================================

st.markdown("## Work Level Distribution")

level_counts = (
    df[LEVEL_COL]
    .value_counts()
    .reset_index()
)

level_counts.columns = ["Level", "Count"]

fig_level = px.bar(
    level_counts,
    x="Count",
    y="Level",
    orientation="h",
    title="Respondents by Work Level"
)

st.plotly_chart(fig_level, use_container_width=True)

# ==========================================================
# POSITION DISTRIBUTION
# ==========================================================

st.markdown("## Position Distribution")

position_counts = (
    df[POSITION_COL]
    .value_counts()
    .head(15)
    .reset_index()
)

position_counts.columns = ["Position", "Count"]

fig_position = px.bar(
    position_counts,
    x="Count",
    y="Position",
    orientation="h",
    title="Top Positions Represented"
)

st.plotly_chart(fig_position, use_container_width=True)

# ==========================================================
# EXPERIENCE PROFILE
# ==========================================================

st.markdown("## Experience Profile")

exp_counts = (
    df[EXP_COL]
    .value_counts()
    .reset_index()
)

exp_counts.columns = ["Experience", "Count"]

fig_exp = px.bar(
    exp_counts,
    x="Experience",
    y="Count",
    title="Years of Experience Distribution"
)

st.plotly_chart(fig_exp, use_container_width=True)

# ==========================================================
# RESPONDENT SUMMARY TABLE
# ==========================================================

st.markdown("## Respondent Summary")

summary_df = pd.DataFrame({
    "Metric": [
        "Total Respondents",
        "Organizations",
        "Positions"
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

- A total of **{total_respondents} practitioners** participated.
- Respondents were drawn from **{total_agencies} organizations**.
- The survey captured perspectives from **{total_positions} distinct positions**.
- The respondent profile provides a diverse representation of stakeholders involved in pavement management and road asset management activities.
""")
