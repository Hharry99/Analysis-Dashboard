# ==========================================================
# OPEN ENDED INSIGHTS
# Sprint 3C.3 - Polished Production Version
# ==========================================================

import html
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset
from utils.theme_coder import build_theme_dataset

from utils.dashboard_style import apply_dashboard_style

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Open Ended Insights",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# VISUAL STYLE SETTINGS
# ==========================================================

BAR_COLOR_SEQUENCE = px.colors.qualitative.Bold
PIE_COLOR_SEQUENCE = px.colors.qualitative.Set2
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

.framework-note {
    background-color: rgba(217, 119, 6, 0.10);
    border-left: 5px solid #D97706;
    padding: 16px 18px;
    border-radius: 10px;
    margin-top: 10px;
    margin-bottom: 20px;
    font-size: 15px;
    line-height: 1.5;
}

.insight-box{
    border-left:6px solid #7C3AED;
    background:rgba(124,58,237,0.08);
    padding:18px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

.quote-card {
    background-color: rgba(59, 130, 246, 0.10);
    border-left: 5px solid #2563EB;
    padding: 16px 18px;
    border-radius: 10px;
    margin-bottom: 14px;
    font-size: 15px;
    line-height: 1.55;
}

.quote-title {
    font-weight: 700;
    margin-bottom: 8px;
    color: #1E40AF;
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

Q27_COL = (
    "Q27. What practical improvements in data systems, institutional "
    "approaches, or technical capacity would most strengthen pavement "
    "performance management in Kenya?"
)

Q28_COL = (
    "Q28. Do you have any additional comments or recommendations regarding "
    "forecasting, modelling, or use of condition data in road asset "
    "management and planning?"
)

TEXT_COLUMNS = [
    Q27_COL,
    Q28_COL
]

REQUIRED_COLS = [
    AGENCY_COL,
    Q27_COL,
    Q28_COL
]

# ==========================================================
# VALIDATION
# ==========================================================

missing_cols = [
    col for col in REQUIRED_COLS
    if col not in master_df.columns
]

if missing_cols:

    st.error(
        f"Missing required columns: {missing_cols}"
    )

    st.stop()

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


def shorten_label(value, max_length=75):

    text = str(value)

    if len(text) > max_length:

        return text[:max_length - 3] + "..."

    return text

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Open Ended Insights"
)

st.markdown("""
This page presents qualitative insights extracted from open-ended survey
responses.

Responses were automatically coded into operational themes covering
institutional capacity, data quality, forecasting, digital transformation
and asset management practices.
""")

st.markdown(
    """
<div class="framework-note">
<b>Theme Framework Note:</b>
This page presents the detailed operational qualitative themes identified
from Q27 and Q28. These operational themes provide the evidence base that
supports the higher-level strategic theme groups used in the Executive
Dashboard and benchmarking framework.
</div>
""",
    unsafe_allow_html=True
)

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

# ==========================================================
# BUILD THEME DATASET
# ==========================================================

theme_df = build_theme_dataset(
    df=analysis_df,
    text_columns=TEXT_COLUMNS,
    agency_column=AGENCY_COL
)

# ==========================================================
# THEME DATASET VALIDATION
# ==========================================================

if theme_df.empty:

    st.warning(
        "No themes were identified from the selected responses."
    )

    st.stop()

required_theme_cols = [
    "Theme",
    "Response",
    "Agency"
]

missing_theme_cols = [
    col for col in required_theme_cols
    if col not in theme_df.columns
]

if missing_theme_cols:

    st.error(
        f"Theme dataset is missing required columns: {missing_theme_cols}"
    )

    st.stop()

# ==========================================================
# KPI SECTION
# ==========================================================

total_q27 = (
    analysis_df[Q27_COL]
    .dropna()
    .shape[0]
)

total_q28 = (
    analysis_df[Q28_COL]
    .dropna()
    .shape[0]
)

total_open_responses = (
    total_q27
    +
    total_q28
)

total_themes = (
    theme_df["Theme"]
    .nunique()
)

coded_records = len(
    theme_df
)

participating_agencies = (
    analysis_df[AGENCY_COL]
    .nunique()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Q27 Responses",
    total_q27
)

c2.metric(
    "Q28 Responses",
    total_q28
)

c3.metric(
    "Operational Themes",
    total_themes
)

c4.metric(
    "Theme Mentions",
    coded_records
)

# ==========================================================
# THEME FREQUENCY ANALYSIS
# ==========================================================

theme_freq = (
    theme_df["Theme"]
    .value_counts()
    .reset_index()
)

theme_freq.columns = [
    "Theme",
    "Count"
]

theme_freq = add_percentage(
    theme_freq,
    "Count"
)

theme_freq = (
    theme_freq
    .sort_values(
        "Count",
        ascending=False
    )
    .reset_index(drop=True)
)

theme_freq["Display Theme"] = theme_freq["Theme"].apply(
    shorten_label
)

top_theme = (
    theme_freq.iloc[0]["Theme"]
    if len(theme_freq) > 0
    else "N/A"
)

top_percentage = (
    theme_freq.iloc[0]["Percentage"]
    if len(theme_freq) > 0
    else 0
)

top_mentions = (
    theme_freq.iloc[0]["Count"]
    if len(theme_freq) > 0
    else 0
)

# ==========================================================
# QUALITATIVE INSIGHTS SNAPSHOT
# ==========================================================

st.markdown(
    f"""
<div class="insight-box">

<b>Qualitative Insights Snapshot:</b><br>
A total of <b>{total_open_responses}</b> open-ended responses were analysed
from Q27 and Q28 across <b>{participating_agencies}</b> participating agencies.

<br><br>
The coding process identified <b>{total_themes}</b> operational themes and
generated <b>{coded_records}</b> theme mentions.

<br><br>
The most frequently mentioned operational theme was <b>{top_theme}</b>,
with <b>{top_mentions}</b> mentions, representing approximately
<b>{top_percentage}%</b> of all coded theme references.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# OPERATIONAL THEME FREQUENCY ANALYSIS
# ==========================================================

st.markdown(
    "<div class='section-title'>Operational Theme Frequency Analysis</div>",
    unsafe_allow_html=True
)

chart_theme_freq = theme_freq.sort_values(
    "Count",
    ascending=True
)

fig_theme = px.bar(
    chart_theme_freq,
    x="Count",
    y="Display Theme",
    orientation="h",
    text="Percentage",
    color="Display Theme",
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title="Most Frequently Mentioned Operational Themes"
)

fig_theme.update_layout(
    yaxis_title="Operational Theme",
    xaxis_title="Number of Mentions",
    height=680,
    showlegend=False
)

fig_theme.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig_theme,
    use_container_width=True
)

# ==========================================================
# THEME DISTRIBUTION BY AGENCY
# ==========================================================

st.markdown(
    "<div class='section-title'>Theme Distribution by Agency</div>",
    unsafe_allow_html=True
)

try:

    cross_df = (
        theme_df
        .groupby(
            [
                "Agency",
                "Theme"
            ]
        )
        .size()
        .unstack(fill_value=0)
    )

    ordered_theme_cols = [
        theme for theme in theme_freq["Theme"].tolist()
        if theme in cross_df.columns
    ]

    cross_df = cross_df[
        ordered_theme_cols
    ]

    fig_heatmap = px.imshow(
        cross_df,
        aspect="auto",
        title="Operational Theme Frequency by Agency",
        labels=dict(
            x="Operational Theme",
            y="Agency",
            color="Mentions"
        ),
        color_continuous_scale=HEATMAP_SCALE
    )

    fig_heatmap.update_layout(
        height=700
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Heatmap could not be generated: {e}"
    )

# ==========================================================
# THEME SHARE DONUT
# ==========================================================

st.markdown(
    "<div class='section-title'>Operational Theme Share</div>",
    unsafe_allow_html=True
)

fig_theme_share = px.pie(
    theme_freq,
    names="Theme",
    values="Percentage",
    hole=0.55,
    title="Share of Operational Theme Mentions",
    color_discrete_sequence=PIE_COLOR_SEQUENCE
)

fig_theme_share.update_layout(
    height=520
)

st.plotly_chart(
    fig_theme_share,
    use_container_width=True
)

# ==========================================================
# THEME SUMMARY
# ==========================================================

st.markdown(
    "<div class='section-title'>Theme Summary</div>",
    unsafe_allow_html=True
)

st.dataframe(
    theme_freq[
        [
            "Theme",
            "Count",
            "Percentage"
        ]
    ],
    use_container_width=True
)

# ==========================================================
# REPRESENTATIVE QUOTATIONS
# ==========================================================

st.markdown(
    "<div class='section-title'>Representative Quotations</div>",
    unsafe_allow_html=True
)

selected_theme = st.selectbox(
    "Select Theme",
    sorted(
        theme_df["Theme"]
        .dropna()
        .unique()
    )
)

theme_quotes = (
    theme_df[
        theme_df["Theme"] == selected_theme
    ]
    .drop_duplicates(
        subset=[
            "Response"
        ]
    )
)

max_quotes = min(
    5,
    len(theme_quotes)
)

st.markdown(
    "### Selected Quotations"
)

if max_quotes == 0:

    st.warning(
        "No representative quotations are available for the selected theme."
    )

else:

    for i, (_, row) in enumerate(
        theme_quotes
        .head(max_quotes)
        .iterrows(),
        start=1
    ):

        quote = (
            str(row["Response"])
            .replace("\n", " ")
            .strip()
        )

        safe_quote = html.escape(
            quote
        )

        st.markdown(
            f"""
<div class="quote-card">
    <div class="quote-title">Quote {i}</div>
    {safe_quote}
</div>
""",
            unsafe_allow_html=True
        )

# ==========================================================
# DETAILED THEME TABLES
# ==========================================================

with st.expander(
    "View Detailed Theme Occurrence Summary",
    expanded=False
):

    theme_agency = (
        theme_df
        .groupby(
            [
                "Theme",
                "Agency"
            ]
        )
        .size()
        .reset_index(name="Count")
    )

    theme_agency = theme_agency.sort_values(
        [
            "Theme",
            "Agency"
        ]
    )

    st.dataframe(
        theme_agency,
        use_container_width=True
    )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(
    f"""
### Executive Interpretation

A total of **{total_open_responses} open-ended responses** were analysed from
Q27 and Q28.

The thematic coding process identified **{total_themes} operational themes**
and generated **{coded_records} coded theme mentions**.

A theme mention represents one occurrence of a theme within a response.
Individual responses may contribute to multiple themes.

The most frequently mentioned operational theme was **{top_theme}**,
representing approximately **{top_percentage}%** of all coded theme references.

The qualitative responses highlight stakeholder priorities relating to
institutional strengthening, data quality, forecasting capability, digital
transformation and evidence-based road asset management.

These findings provide valuable context to the quantitative maturity indices
and help explain the practical needs identified by respondents across
participating agencies.
"""
)
