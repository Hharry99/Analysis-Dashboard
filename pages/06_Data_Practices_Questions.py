# ==========================================================
# DATA PRACTICES QUESTION ANALYTICS
# Sprint 3B.5A - Framework Aligned Production Version
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
    return pd.read_csv(
        "data/clean_master.csv"
    )


master_df = load_data()
master_df = clean_master_dataset(master_df)

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

AGENCY_COL = "Q1. What agency do you work for?"

# ==========================================================
# VALIDATION
# ==========================================================

if AGENCY_COL not in master_df.columns:

    st.error(
        f"Missing required column: {AGENCY_COL}"
    )

    st.stop()

# ==========================================================
# HELPER FUNCTION FOR QUESTION COLUMNS
# ==========================================================

def get_question_column(question_code):

    matches = [
        col for col in master_df.columns
        if col.startswith(question_code)
    ]

    if matches:
        return matches[0]

    return None

# ==========================================================
# QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Q5 - Primary Involvement Areas":
        get_question_column("Q5"),

    "Q6 - Condition Data Sources":
        get_question_column("Q6"),

    "Q7 - Data Collection Frequency":
        get_question_column("Q7"),

    "Q8 - Data Types Collected":
        get_question_column("Q8"),

    "Q9 - Data Adequacy":
        get_question_column("Q9"),

    "Q10 - Data Quality Assessment":
        get_question_column("Q10"),

    "Q11 - Data Storage Methods":
        get_question_column("Q11"),

    "Q12 - Data Accessibility":
        get_question_column("Q12"),

    "Q13 - Data Management Challenges":
        get_question_column("Q13"),

    "Q14 - Data Governance Practices":
        get_question_column("Q14"),

    "Q15 - Overall Data Maturity":
        get_question_column("Q15")
}

QUESTION_MAP = {
    key: value
    for key, value in QUESTION_MAP.items()
    if value is not None
}

if not QUESTION_MAP:

    st.error(
        "No Data Practices question columns were found in the dataset."
    )

    st.stop()

# ==========================================================
# QUESTION DESCRIPTIONS
# ==========================================================

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
        "Overall perception of agency data maturity."
}

# ==========================================================
# MULTI-SELECT QUESTIONS
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

st.title(
    "Data Practices Question Analytics"
)

st.markdown("""
This page explores the survey questions that contribute
to agency Data Maturity.
""")

# ==========================================================
# FILTERS
# ==========================================================

agencies = sorted(
    master_df[AGENCY_COL]
    .dropna()
    .unique()
)

selected_agencies = st.multiselect(
    "Filter Agency",
    agencies,
    default=agencies
)

analysis_df = master_df[
    master_df[AGENCY_COL]
    .isin(selected_agencies)
]

selected_question = st.selectbox(
    "Select Question",
    list(QUESTION_MAP.keys())
)

st.info(
    QUESTION_DESCRIPTIONS.get(
        selected_question,
        ""
    )
)

question_col = QUESTION_MAP[
    selected_question
]

question_code = (
    selected_question
    .split(" - ")[0]
)

# ==========================================================
# QUESTION VALIDATION
# ==========================================================

if question_col not in analysis_df.columns:

    st.error(
        f"Column not found: {question_col}"
    )

    st.stop()

if analysis_df.empty:

    st.warning(
        "No records found for the selected agency filter."
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

responses = responses[
    responses.astype(str).str.len() > 0
]

if responses.empty:

    st.warning(
        "No valid responses were found for the selected question and agency filter."
    )

    st.stop()

# ==========================================================
# KPI SECTION
# ==========================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Survey Responses",
    len(responses)
)

c2.metric(
    "Participating Agencies",
    analysis_df[AGENCY_COL].nunique()
)

c3.metric(
    "Unique Response Categories",
    responses.nunique()
)

# ==========================================================
# RESPONSE DISTRIBUTION
# ==========================================================

st.markdown(
    "## Response Distribution"
)

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

freq_df = (
    freq_df
    .sort_values(
        "Count",
        ascending=False
    )
    .reset_index(drop=True)
)

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
    xaxis_title="Number of Responses",
    height=650
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# AGENCY COMPARISON
# ==========================================================

st.markdown(
    "## Agency Comparison"
)

try:

    if question_code in MULTISELECT_QUESTIONS:

        heatmap_df = (
            analysis_df[
                [
                    AGENCY_COL,
                    question_col
                ]
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
            .astype(str)
            .str.strip()
        )

    else:

        heatmap_df = (
            analysis_df[
                [
                    AGENCY_COL,
                    question_col
                ]
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
            [
                AGENCY_COL,
                question_col
            ]
        )
        .size()
        .unstack(fill_value=0)
    )

    fig2 = px.imshow(
        cross_df,
        aspect="auto",
        title="Response Heatmap by Agency",
        labels=dict(
            x="Response",
            y="Agency",
            color="Count"
        )
    )

    fig2.update_layout(
        height=650
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

st.markdown(
    "## Response Summary"
)

st.dataframe(
    freq_df[
        [
            "Response",
            "Count",
            "Percentage"
        ]
    ],
    use_container_width=True
)

# ==========================================================
# EXECUTIVE INTERPRETATION
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
were analyzed across
**{analysis_df[AGENCY_COL].nunique()} agencies**.

The findings provide insight into how
road agencies collect, manage, store,
govern and utilize pavement information.

Differences across agencies may highlight
opportunities for benchmarking, capacity building
and improved data governance practices.
""")
