# ==========================================================
# BENCHMARKING AND GAP ANALYSIS
# Sprint 3C.4 - Framework Aligned Production Version
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

# ----------------------------------------------------------
# IMPORTANT:
# Display-level de-duplication only.
# This keeps one benchmark row per agency on the dashboard.
# The final benchmark dataset will still be regenerated
# after survey closure and final validation.
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

# ----------------------------------------------------------
# Recalculate display rank using one row per agency.
# ----------------------------------------------------------

benchmark_df["Display_Rank"] = (
    benchmark_df.index + 1
)

agency_count = benchmark_df["Agency"].nunique()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Benchmarking & Gap Analysis"
)

st.markdown("""
This page benchmarks participating agencies across maturity
indices and strategic capability dimensions, highlighting
performance gaps and priority improvement areas.
""")

st.caption(
    """
    Note: Current benchmarking outputs use the available benchmark dataset.
    Final rankings, scores and agency-level gaps will be refreshed after
    survey closure and final dataset validation.
    """
)

# ==========================================================
# KPI SECTION
# ==========================================================

highest = round(
    benchmark_df["Overall_Score"].max(),
    2
)

lowest = round(
    benchmark_df["Overall_Score"].min(),
    2
)

average = round(
    benchmark_df["Overall_Score"].mean(),
    2
)

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
# AGENCY BENCHMARK RANKING
# ==========================================================

st.markdown(
    "## Agency Benchmark Ranking"
)

ranking_df = benchmark_df[
    [
        "Display_Rank",
        "Agency",
        "Overall_Score",
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
    "## Overall Readiness Ranking"
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
    title="Overall Agency Ranking"
)

fig_rank.update_layout(
    xaxis_title="Overall Score",
    yaxis_title="Agency"
)

fig_rank.update_traces(
    texttemplate="%{text:.1f}",
    textposition="inside"
)

st.plotly_chart(
    fig_rank,
    use_container_width=True
)

# ==========================================================
# MATURITY RADAR COMPARISON
# ==========================================================

st.markdown(
    "## Maturity Radar Comparison"
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

    # Close the radar shape
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
        "## Strategic Dimension Benchmark"
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

    strategic_df = strategic_df.set_index(
        "Agency"
    )

    fig_heat = px.imshow(
        strategic_df,
        aspect="auto",
        title="Strategic Capability Benchmark"
    )

    fig_heat.update_layout(
        height=700,
        xaxis_title="Strategic Capability Dimension",
        yaxis_title="Agency"
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

# ==========================================================
# GAP ANALYSIS
# ==========================================================

st.markdown(
    "## Gap Analysis"
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
    ).round(2)

gap_df = gap_df.rename(
    columns=INDEX_LABELS
)

gap_matrix = gap_df.set_index(
    "Agency"
)

fig_gap = px.imshow(
    gap_matrix,
    aspect="auto",
    title="Maturity Gap Analysis"
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
    "## Priority Improvement Areas"
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

The highest performing agency was **{best_agency}**
with an overall score of **{best_score:.2f}**.

The lowest overall score was recorded by **{lowest_agency}**
with a score of **{lowest_score:.2f}**.

The gap analysis indicates that **{largest_gap_dimension}**
has the largest average benchmark gap across agencies.

The radar and gap analyses identify maturity differences across
agencies and highlight areas requiring targeted intervention.

Improvement efforts should focus on the lowest-scoring dimensions
within each agency to accelerate overall asset management maturity.
""")
