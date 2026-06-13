# ==========================================================
# RESPONDENT PROFILE ANALYSIS
# Sprint 3A - Page 1
# Polished Production Version
# ==========================================================

import streamlit as st
import textwrap
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

from utils.dashboard_style import apply_dashboard_style
from utils.dashboard_navigation import apply_sidebar_navigation

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Respondent Profile",
    page_icon="☷",
    layout="wide"
)

# ==========================================================
# VISUAL STYLE SETTINGS
# ==========================================================

COLOR_SEQUENCE = px.colors.qualitative.Set2
ALT_COLOR_SEQUENCE = px.colors.qualitative.Pastel
POSITION_COLOR_SEQUENCE = px.colors.qualitative.Bold

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

/* Respondent Profile fallback override for grouped navigation visibility */
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
    "Respondent Profile"
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


df = load_data()

df = clean_master_dataset(
    df
)

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

AGENCY_COL = "Q1. What agency do you work for?"
LEVEL_COL = "Q2. At what level do you work?"
POSITION_COL = "Q3. What position do you currently hold?"
EXP_COL = "Q4. How many years of experience do you have in road asset management?"

REQUIRED_COLS = [
    AGENCY_COL,
    LEVEL_COL,
    POSITION_COL,
    EXP_COL
]

# ==========================================================
# VALIDATION
# ==========================================================

missing_cols = [
    col for col in REQUIRED_COLS
    if col not in df.columns
]

if missing_cols:

    st.error(
        f"Missing required columns: {missing_cols}"
    )

    st.stop()

df = df.dropna(
    subset=[
        AGENCY_COL
    ]
)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

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


def sort_experience_categories(exp_df):

    order = [
        "Less than 5 years",
        "5–10 years",
        "5-10 years",
        "10–20 years",
        "10-20 years",
        "More than 20 years"
    ]

    exp_df = exp_df.copy()

    exp_df["Sort_Order"] = exp_df["Experience"].apply(
        lambda x: order.index(x)
        if x in order
        else len(order)
    )

    exp_df = exp_df.sort_values(
        [
            "Sort_Order",
            "Experience"
        ]
    )

    exp_df = exp_df.drop(
        columns=[
            "Sort_Order"
        ]
    )

    return exp_df


def wrap_label(value, width=34):

    text = str(value)

    wrapped = textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False
    )

    if not wrapped:
        return text

    return "<br>".join(
        wrapped
    )


def shorten_label(value, max_length=34):

    return wrap_label(
        value,
        width=max_length
    )


def shorten_work_level(label):

    return wrap_label(
        label,
        width=34
    )


def apply_readable_donut_layout(fig, height=560):

    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        insidetextorientation="radial",
        hovertemplate=(
            "Category: %{label}<br>"
            "Responses: %{value}<br>"
            "Share: %{percent}<extra></extra>"
        )
    )

    fig.update_layout(
        height=height,
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=70,
            b=40
        ),
        uniformtext_minsize=10,
        uniformtext_mode="show"
    )

    return fig


def apply_readable_horizontal_bar_layout(fig, height=540):

    fig.update_layout(
        height=height,
        showlegend=False,
        margin=dict(
            l=60,
            r=105,
            t=80,
            b=90
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
        texttemplate="%{text}",
        textposition="outside",
        cliponaxis=False
    )

    return fig

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Respondent Profile Analysis"
)

