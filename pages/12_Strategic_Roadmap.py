# ==========================================================
# STRATEGIC ROADMAP
# Sprint 3D.1 - Framework Aligned Production Version
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Strategic Roadmap",
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
# This is display-level de-duplication only.
# It does not permanently clean the dataset.
# The final benchmark dataset will still be regenerated
# after survey closure.
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
# Recalculate display rank using one record per agency.
# This prevents Rank 2/6 when there are only 5 agencies.
# ----------------------------------------------------------

benchmark_df["Display_Rank"] = (
    benchmark_df.index + 1
)

agency_count = benchmark_df["Agency"].nunique()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Strategic Roadmap"
)

st.markdown("""
This page provides an agency-specific roadmap for improving
road asset management maturity based on benchmarking results.

Recommendations are generated from each agency's maturity profile.
""")

st.caption(
    """
    Note: Current roadmap outputs use the available benchmark dataset.
    Final rankings and agency-specific recommendations will be refreshed
    after survey closure and final dataset validation.
    """
)

# ==========================================================
# AGENCY SELECTOR
# ==========================================================

selected_agency = st.selectbox(
    "Select Agency",
    sorted(
        benchmark_df[
            "Agency"
        ]
        .dropna()
        .unique()
    )
)

agency_row = (
    benchmark_df[
        benchmark_df[
            "Agency"
        ] == selected_agency
    ]
    .iloc[0]
)

# ==========================================================
# AGENCY STRATEGIC PROFILE
# ==========================================================

st.markdown(
    "## Agency Strategic Profile"
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "DMI",
    round(
        agency_row["DMI"],
        1
    )
)

c2.metric(
    "FMI",
    round(
        agency_row["FMI"],
        1
    )
)

c3.metric(
    "RRI",
    round(
        agency_row["RRI"],
        1
    )
)

c4.metric(
    "DRI",
    round(
        agency_row["DRI"],
        1
    )
)

c5.metric(
    "Overall Score",
    round(
        agency_row["Overall_Score"],
        1
    )
)

c6.metric(
    "Rank",
    f"{int(agency_row['Display_Rank'])} / {agency_count}"
)

# ==========================================================
# MATURITY PROFILE
# ==========================================================

st.markdown(
    "## Maturity Profile"
)

profile_df = pd.DataFrame({

    "Dimension": [
        "Data Maturity",
        "Forecasting Maturity",
        "Reconstruction Readiness",
        "Digital Readiness"
    ],

    "Code": [
        "DMI",
        "FMI",
        "RRI",
        "DRI"
    ],

    "Score": [
        agency_row["DMI"],
        agency_row["FMI"],
        agency_row["RRI"],
        agency_row["DRI"]
    ]
})

fig_profile = px.bar(
    profile_df,
    x="Dimension",
    y="Score",
    text="Score",
    title=f"{selected_agency} Maturity Profile"
)

fig_profile.update_layout(
    xaxis_title="Maturity Dimension",
    yaxis_title="Score",
    yaxis=dict(
        range=[
            0,
            100
        ]
    )
)

fig_profile.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_profile,
    use_container_width=True
)

# ==========================================================
# STRENGTHS AND WEAKNESSES
# ==========================================================

st.markdown(
    "## Strengths and Weaknesses"
)

scores = {

    "Data Maturity":
        agency_row["DMI"],

    "Forecasting Maturity":
        agency_row["FMI"],

    "Reconstruction Readiness":
        agency_row["RRI"],

    "Digital Readiness":
        agency_row["DRI"]
}

strongest = max(
    scores,
    key=scores.get
)

weakest = min(
    scores,
    key=scores.get
)

c1, c2 = st.columns(2)

c1.success(
    f"Strongest Area: {strongest} ({scores[strongest]:.1f})"
)

c2.error(
    f"Priority Improvement Area: {weakest} ({scores[weakest]:.1f})"
)

# ==========================================================
# ROADMAP ACTION LIBRARY
# ==========================================================

