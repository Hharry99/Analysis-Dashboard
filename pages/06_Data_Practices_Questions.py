
# ==========================================================
# DATA PRACTICES QUESTION ANALYTICS
# Sprint 3B.5A (Production Version)
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
        [c for c in master_df.columns if c.startswith("Q15")][0]
}

# ==========================================================
# MULTISELECT QUESTIONS
# ==========================================================

MULTISELECT_QUESTIONS = [
    "Q5",
    "Q6",
    "Q8",
    "Q13"
]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("📋 Data Practices Question Analytics")

st.markdown("""
This page explores the underlying survey questions that contribute
to Data Maturity across participating organizations.
""")

# ==========================================================
# FILTERS
# ==========================================================

agencies = sorted(
    master_df[ORG_COL]
    .dropna()
    .unique()
)

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

QUESTION_DESCRIPTIONS = {

    "Q5 - Primary Involvement Areas":
        "Areas where respondents are primarily involved in pavement management activities.",

    "Q6 - Condition Data Sources":
        "Sources used for pavement condition information.",

    "Q7 - Data Collection Frequency":
        "Frequency at which pavement condition data is collected.",

    "Q8 - Data Types Collected":
        "Types of pavement and asset information routinely collected.",

    "Q9 - Data Adequacy":
        "Perceptions of adequacy of available pavement data.",

    "Q10 - Data Quality Assessment":
        "Assessment of reliability and quality of pavement information.",

    "Q11 - Data Storage Methods":
        "Methods used to store and manage pavement data.",

    "Q12 - Data Accessibility":
        "Ease of access to pavement information.",

    "Q13 - Data Management Challenges":
        "Key challenges affecting data management.",

    "Q14 - Data Governance Practices":
        "Governance and stewardship of pavement information.",

    "Q15 - Overall Data Maturity":
        "Overall perception of data maturity."
}

st.info(
    QUESTION_DESCRIPTIONS.get(
        selected_question,
        ""
    )
)
question_col = QUESTION_MAP[selected_question]

question_code = (
    selected_question
    .split(" - ")[0]
)

# ==========================================================
# VALIDATION
# ==========================================================

if question_col not in analysis_df.columns:

    st.error(
        f"Column not found: {question_col}"
    )
    st.stop()

# ==========================================================
# RESPONSE PROCESSING
# ==========================================================

responses = (
    analysis_df[question_col]
    .dropna()
)

if question_code in MULTISELECT_QUESTIONS:

    responses = (
        responses
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
    )

# ==========================================================
# KPI SECTION
# ==========================================================

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

freq_df.columns = [
    "Response",
    "Count"
]

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
    text="Percentage",
    title=f"{selected_question} Response Distribution"
)

fig.update_layout(
    yaxis_title="Response",
    xaxis_title="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# ORGANIZATION COMPARISON
# ==========================================================

st.markdown("## Organization Comparison")

try:

    if question_code in MULTISELECT_QUESTIONS:

        heatmap_df = (
            analysis_df[
                [ORG_COL, question_col]
            ]
            .dropna()
            .copy()
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

        heatmap_df = (
            heatmap_df
            .reset_index(drop=True)
        )

    else:

        heatmap_df = (
            analysis_df[
                [ORG_COL, question_col]
            ]
            .dropna()
            .copy()
        )

    top_responses = (
        freq_df
        .head(10)["Response"]
        .tolist()
    )

    heatmap_df = heatmap_df[
        heatmap_df[question_col]
        .isin(top_responses)
    ]

    cross_df = (
        heatmap_df
        .groupby(
            [ORG_COL, question_col]
        )
        .size()
        .unstack(fill_value=0)
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

except Exception as e:

    st.warning(
        f"Heatmap could not be generated: {e}"
    )

# ==========================================================
# RESPONSE SUMMARY
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

top_percentage = (
    freq_df.iloc[0]["Percentage"]
    if len(freq_df) > 0
    else 0
)

st.info(f"""
### Executive Interpretation

Question analyzed:
**{selected_question}**

Most common response:

**{top_response}**

Response share:

**{top_percentage}%**

A total of **{len(responses)} responses**
were analyzed across **{analysis_df[ORG_COL].nunique()} organizations**.

The results provide insight into current
data collection, management, governance,
storage and utilization practices across
Kenya's road agencies.

Differences across organizations may
highlight opportunities for benchmarking,
capacity building and improved data
governance practices.
""")