st.markdown("""
This section examines the demographic and professional characteristics
of practitioners who participated in the study.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

total_respondents = len(df)
total_agencies = df[AGENCY_COL].nunique()
total_positions = df[POSITION_COL].nunique()
total_work_levels = df[LEVEL_COL].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Respondents",
    total_respondents
)

c2.metric(
    "Agencies",
    total_agencies
)

c3.metric(
    "Positions",
    total_positions
)

c4.metric(
    "Work Levels",
    total_work_levels
)

# ==========================================================
# RESPONDENT COVERAGE SNAPSHOT
# ==========================================================

agency_list = ", ".join(
    sorted(
        df[AGENCY_COL]
        .dropna()
        .astype(str)
        .unique()
    )
)

st.markdown(
    f"""
<div class="insight-box">

<b>Respondent Coverage Snapshot:</b><br>
The survey captured <b>{total_respondents}</b> practitioner responses
from <b>{total_agencies}</b> road-sector agencies and
<b>{total_positions}</b> distinct professional positions.

<br><br>
<b>Agencies represented:</b> {agency_list}

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# AGENCY DISTRIBUTION
# ==========================================================

st.markdown(
    "<div class='section-title'>Agency Distribution</div>",
    unsafe_allow_html=True
)

agency_counts = (
    df[AGENCY_COL]
    .dropna()
    .value_counts()
    .reset_index()
)

agency_counts.columns = [
    "Agency",
    "Responses"
]

agency_counts = add_percentage(
    agency_counts,
    "Responses"
)

fig_agency = px.pie(
    agency_counts,
    names="Agency",
    values="Responses",
    hole=0.55,
    title="Distribution of Respondents by Agency",
    color_discrete_sequence=ALT_COLOR_SEQUENCE
)

fig_agency = apply_readable_donut_layout(
    fig_agency,
    height=560
)

st.plotly_chart(
    fig_agency,
    use_container_width=True
)

agency_display_df = agency_counts.copy()

agency_display_df["Percentage"] = (
    agency_display_df["Percentage"]
    .map(lambda x: f"{x:.1f}%")
)

st.dataframe(
    agency_display_df,
    use_container_width=True,
    hide_index=True,
    height=min(
        300,
        36 * len(agency_display_df) + 40
    )
)

# ==========================================================
# WORK LEVEL DISTRIBUTION
# ==========================================================

st.markdown(
    "<div class='section-title'>Work Level Distribution</div>",
    unsafe_allow_html=True
)

level_counts = (
    df[LEVEL_COL]
    .dropna()
    .value_counts()
    .reset_index()
)

level_counts.columns = [
    "Work Level",
    "Respondents"
]

level_counts = add_percentage(
    level_counts,
    "Respondents"
)

level_counts["Display Work Level"] = (
    level_counts["Work Level"]
    .apply(
        shorten_work_level
    )
)

level_chart_df = level_counts.sort_values(
    "Respondents",
    ascending=True
)

fig_level = px.bar(
    level_chart_df,
    x="Respondents",
    y="Display Work Level",
    orientation="h",
    text="Respondents",
    color="Display Work Level",
    custom_data=[
        "Work Level"
    ],
    color_discrete_sequence=COLOR_SEQUENCE,
    title="Respondents by Work Level"
)

fig_level.update_layout(
    xaxis_title="Number of Respondents",
    yaxis_title="Work Level",
    xaxis=dict(
        range=[
            0,
            max(
                5,
                level_chart_df["Respondents"].max() * 1.18
            )
        ]
    )
)

fig_level.update_traces(
    hovertemplate=(
        "Work Level: %{customdata[0]}<br>"
        "Respondents: %{x}<extra></extra>"
    )
)

fig_level = apply_readable_horizontal_bar_layout(
    fig_level,
    height=520
)

st.plotly_chart(
    fig_level,
    use_container_width=True
)

# ==========================================================
# POSITION DISTRIBUTION
# ==========================================================

st.markdown(
    "<div class='section-title'>Position Distribution</div>",
    unsafe_allow_html=True
)

position_counts = (
    df[POSITION_COL]
    .dropna()
    .value_counts()
    .head(15)
    .reset_index()
)

position_counts.columns = [
    "Position",
    "Respondents"
]

position_counts = add_percentage(
    position_counts,
    "Respondents"
)

position_counts["Display Position"] = (
    position_counts["Position"]
    .apply(
        lambda x: shorten_label(
            x,
            max_length=42
        )
    )
)

position_chart_df = position_counts.sort_values(
    "Respondents",
    ascending=True
)

fig_position = px.bar(
    position_chart_df,
    x="Respondents",
    y="Display Position",
    orientation="h",
    text="Respondents",
    color="Display Position",
    custom_data=[
        "Position"
    ],
    color_discrete_sequence=POSITION_COLOR_SEQUENCE,
    title="Top Positions Represented"
)

fig_position.update_layout(
    xaxis_title="Number of Respondents",
    yaxis_title="Position",
    xaxis=dict(
        range=[
            0,
            max(
                5,
                position_chart_df["Respondents"].max() * 1.20
            )
        ]
    )
)

fig_position.update_traces(
    hovertemplate=(
        "Position: %{customdata[0]}<br>"
        "Respondents: %{x}<extra></extra>"
    )
)

fig_position = apply_readable_horizontal_bar_layout(
    fig_position,
    height=780
)

st.plotly_chart(
    fig_position,
    use_container_width=True
)

# ==========================================================
# EXPERIENCE PROFILE
# ==========================================================

st.markdown(
    "<div class='section-title'>Experience Profile</div>",
    unsafe_allow_html=True
)

exp_counts = (
    df[EXP_COL]
    .dropna()
    .value_counts()
    .reset_index()
)

exp_counts.columns = [
    "Experience",
    "Respondents"
]

exp_counts = sort_experience_categories(
    exp_counts
)

exp_counts = add_percentage(
    exp_counts,
    "Respondents"
)

fig_exp = px.bar(
    exp_counts,
    x="Experience",
    y="Respondents",
    text="Respondents",
    color="Experience",
    color_discrete_sequence=COLOR_SEQUENCE,
    title="Years of Experience Distribution"
)

fig_exp.update_layout(
    xaxis_title="Years of Experience",
    yaxis_title="Number of Respondents",
    height=520,
    showlegend=False,
    margin=dict(
        l=50,
        r=60,
        t=70,
        b=90
    ),
    xaxis=dict(
        automargin=True,
        title_standoff=20
    ),
    yaxis=dict(
        automargin=True
    )
)

fig_exp.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    cliponaxis=False
)