ROADMAP = {

    "Data Maturity": {

        "short": [
            "Standardize pavement data collection templates",
            "Improve condition survey documentation",
            "Create basic data governance procedures"
        ],

        "medium": [
            "Integrate pavement condition, maintenance and inventory records",
            "Introduce routine data quality checks",
            "Develop agency-wide reporting standards"
        ],

        "long": [
            "Establish an enterprise road asset database",
            "Adopt advanced analytics for pavement data",
            "Institutionalize data-driven decision-making culture"
        ]
    },

    "Forecasting Maturity": {

        "short": [
            "Train technical staff on pavement deterioration forecasting",
            "Compile historical pavement condition records",
            "Identify suitable forecasting methods for local conditions"
        ],

        "medium": [
            "Develop locally calibrated deterioration models",
            "Integrate forecasting outputs into maintenance planning",
            "Introduce scenario-based planning and budget forecasting"
        ],

        "long": [
            "Adopt predictive analytics for pavement performance",
            "Use AI-assisted deterioration modelling",
            "Apply risk-based long-term investment planning"
        ]
    },

    "Reconstruction Readiness": {

        "short": [
            "Strengthen pavement condition assessment practices",
            "Develop clear treatment selection criteria",
            "Improve prioritization of rehabilitation needs"
        ],

        "medium": [
            "Introduce life-cycle planning approaches",
            "Improve capital works programming",
            "Link reconstruction decisions to condition and traffic data"
        ],

        "long": [
            "Adopt network-level optimization tools",
            "Automate treatment selection and prioritization",
            "Develop long-term reconstruction investment strategies"
        ]
    },

    "Digital Readiness": {

        "short": [
            "Digitize key road asset management records",
            "Improve ICT infrastructure and system connectivity",
            "Build user awareness of digital tools"
        ],

        "medium": [
            "Implement integrated road asset management platforms",
            "Improve inter-agency data sharing",
            "Strengthen cybersecurity and data access controls"
        ],

        "long": [
            "Adopt smart asset management systems",
            "Introduce real-time monitoring technologies",
            "Develop digital twin and advanced decision-support capability"
        ]
    }
}

# ==========================================================
# STRATEGIC ROADMAP
# ==========================================================

st.markdown(
    "## Strategic Roadmap"
)

roadmap = ROADMAP[
    weakest
]

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        "### Short Term"
    )

    st.caption(
        "0–12 Months"
    )

    for item in roadmap["short"]:

        st.write(
            f"• {item}"
        )

with col2:

    st.markdown(
        "### Medium Term"
    )

    st.caption(
        "1–3 Years"
    )

    for item in roadmap["medium"]:

        st.write(
            f"• {item}"
        )

with col3:

    st.markdown(
        "### Long Term"
    )

    st.caption(
        "3–5 Years"
    )

    for item in roadmap["long"]:

        st.write(
            f"• {item}"
        )

# ==========================================================
# PRIORITY INVESTMENT AREAS
# ==========================================================

st.markdown(
    "## Priority Investment Areas"
)

priority_df = (
    profile_df
    .sort_values(
        "Score",
        ascending=True
    )
    .reset_index(drop=True)
)

priority_df["Priority Rank"] = (
    priority_df.index + 1
)

priority_df = priority_df[
    [
        "Priority Rank",
        "Dimension",
        "Score"
    ]
]

st.dataframe(
    priority_df,
    use_container_width=True
)

# ==========================================================
# MATURITY IMPROVEMENT PATH
# ==========================================================

st.markdown(
    "## Maturity Improvement Path"
)

overall_score = agency_row[
    "Overall_Score"
]

if overall_score < 40:

    maturity_stage = "Emerging"

elif overall_score < 60:

    maturity_stage = "Developing"

elif overall_score < 80:

    maturity_stage = "Advanced"

else:

    maturity_stage = "Leading"

st.info(
    f"""
Current maturity stage for **{selected_agency}**:

**{maturity_stage}**

The strategic roadmap is intended to move the agency progressively
towards a higher maturity stage through targeted interventions.
"""
)

# ==========================================================
# EXPECTED OUTCOMES
# ==========================================================

st.markdown(
    "## Expected Outcomes"
)

st.success("""
Successful implementation of the roadmap is expected to support:

• Improved evidence-based maintenance planning

• Better data quality and institutional coordination

• Stronger forecasting and long-term investment planning

• Improved funding justification and prioritization

• Higher road asset management maturity
""")

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Executive Interpretation

**{selected_agency}** currently ranks
**{int(agency_row['Display_Rank'])} out of {agency_count}**
participating agencies, with an overall score of
**{agency_row['Overall_Score']:.1f}**.

The agency's strongest maturity dimension is
**{strongest}**, while the main priority improvement area is
**{weakest}**.

The proposed roadmap focuses on addressing the weakest maturity
dimension first, while building on the agency's existing strengths.

If implemented progressively, the roadmap can improve
evidence-based planning, asset management decision-making,
forecasting capability and long-term infrastructure performance.
""")
