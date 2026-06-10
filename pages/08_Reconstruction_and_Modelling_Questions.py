
# ==========================================================
# RECONSTRUCTION AND MODELLING QUESTION ANALYTICS
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
    page_title="Reconstruction & Modelling Questions",
    page_icon="🏗️",
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
# RECONSTRUCTION QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Q20 - Willingness to Use Reconstructed Data":
        [c for c in master_df.columns
         if c.startswith("Q20")][0],

    "Q21 - Conditions for Trusting Reconstructed Data":
        [c for c in master_df.columns
         if c.startswith("Q21")][0],

    "Q22a - Network-Level Performance Analysis":
        [c for c in master_df.columns
         if "Network-level performance analysis" in c][0],

    "Q22b - Life-Cycle Modelling and Long-Term Planning":
        [c for c in master_df.columns
         if "Life-cycle modelling" in c][0],

    "Q22c - Treatment Timing and Optimisation":
        [c for c in master_df.columns
         if "Treatment timing" in c][0],

    "Q22d - Budget Allocation and Justification":
        [c for c in master_df.columns
         if "Budget allocation" in c][0]
}

# ==========================================================
# QUESTION DESCRIPTIONS
# ==========================================================

QUESTION_DESCRIPTIONS = {

    "Q20 - Willingness to Use Reconstructed Data":
        """
        Assesses the likelihood that respondents would use
        analytically reconstructed or model-estimated pavement
        condition data where direct condition data are unavailable.
        """,

    "Q21 - Conditions for Trusting Reconstructed Data":
        """
        Identifies the requirements respondents consider necessary
        before relying on reconstructed condition information for
        planning and investment decisions.
        """,

    "Q22a - Network-Level Performance Analysis":
        """
        Assesses the suitability of reconstructed condition data
        for network performance monitoring and analysis.
        """,

    "Q22b - Life-Cycle Modelling and Long-Term Planning":
        """
        Assesses the suitability of reconstructed condition data
        for long-term pavement management and life-cycle planning.
        """,

    "Q22c - Treatment Timing and Optimisation":
        """
        Assesses the suitability of reconstructed condition data
        for maintenance timing and intervention optimisation.
        """,

    "Q22d - Budget Allocation and Justification":
        """
        Assesses the suitability of reconstructed condition data
        for funding allocation and investment justification.
        """
}

# ==========================================================
# MULTI-SELECT QUESTIONS
# ==========================================================

MULTISELECT_QUESTIONS = [
    "Q21"
]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "🏗️ Reconstruction & Modelling Questions"
)

st.markdown("""
This page examines stakeholder attitudes towards
reconstructed condition data, model-estimated pavement
conditions and the potential application of such data
in road asset management decision-making.
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
    "Select Reconstruction Question",
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
    analysis_df[
        question_col
    ]
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

    if question_code in MULTISELECT_QUESTIONS:

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

        heatmap_df[
            question_col
        ] = (
            heatmap_df[
                question_col
            ]
            .astype(str)
            .str.split(";")
        )

        heatmap_df = (
            heatmap_df
            .explode(
                question_col
            )
        )

        heatmap_df[
            question_col
        ] = (
            heatmap_df[
                question_col
            ]
            .str.strip()
        )

    else:

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
    freq_df,
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

The results provide insight into stakeholder
confidence in reconstructed pavement condition
data and the potential role of analytical
reconstruction techniques in supporting
asset management decisions.

Differences across organizations may indicate
varying levels of readiness to adopt model-based
approaches for network management, planning,
prioritisation and funding allocation.
""")
