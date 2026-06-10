# ==========================================================
# FORECASTING QUESTION ANALYTICS
# Sprint 3B.5A - Final Production Version
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

ORG_COL = "Q1. What agency do you work for?"

# ==========================================================
# QUESTION MAP
# ==========================================================

QUESTION_MAP = {

    "Q16 - Forecasting Method":
        [c for c in master_df.columns
         if c.startswith("Q16")][0],

    "Q17 - Forecast Confidence":
        [c for c in master_df.columns
         if c.startswith("Q17")][0],

    "Q18 - Forecasting Barriers":
        [c for c in master_df.columns
         if c.startswith("Q18")][0],

    "Q19a - Multi-Year Budgeting":
        [c for c in master_df.columns
         if "Multi-year budgeting" in c][0],

    "Q19b - Treatment Timing Decisions":
        [c for c in master_df.columns
         if "Treatment timing decisions" in c][0],

    "Q19c - Network-Level Optimisation":
        [c for c in master_df.columns
         if "Network-level optimisation" in c][0],

    "Q19d - Risk-Based Prioritisation":
        [c for c in master_df.columns
         if "Risk-based prioritisation" in c][0],

    "Q19e - Funding Justification":
        [c for c in master_df.columns
         if "Justification of funding requests" in c][0]
}

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
# PAGE HEADER
# ==========================================================

st.title("🔮 Forecasting Question Analytics")

st.markdown("""
This page explores forecasting practices,
confidence levels, barriers and decision-support
applications that contribute to Forecasting Maturity.
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
    master_df[ORG_COL]
    .isin(selected_agencies)
]

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
# NORMALIZE Q16 OTHER RESPONSES
# ==========================================================

if selected_question == \
    "Q16 - Forecasting Method":

    responses = responses.apply(

        lambda x:
        "Other Forecasting Method"

        if str(x).startswith(
            "Other"
        )

        else x
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
    analysis_df[ORG_COL]
    .nunique()
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
            [ORG_COL, question_col]
        ]
        .dropna()
        .copy()
    )

    if selected_question == \
        "Q16 - Forecasting Method":

        heatmap_df[question_col] = (
            heatmap_df[question_col]
            .apply(
                lambda x:
                "Other Forecasting Method"

                if str(x).startswith(
                    "Other"
                )

                else x
            )
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
        title="Agency Comparison Heatmap"
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

The findings provide insight into
forecasting maturity, confidence in
deterioration modelling and the use
of forecasting in decision-making.

Differences across organizations may
highlight opportunities for improved
forecasting capability, evidence-based
planning and asset management maturity.
""")
