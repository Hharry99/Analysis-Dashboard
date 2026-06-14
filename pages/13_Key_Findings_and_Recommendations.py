# ==========================================================
# KEY FINDINGS AND RECOMMENDATIONS
# Sprint 3D.2 - Polished Production Version
# ==========================================================

import html
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.dashboard_style import apply_dashboard_style
from utils.dashboard_navigation import apply_sidebar_navigation

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Key Findings & Recommendations",
    page_icon="★",
    layout="wide"
)

# ==========================================================
# VISUAL STYLE SETTINGS
# ==========================================================

BAR_COLOR_SEQUENCE = px.colors.qualitative.Bold
ALT_COLOR_SEQUENCE = px.colors.qualitative.Set2

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

.note-box{
    border-left:5px solid #2563EB;
    background:rgba(37,99,235,0.08);
    padding:15px;
    border-radius:10px;
    margin-top:10px;
    margin-bottom:20px;
}

.insight-box{
    border-left:6px solid #D97706;
    background:rgba(217,119,6,0.08);
    padding:18px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

.finding-card{
    border-left:5px solid #7C3AED;
    background:rgba(124,58,237,0.08);
    padding:16px 18px;
    border-radius:10px;
    margin-bottom:14px;
    line-height:1.5;
}

.recommendation-card{
    border-left:5px solid #059669;
    background:rgba(5,150,105,0.08);
    padding:16px 18px;
    border-radius:10px;
    margin-bottom:14px;
    line-height:1.5;
}

.risk-note{
    border-left:5px solid #DC2626;
    background:rgba(220,38,38,0.08);
    padding:16px 18px;
    border-radius:10px;
    margin-top:12px;
    margin-bottom:18px;
}

.benefit-box{
    border-left:5px solid #2563EB;
    background:rgba(37,99,235,0.08);
    padding:16px 18px;
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


def apply_sidebar_visibility_override():

    st.markdown(
        """
<style>

/* Key Findings & Recommendations fallback override for grouped navigation visibility */
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
    "Key Findings & Recommendations"
)
apply_sidebar_visibility_override()

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_benchmark_data():
    return pd.read_csv(
        "data/benchmark_dataset.csv"
    )


benchmark_df = load_benchmark_data()

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

INDEX_COLS = [
    "DMI",
    "FMI",
    "RRI",
    "DRI"
]

INDEX_LABELS = {
    "DMI": "Data Maturity",
    "FMI": "Forecasting Maturity",
    "RRI": "Reconstruction Readiness",
    "DRI": "Digital Readiness"
}

required_cols = [
    "Agency",
    "Overall_Score",
    "DMI",
    "FMI",
    "RRI",
    "DRI"
]

missing_cols = [
    col for col in required_cols
    if col not in benchmark_df.columns
]

if missing_cols:

    st.error(
        f"Missing required columns: {missing_cols}"
    )

    st.stop()

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def classify_score(score):

    if pd.isna(score):
        return "Not Available"

    if score < 40:
        return "Emerging"

    if score < 60:
        return "Developing"

    if score < 80:
        return "Advanced"

    return "Leading"


def round_columns(df, cols, decimals=1):

    df = df.copy()

    for col in cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).round(decimals)

    return df


def render_finding_card(number, title, evidence):

    safe_title = html.escape(str(title))
    safe_evidence = html.escape(str(evidence))

    st.markdown(
        f"""
<div class="finding-card">
<b>Finding {number}: {safe_title}</b><br>
{safe_evidence}
</div>
""",
        unsafe_allow_html=True
    )


def render_recommendation_card(number, title, rationale):

    safe_title = html.escape(str(title))
    safe_rationale = html.escape(str(rationale))

    st.markdown(
        f"""
<div class="recommendation-card">
<b>Recommendation {number}: {safe_title}</b><br>
{safe_rationale}
</div>
""",
        unsafe_allow_html=True
    )


def apply_readable_horizontal_bar_layout(fig, height=500):

    fig.update_layout(
        height=height,
        showlegend=False,
        margin=dict(
            l=70,
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
        textposition="outside",
        cliponaxis=False
    )

    return fig


def format_score_dataframe(df_in):

    df_out = df_in.copy()

    score_cols = [
        "Average Score",
        "Overall Score",
        "DMI",
        "FMI",
        "RRI",
        "DRI"
    ]

    for col in score_cols:

        if col in df_out.columns:

            df_out[col] = pd.to_numeric(
                df_out[col],
                errors="coerce"
            ).round(1)

    return df_out

# ==========================================================
# CLEAN AND STANDARDIZE BENCHMARK DATA
# ==========================================================

benchmark_df = benchmark_df.copy()

numeric_cols = [
    "Overall_Score",
    "DMI",
    "FMI",
    "RRI",
    "DRI"
]

for col in numeric_cols:

    benchmark_df[col] = pd.to_numeric(
        benchmark_df[col],
        errors="coerce"
    )

benchmark_df = benchmark_df.dropna(
    subset=[
        "Agency",
        "Overall_Score"
    ]
)

if benchmark_df.empty:

    st.warning(
        "No valid benchmark records were found."
    )

    st.stop()

# ----------------------------------------------------------
# Display-level de-duplication only.
# This ensures the page uses one benchmark row per agency.
# The final benchmark dataset will still be regenerated after
# survey closure and final validation.
# ----------------------------------------------------------

benchmark_df = (
    benchmark_df
    .sort_values(
        "Overall_Score",
        ascending=False
    )
    .drop_duplicates(
        subset=[
            "Agency"
        ],
        keep="first"
    )
    .reset_index(drop=True)
)

benchmark_df["Display_Rank"] = (
    benchmark_df.index + 1
)

benchmark_df["Maturity Stage"] = benchmark_df["Overall_Score"].apply(
    classify_score
)

benchmark_df = round_columns(
    benchmark_df,
    numeric_cols,
    decimals=1
)

agency_count = benchmark_df["Agency"].nunique()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Key Findings & Recommendations"
)

st.markdown("""
This page consolidates the major findings from the maturity assessment,
question-level analytics, thematic insights, benchmarking results and strategic
roadmap.

It is designed as an executive summary for decision-makers.
""")

st.markdown(
    """
<div class="note-box">
<b>Findings Note:</b>
Current findings use the available benchmark dataset. Final findings, rankings
and recommendations will be refreshed after survey closure and final dataset
validation.
</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# EXECUTIVE KPI SUMMARY
# ==========================================================

st.markdown(
    "<div class='section-title'>Executive Summary KPIs</div>",
    unsafe_allow_html=True
)

avg_score = round(
    benchmark_df[
        "Overall_Score"
    ].mean(),
    1
)

highest_score = round(
    benchmark_df[
        "Overall_Score"
    ].max(),
    1
)

lowest_score = round(
    benchmark_df[
        "Overall_Score"
    ].min(),
    1
)

top_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmax(),
    "Agency"
]

lowest_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmin(),
    "Agency"
]

overall_stage = classify_score(
    avg_score
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Agencies Assessed",
    agency_count
)

c2.metric(
    "Average Overall Score",
    avg_score
)

c3.metric(
    "Highest Score",
    highest_score
)

c4.metric(
    "Lowest Score",
    lowest_score
)

# ==========================================================
# EXECUTIVE SNAPSHOT
# ==========================================================

score_range = round(
    highest_score
    -
    lowest_score,
    1
)

st.markdown(
    f"""
<div class="insight-box">

<b>Executive Findings Snapshot:</b><br>
A total of <b>{agency_count}</b> agencies were assessed. The current sector
average overall maturity score is <b>{avg_score}</b>, placing the overall
position in the <b>{overall_stage}</b> maturity stage.

<br><br>
The current benchmark leader is <b>{top_agency}</b> with a score of
<b>{highest_score}</b>, while the lowest current overall score is recorded by
<b>{lowest_agency}</b> with a score of <b>{lowest_score}</b>.

<br><br>
The current spread between the highest and lowest overall scores is
<b>{score_range}</b> points.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# MATURITY DIMENSION SUMMARY
# ==========================================================

st.markdown(
    "<div class='section-title'>Maturity Dimension Summary</div>",
    unsafe_allow_html=True
)

dimension_summary = pd.DataFrame({

    "Dimension": [
        INDEX_LABELS[col]
        for col in INDEX_COLS
    ],

    "Code": INDEX_COLS,

    "Average Score": [
        benchmark_df[col].mean()
        for col in INDEX_COLS
    ]
})

dimension_summary["Average Score"] = (
    dimension_summary["Average Score"]
    .round(1)
)

dimension_summary["Maturity Stage"] = dimension_summary["Average Score"].apply(
    classify_score
)

fig_dim = px.bar(
    dimension_summary.sort_values(
        "Average Score",
        ascending=True
    ),
    x="Average Score",
    y="Dimension",
    orientation="h",
    text="Average Score",
    color="Dimension",
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title="Average Maturity Scores by Dimension"
)

fig_dim.update_layout(
    xaxis_title="Average Score",
    yaxis_title="Maturity Dimension",
    xaxis=dict(
        range=[
            0,
            100
        ],
        automargin=True,
        title_standoff=20
    ),
    yaxis=dict(
        automargin=True,
        title_standoff=20
    )
)

fig_dim.update_traces(
    texttemplate="%{text:.1f}"
)

fig_dim = apply_readable_horizontal_bar_layout(
    fig_dim,
    height=500
)

st.plotly_chart(
    fig_dim,
    use_container_width=True
)

st.caption(
    "Takeaway: Data Maturity is the weakest system-wide maturity dimension, while Reconstruction Readiness is the strongest."
)

dimension_summary_display_df = format_score_dataframe(
    dimension_summary
)

dimension_summary_display_df.insert(
    0,
    "No.",
    range(
        1,
        len(dimension_summary_display_df) + 1
    )
)

st.dataframe(
    dimension_summary_display_df,
    use_container_width=True,
    hide_index=True,
    height=min(
        300,
        36 * len(dimension_summary_display_df) + 40
    )
)

# ==========================================================
# AUTOMATED FINDINGS
# ==========================================================

st.markdown(
    "<div class='section-title'>Key Findings</div>",
    unsafe_allow_html=True
)

best_dimension_code = (
    benchmark_df[
        INDEX_COLS
    ]
    .mean()
    .idxmax()
)

weakest_dimension_code = (
    benchmark_df[
        INDEX_COLS
    ]
    .mean()
    .idxmin()
)

best_dimension = INDEX_LABELS[
    best_dimension_code
]

weakest_dimension = INDEX_LABELS[
    weakest_dimension_code
]

findings = [

    {
        "Finding": "Overall maturity remains at a developing level",
        "Evidence": (
            f"The average overall maturity score across participating agencies "
            f"is {avg_score}."
        )
    },

    {
        "Finding": f"{top_agency} is the current benchmark leader",
        "Evidence": (
            f"{top_agency} recorded the highest overall score of "
            f"{highest_score}."
        )
    },

    {
        "Finding": f"{weakest_dimension} is the main system-wide gap",
        "Evidence": (
            f"{weakest_dimension} recorded the lowest average score among "
            f"the four maturity dimensions."
        )
    },

    {
        "Finding": f"{best_dimension} is the strongest maturity dimension",
        "Evidence": (
            f"{best_dimension} recorded the highest average score across "
            f"agencies."
        )
    },

    {
        "Finding": "Agency performance gaps remain visible",
        "Evidence": (
            f"The difference between the highest and lowest overall scores "
            f"is {score_range} points."
        )
    }
]

for i, item in enumerate(
    findings,
    start=1
):

    render_finding_card(
        i,
        item["Finding"],
        item["Evidence"]
    )

# ==========================================================
# KEY RISKS
# ==========================================================

st.markdown(
    "<div class='section-title'>Key Risks</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="risk-note">
The risks below summarise the main implementation concerns that may affect
progress towards more mature, evidence-based road asset management.
</div>
""",
    unsafe_allow_html=True
)

risk_df = pd.DataFrame({

    "Risk Area": [
        "Weak data maturity",
        "Limited forecasting capability",
        "Digital transformation gaps",
        "Institutional capacity constraints",
        "Funding and resource limitations"
    ],

    "Potential Impact": [
        "Poor data quality may weaken planning, reporting and prioritisation.",
        "Limited forecasting may reduce long-term maintenance planning effectiveness.",
        "Low digital readiness may slow adoption of modern asset management systems.",
        "Limited technical capacity may constrain implementation of advanced tools.",
        "Funding gaps may delay data collection, modelling and system upgrades."
    ],

    "Risk Level": [
        "High",
        "High",
        "Medium",
        "Medium",
        "Medium"
    ],

    "Recommended Mitigation": [
        "Strengthen data governance, data standards and condition data quality checks.",
        "Develop deterioration modelling capability and improve historical datasets.",
        "Invest in integrated digital asset management systems and analytical platforms.",
        "Expand staff training, technical support and institutional learning.",
        "Improve evidence-based funding justification and lifecycle investment planning."
    ]
})

risk_df.insert(
    0,
    "No.",
    range(
        1,
        len(risk_df) + 1
    )
)

st.dataframe(
    risk_df,
    use_container_width=True,
    hide_index=True,
    height=min(
        340,
        38 * len(risk_df) + 40
    )
)

# ==========================================================
# STRATEGIC RECOMMENDATIONS
# ==========================================================

st.markdown(
    "<div class='section-title'>Strategic Recommendations</div>",
    unsafe_allow_html=True
)

recommendations = [

    {
        "Recommendation": "Strengthen data governance and quality assurance",
        "Rationale": (
            "Reliable condition data is the foundation for evidence-based "
            "maintenance planning and performance monitoring."
        )
    },

    {
        "Recommendation": "Develop forecasting and deterioration modelling capability",
        "Rationale": (
            "Forecasting capability is required for long-term planning, "
            "budget justification and lifecycle decision-making."
        )
    },

    {
        "Recommendation": "Invest in integrated digital asset management systems",
        "Rationale": (
            "Integrated systems improve accessibility, coordination and "
            "real-time use of road asset information."
        )
    },

    {
        "Recommendation": "Enhance capacity building and technical training",
        "Rationale": (
            "Staff capacity is required to translate data, models and systems "
            "into effective decisions."
        )
    },

    {
        "Recommendation": "Improve institutional coordination and information sharing",
        "Rationale": (
            "Cross-agency coordination supports consistency, standardisation "
            "and better sector-wide performance management."
        )
    }
]

for i, rec in enumerate(
    recommendations,
    start=1
):

    render_recommendation_card(
        i,
        rec["Recommendation"],
        rec["Rationale"]
    )

# ==========================================================
# PRIORITY INVESTMENT AREAS
# ==========================================================

st.markdown(
    "<div class='section-title'>Priority Investment Areas</div>",
    unsafe_allow_html=True
)

priority_df = (
    dimension_summary
    .sort_values(
        "Average Score",
        ascending=True
    )
    .reset_index(drop=True)
)

priority_df["Priority Rank"] = (
    priority_df.index
    +
    1
)

priority_df = priority_df[
    [
        "Priority Rank",
        "Dimension",
        "Average Score",
        "Maturity Stage"
    ]
]

priority_display_df = format_score_dataframe(
    priority_df
)

st.dataframe(
    priority_display_df,
    use_container_width=True,
    hide_index=True,
    height=min(
        300,
        36 * len(priority_display_df) + 40
    )
)

fig_priority = px.bar(
    priority_df.sort_values(
        "Average Score",
        ascending=True
    ),
    x="Average Score",
    y="Dimension",
    orientation="h",
    text="Average Score",
    color="Dimension",
    color_discrete_sequence=ALT_COLOR_SEQUENCE,
    title="Priority Areas Based on Average Maturity Scores"
)

fig_priority.update_layout(
    xaxis_title="Average Score",
    yaxis_title="Priority Area",
    xaxis=dict(
        range=[
            0,
            100
        ],
        automargin=True,
        title_standoff=20
    ),
    yaxis=dict(
        automargin=True,
        title_standoff=20
    )
)

fig_priority.update_traces(
    texttemplate="%{text:.1f}"
)

fig_priority = apply_readable_horizontal_bar_layout(
    fig_priority,
    height=500
)

st.plotly_chart(
    fig_priority,
    use_container_width=True
)

st.caption(
    "Takeaway: Priority investment should begin with the lowest-scoring maturity areas, especially Data Maturity and Forecasting Maturity."
)

# ==========================================================
# EXPECTED BENEFITS
# ==========================================================

st.markdown(
    "<div class='section-title'>Expected Benefits</div>",
    unsafe_allow_html=True
)

benefits = [
    "Improved evidence-based road maintenance planning",
    "Better justification of funding and investment priorities",
    "Improved quality and availability of pavement condition data",
    "Stronger forecasting and long-term asset management capability",
    "Greater digital readiness and institutional coordination",
    "Improved road network performance monitoring"
]

benefit_items = ""

for benefit in benefits:

    benefit_items += (
        f'<li>{html.escape(benefit)}</li>'
    )

st.markdown(
    f"""
<div class="benefit-box">
<b>Successful implementation of the recommendations is expected to support:</b>
<ul>
{benefit_items}
</ul>
</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# DETAILED TABLES
# ==========================================================

with st.expander(
    "View Detailed Findings Tables",
    expanded=False
):

    st.markdown(
        "### Benchmark Ranking"
    )

    ranking_df = benchmark_df[
        [
            "Display_Rank",
            "Agency",
            "Overall_Score",
            "Maturity Stage",
            "DMI",
            "FMI",
            "RRI",
            "DRI"
        ]
    ].copy()

    ranking_df = ranking_df.rename(
        columns={
            "Display_Rank": "Rank",
            "Overall_Score": "Overall Score"
        }
    )

    ranking_display_df = format_score_dataframe(
        ranking_df
    )

    st.dataframe(
        ranking_display_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "### Dimension Summary"
    )

    st.dataframe(
        dimension_summary_display_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "### Priority Investment Areas"
    )

    st.dataframe(
        priority_display_df,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# FINAL EXECUTIVE SUMMARY
# ==========================================================

st.markdown(
    "<div class='section-title'>Final Executive Summary</div>",
    unsafe_allow_html=True
)

st.info(f"""
The assessment shows that participating agencies have established a foundation
for road asset management maturity, but important improvement gaps remain.

The highest benchmark score was recorded by **{top_agency}**, while
**{lowest_agency}** recorded the lowest overall score. The system-wide average
maturity score is **{avg_score}** across **{agency_count} participating
agencies**.

The strongest maturity area is **{best_dimension}**, while the main improvement
priority is **{weakest_dimension}**.

The evidence from the maturity indices, question-level analysis, open-ended
responses and benchmarking results points to the need for targeted investment
in data systems, forecasting capability, capacity building, digital
transformation and institutional coordination.

The dashboard provides a practical decision-support framework for moving
agencies toward more mature, evidence-based and performance-oriented road asset
management.
""")

# ==========================================================
# FINAL NAVIGATION HINT
# ==========================================================

st.divider()

try:

    st.page_link(
        "Executive Dashboard.py",
        label="Return to Executive Dashboard",
        icon="⬅️"
    )

except Exception:

    st.caption(
        "Return to Executive Dashboard ←"
    )

