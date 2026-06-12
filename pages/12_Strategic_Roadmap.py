# ==========================================================
# STRATEGIC ROADMAP
# Sprint 3D.1 - Polished Production Version
# ==========================================================

import html
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
# VISUAL STYLE SETTINGS
# ==========================================================

BAR_COLOR_SEQUENCE = px.colors.qualitative.Bold
ROADMAP_COLORS = {
    "short": "#2563EB",
    "medium": "#D97706",
    "long": "#059669"
}

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

.roadmap-card{
    border-radius:14px;
    border:1px solid rgba(128,128,128,0.25);
    padding:18px;
    min-height:310px;
    background:rgba(15,23,42,0.04);
    margin-bottom:18px;
}

.roadmap-card h4{
    margin-top:0;
    margin-bottom:4px;
}

.roadmap-period{
    font-size:13px;
    color:#6B7280;
    margin-bottom:12px;
    font-weight:600;
}

.roadmap-item{
    margin-bottom:10px;
    line-height:1.45;
}

.outcome-box{
    border-left:5px solid #059669;
    background:rgba(5,150,105,0.08);
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


def render_roadmap_card(title, period, items, color):

    safe_title = html.escape(title)
    safe_period = html.escape(period)

    list_items = ""

    for item in items:

        safe_item = html.escape(item)

        list_items += f"""
        <div class="roadmap-item">
            <span style="color:{color}; font-weight:700;">●</span>
            {safe_item}
        </div>
        """

    st.markdown(
        f"""
<div class="roadmap-card" style="border-top:5px solid {color};">
    <h4>{safe_title}</h4>
    <div class="roadmap-period">{safe_period}</div>
    {list_items}
</div>
""",
        unsafe_allow_html=True
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
# This does not permanently clean the dataset.
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
    "Strategic Roadmap"
)

st.markdown("""
This page provides an agency-specific roadmap for improving road asset
management maturity based on benchmarking results.

Recommendations are generated from each agency's maturity profile.
""")

st.markdown(
    """
<div class="note-box">
<b>Roadmap Note:</b>
Current roadmap outputs use the available benchmark dataset. Final rankings,
scores and agency-specific recommendations will be refreshed after survey
closure and final dataset validation.
</div>
""",
    unsafe_allow_html=True
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
    "<div class='section-title'>Agency Strategic Profile</div>",
    unsafe_allow_html=True
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

profile_df["Maturity Band"] = profile_df["Score"].apply(
    classify_score
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

overall_score = agency_row[
    "Overall_Score"
]

maturity_stage = classify_score(
    overall_score
)

st.markdown(
    f"""
<div class="insight-box">

<b>Agency Strategic Snapshot:</b><br>
<b>{selected_agency}</b> currently ranks
<b>{int(agency_row['Display_Rank'])} out of {agency_count}</b>
participating agencies with an overall score of <b>{overall_score:.1f}</b>.

<br><br>
The agency's current maturity stage is <b>{maturity_stage}</b>.
The strongest maturity dimension is <b>{strongest}</b>
(<b>{scores[strongest]:.1f}</b>), while the main priority improvement area is
<b>{weakest}</b> (<b>{scores[weakest]:.1f}</b>).

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# MATURITY PROFILE CHART
# ==========================================================

st.markdown(
    "<div class='section-title'>Maturity Profile</div>",
    unsafe_allow_html=True
)

fig_profile = px.bar(
    profile_df.sort_values(
        "Score",
        ascending=True
    ),
    x="Score",
    y="Dimension",
    orientation="h",
    text="Score",
    color="Dimension",
    color_discrete_sequence=BAR_COLOR_SEQUENCE,
    title=f"{selected_agency} Maturity Profile"
)

fig_profile.update_layout(
    xaxis_title="Score",
    yaxis_title="Maturity Dimension",
    xaxis=dict(
        range=[
            0,
            100
        ]
    ),
    height=460,
    showlegend=False
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
    "<div class='section-title'>Strengths and Weaknesses</div>",
    unsafe_allow_html=True
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
    "<div class='section-title'>Strategic Roadmap</div>",
    unsafe_allow_html=True
)

roadmap = ROADMAP[
    weakest
]

col1, col2, col3 = st.columns(3)

with col1:

    render_roadmap_card(
        title="Short Term",
        period="0–12 Months",
        items=roadmap["short"],
        color=ROADMAP_COLORS["short"]
    )

with col2:

    render_roadmap_card(
        title="Medium Term",
        period="1–3 Years",
        items=roadmap["medium"],
        color=ROADMAP_COLORS["medium"]
    )

with col3:

    render_roadmap_card(
        title="Long Term",
        period="3–5 Years",
        items=roadmap["long"],
        color=ROADMAP_COLORS["long"]
    )

# ==========================================================
# PRIORITY INVESTMENT AREAS
# ==========================================================

st.markdown(
    "<div class='section-title'>Priority Investment Areas</div>",
    unsafe_allow_html=True
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
        "Score",
        "Maturity Band"
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
    "<div class='section-title'>Maturity Improvement Path</div>",
    unsafe_allow_html=True
)

st.info(
    f"""
Current maturity stage for **{selected_agency}**:

**{maturity_stage}**

The strategic roadmap is intended to move the agency progressively towards a
higher maturity stage through targeted interventions, starting with the weakest
maturity dimension.
"""
)

# ==========================================================
# EXPECTED OUTCOMES
# ==========================================================

st.markdown(
    "<div class='section-title'>Expected Outcomes</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="outcome-box">
Successful implementation of the roadmap is expected to support improved
evidence-based maintenance planning, better data quality, stronger institutional
coordination, improved forecasting, stronger investment justification and higher
road asset management maturity.
</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# DETAILED ROADMAP TABLES
# ==========================================================

with st.expander(
    "View Detailed Roadmap and Priority Tables",
    expanded=False
):

    roadmap_rows = []

    for period_key, period_label in [
        ("short", "Short Term"),
        ("medium", "Medium Term"),
        ("long", "Long Term")
    ]:

        for action in roadmap[period_key]:

            roadmap_rows.append({
                "Agency": selected_agency,
                "Priority Dimension": weakest,
                "Time Horizon": period_label,
                "Recommended Action": action
            })

    roadmap_df = pd.DataFrame(
        roadmap_rows
    )

    st.markdown(
        "### Roadmap Actions"
    )

    st.dataframe(
        roadmap_df,
        use_container_width=True
    )

    st.markdown(
        "### Priority Investment Areas"
    )

    st.dataframe(
        priority_df,
        use_container_width=True
    )

# ==========================================================
# EXECUTIVE INTERPRETATION
# ==========================================================

st.info(f"""
### Executive Interpretation

**{selected_agency}** currently ranks
**{int(agency_row['Display_Rank'])} out of {agency_count}**
participating agencies, with an overall score of
**{agency_row['Overall_Score']:.1f}**.

The agency's strongest maturity dimension is **{strongest}**, while the main
priority improvement area is **{weakest}**.

The proposed roadmap focuses on addressing the weakest maturity dimension first,
while building on the agency's existing strengths.

If implemented progressively, the roadmap can improve evidence-based planning,
asset management decision-making, forecasting capability and long-term
infrastructure performance.
""")
