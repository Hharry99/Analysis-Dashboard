# ==========================================================
# DIGITAL READINESS QUESTION ANALYTICS
# Sprint 3B.5B - Framework Aligned Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Digital Readiness Questions",
    page_icon="📊",
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

master_df = clean_master_dataset(
    master_df
)

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
# HELPER FUNCTION
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
# DIGITAL READINESS QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Q23 - Road Infrastructure Databases":
        get_question_column("Q23"),

    "Q24 - Artificial Intelligence (AI)":
        get_question_column("Q24"),

    "Q25 - Data Analytics":
        get_question_column("Q25"),

    "Q26 - Multi-Criteria Decision Analysis (MCDA)":
        get_question_column("Q26")
}

QUESTION_MAP = {
    key: value
    for key, value in QUESTION_MAP.items()
    if value is not None
}

if not QUESTION_MAP:

    st.error(
        "No Digital Readiness question columns were found in the dataset."
    )

    st.stop()

# ==========================================================
# QUESTION DESCRIPTIONS
# ==========================================================

QUESTION_DESCRIPTIONS = {

    "Q23 - Road Infrastructure Databases":
        """
        Assesses familiarity with road infrastructure databases
        and their application in maintenance planning and
        decision-making.
        """,

    "Q24 - Artificial Intelligence (AI)":
        """
        Assesses familiarity with Artificial Intelligence techniques
        and their potential application in road asset management and
        pavement performance prediction.
        """,

    "Q25 - Data Analytics":
        """
        Assesses familiarity with data analytics tools, techniques
        and data-driven decision-making for infrastructure management.
        """,

    "Q26 - Multi-Criteria Decision Analysis (MCDA)":
        """
        Assesses familiarity with MCDA approaches used to support
        prioritisation and investment decisions in road asset management.
        """
}

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Digital Readiness Questions"
)

st.markdown("""
This page evaluates agency readiness for digital transformation by examining
familiarity with road infrastructure databases, Artificial Intelligence (AI),
data analytics and Multi-Criteria Decision Analysis (MCDA) technologies.
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

if analysis_df.empty:

    st.warning(
        "No records found for the selected agency filter."
    )

    st.stop()

selected_question = st.selectbox(
    "Select Digital Readiness Question",
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

# ==========================================================
# QUESTION VALIDATION
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
    .astype(str)
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
    height=550
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
        .str.strip()
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

The findings provide insight into the digital readiness of road agencies
and their familiarity with emerging digital technologies, analytical tools
and decision-support approaches.

The results help identify opportunities for digital transformation,
capacity development and adoption of advanced decision-support technologies
across the road sector.

Differences across agencies may highlight varying levels of readiness for
data-driven asset management, digital innovation, analytics adoption and
technology-enabled infrastructure planning.
""")
