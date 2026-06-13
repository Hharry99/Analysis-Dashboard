# ==========================================================
# OPEN ENDED INSIGHTS
# Sprint 3C.3 - Polished Production Version
# ==========================================================

import html
import streamlit as st
import textwrap
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


def apply_readable_horizontal_bar_layout(fig, row_count, height_min=560):

    chart_height = max(
        height_min,
        min(
            980,
            220 + row_count * 50
        )
    )

    fig.update_layout(
        height=chart_height,
        showlegend=False,
        margin=dict(
            l=70,
            r=120,
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


def apply_readable_heatmap_layout(fig, height=650):

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


def apply_readable_donut_layout(fig, height=600):

    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        insidetextorientation="radial",
        hovertemplate=(
            "Theme: %{customdata[0]}<br>"
            "Mentions: %{customdata[1]}<br>"
            "Share: %{percent}<extra></extra>"
        )
    )

    fig.update_layout(
        height=height,
        showlegend=True,
        margin=dict(
            l=20,
            r=20,
            t=80,
            b=110
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.50,
            font=dict(
                size=11
            )
        ),
        uniformtext_minsize=10,
        uniformtext_mode="show"
    )

    return fig


def make_display_table(df_in, text_col="Theme", max_length=78):

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


def build_theme_key(themes):

    key_rows = []

    for idx, theme in enumerate(
        themes,
        start=1
    ):

        key_rows.append({
            "Code": f"T{idx}",
            "Full Operational Theme": theme
        })

    return pd.DataFrame(
        key_rows
    )

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

theme_key_df = build_theme_key(
    theme_freq["Theme"].tolist()
)

theme_code_map = dict(
    zip(
        theme_key_df["Full Operational Theme"],
        theme_key_df["Code"]
    )
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

chart_theme_freq = (
    theme_freq
    .sort_values(
        "Count",
        ascending=True
    )
    .copy()
)

chart_theme_freq["Display Theme"] = chart_theme_freq["Theme"].apply(
    lambda x: shorten_label(
        x,
        max_length=44
    )
)

max_theme_count = chart_theme_freq["Count"].max()

fig_theme = px.bar(
    chart_theme_freq,
    x="Count",
    y="Display Theme",
    orientation="h",
    text="Percentage",
    color="Display Theme",
    custom_data=[
        "Theme",
        "Count"
    ],
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title="Most Frequently Mentioned Operational Themes"
)

fig_theme.update_layout(
    yaxis_title="Operational Theme",
    xaxis_title="Number of Mentions",
    xaxis=dict(
        range=[
            0,
            max(
                5,
                max_theme_count * 1.18
            )
        ]
    )
)

fig_theme.update_traces(
    texttemplate="%{text:.1f}%",
    hovertemplate=(
        "Theme: %{customdata[0]}<br>"
        "Mentions: %{customdata[1]}<br>"
        "Share: %{text:.1f}%<extra></extra>"
    )
)

fig_theme = apply_readable_horizontal_bar_layout(
    fig_theme,
    row_count=len(chart_theme_freq),
    height_min=620
)

st.plotly_chart(
    fig_theme,
    use_container_width=True
)

st.caption(
    "Takeaway: Digital Transformation & Technology is the most frequently mentioned operational theme, followed by asset management and capacity building themes."
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

    cross_df = cross_df.rename(
        columns=theme_code_map
    )

    fig_heatmap = px.imshow(
        cross_df,
        aspect="auto",
        title="Operational Theme Frequency by Agency",
        labels=dict(
            x="Operational theme code",
            y="Agency",
            color="Mentions"
        ),
        color_continuous_scale=HEATMAP_SCALE,
        text_auto=True
    )

    fig_heatmap.update_xaxes(
        tickangle=0
    )

    fig_heatmap = apply_readable_heatmap_layout(
        fig_heatmap,
        height=520
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

    st.caption(
        "Takeaway: The heatmap uses theme codes to avoid congested labels. The full operational theme names are shown in the key below."
    )

    st.markdown(
        "#### Operational Theme Code Key"
    )

    render_compact_table(
        theme_key_df,
        numeric_columns=[],
        max_rows=None
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

theme_share_df = theme_freq.copy()

theme_share_df["Display Theme"] = theme_share_df["Theme"].map(
    theme_code_map
)

fig_theme_share = px.pie(
    theme_share_df,
    names="Display Theme",
    values="Percentage",
    hole=0.55,
    title="Share of Operational Theme Mentions",
    custom_data=[
        "Theme",
        "Count"
    ],
    color_discrete_sequence=PIE_COLOR_SEQUENCE
)

fig_theme_share = apply_readable_donut_layout(
    fig_theme_share,
    height=620
)

st.plotly_chart(
    fig_theme_share,
    use_container_width=True
)

st.caption(
    "Takeaway: The donut chart uses the same theme codes shown in the Operational Theme Code Key above. The bar chart remains the clearest view for exact ranking."
)

# ==========================================================
# THEME SUMMARY
# ==========================================================

st.markdown(
    "<div class='section-title'>Theme Summary</div>",
    unsafe_allow_html=True
)

theme_summary_display_df = theme_freq[
    [
        "Theme",
        "Count",
        "Percentage"
    ]
].copy()

theme_summary_display_df = make_display_table(
    theme_summary_display_df,
    text_col="Theme",
    max_length=78
)

theme_summary_display_df.insert(
    0,
    "No.",
    range(
        1,
        len(theme_summary_display_df) + 1
    )
)

render_compact_table(
    theme_summary_display_df,
    numeric_columns=[
        "No.",
        "Count",
        "Percentage"
    ],
    max_rows=None
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

    theme_agency_display_df = make_display_table(
        theme_agency,
        text_col="Theme",
        max_length=85
    )

    theme_agency_display_df.insert(
        0,
        "No.",
        range(
            1,
            len(theme_agency_display_df) + 1
        )
    )

    render_compact_table(
        theme_agency_display_df,
        numeric_columns=[
            "No.",
            "Count"
        ],
        max_rows=None
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

# ==========================================================
# NEXT PAGE HINT
# ==========================================================

st.divider()

try:

    st.page_link(
        "pages/11_Benchmarking_and_Gap_Analysis.py",
        label="Next suggested page: Benchmarking and Gap Analysis",
        icon="➡️"
    )

except Exception:

    st.caption(
        "Next suggested page: Benchmarking and Gap Analysis →"
    )