st.plotly_chart(
    fig_exp,
    use_container_width=True
)

# ==========================================================
# RESPONDENT SUMMARY TABLE
# ==========================================================

st.markdown(
    "<div class='section-title'>Respondent Summary</div>",
    unsafe_allow_html=True
)

summary_df = pd.DataFrame({
    "Metric": [
        "Total Respondents",
        "Participating Agencies",
        "Distinct Positions",
        "Work Levels Represented"
    ],
    "Value": [
        total_respondents,
        total_agencies,
        total_positions,
        total_work_levels
    ]
})

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
    height=min(
        260,
        36 * len(summary_df) + 40
    )
)

# ==========================================================
# DETAILED SUMMARY TABLES
# ==========================================================

with st.expander(
    "View Detailed Respondent Tables",
    expanded=False
):

    st.markdown(
        "### Agency Response Summary"
    )

    st.dataframe(
        agency_counts,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "### Work Level Summary"
    )

    st.dataframe(
        level_counts,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "### Position Summary"
    )

    st.dataframe(
        position_counts,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "### Experience Summary"
    )

    st.dataframe(
        exp_counts,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

largest_agency = (
    agency_counts.iloc[0]["Agency"]
    if not agency_counts.empty
    else "Not Available"
)

largest_agency_share = (
    agency_counts.iloc[0]["Percentage"]
    if not agency_counts.empty
    else 0
)

dominant_level = (
    level_counts.iloc[0]["Work Level"]
    if not level_counts.empty
    else "Not Available"
)

dominant_position = (
    position_counts.iloc[0]["Position"]
    if not position_counts.empty
    else "Not Available"
)

st.info(f"""
### Key Insights

A total of **{total_respondents} practitioners** participated in the study.

Respondents were drawn from **{total_agencies} road-sector agencies** and
represented **{total_positions} distinct professional positions** across
**{total_work_levels} work levels**.

The largest respondent share came from **{largest_agency}**,
representing approximately **{largest_agency_share}%** of responses.

The most represented work level was **{dominant_level}**, while the most
common position category was **{dominant_position}**.

The respondent profile provides a diverse representation of stakeholders
involved in pavement management, road asset management, maintenance planning,
technical assessment and institutional decision-making.
""")

# ==========================================================
# NEXT PAGE HINT
# ==========================================================

st.divider()

try:

    st.page_link(
        "pages/02_Data_Maturity_Analysis.py",
        label="Next suggested page: Data Maturity Analysis",
        icon="➡️"
    )

except Exception:

    st.caption(
        "Next suggested page: Data Maturity Analysis →"
    )

