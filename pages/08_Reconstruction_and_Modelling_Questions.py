# ==========================================================
# RECONSTRUCTION AND MODELLING QUESTION ANALYTICS
# Sprint 3B.5B - Polished Production Version
# ==========================================================

import streamlit as st
import textwrap
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

from utils.dashboard_style import apply_dashboard_style
from utils.dashboard_navigation import apply_sidebar_navigation

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Reconstruction & Modelling Questions",
    page_icon="◇",
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
    border-left:6px solid #059669;
    background:rgba(5,150,105,0.08);
    padding:18px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}


.compact-table{
    width:100%;
    border-collapse:collapse;
    font-size:13px;
    line-height:1.35;
    margin-top:8px;
    margin-bottom:18px;
}

.compact-table th{
    text-align:left;
    padding:8px 10px;
    border-bottom:1px solid rgba(128,128,128,0.35);
    background:rgba(15,23,42,0.04);
    font-weight:700;
}

.compact-table td{
    padding:8px 10px;
    border-bottom:1px solid rgba(128,128,128,0.22);
    vertical-align:top;
    white-space:normal;
    word-break:normal;
    overflow-wrap:break-word;
}

.compact-table .num{
    text-align:right;
    white-space:nowrap;
}

.compact-table .center{
    text-align:center;
    white-space:nowrap;
}

