# ==========================================================
# OPEN ENDED INSIGHTS
# Sprint 3C.3 - Framework Aligned Production Version
# ==========================================================

import html
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset
from utils.theme_coder import build_theme_dataset

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Open Ended Insights",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS FOR QUOTATION CARDS
# ==========================================================

st.markdown(
    """
    <style>
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

    .framework-note {
        background-color: rgba(217, 119, 6, 0.10);
        border-left: 5px solid #D97706;
        padding: 14px 18px;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 15px;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True
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

st.markdown(
    "## Operational Theme Frequency Analysis"
)

theme_freq = (
    theme_df["Theme"]
    .value_counts()
    .reset_index()
)

theme_freq.columns = [
    "Theme",
    "Count"
]

theme_freq["Percentage"] = (
    theme_freq["Count"]
    /
    theme_freq["Count"].sum()
    *
    100
).round(1)

theme_freq = (
    theme_freq
    .sort_values(
        "Count",
        ascending=False
    )
    .reset_index(drop=True)
)

chart_theme_freq = theme_freq.sort_values(
    "Count",
    ascending=True
)

fig_theme = px.bar(
    chart_theme_freq,
    x="Count",
    y="Theme",
    orientation="h",
    text="Percentage",
    title="Most Frequently Mentioned Operational Themes"
)

fig_theme.update_layout(
    yaxis_title="Operational Theme",
    xaxis_title="Number of Mentions",
    height=650
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
    "## Theme Distribution by Agency"
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

    fig_heatmap = px.imshow(
        cross_df,
        aspect="auto",
        title="Operational Theme Frequency by Agency",
        labels=dict(
            x="Operational Theme",
            y="Agency",
            color="Mentions"
        )
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
# THEME SUMMARY
# ==========================================================

st.markdown(
    "## Theme Summary"
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
    "## Representative Quotations"
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
# THEME OCCURRENCE SUMMARY
# ==========================================================

st.markdown(
    "## Theme Occurrence Summary"
)

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

st.info(
    f"""
### Executive Interpretation

A total of **{total_open_responses} open-ended responses**
were analysed from Q27 and Q28.

The thematic coding process identified **{total_themes} operational themes**
and generated **{coded_records} coded theme mentions**.

A theme mention represents one occurrence of a theme within a response.
Individual responses may contribute to multiple themes.

The most frequently mentioned operational theme was:

**{top_theme}**

representing approximately **{top_percentage}%** of all coded theme
references.

The qualitative responses highlight stakeholder priorities relating to
institutional strengthening, data quality, forecasting capability, digital
transformation and evidence-based road asset management.

These findings provide valuable context to the quantitative maturity indices
and help explain the practical needs identified by respondents across
participating agencies.
"""
)
