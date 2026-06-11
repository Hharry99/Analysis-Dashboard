# ==========================================================
# KEY FINDINGS AND RECOMMENDATIONS
# Sprint 3D.2 - Framework Aligned Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Key Findings & Recommendations",
    page_icon="✅",
    layout="wide"
)

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

# ----------------------------------------------------------
# IMPORTANT:
# Display-level de-duplication only.
# This ensures the page uses one benchmark row per agency.
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

benchmark_df["Display_Rank"] = (
    benchmark_df.index + 1
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
question-level analytics, thematic insights, benchmarking results and
strategic roadmap.

It is designed as an executive summary for decision-makers.
""")

st.caption(
    """
    Note: Current findings use the available benchmark dataset.
    Final findings, rankings and recommendations will be refreshed
    after survey closure and final dataset validation.
    """
)

# ==========================================================
# EXECUTIVE KPI SUMMARY
# ==========================================================

st.markdown(
    "## Executive Summary KPIs"
)

avg_score = benchmark_df[
    "Overall_Score"
].mean()

highest_score = benchmark_df[
    "Overall_Score"
].max()

lowest_score = benchmark_df[
    "Overall_Score"
].min()

top_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmax(),
    "Agency"
]

lowest_agency = benchmark_df.loc[
    benchmark_df["Overall_Score"].idxmin(),
    "Agency"
]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Agencies Assessed",
    agency_count
)

c2.metric(
    "Average Overall Score",
    round(
        avg_score,
        2
    )
)

c3.metric(
    "Highest Score",
    round(
        highest_score,
        2
    )
)

c4.metric(
    "Lowest Score",
    round(
        lowest_score,
        2
    )
)

# ==========================================================
# MATURITY DIMENSION SUMMARY
# ==========================================================

st.markdown(
    "## Maturity Dimension Summary"
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
    .round(2)
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
    title="Average Maturity Scores by Dimension"
)

fig_dim.update_layout(
    xaxis_title="Average Score",
    yaxis_title="Maturity Dimension"
)

fig_dim.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig_dim,
    use_container_width=True
)

# ==========================================================
# AUTOMATED FINDINGS
# ==========================================================

st.markdown(
    "## Key Findings"
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

score_range = (
    highest_score
    -
    lowest_score
)

findings = [

    {
        "Finding": "Overall maturity levels are moderate",
        "Evidence": (
            f"The average overall maturity score across participating "
            f"agencies is {avg_score:.2f}."
        )
    },

    {
        "Finding": f"{top_agency} is the current benchmark leader",
        "Evidence": (
            f"{top_agency} recorded the highest overall score "
            f"of {highest_score:.2f}."
        )
    },

    {
        "Finding": f"{weakest_dimension} is the main system-wide gap",
        "Evidence": (
            f"{weakest_dimension} recorded the lowest average score "
            f"among the four maturity dimensions."
        )
    },

    {
        "Finding": f"{best_dimension} is the strongest maturity dimension",
        "Evidence": (
            f"{best_dimension} recorded the highest average score "
            f"across agencies."
        )
    },

    {
        "Finding": "Agency performance gaps remain visible",
        "Evidence": (
            f"The difference between the highest and lowest overall "
            f"scores is {score_range:.2f} points."
        )
    }
]

for i, item in enumerate(
    findings,
    start=1
):

    st.info(f"""
### Finding {i}: {item["Finding"]}

{item["Evidence"]}
""")

# ==========================================================
# KEY RISKS
# ==========================================================

st.markdown(
    "## Key Risks"
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

st.dataframe(
    risk_df,
    use_container_width=True
)

# ==========================================================
# STRATEGIC RECOMMENDATIONS
# ==========================================================

st.markdown(
    "## Strategic Recommendations"
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
            "Staff capacity is required to translate data, models and "
            "systems into effective decisions."
        )
    },

    {
        "Recommendation": "Improve institutional coordination and information sharing",
        "Rationale": (
            "Cross-agency coordination supports consistency, standardization "
            "and better sector-wide performance management."
        )
    }
]

for i, rec in enumerate(
    recommendations,
    start=1
):

    st.success(f"""
### Recommendation {i}: {rec["Recommendation"]}

{rec["Rationale"]}
""")

# ==========================================================
# PRIORITY INVESTMENT AREAS
# ==========================================================

st.markdown(
    "## Priority Investment Areas"
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
        "Average Score"
    ]
]

st.dataframe(
    priority_df,
    use_container_width=True
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
    title="Priority Areas Based on Average Maturity Scores"
)

fig_priority.update_layout(
    xaxis_title="Average Score",
    yaxis_title="Priority Area"
)

fig_priority.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig_priority,
    use_container_width=True
)

# ==========================================================
# EXPECTED BENEFITS
# ==========================================================

st.markdown(
    "## Expected Benefits"
)

benefits = [
    "Improved evidence-based road maintenance planning",
    "Better justification of funding and investment priorities",
    "Improved quality and availability of pavement condition data",
    "Stronger forecasting and long-term asset management capability",
    "Greater digital readiness and institutional coordination",
    "Improved road network performance monitoring"
]

benefit_text = "\n".join(
    [
        f"• {benefit}"
        for benefit in benefits
    ]
)

st.success(f"""
Successful implementation of the recommendations is expected to support:

{benefit_text}
""")

# ==========================================================
# FINAL EXECUTIVE SUMMARY
# ==========================================================

st.markdown(
    "## Final Executive Summary"
)

st.info(f"""
The assessment shows that participating agencies have established
a foundation for road asset management maturity, but important
improvement gaps remain.

The highest benchmark score was recorded by **{top_agency}**,
while **{lowest_agency}** recorded the lowest overall score.
The system-wide average maturity score is **{avg_score:.2f}**
across **{agency_count} participating agencies**.

The strongest maturity area is **{best_dimension}**, while the
main improvement priority is **{weakest_dimension}**.

The evidence from the maturity indices, question-level analysis,
open-ended responses and benchmarking results points to the need
for targeted investment in data systems, forecasting capability,
capacity building, digital transformation and institutional
coordination.

The dashboard provides a practical decision-support framework
for moving agencies toward more mature, evidence-based and
performance-oriented road asset management.
""")