.question-box{
    border-left:5px solid #2563EB;
    background:rgba(37,99,235,0.08);
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


def apply_sidebar_visibility_override():

    st.markdown(
        """
<style>

/* Reconstruction & Modelling Questions fallback override for grouped navigation visibility */
section[data-testid="stSidebar"] div[data-testid="stExpander"] details summary,
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary,
section[data-testid="stSidebar"] details summary{
    background:#F3F4F6 !important;
    color:#111827 !important;
    min-height:44px !important;
    padding:10px 13px !important;
    font-size:16px !important;
    font-weight:900 !important;
    line-height:1.25 !important;
}

section[data-testid="stSidebar"] div[data-testid="stExpander"] details summary *,
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary *,
section[data-testid="stSidebar"] details summary *{
    color:#111827 !important;
    fill:#111827 !important;
    stroke:#111827 !important;
    font-size:16px !important;
    font-weight:900 !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] *,
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a *{
    color:#F9FAFB !important;
    font-size:15.8px !important;
    font-weight:800 !important;
    line-height:1.25 !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]{
    padding:8px 10px !important;
    border-radius:9px !important;
    margin-bottom:3px !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover{
    background:rgba(255,255,255,0.12) !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div{
    background:#FFFFFF !important;
    color:#111827 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] input,
section[data-testid="stSidebar"] [data-baseweb="select"] div,
section[data-testid="stSidebar"] [data-baseweb="select"] span{
    color:#111827 !important;
    font-weight:600 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] input::placeholder{
    color:#374151 !important;
    opacity:1 !important;
}

</style>
""",
        unsafe_allow_html=True
    )

# ==========================================================
# DASHBOARD VISUAL POLISH ADDITIONS
# ==========================================================

apply_dashboard_style()
apply_sidebar_navigation(
    "Reconstruction & Modelling Questions"
)
apply_sidebar_visibility_override()

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


def prepare_multiselect_responses(series):

    return (
        series
        .dropna()
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
    )


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

    wrapped = textwrap.wrap(
        text,
        width=max_length,
        break_long_words=False,
        break_on_hyphens=False
    )

    if not wrapped:
        return text

    return "<br>".join(
        wrapped
    )


def apply_readable_horizontal_bar_layout(fig, row_count, height_min=520):

    chart_height = max(
        height_min,
        min(
            940,
            210 + row_count * 50
        )
    )

    fig.update_layout(
        height=chart_height,
        showlegend=False,
        margin=dict(
            l=60,
            r=115,
            t=80,
            b=95
        ),
        xaxis=dict(
            automargin=True,
            title_standoff=20
        ),
        yaxis=dict(
            automargin=True,
            title_standoff=20
        )
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    return fig


def apply_readable_heatmap_layout(fig, height=610):

    fig.update_layout(
        height=height,
        margin=dict(
            l=80,
            r=40,
            t=80,
            b=80
        ),
        xaxis=dict(
            automargin=True,
            tickangle=0,
            title_standoff=25
        ),
        yaxis=dict(
            automargin=True,
            title_standoff=20
        ),
        coloraxis_showscale=False
    )

    return fig


def make_display_table(df_in, response_col="Response", max_length=78):

    df_out = df_in.copy()

    if "Percentage" in df_out.columns:

        df_out["Percentage"] = df_out["Percentage"].map(
            lambda x: f"{float(x):.1f}%"
        )

    return df_out


def render_compact_table(df_in, numeric_columns=None, max_rows=None):

    numeric_columns = numeric_columns or []

    df_out = df_in.copy()

    if max_rows is not None:

        df_out = df_out.head(max_rows)

    html_rows = []

    headers = "".join(
        f"<th>{str(col)}</th>"
        for col in df_out.columns
    )

    for _, row in df_out.iterrows():

        cells = []

        for col in df_out.columns:

            value = row[col]

            css_class = (
                "num"
                if col in numeric_columns
                else ""
            )

            cells.append(
                f"<td class='{css_class}'>{str(value)}</td>"
            )

        html_rows.append(
            "<tr>" + "".join(cells) + "</tr>"
        )

    table_html = (
        "<table class='compact-table'>"
        "<thead><tr>"
        + headers
        + "</tr></thead>"
        "<tbody>"
        + "".join(html_rows)
        + "</tbody></table>"
    )

    st.markdown(
        table_html,
        unsafe_allow_html=True
    )


def build_response_key(responses):

    key_rows = []

    for idx, response in enumerate(
        responses,
        start=1
    ):

        key_rows.append({
            "Code": f"R{idx}",
            "Full Response Category": response
        })

    return pd.DataFrame(
        key_rows
    )

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
        reconstructed or model-estimated pavement condition data where direct
        condition data are unavailable.
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

question_col = QUESTION_MAP[
    selected_question
]

question_code = (
    selected_question
    .split(" - ")[0]
)

question_type = (
    "Multi-select"
    if question_code in MULTISELECT_QUESTIONS
    else "Single-select"
)

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

if question_code in MULTISELECT_QUESTIONS:

    responses = prepare_multiselect_responses(
        analysis_df[question_col]
    )

else:

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

chart_df = (
    freq_df
    .head(10)
    .sort_values(
        "Count",
        ascending=True
    )
    .copy()
)

chart_df["Display Response"] = chart_df["Response"].apply(
    lambda x: shorten_label(
        x,
        max_length=46
    )
)

max_count = chart_df["Count"].max()

fig = px.bar(
    chart_df,
    x="Count",
    y="Display Response",
    orientation="h",
    text="Percentage",
    color="Display Response",
    custom_data=[
        "Response",
        "Count"
    ],
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title=f"{selected_question} Response Distribution"
)

fig.update_layout(
    yaxis_title="Response",
    xaxis_title="Number of Responses",
    xaxis=dict(
        range=[
            0,
            max(
                5,
                max_count * 1.20
            )
        ]
    )
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    hovertemplate=(
        "Response: %{customdata[0]}<br>"
        "Count: %{customdata[1]}<br>"
        "Share: %{text:.1f}%<extra></extra>"
    )
)

fig = apply_readable_horizontal_bar_layout(
    fig,
    row_count=len(chart_df),
    height_min=560
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "Takeaway: The chart shows the leading response categories for the selected reconstruction and modelling question. Full response details remain available in the summary table below."
)

# ==========================================================
# AGENCY COMPARISON
# ==========================================================

st.markdown(
    "<div class='section-title'>Agency Comparison</div>",
    unsafe_allow_html=True
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
        .head(8)["Response"]
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

    response_key_df = build_response_key(
        list(cross_df.columns)
    )

    response_code_map = dict(
        zip(
            response_key_df["Full Response Category"],
            response_key_df["Code"]
        )
    )

    cross_df = cross_df.rename(
        columns=response_code_map
    )

    fig2 = px.imshow(
        cross_df,
        aspect="auto",
        title="Response Heatmap by Agency",
        labels=dict(
            x="Response category code",
            y="Agency",
            color="Count"
        ),
        color_continuous_scale=HEATMAP_SCALE,
        text_auto=True
    )

    fig2.update_xaxes(
        tickangle=0
    )

    fig2 = apply_readable_heatmap_layout(
        fig2,
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.caption(
        "Takeaway: The heatmap uses response category codes to avoid congested labels. The full response names are shown in the key below."
    )

    st.markdown(
        "#### Response Category Key"
    )

    render_compact_table(
        response_key_df,
        numeric_columns=[],
        max_rows=None
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

summary_display_df = make_display_table(
    summary_display_df,
    response_col="Response",
    max_length=78
)

summary_display_df.insert(
    0,
    "No.",
    range(
        1,
        len(summary_display_df) + 1
    )
)

render_compact_table(
    summary_display_df,
    numeric_columns=[
        "No.",
        "Count",
        "Percentage"
    ],
    max_rows=None
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

        agency_response_display_df = make_display_table(
            agency_response_df,
            response_col="Response",
            max_length=85
        )

        agency_response_display_df.insert(
            0,
            "No.",
            range(
                1,
                len(agency_response_display_df) + 1
            )
        )

        render_compact_table(
            agency_response_display_df,
            numeric_columns=[
                "No.",
                "Count"
            ],
            max_rows=None
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

The findings provide insight into stakeholder confidence in reconstructed
pavement condition data and the potential role of analytical reconstruction
or model-estimated condition data in supporting road asset management decisions.

Differences across agencies may indicate varying levels of readiness to adopt
model-based approaches for network management, lifecycle planning, treatment
prioritisation, budgeting and funding allocation.
""")

# ==========================================================
# NEXT PAGE HINT
# ==========================================================

st.divider()

try:

    st.page_link(
        "pages/09_Digital_Readiness_Questions.py",
        label="Next suggested page: Digital Readiness Questions",
        icon="➡️"
    )

except Exception:

    st.caption(
        "Next suggested page: Digital Readiness Questions →"
    )

