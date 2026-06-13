# ==========================================================
# DIGITAL READINESS QUESTION ANALYTICS
# Sprint 3B.5B - Polished Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

from utils.dashboard_style import apply_dashboard_style

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Digital Readiness Questions",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# VISUAL STYLE SETTINGS
# ==========================================================

COLOR_SEQUENCE = px.colors.qualitative.Set2
BAR_COLOR_SEQUENCE = px.colors.qualitative.Bold
HEATMAP_SCALE = "YlGnBu"

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:15px;
}

.insight-box{
    border-left:6px solid #2563EB;
    background:rgba(37,99,235,0.08);
    padding:18px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

.question-box{
    border-left:5px solid #7C3AED;
    background:rgba(124,58,237,0.08);
    padding:15px;
    border-radius:10px;
    margin-top:10px;
    margin-bottom:20px;
}

div[data-testid="metric-container"]{
    border-radius:16px;
    padding:18px;
    border:1px solid rgba(128,128,128,0.25);
    background:rgba(15,23,42,0.05);
}

</style>
""",
    unsafe_allow_html=True
)

# ==========================================================
# DASHBOARD VISUAL POLISH ADDITIONS
# ==========================================================

apply_dashboard_style()

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

def get_question_column(question_code):

    matches = [
        col for col in master_df.columns
        if col.startswith(question_code)
    ]

    if matches:
        return matches[0]

    return None


def prepare_single_responses(series):

    return (
        series
        .dropna()
        .astype(str)
        .str.strip()
    )


def add_percentage(df_in, count_col):

    df_out = df_in.copy()

    total = df_out[count_col].sum()

    if total > 0:

        df_out["Percentage"] = (
            df_out[count_col]
            /
            total
            *
            100
        ).round(1)

    else:

        df_out["Percentage"] = 0

    return df_out


def shorten_label(value, max_length=80):

    text = str(value)

    if len(text) > max_length:

        return text[:max_length - 3] + "..."

    return text

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
        Assesses familiarity with road infrastructure databases and their
        application in maintenance planning and decision-making.
        """,

    "Q24 - Artificial Intelligence (AI)":
        """
        Assesses familiarity with Artificial Intelligence techniques and their
        potential application in road asset management and pavement performance
        prediction.
        """,

    "Q25 - Data Analytics":
        """
        Assesses familiarity with data analytics tools, techniques and
        data-driven decision-making for infrastructure management.
        """,

    "Q26 - Multi-Criteria Decision Analysis (MCDA)":
        """
        Assesses familiarity with MCDA approaches used to support prioritisation
        and investment decisions in road asset management.
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

question_col = QUESTION_MAP[
    selected_question
]

question_type = "Single-select"

st.markdown(
    f"""
<div class="question-box">

<b>Question focus:</b> {selected_question}<br>
<b>Question type:</b> {question_type}<br><br>
{QUESTION_DESCRIPTIONS.get(selected_question, "")}

</div>
""",
    unsafe_allow_html=True
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

responses = prepare_single_responses(
    analysis_df[question_col]
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
# RESPONSE FREQUENCY TABLE
# ==========================================================

freq_df = (
    responses
    .value_counts()
    .reset_index()
)

freq_df.columns = [
    "Response",
    "Count"
]

freq_df = add_percentage(
    freq_df,
    "Count"
)

freq_df = (
    freq_df
    .sort_values(
        "Count",
        ascending=False
    )
    .reset_index(drop=True)
)

freq_df["Display Response"] = freq_df["Response"].apply(
    shorten_label
)

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

# ==========================================================
# KPI SECTION
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Survey Responses",
    len(responses)
)

c2.metric(
    "Participating Agencies",
    analysis_df[AGENCY_COL].nunique()
)

c3.metric(
    "Response Categories",
    responses.nunique()
)

c4.metric(
    "Top Response Share",
    f"{top_percentage}%"
)

# ==========================================================
# QUESTION SNAPSHOT
# ==========================================================

st.markdown(
    f"""
<div class="insight-box">

<b>Question-Level Snapshot:</b><br>
For <b>{selected_question}</b>, the most common response is
<b>{top_response}</b>, accounting for <b>{top_percentage}%</b>
of analysed responses.

<br><br>
A total of <b>{len(responses)}</b> responses were analysed across
<b>{analysis_df[AGENCY_COL].nunique()}</b> participating agencies.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# RESPONSE DISTRIBUTION
# ==========================================================

st.markdown(
    "<div class='section-title'>Response Distribution</div>",
    unsafe_allow_html=True
)

chart_df = freq_df.sort_values(
    "Count",
    ascending=True
)

fig = px.bar(
    chart_df,
    x="Count",
    y="Display Response",
    orientation="h",
    text="Percentage",
    color="Display Response",
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title=f"{selected_question} Response Distribution"
)

fig.update_layout(
    yaxis_title="Response",
    xaxis_title="Number of Responses",
    height=620,
    showlegend=False
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
    "<div class='section-title'>Agency Comparison</div>",
    unsafe_allow_html=True
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

    cross_df = cross_df[
        [
            col for col in top_responses
            if col in cross_df.columns
        ]
    ]

    fig2 = px.imshow(
        cross_df,
        aspect="auto",
        title="Response Heatmap by Agency",
        labels=dict(
            x="Response",
            y="Agency",
            color="Count"
        ),
        color_continuous_scale=HEATMAP_SCALE
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
    "<div class='section-title'>Response Summary</div>",
    unsafe_allow_html=True
)

summary_display_df = freq_df[
    [
        "Response",
        "Count",
        "Percentage"
    ]
].copy()

st.dataframe(
    summary_display_df,
    use_container_width=True
)

# ==========================================================
# DETAILED TABLES
# ==========================================================

with st.expander(
    "View Detailed Agency Response Table",
    expanded=False
):

    try:

        agency_response_df = (
            heatmap_df
            .groupby(
                [
                    AGENCY_COL,
                    question_col
                ]
            )
            .size()
            .reset_index(name="Count")
        )

        agency_response_df = agency_response_df.rename(
            columns={
                AGENCY_COL: "Agency",
                question_col: "Response"
            }
        )

        agency_response_df = agency_response_df.sort_values(
            [
                "Agency",
                "Count"
            ],
            ascending=[
                True,
                False
            ]
        )

        st.dataframe(
            agency_response_df,
            use_container_width=True
        )

    except Exception:

        st.info(
            "Detailed agency response table is not available for this selection."
        )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Executive Interpretation

The selected question was **{selected_question}**.

The most common response was **{top_response}**, representing
**{top_percentage}%** of the analysed responses.

A total of **{len(responses)} responses** were analysed across
**{analysis_df[AGENCY_COL].nunique()} agencies**.

The findings provide insight into the digital readiness of road agencies and
their familiarity with emerging digital technologies, analytical tools and
decision-support approaches.

The results help identify opportunities for digital transformation, capacity
development and adoption of advanced decision-support technologies across the
road sector.

Differences across agencies may highlight varying levels of readiness for
data-driven asset management, digital innovation, analytics adoption and
technology-enabled infrastructure planning.
""")
