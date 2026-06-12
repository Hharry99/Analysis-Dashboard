# ==========================================================
# BENCHMARKING AND GAP ANALYSIS
# Sprint 3C.4 - Polished Production Version V2
# Strategic Capability Visual Improved
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Benchmarking & Gap Analysis",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# VISUAL STYLE SETTINGS
# ==========================================================

BAR_COLOR_SEQUENCE = px.colors.qualitative.Bold
STRATEGIC_COLOR_SEQUENCE = px.colors.qualitative.Set2
HEATMAP_SCALE = "Viridis"
GAP_SCALE = "OrRd"

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
    border-left:6px solid #D97706;
    background:rgba(217,119,6,0.08);
    padding:18px;
    border-radius:10px;
    margin-top:15px;
    margin-bottom:20px;
}

.note-box{
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

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/benchmark_dataset.csv"
    )


benchmark_df = load_data()

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

STRATEGIC_COLS = [
    "Data_Systems_Databases",
    "Routine_Data_Collection",
    "Forecasting_AI_Analytics",
    "Capacity_Building_Training",
    "Institutional_Coordination_Policy",
    "Funding_Resource_Allocation"
]

STRATEGIC_LABELS = {
    "Data_Systems_Databases": "Data Systems & Databases",
    "Routine_Data_Collection": "Routine Data Collection",
    "Forecasting_AI_Analytics": "Forecasting, AI & Analytics",
    "Capacity_Building_Training": "Capacity Building & Training",
    "Institutional_Coordination_Policy": "Institutional Coordination & Policy",
    "Funding_Resource_Allocation": "Funding & Resource Allocation"
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


def shorten_dimension(label):

    label_map = {
        "Data Systems & Databases": "Data Systems",
        "Routine Data Collection": "Data Collection",
        "Forecasting, AI & Analytics": "Forecasting & AI",
        "Capacity Building & Training": "Capacity Building",
        "Institutional Coordination & Policy": "Institutional Coordination",
        "Funding & Resource Allocation": "Funding"
    }

    return label_map.get(
        label,
        label
    )

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

available_strategic_cols = [
    col for col in STRATEGIC_COLS
    if col in benchmark_df.columns
]

for col in available_strategic_cols:

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
# This keeps one benchmark row per agency on the dashboard.
# Final benchmark dataset will be regenerated after survey
# closure and final validation.
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

benchmark_df["Benchmark Band"] = benchmark_df["Overall_Score"].apply(
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
    "Benchmarking & Gap Analysis"
)

st.markdown("""
This page benchmarks participating agencies across maturity indices and
strategic capability dimensions, highlighting performance gaps and priority
improvement areas.
""")

st.markdown(
    """
<div class="note-box">
<b>Benchmarking Note:</b>
Current benchmarking outputs use the available benchmark dataset. Final
rankings, scores and agency-level gaps will be refreshed after survey closure
and final dataset validation.
</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# KPI SECTION
# ==========================================================

highest = round(
    benchmark_df["Overall_Score"].max(),
    1
)

lowest = round(
    benchmark_df["Overall_Score"].min(),
    1
)

average = round(
    benchmark_df["Overall_Score"].mean(),
    1
)

highest_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmax(),
    "Agency"
]

lowest_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmin(),
    "Agency"
]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Agencies",
    agency_count
)

c2.metric(
    "Highest Score",
    highest
)

c3.metric(
    "Lowest Score",
    lowest
)

c4.metric(
    "Average Score",
    average
)

# ==========================================================
# BENCHMARK SNAPSHOT
# ==========================================================

st.markdown(
    f"""
<div class="insight-box">

<b>Benchmark Snapshot:</b><br>
A total of <b>{agency_count}</b> agencies were benchmarked.

<br><br>
The current benchmark leader is <b>{highest_agency}</b> with an overall score
of <b>{highest}</b>. The lowest current overall score is recorded by
<b>{lowest_agency}</b> with an overall score of <b>{lowest}</b>.

<br><br>
The current sector average benchmark score is <b>{average}</b>. These figures
will be refreshed after survey closure and final validation of the dataset.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# AGENCY BENCHMARK RANKING
# ==========================================================

st.markdown(
    "<div class='section-title'>Agency Benchmark Ranking</div>",
    unsafe_allow_html=True
)

ranking_df = benchmark_df[
    [
        "Display_Rank",
        "Agency",
        "Overall_Score",
        "Benchmark Band",
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

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================================
# OVERALL READINESS RANKING
# ==========================================================

st.markdown(
    "<div class='section-title'>Overall Readiness Ranking</div>",
    unsafe_allow_html=True
)

fig_rank = px.bar(
    ranking_df.sort_values(
        "Overall Score",
        ascending=True
    ),
    x="Overall Score",
    y="Agency",
    orientation="h",
    text="Overall Score",
    color="Agency",
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title="Overall Agency Ranking"
)

fig_rank.update_layout(
    xaxis_title="Overall Score",
    yaxis_title="Agency",
    xaxis=dict(
        range=[
            0,
            100
        ]
    ),
    height=520,
    showlegend=False
)

fig_rank.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_rank,
    use_container_width=True
)

# ==========================================================
# MATURITY RADAR COMPARISON
# ==========================================================

st.markdown(
    "<div class='section-title'>Maturity Radar Comparison</div>",
    unsafe_allow_html=True
)

fig_radar = go.Figure()

for _, row in benchmark_df.iterrows():

    radar_values = [
        row[col]
        for col in INDEX_COLS
    ]

    radar_labels = [
        INDEX_LABELS[col]
        for col in INDEX_COLS
    ]

    radar_values.append(
        radar_values[0]
    )

    radar_labels.append(
        radar_labels[0]
    )

    fig_radar.add_trace(
        go.Scatterpolar(
            r=radar_values,
            theta=radar_labels,
            fill="toself",
            name=row["Agency"]
        )
    )

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[
                0,
                100
            ]
        )
    ),
    showlegend=True,
    height=700
)

