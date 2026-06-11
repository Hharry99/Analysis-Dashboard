# ==========================================================
# BENCHMARKING AND GAP ANALYSIS
# Sprint 3C.4 - Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Benchmarking & Gap Analysis",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/benchmark_dataset.csv")

benchmark_df = load_data()

INDEX_COLS = ["DMI","FMI","RRI","DRI"]

STRATEGIC_COLS = [
    "Data_Systems_Databases",
    "Routine_Data_Collection",
    "Forecasting_AI_Analytics",
    "Capacity_Building_Training",
    "Institutional_Coordination_Policy",
    "Funding_Resource_Allocation"
]

st.title("📊 Benchmarking & Gap Analysis")

st.markdown(
    """
This page benchmarks participating agencies across maturity
indices and strategic capability dimensions, highlighting
performance gaps and priority improvement areas.
"""
)

required = ["Agency","Overall_Score","Overall_Rank"] + INDEX_COLS
missing = [c for c in required if c not in benchmark_df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

orgs = benchmark_df["Agency"].nunique()
highest = round(benchmark_df["Overall_Score"].max(), 2)
lowest = round(benchmark_df["Overall_Score"].min(), 2)
average = round(benchmark_df["Overall_Score"].mean(), 2)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Organizations", orgs)
c2.metric("Highest Score", highest)
c3.metric("Lowest Score", lowest)
c4.metric("Average Score", average)

st.markdown("## Agency Benchmark Ranking")

ranking_df = benchmark_df[
    ["Agency","Overall_Score","Overall_Rank","DMI","FMI","RRI","DRI"]
].sort_values("Overall_Rank")

st.dataframe(ranking_df, use_container_width=True)

st.markdown("## Overall Readiness Ranking")

fig_rank = px.bar(
    ranking_df.sort_values("Overall_Score"),
    x="Overall_Score",
    y="Agency",
    orientation="h",
    text="Overall_Score",
    title="Overall Agency Ranking"
)

st.plotly_chart(fig_rank, use_container_width=True)

st.markdown("## Maturity Radar Comparison")

fig_radar = go.Figure()

for _, row in benchmark_df.iterrows():
    fig_radar.add_trace(
        go.Scatterpolar(
            r=[row[c] for c in INDEX_COLS],
            theta=INDEX_COLS,
            fill="toself",
            name=row["Agency"]
        )
    )

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    height=700
)

st.plotly_chart(fig_radar, use_container_width=True)

available = [c for c in STRATEGIC_COLS if c in benchmark_df.columns]

if available:
    st.markdown("## Strategic Dimension Benchmark")

    strategic_df = benchmark_df.set_index("Agency")[available]

    fig_heat = px.imshow(
        strategic_df,
        aspect="auto",
        title="Strategic Capability Benchmark"
    )

    fig_heat.update_layout(height=700)

    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("## Gap Analysis")

gap_df = benchmark_df[["Agency"] + INDEX_COLS].copy()

for col in INDEX_COLS:
    gap_df[col] = (
        benchmark_df[col].max() - benchmark_df[col]
    ).round(2)

fig_gap = px.imshow(
    gap_df.set_index("Agency"),
    aspect="auto",
    title="Maturity Gap Analysis"
)

fig_gap.update_layout(height=600)

st.plotly_chart(fig_gap, use_container_width=True)

st.markdown("## Priority Improvement Areas")

priority_rows = []

for _, row in benchmark_df.iterrows():
    weakest = min(INDEX_COLS, key=lambda x: row[x])

    priority_rows.append({
        "Agency": row["Agency"],
        "Priority Area": weakest,
        "Score": row[weakest]
    })

priority_df = pd.DataFrame(priority_rows)

st.dataframe(priority_df, use_container_width=True)

best_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmax(),
    "Agency"
]

best_score = benchmark_df["Overall_Score"].max()

st.info(f"""
### Executive Interpretation

A total of **{orgs} organizations** were benchmarked.

The highest performing organization was
**{best_agency}** with an overall score of
**{best_score:.2f}**.

The radar and gap analyses identify maturity
differences across agencies and highlight
priority areas requiring targeted intervention.

Improvement efforts should focus on the
lowest-scoring dimensions within each agency
to accelerate asset management maturity.
""")

