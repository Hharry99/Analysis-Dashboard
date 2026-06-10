
# ==========================================================
# DIGITAL READINESS QUESTION ANALYTICS
# Sprint 3B.5B - Final Production Version
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
    page_icon="💻",
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
# CORE COLUMN DEFINITIONS
# ==========================================================

ORG_COL = (
    "Q1. What agency do you work for?"
)

# ==========================================================
# DIGITAL READINESS QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Q23 - Road Infrastructure Databases":

        [c for c in master_df.columns
         if c.startswith("Q23")][0],

    "Q24 - Artificial Intelligence (AI)":

        [c for c in master_df.columns
         if c.startswith("Q24")][0],

    "Q25 - Data Analytics":

        [c for c in master_df.columns
         if c.startswith("Q25")][0],

    "Q26 - Multi-Criteria Decision Analysis (MCDA)":

        [c for c in master_df.columns
         if c.startswith("Q26")][0]
}

# ==========================================================
# QUESTION DESCRIPTIONS
# ==========================================================

QUESTION_DESCRIPTIONS = {

    "Q23 - Road Infrastructure Databases":
        """
        Assesses familiarity with road infrastructure
        databases and their application in maintenance
        planning and decision-making.
        """,

    "Q24 - Artificial Intelligence (AI)":
        """
        Assesses familiarity with Artificial Intelligence
        techniques and their potential application in road
        asset management and pavement performance prediction.
        """,

    "Q25 - Data Analytics":
        """
        Assesses familiarity with data analytics tools,
        techniques and data-driven decision making for
        infrastructure management.
        """,

    "Q26 - Multi-Criteria Decision Analysis (MCDA)":
        """
        Assesses familiarity with MCDA approaches used
        to support prioritisation and investment decisions
        in road asset management.
        """
}

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "💻 Digital Readiness Questions"
)

st.markdown("""
This page evaluates organizational readiness for
digital transformation by examining familiarity
with databases, Artificial Intelligence (AI),
data analytics and Multi-Criteria Decision
Analysis (MCDA) technologies.
""")

# ==========================================================
# FILTERS
# ==========================================================

agencies = sorted(
    master_df[
        ORG_COL
    ]
    .dropna()
    .unique()
)

selected_agencies = st.multiselect(
    "Filter Organization",
    agencies,
    default=agencies
)

analysis_df = master_df[
    master_df[
        ORG_COL
    ]
    .isin(selected_agencies)
]

selected_question = st.selectbox(
    "Select Digital Readiness Question",
    list(
        QUESTION_MAP.keys()
    )
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
    analysis_df[
        question_col
    ]
    .dropna()
)

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
    analysis_df[
        ORG_COL
    ].nunique()
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
    .reset_index(
        drop=True
    )
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
    xaxis_title="Number of Responses"
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
# ORGANIZATION COMPARISON
# ==========================================================

st.markdown(
    "## Organization Comparison"
)

try:

    heatmap_df = (
        analysis_df[
            [
                ORG_COL,
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
        heatmap_df[
            question_col
        ]
        .isin(
            top_responses
        )
    ]

    cross_df = (
        heatmap_df
        .groupby(
            [
                ORG_COL,
                question_col
            ]
        )
        .size()
        .unstack(
            fill_value=0
        )
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
**{analysis_df[ORG_COL].nunique()} organizations**.

The findings provide insight into the
digital readiness of road agencies and
their familiarity with emerging digital
technologies and analytical approaches.

The results help identify opportunities
for digital transformation, capacity
development and adoption of advanced
decision-support technologies across
the road sector.

Differences across organizations may
highlight varying levels of readiness
for data-driven asset management and
digital innovation.
""")