st.plotly_chart(
    fig_radar,
    use_container_width=True
)

# ==========================================================
# STRATEGIC DIMENSION BENCHMARK
# ==========================================================

if available_strategic_cols:

    st.markdown(
        "<div class='section-title'>Strategic Dimension Benchmark</div>",
        unsafe_allow_html=True
    )

    strategic_df = benchmark_df[
        [
            "Agency"
        ]
        +
        available_strategic_cols
    ].copy()

    strategic_df = strategic_df.rename(
        columns=STRATEGIC_LABELS
    )

    strategic_df = round_columns(
        strategic_df,
        [
            col for col in strategic_df.columns
            if col != "Agency"
        ],
        decimals=1
    )

    strategic_long_df = strategic_df.melt(
        id_vars="Agency",
        var_name="Strategic Capability Dimension",
        value_name="Score"
    )

    strategic_long_df["Short Dimension"] = strategic_long_df[
        "Strategic Capability Dimension"
    ].apply(
        shorten_dimension
    )

    st.markdown(
        """
<div class="note-box">
<b>Strategic Capability View:</b>
The grouped bar chart below is used as the primary visual because it is easier
to compare agencies and capability dimensions than a low-contrast heatmap.
The heatmap is retained below as a compact scorecard.
</div>
""",
        unsafe_allow_html=True
    )

    fig_strategic_bar = px.bar(
        strategic_long_df,
        x="Score",
        y="Agency",
        color="Short Dimension",
        barmode="group",
        text="Score",
        orientation="h",
        title="Strategic Capability Scores by Agency",
        color_discrete_sequence=STRATEGIC_COLOR_SEQUENCE
    )

    fig_strategic_bar.update_layout(
        height=720,
        xaxis_title="Strategic Capability Score",
        yaxis_title="Agency",
        xaxis=dict(
            range=[
                0,
                max(
                    10,
                    strategic_long_df["Score"].max() * 1.20
                )
            ]
        ),
        legend_title_text="Strategic Capability"
    )

    fig_strategic_bar.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_strategic_bar,
        use_container_width=True
    )

    strategic_heatmap_df = strategic_df.copy()

    strategic_heatmap_df = strategic_heatmap_df.set_index(
        "Agency"
    )

    strategic_heatmap_df = strategic_heatmap_df.rename(
        columns={
            col: shorten_dimension(col)
            for col in strategic_heatmap_df.columns
        }
    )

    strategic_min = strategic_heatmap_df.min().min()
    strategic_max = strategic_heatmap_df.max().max()

    if pd.isna(strategic_min) or pd.isna(strategic_max) or strategic_min == strategic_max:

        strategic_min = 0
        strategic_max = 100

    fig_heat = px.imshow(
        strategic_heatmap_df,
        aspect="auto",
        title="Strategic Capability Scorecard",
        labels=dict(
            x="Strategic Capability Dimension",
            y="Agency",
            color="Score"
        ),
        color_continuous_scale=HEATMAP_SCALE,
        zmin=strategic_min,
        zmax=strategic_max,
        text_auto=".1f"
    )

    fig_heat.update_layout(
        height=620,
        xaxis_title="Strategic Capability Dimension",
        yaxis_title="Agency"
    )

    fig_heat.update_xaxes(
        tickangle=25
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

# ==========================================================
# GAP ANALYSIS
# ==========================================================

st.markdown(
    "<div class='section-title'>Gap Analysis</div>",
    unsafe_allow_html=True
)

gap_df = benchmark_df[
    [
        "Agency"
    ]
    +
    INDEX_COLS
].copy()

for col in INDEX_COLS:

    gap_df[col] = (
        benchmark_df[col].max()
        -
        benchmark_df[col]
    ).round(1)

gap_df = gap_df.rename(
    columns=INDEX_LABELS
)

gap_matrix = gap_df.set_index(
    "Agency"
)

fig_gap = px.imshow(
    gap_matrix,
    aspect="auto",
    title="Maturity Gap Analysis",
    labels=dict(
        x="Maturity Dimension",
        y="Agency",
        color="Gap"
    ),
    color_continuous_scale=GAP_SCALE,
    text_auto=".1f"
)

fig_gap.update_layout(
    height=600,
    xaxis_title="Maturity Dimension",
    yaxis_title="Agency"
)

st.plotly_chart(
    fig_gap,
    use_container_width=True
)

# ==========================================================
# PRIORITY IMPROVEMENT AREAS
# ==========================================================

st.markdown(
    "<div class='section-title'>Priority Improvement Areas</div>",
    unsafe_allow_html=True
)

priority_rows = []

for _, row in benchmark_df.iterrows():

    weakest_code = min(
        INDEX_COLS,
        key=lambda x: row[x]
    )

    priority_rows.append({
        "Agency": row["Agency"],
        "Priority Area": INDEX_LABELS[weakest_code],
        "Score": round(
            row[weakest_code],
            1
        )
    })

priority_df = pd.DataFrame(
    priority_rows
)

st.dataframe(
    priority_df,
    use_container_width=True
)

# ==========================================================
# DETAILED BENCHMARK TABLES
# ==========================================================

with st.expander(
    "View Detailed Benchmark Tables",
    expanded=False
):

    st.markdown(
        "### Full Benchmark Ranking"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.markdown(
        "### Maturity Gap Matrix"
    )

    st.dataframe(
        gap_matrix,
        use_container_width=True
    )

    if available_strategic_cols:

        st.markdown(
            "### Strategic Capability Matrix"
        )

        st.dataframe(
            strategic_heatmap_df,
            use_container_width=True
        )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

best_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmax(),
    "Agency"
]

best_score = benchmark_df[
    "Overall_Score"
].max()

lowest_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmin(),
    "Agency"
]

lowest_score = benchmark_df[
    "Overall_Score"
].min()

largest_gap_dimension = (
    gap_matrix
    .mean()
    .idxmax()
)

st.info(f"""
### Executive Interpretation

A total of **{agency_count} agencies** were benchmarked.

The highest performing agency was **{best_agency}** with an overall score of
**{best_score:.1f}**.

The lowest overall score was recorded by **{lowest_agency}** with a score of
**{lowest_score:.1f}**.

The gap analysis indicates that **{largest_gap_dimension}** has the largest
average benchmark gap across agencies.

The radar, strategic capability and gap analyses identify maturity differences
across agencies and highlight areas requiring targeted intervention.

Improvement efforts should focus on the lowest-scoring dimensions within each
agency to accelerate overall asset management maturity.
""")
