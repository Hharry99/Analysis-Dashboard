# ==========================================================
# DIGITAL READINESS ANALYSIS
# Sprint 3A - Page 5
# Polished Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_cleaning import clean_master_dataset

from utils.dashboard_style import apply_dashboard_style
from utils.dashboard_navigation import apply_sidebar_navigation

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Digital Readiness Analysis",
    page_icon="◌",
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

/* Digital Readiness fallback override for grouped navigation visibility */
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
    "Digital Readiness Analysis"
)
apply_sidebar_visibility_override()

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
INDEX_COL = "DRI"

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
        "No valid DRI records were found after cleaning."
    )

    st.stop()

analysis_df["Maturity Band"] = analysis_df[INDEX_COL].apply(
    classify_maturity
)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Digital Readiness Analysis"
)

st.markdown("""
This section evaluates the adoption of digital technologies, electronic
databases, analytics platforms, decision-support systems and digital
transformation capabilities across participating agencies.
""")

# ==========================================================
# KPI SECTION
# ==========================================================

avg_dri = round(
    analysis_df[INDEX_COL].mean(),
    1
)

highest_dri = round(
    analysis_df[INDEX_COL].max(),
    1
)

lowest_dri = round(
    analysis_df[INDEX_COL].min(),
    1
)

agencies = analysis_df[
    AGENCY_COL
].nunique()

overall_band = classify_maturity(
    avg_dri
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average DRI",
    avg_dri
)

c2.metric(
    "Highest DRI",
    highest_dri
)

c3.metric(
    "Lowest DRI",
    lowest_dri
)

c4.metric(
    "Agencies",
    agencies
)

# ==========================================================
# AGENCY LEVEL SUMMARY
# ==========================================================

agency_dri = (
    analysis_df
    .groupby(
        AGENCY_COL
    )[INDEX_COL]
    .mean()
    .reset_index()
)

agency_dri[INDEX_COL] = (
    agency_dri[INDEX_COL]
    .round(1)
)

agency_dri["Maturity Band"] = agency_dri[INDEX_COL].apply(
    classify_maturity
)

agency_dri = agency_dri.sort_values(
    INDEX_COL,
    ascending=False
)

top_agency = (
    agency_dri.iloc[0][AGENCY_COL]
    if not agency_dri.empty
    else "Not Available"
)

top_agency_score = (
    agency_dri.iloc[0][INDEX_COL]
    if not agency_dri.empty
    else 0
)

lowest_agency = (
    agency_dri.iloc[-1][AGENCY_COL]
    if not agency_dri.empty
    else "Not Available"
)

lowest_agency_score = (
    agency_dri.iloc[-1][INDEX_COL]
    if not agency_dri.empty
    else 0
)

# ==========================================================
# EXECUTIVE SNAPSHOT
# ==========================================================

st.markdown(
    f"""
<div class="insight-box">

<b>Digital Readiness Snapshot:</b><br>
The average Digital Readiness Index is <b>{avg_dri}</b>, placing the overall
digital readiness position in the <b>{overall_band}</b> maturity band.

<br><br>
The highest average agency DRI is recorded by <b>{top_agency}</b>
(<b>{top_agency_score}</b>), while the lowest average agency DRI is recorded by
<b>{lowest_agency}</b> (<b>{lowest_agency_score}</b>).

<br><br>
This indicates moderate progress towards digital transformation, while also
showing opportunities to strengthen digital systems, analytics platforms,
decision-support tools, cybersecurity and technology-enabled asset management.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# DRI DISTRIBUTION
# ==========================================================

st.markdown(
    "<div class='section-title'>DRI Distribution</div>",
    unsafe_allow_html=True
)

fig_hist = px.histogram(
    analysis_df,
    x=INDEX_COL,
    color="Maturity Band",
    nbins=10,
    title="Distribution of Digital Readiness Scores",
    color_discrete_sequence=COLOR_SEQUENCE
)

fig_hist.update_layout(
    xaxis_title="Digital Readiness Index",
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
    "Takeaway: The distribution shows that digital readiness is mainly developing, with room to strengthen digital systems and decision-support capability."
)

# ==========================================================
# DRI BY AGENCY
# ==========================================================

st.markdown(
    "<div class='section-title'>DRI by Agency</div>",
    unsafe_allow_html=True
)

fig_agency = px.bar(
    agency_dri,
    x=AGENCY_COL,
    y=INDEX_COL,
    text=INDEX_COL,
    color=AGENCY_COL,
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title="Average Digital Readiness Index by Agency"
)

fig_agency.update_layout(
    xaxis_title="Agency",
    yaxis_title="Average DRI",
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
    "Takeaway: MTRD records the highest average DRI, while KURA records the lowest average DRI among the participating agencies."
)

# ==========================================================
# AGENCY RANKING
# ==========================================================

st.markdown(
    "<div class='section-title'>Agency Ranking</div>",
    unsafe_allow_html=True
)

ranking_df = agency_dri.copy()

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
        INDEX_COL: "DRI"
    }
)

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True,
    height=min(
        300,
        36 * len(ranking_df) + 40
    )
)

# ==========================================================
# DRI HEATMAP
# ==========================================================

st.markdown(
    "<div class='section-title'>DRI Heatmap</div>",
    unsafe_allow_html=True
)

heatmap_df = agency_dri.copy()

fig_heatmap = px.imshow(
    heatmap_df[
        [
            INDEX_COL
        ]
    ].T,
    labels=dict(
        x="Agency",
        y="Index",
        color="DRI"
    ),
    x=heatmap_df[
        AGENCY_COL
    ],
    y=[
        "DRI"
    ],
    aspect="auto",
    title="Digital Readiness Heatmap by Agency",
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
    "Takeaway: The heatmap provides a compact scorecard view of agency-level DRI performance."
)

# ==========================================================
# DRI SUMMARY TABLES
# ==========================================================

with st.expander(
    "View Detailed DRI Summary Tables",
    expanded=False
):

    st.markdown(
        "### Agency DRI Summary"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
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
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Interpretation

The average Digital Readiness Index (DRI) was **{avg_dri}**, which indicates
an overall **{overall_band}** level of digital readiness across participating
agencies.

This reflects the extent to which agencies have adopted digital technologies,
electronic databases, decision-support tools, analytics platforms and digital
workflows.

The results indicate moderate progress towards digital transformation, but
also show a need to strengthen integrated asset management systems, analytics
capability, system interoperability, cybersecurity and digital decision-support
platforms.

Agencies with higher DRI scores are better positioned to leverage data-driven
pavement management, predictive maintenance practices and integrated asset
management systems.

Agency-level variation highlights opportunities for digital modernization,
technology adoption, capacity development and improved use of digital tools
for infrastructure planning and decision-making.
""")

# ==========================================================
# NEXT PAGE HINT
# ==========================================================

st.divider()

try:

    st.page_link(
        "pages/06_Data_Practices_Questions.py",
        label="Next suggested page: Data Practices Questions",
        icon="➡️"
    )

except Exception:

    st.caption(
        "Next suggested page: Data Practices Questions →"
    )

