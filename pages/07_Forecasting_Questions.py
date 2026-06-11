# ==========================================================
# FORECASTING QUESTION ANALYTICS
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


def normalize_other_response(value):

    value_text = str(value).strip()

    if value_text.lower().startswith("other"):
        return "Other Forecasting Method"

    return value_text

# ==========================================================
# QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Q16 - Forecasting Method":
        get_question_column_by_prefix("Q16"),

    "Q17 - Forecast Confidence":
        get_question_column_by_prefix("Q17"),

    "Q18 - Forecasting Barriers":
        get_question_column_by_prefix("Q18"),

    "Q19a - Multi-Year Budgeting":
        get_question_column_by_text("Multi-year budgeting"),

    "Q19b - Treatment Timing Decisions":
        get_question_column_by_text("Treatment timing decisions"),

    "Q19c - Network-Level Optimisation":
        get_question_column_by_text("Network-level optimisation"),

    "Q19d - Risk-Based Prioritisation":
        get_question_column_by_text("Risk-based prioritisation"),

    "Q19e - Funding Justification":
        get_question_column_by_text("Justification of funding requests")
}

QUESTION_MAP = {
    key: value
    for key, value in QUESTION_MAP.items()
    if value is not None
}

if not QUESTION_MAP:

    st.error(
        "No Forecasting question columns were found in the dataset."
    )

    st.stop()

# ==========================================================
# QUESTION DESCRIPTIONS
# ==========================================================

QUESTION_DESCRIPTIONS = {

    "Q16 - Forecasting Method":
        "Methods used by agencies to forecast pavement deterioration and future condition.",

    "Q17 - Forecast Confidence":
        "Level of confidence in existing deterioration forecasts.",

    "Q18 - Forecasting Barriers":
        "Factors limiting the use of forecasting techniques and deterioration modelling.",

    "Q19a - Multi-Year Budgeting":
        "Influence of forecasting outputs on multi-year budgeting decisions.",

    "Q19b - Treatment Timing Decisions":
        "Influence of forecasting outputs on treatment timing decisions.",

    "Q19c - Network-Level Optimisation":
        "Influence of forecasting outputs on network-level optimisation.",

    "Q19d - Risk-Based Prioritisation":
        "Influence of forecasting outputs on risk-based prioritisation.",

    "Q19e - Funding Justification":
        "Influence of forecasting outputs on justification of funding requests."
}

# ==========================================================
# MULTI-SELECT QUESTIONS
# ==========================================================

MULTISELECT_QUESTIONS = [
    "Q18"
]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Forecasting Question Analytics"
)

st.markdown("""
This page explores forecasting practices, confidence levels, barriers
and decision-support applications that contribute to Forecasting Maturity.
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
    "Select Forecasting Question",
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

# ==========================================================
# NORMALIZE Q16 OTHER RESPONSES
# ==========================================================

if selected_question == "Q16 - Forecasting Method":

    responses = responses.apply(
        normalize_other_response
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

    if question_code in MULTISELECT_QUESTIONS:

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

        heatmap_df[question_col] = (
            heatmap_df[question_col]
            .astype(str)
            .str.strip()
        )

    if selected_question == "Q16 - Forecasting Method":

        heatmap_df[question_col] = (
            heatmap_df[question_col]
            .apply(normalize_other_response)
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

The findings provide insight into forecasting maturity, confidence in
deterioration modelling and the use of forecasting in decision-making.

Differences across agencies may highlight opportunities for improved
forecasting capability, evidence-based planning and asset management maturity.
""")
