# ==========================================================
# OPEN ENDED INSIGHTS
# Sprint 3C.3 - Final Production Version (V2)
# ==========================================================

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
    page_icon="💡",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/clean_master.csv")

master_df = load_data()
master_df = clean_master_dataset(master_df)

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

ORG_COL = "Q1. What agency do you work for?"

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

TEXT_COLUMNS = [Q27_COL, Q28_COL]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("💡 Open Ended Insights")

st.markdown(
    """
This page presents qualitative insights extracted from open-ended survey
responses.

Responses were automatically coded into themes covering institutional
capacity, data quality, forecasting, digital transformation and asset
management practices.
"""
)

# ==========================================================
# FILTERS
# ==========================================================

agencies = sorted(master_df[ORG_COL].dropna().unique())

selected_agencies = st.multiselect(
    "Filter Organization",
    agencies,
    default=agencies
)

analysis_df = master_df[
    master_df[ORG_COL].isin(selected_agencies)
]

# ==========================================================
# BUILD THEME DATASET
# ==========================================================

theme_df = build_theme_dataset(
    df=analysis_df,
    text_columns=TEXT_COLUMNS,
    agency_column=ORG_COL
)

# ==========================================================
# VALIDATION
# ==========================================================

if theme_df.empty:
    st.warning("No themes were identified from the selected responses.")
    st.stop()

# ==========================================================
# KPI SECTION
# ==========================================================

total_q27 = analysis_df[Q27_COL].dropna().shape[0]
total_q28 = analysis_df[Q28_COL].dropna().shape[0]
total_themes = theme_df["Theme"].nunique()
coded_records = len(theme_df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Q27 Responses", total_q27)
c2.metric("Q28 Responses", total_q28)
c3.metric("Themes Identified", total_themes)
c4.metric("Theme Mentions", coded_records)

# ==========================================================
# THEME FREQUENCY ANALYSIS
# ==========================================================

st.markdown("## Theme Frequency Analysis")

theme_freq = (
    theme_df["Theme"]
    .value_counts()
    .reset_index()
)

theme_freq.columns = ["Theme", "Count"]

theme_freq["Percentage"] = (
    theme_freq["Count"] / theme_freq["Count"].sum() * 100
).round(1)

fig_theme = px.bar(
    theme_freq,
    x="Count",
    y="Theme",
    orientation="h",
    text="Percentage",
    title="Most Frequently Mentioned Themes"
)

fig_theme.update_layout(
    yaxis_title="Theme",
    xaxis_title="Number of Mentions"
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
# THEME DISTRIBUTION BY ORGANIZATION
# ==========================================================

st.markdown("## Theme Distribution by Organization")

try:

    cross_df = (
        theme_df
        .groupby(["Agency", "Theme"])
        .size()
        .unstack(fill_value=0)
    )

    fig_heatmap = px.imshow(
        cross_df,
        aspect="auto",
        title="Theme Frequency by Organization"
    )

    fig_heatmap.update_layout(height=700)

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

st.markdown("## Theme Summary")

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

st.markdown("## Representative Quotations")

selected_theme = st.selectbox(
    "Select Theme",
    sorted(theme_df["Theme"].unique())
)

theme_quotes = (
    theme_df[theme_df["Theme"] == selected_theme]
    .drop_duplicates(subset=["Response"])
)

max_quotes = min(5, len(theme_quotes))

st.markdown("### Selected Quotations")

for i, (_, row) in enumerate(
    theme_quotes.head(max_quotes).iterrows(),
    start=1
):

    quote = (
        str(row["Response"])
        .replace("\n", " ")
        .strip()
    )

    st.info(
        f"Quote {i}\n\n{quote}"
    )

# ==========================================================
# THEME OCCURRENCE SUMMARY
# ==========================================================

st.markdown("## Theme Occurrence Summary")

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

st.dataframe(
    theme_agency,
    use_container_width=True
)

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

top_theme = theme_freq.iloc[0]["Theme"]
top_percentage = theme_freq.iloc[0]["Percentage"]

st.info(
    f"""
### Executive Interpretation

A total of **{total_q27 + total_q28}**
open-ended responses were analysed.

The thematic coding process identified
**{total_themes} major themes** and generated
**{coded_records} coded theme mentions**.

A theme mention represents one occurrence
of a theme within a response. Individual
responses may contribute to multiple themes.

The most frequently mentioned theme was:

**{top_theme}**

representing approximately
**{top_percentage}%** of all coded theme
references.

The qualitative responses highlight
stakeholder priorities relating to
institutional strengthening, data quality,
forecasting capability, digital transformation
and evidence-based road asset management.

These findings provide valuable context to
the quantitative maturity indices and help
explain the practical needs identified by
respondents.
"""
)
