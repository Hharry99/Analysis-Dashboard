# ==========================================================
# RECONSTRUCTION AND MODELLING QUESTION ANALYTICS
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
    page_title="Reconstruction & Modelling Questions",
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
# HELPER FUNCTIONS
# ==========================================================

def get_question_column_by_prefix(question_code):

    matches = [
        col for col in master_df.columns
        if col.startswith(question_code)
    ]

    if matches:
        return matches[0]

    return None


def get_question_column_by_text(search_text):

    matches = [
        col for col in master_df.columns
        if search_text.lower() in col.lower()
    ]

    if matches:
        return matches[0]

    return None

# ==========================================================
# QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Q20 - Willingness to Use Reconstructed Data":
        get_question_column_by_prefix("Q20"),

    "Q21 - Conditions for Trusting Reconstructed Data":
        get_question_column_by_prefix("Q21"),

    "Q22a - Network-Level Performance Analysis":
        get_question_column_by_text("Network-level performance analysis"),

    "Q22b - Life-Cycle Modelling and Long-Term Planning":
        get_question_column_by_text("Life-cycle modelling"),

    "Q22c - Treatment Timing and Optimisation":
        get_question_column_by_text("Treatment timing"),

    "Q22d - Budget Allocation and Justification":
        get_question_column_by_text("Budget allocation")
}

QUESTION_MAP = {
    key: value
    for key, value in QUESTION_MAP.items()
    if value is not None
}

if not QUESTION_MAP:

    st.error(
        "No Reconstruction and Modelling question columns were found in the dataset."
    )

    st.stop()

# ==========================================================
# QUESTION DESCRIPTIONS
# ==========================================================

QUESTION_DESCRIPTIONS = {

    "Q20 - Willingness to Use Reconstructed Data":
        """
        Assesses the likelihood that respondents would use analytically
        reconstructed or model-estimated pavement condition data where
        direct condition data are unavailable.
        """,

    "Q21 - Conditions for Trusting Reconstructed Data":
        """
        Identifies the requirements respondents consider necessary before
        relying on reconstructed condition information for planning and
        investment decisions.
        """,

    "Q22a - Network-Level Performance Analysis":
        """
        Assesses the suitability of reconstructed condition data for network
        performance monitoring and analysis.
        """,

    "Q22b - Life-Cycle Modelling and Long-Term Planning":
        """
        Assesses the suitability of reconstructed condition data for long-term
        pavement management and life-cycle planning.
        """,

    "Q22c - Treatment Timing and Optimisation":
        """
        Assesses the suitability of reconstructed condition data for maintenance
        timing and intervention optimisation.
        """,

    "Q22d - Budget Allocation and Justification":
        """
        Assesses the suitability of reconstructed condition data for funding
        allocation and investment justification.
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
    "Reconstruction & Modelling Questions"
)

st.markdown("""
This page examines stakeholder attitudes towards reconstructed condition data,
model-estimated pavement conditions and the potential application of such data
in road asset management decision-making.
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
    "Select Reconstruction Question",
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

else:

    responses = (
        responses
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
    height=600
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

The results provide insight into stakeholder confidence in reconstructed
pavement condition data and the potential role of analytical reconstruction
techniques in supporting road asset management decisions.

Differences across agencies may indicate varying levels of readiness to adopt
model-based approaches for network management, planning, prioritisation and
funding allocation.
""")
