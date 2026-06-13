# ==========================================================
# RECONSTRUCTION READINESS ANALYSIS
# Sprint 3A - Page 4
# Polished Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

from utils.dashboard_style import apply_dashboard_style

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Reconstruction Readiness Analysis",
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
    border-left:6px solid #059669;
    background:rgba(5,150,105,0.08);
    padding:18px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

.warning-note{
    border-left:6px solid #F59E0B;
    background:rgba(245,158,11,0.10);
    padding:16px;
    border-radius:10px;
    margin-top:12px;
    margin-bottom:18px;
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
# SIDEBAR NAVIGATION GUIDE
# ==========================================================

st.sidebar.markdown(
    """
    <div style="font-size:13px; line-height:1.45; margin-bottom:12px;">
    <b>Dashboard Navigation Groups</b><br>
    <b>Executive Overview</b><br>
    • Executive Dashboard<br>
    • Respondent Profile<br><br>
    <b>Maturity Analysis</b><br>
    • Data Maturity<br>
    • Forecasting Maturity<br>
    • Reconstruction Readiness<br>
    • Digital Readiness<br><br>
    <b>Question Analytics</b><br>
    • Data Practices Questions<br>
    • Forecasting Questions<br>
    • Reconstruction & Modelling Questions<br>
    • Digital Readiness Questions<br><br>
    <b>Strategic Insights</b><br>
    • Open Ended Insights<br>
    • Benchmarking & Gap Analysis<br>
    • Strategic Roadmap<br>
    • Key Findings & Recommendations
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    master = pd.read_csv(
        "data/clean_master.csv"
    )

    indices = pd.read_csv(
        "data/indices_dataset.csv"
    )

    return master, indices


master_df, indices_df = load_data()

master_df = clean_master_dataset(
    master_df
)

# ==========================================================
# COLUMN DEFINITIONS
# ==========================================================

AGENCY_COL = "Q1. What agency do you work for?"
INDEX_COL = "RRI"

REQUIRED_MASTER_COLS = [
    AGENCY_COL
]

REQUIRED_INDEX_COLS = [
    INDEX_COL
]

# ==========================================================
# VALIDATION
# ==========================================================

missing_master_cols = [
    col for col in REQUIRED_MASTER_COLS
    if col not in master_df.columns
]

missing_index_cols = [
    col for col in REQUIRED_INDEX_COLS
    if col not in indices_df.columns
]

if missing_master_cols:

    st.error(
        f"Missing required master dataset columns: {missing_master_cols}"
    )

    st.stop()

if missing_index_cols:

    st.error(
        f"Missing required indices dataset columns: {missing_index_cols}"
    )

    st.stop()

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def classify_maturity(score):

    if pd.isna(score):
        return "Not Available"

    if score < 40:
        return "Emerging"

    if score < 60:
        return "Developing"

    if score < 80:
        return "Advanced"

    return "Leading"


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


def apply_readable_histogram_layout(fig, height=540):

    fig.update_layout(
        height=height,
        bargap=0.10,
        margin=dict(
            l=60,
            r=40,
            t=80,
            b=120
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.50
        ),
        legend_title_text="Maturity Band",
        xaxis=dict(
            automargin=True,
            title_standoff=20
        ),
        yaxis=dict(
            automargin=True,
            title_standoff=20
        )
    )

    return fig


def apply_readable_vertical_bar_layout(fig, height=540):

    fig.update_layout(
        height=height,
        showlegend=False,
        margin=dict(
            l=60,
            r=70,
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
        texttemplate="%{text:.1f}",
        textposition="outside",
        cliponaxis=False
    )

    return fig


def apply_readable_heatmap_layout(fig, height=360):

    fig.update_layout(
        height=height,
        margin=dict(
            l=60,
            r=40,
            t=80,
            b=80
        ),
        xaxis=dict(
            automargin=True,
            title_standoff=20
        ),
        yaxis=dict(
            automargin=True,
            title_standoff=20
        ),
        coloraxis_showscale=False
    )

    return fig

# ==========================================================
# PREPARE DATA
# ==========================================================

master_df = master_df.reset_index(
    drop=True
)

indices_df = indices_df.reset_index(
    drop=True
)

analysis_df = pd.concat(
    [
        master_df[
            [
                AGENCY_COL
            ]
        ],
        indices_df[
            [
                INDEX_COL
            ]
        ]
    ],
    axis=1
)

analysis_df[INDEX_COL] = pd.to_numeric(
    analysis_df[INDEX_COL],
    errors="coerce"
)

analysis_df = analysis_df.dropna(
    subset=[
        AGENCY_COL,
        INDEX_COL
    ]
)

if analysis_df.empty:

    st.warning(
        "No valid RRI records were found after cleaning."
    )

    st.stop()

analysis_df["Maturity Band"] = analysis_df[INDEX_COL].apply(
    classify_maturity
)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Reconstruction Readiness Analysis"
)

st.markdown("""
This section evaluates agency readiness for pavement rehabilitation,
reconstruction planning, prioritization and implementation.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_rri = round(
    analysis_df[INDEX_COL].mean(),
    1
)

highest_rri = round(
    analysis_df[INDEX_COL].max(),
    1
)

lowest_rri = round(
    analysis_df[INDEX_COL].min(),
    1
)

agencies = analysis_df[
    AGENCY_COL
].nunique()

overall_band = classify_maturity(
    avg_rri
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average RRI",
    avg_rri
)

c2.metric(
    "Highest RRI",
    highest_rri
)

c3.metric(
    "Lowest RRI",
    lowest_rri
)

c4.metric(
    "Agencies",
    agencies
)

# ==========================================================
# AGENCY LEVEL SUMMARY
# ==========================================================

agency_rri = (
    analysis_df
    .groupby(
        AGENCY_COL
    )[INDEX_COL]
    .mean()
    .reset_index()
)

agency_rri[INDEX_COL] = (
    agency_rri[INDEX_COL]
    .round(1)
)

agency_rri["Maturity Band"] = agency_rri[INDEX_COL].apply(
    classify_maturity
)

agency_rri = agency_rri.sort_values(
    INDEX_COL,
    ascending=False
)

top_agency = (
    agency_rri.iloc[0][AGENCY_COL]
    if not agency_rri.empty
    else "Not Available"
)

top_agency_score = (
    agency_rri.iloc[0][INDEX_COL]
    if not agency_rri.empty
    else 0
)

lowest_agency = (
    agency_rri.iloc[-1][AGENCY_COL]
    if not agency_rri.empty
    else "Not Available"
)

lowest_agency_score = (
    agency_rri.iloc[-1][INDEX_COL]
    if not agency_rri.empty
    else 0
)

# ==========================================================
# EXECUTIVE SNAPSHOT
# ==========================================================

st.markdown(
    f"""
<div class="insight-box">

<b>Reconstruction Readiness Snapshot:</b><br>
The average Reconstruction Readiness Index is <b>{avg_rri}</b>, placing the
overall reconstruction readiness position in the <b>{overall_band}</b> maturity band.

<br><br>
The highest average agency RRI is recorded by <b>{top_agency}</b>
(<b>{top_agency_score}</b>), while the lowest average agency RRI is recorded by
<b>{lowest_agency}</b> (<b>{lowest_agency_score}</b>).

<br><br>
This suggests that reconstruction planning and rehabilitation readiness are
relatively stronger than other maturity dimensions, but agency-level differences
still point to opportunities for improved prioritization, lifecycle planning and
investment programming.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# RRI DATA CHECK
# ==========================================================

if analysis_df[INDEX_COL].nunique() <= 1:

    st.markdown(
        """
<div class="warning-note">

<b>Data Quality Note:</b>
RRI contains only one unique value. This may suggest that the index was
reconstructed as a constant rather than calculated per respondent. Review
indices_dataset.csv during the final dataset refresh.

</div>
""",
        unsafe_allow_html=True
    )

# ==========================================================
# RRI DISTRIBUTION
# ==========================================================

st.markdown(
    "<div class='section-title'>RRI Distribution</div>",
    unsafe_allow_html=True
)

fig_hist = px.histogram(
    analysis_df,
    x=INDEX_COL,
    color="Maturity Band",
    nbins=10,
    title="Distribution of Reconstruction Readiness Scores",
    color_discrete_sequence=COLOR_SEQUENCE
)

fig_hist.update_layout(
    xaxis_title="Reconstruction Readiness Index",
    yaxis_title="Number of Responses"
)

fig_hist = apply_readable_histogram_layout(
    fig_hist,
    height=540
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

st.caption(
    "Takeaway: The distribution shows that reconstruction readiness is comparatively stronger, with many responses falling in the advanced maturity range."
)

# ==========================================================
# RRI BY AGENCY
# ==========================================================

st.markdown(
    "<div class='section-title'>RRI by Agency</div>",
    unsafe_allow_html=True
)

fig_agency = px.bar(
    agency_rri,
    x=AGENCY_COL,
    y=INDEX_COL,
    text=INDEX_COL,
    color=AGENCY_COL,
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title="Average Reconstruction Readiness Index by Agency"
)

fig_agency.update_layout(
    xaxis_title="Agency",
    yaxis_title="Average RRI",
    yaxis=dict(
        range=[
            0,
            100
        ],
        automargin=True,
        title_standoff=20
    ),
    xaxis=dict(
        automargin=True,
        title_standoff=20
    )
)

fig_agency = apply_readable_vertical_bar_layout(
    fig_agency,
    height=540
)

st.plotly_chart(
    fig_agency,
    use_container_width=True
)

st.caption(
    "Takeaway: KURA records the highest average RRI, while KeNHA records the lowest average RRI among the participating agencies."
)

# ==========================================================
# AGENCY RANKING
# ==========================================================

st.markdown(
    "<div class='section-title'>Agency Ranking</div>",
    unsafe_allow_html=True
)

ranking_df = agency_rri.copy()

ranking_df["Rank"] = range(
    1,
    len(ranking_df) + 1
)

ranking_df = ranking_df[
    [
        "Rank",
        AGENCY_COL,
        INDEX_COL,
        "Maturity Band"
    ]
]

ranking_df = ranking_df.rename(
    columns={
        AGENCY_COL: "Agency",
        INDEX_COL: "RRI"
    }
)

st.table(
    ranking_df
)

# ==========================================================
# RRI HEATMAP
# ==========================================================

st.markdown(
    "<div class='section-title'>RRI Heatmap</div>",
    unsafe_allow_html=True
)

heatmap_df = agency_rri.copy()

fig_heatmap = px.imshow(
    heatmap_df[
        [
            INDEX_COL
        ]
    ].T,
    labels=dict(
        x="Agency",
        y="Index",
        color="RRI"
    ),
    x=heatmap_df[
        AGENCY_COL
    ],
    y=[
        "RRI"
    ],
    aspect="auto",
    title="Reconstruction Readiness Heatmap by Agency",
    color_continuous_scale=HEATMAP_SCALE,
    zmin=0,
    zmax=100,
    text_auto=".1f"
)

fig_heatmap = apply_readable_heatmap_layout(
    fig_heatmap,
    height=360
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

st.caption(
    "Takeaway: The heatmap provides a compact scorecard view of agency-level RRI performance."
)

# ==========================================================
# RRI SUMMARY TABLES
# ==========================================================

with st.expander(
    "View Detailed RRI Summary Tables",
    expanded=False
):

    st.markdown(
        "### Agency RRI Summary"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.markdown(
        "### Maturity Band Distribution"
    )

    band_summary = (
        analysis_df["Maturity Band"]
        .value_counts()
        .reset_index()
    )

    band_summary.columns = [
        "Maturity Band",
        "Responses"
    ]

    band_summary = add_percentage(
        band_summary,
        "Responses"
    )

    st.dataframe(
        band_summary,
        use_container_width=True
    )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Interpretation

The average Reconstruction Readiness Index (RRI) was **{avg_rri}**, which
indicates an overall **{overall_band}** level of reconstruction readiness
across participating agencies.

This reflects the extent to which agencies are prepared for pavement
rehabilitation, reconstruction planning, treatment selection, prioritization
and implementation decision-making.

The relatively strong readiness score suggests that reconstruction planning
practices are more mature than data maturity and forecasting capability.

However, agency-level differences indicate opportunities for improved
prioritization, lifecycle planning, investment programming and evidence-based
reconstruction decision-making.
""")

# ==========================================================
# NEXT PAGE HINT
# ==========================================================

st.divider()

try:

    st.page_link(
        "pages/05_Digital_Readiness.py",
        label="Next suggested page: Digital Readiness",
        icon="➡️"
    )

except Exception:

    st.caption(
        "Next suggested page: Digital Readiness →"
    )

