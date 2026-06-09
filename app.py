# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# SPRINT 1.5 - EXECUTIVE FOUNDATION DASHBOARD
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Pavement Performance Management Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* HERO SECTION */

.hero-badge{
    display:inline-block;
    padding:10px 25px;
    border-radius:25px;
    border:2px solid #D97706;
    color:#D97706;
    font-weight:600;
    margin-bottom:20px;
}

.hero-title{
    font-size:48px;
    font-weight:800;
    text-align:center;
    line-height:1.1;
}

.hero-subtitle{
    text-align:center;
    color:#D97706;
    font-size:26px;
    font-weight:600;
    margin-top:15px;
}

.hero-description{
    text-align:center;
    font-size:18px;
    color:#6B7280;
    margin-top:10px;
}

/* KPI CARDS */

div[data-testid="metric-container"]{
    border:1px solid rgba(128,128,128,0.20);
    padding:18px;
    border-radius:16px;
    background:rgba(15,23,42,0.05);
}

/* FINDINGS BOX */

.findings-box{
    border-left:6px solid #D97706;
    padding:20px;
    border-radius:10px;
    background:rgba(217,119,6,0.08);
    margin-top:20px;
    margin-bottom:20px;
}

/* SECTION TITLES */

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:20px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_data():

    master = pd.read_csv("data/clean_master.csv")
    multiselect = pd.read_csv("data/multiselect_dataset.csv")
    indices = pd.read_csv("data/indices_dataset.csv")
    themes = pd.read_csv("data/theme_dataset.csv")
    benchmark = pd.read_csv("data/benchmark_dataset.csv")

    return master, multiselect, indices, themes, benchmark


try:

    master_df, multi_df, indices_df, theme_df, benchmark_df = load_data()

except Exception as e:

    st.error(f"Dataset Loading Error: {e}")
    st.stop()

# ==========================================================
# COLUMN DETECTION
# ==========================================================

agency_col = next(
    (c for c in master_df.columns if "agency" in c.lower()),
    None
)

position_col = next(
    (c for c in master_df.columns if "position" in c.lower()),
    None
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Dashboard Filters")

selected_orgs = []

if agency_col:

    selected_orgs = st.sidebar.multiselect(
        "Organization",
        sorted(master_df[agency_col].dropna().unique())
    )

selected_positions = []

if position_col:

    selected_positions = st.sidebar.multiselect(
        "Position",
        sorted(master_df[position_col].dropna().unique())
    )

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = master_df.copy()

if agency_col and selected_orgs:

    filtered_df = filtered_df[
        filtered_df[agency_col].isin(selected_orgs)
    ]

if position_col and selected_positions:

    filtered_df = filtered_df[
        filtered_df[position_col].isin(selected_positions)
    ]

# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown(
"""
<div style='text-align:center'>
<div class='hero-badge'>
📋 DOCTORAL RESEARCH
</div>
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class='hero-title'>
Pavement Performance<br>
Management under Data<br>
Constraints
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class='hero-subtitle'>
Perspectives of Practitioners in Kenya
</div>
""",
unsafe_allow_html=True
)

st.markdown(
f"""
<div class='hero-description'>
Based on {len(master_df)} practitioner responses
</div>
""",
unsafe_allow_html=True
)

st.divider()

# ==========================================================
# KPI ENGINE
# ==========================================================

def safe_mean(df, col):

    if col not in df.columns:
        return 0

    return round(
        pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0).mean(),
        1
    )

responses = len(filtered_df)

organizations = (
    filtered_df[agency_col].nunique()
    if agency_col else 0
)

dmi = safe_mean(indices_df, "DMI")
fmi = safe_mean(indices_df, "FMI")
rri = safe_mean(indices_df, "RRI")
dri = safe_mean(indices_df, "DRI")

# ==========================================================
# EXECUTIVE FINDINGS
# ==========================================================

st.markdown(
"""
<div class='findings-box'>

<h4>Executive Findings</h4>

<ul>
<li>81 practitioners participated in the survey.</li>
<li>Multiple road sector organizations are represented.</li>
<li>Forecasting, AI and Analytics emerged as a dominant theme.</li>
<li>Respondents emphasized stronger data systems and capacity building.</li>
<li>Digital readiness remains an important area for improvement.</li>

</ul>

</div>
""",
unsafe_allow_html=True
)

# ==========================================================
# KPI SECTION
# ==========================================================

st.markdown(
"<div class='section-title'>Executive KPI Summary</div>",
unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Respondents", responses)

with c2:
    st.metric("Organizations", organizations)

with c3:
    st.metric("Data Maturity Index", dmi)

c4, c5, c6 = st.columns(3)

with c4:
    st.metric("Forecasting Maturity", fmi)

with c5:
    st.metric("Reconstruction Readiness", rri)

with c6:
    st.metric("Digital Readiness", dri)

# ==========================================================
# THEME SUMMARY
# ==========================================================

st.markdown(
"<div class='section-title'>Theme Frequency Summary</div>",
unsafe_allow_html=True
)

theme_names = {
    "Data_Systems_Databases":
        "Data Systems & Databases",

    "Routine_Data_Collection":
        "Routine Data Collection & Monitoring",

    "Forecasting_AI_Analytics":
        "Forecasting, AI & Analytics",

    "Capacity_Building_Training":
        "Capacity Building & Training",

    "Institutional_Coordination_Policy":
        "Institutional Coordination & Policy",

    "Funding_Resource_Allocation":
        "Funding & Resource Allocation"
}

theme_data = []

for col in theme_df.columns:

    if col in theme_names:

        theme_data.append({
            "Theme":
                theme_names[col],

            "Mentions":
                theme_df[col].sum()
        })

if len(theme_data) > 0:

    theme_summary = pd.DataFrame(theme_data)

    st.dataframe(
        theme_summary.sort_values(
            "Mentions",
            ascending=False
        ),
        use_container_width=True
    )

# ==========================================================
# ORGANIZATION SUMMARY
# ==========================================================

st.markdown(
"<div class='section-title'>Organization Theme Summary</div>",
unsafe_allow_html=True
)

if not benchmark_df.empty:

    display_cols = [
        col for col in benchmark_df.columns
        if col != "Response ID"
    ]

    st.dataframe(
        benchmark_df[display_cols],
        use_container_width=True
    )

else:

    st.info("Benchmark dataset not available.")

# ==========================================================
# DATASET HEALTH
# ==========================================================

with st.expander("Dataset Health"):

    st.write(
        f"Master Records: {len(master_df)}"
    )

    st.write(
        f"Theme Records: {len(theme_df)}"
    )

    st.write(
        f"Benchmark Records: {len(benchmark_df)}"
    )

    st.write(
        f"Indices Records: {len(indices_df)}"
    )

# ==========================================================
# DIAGNOSTICS
# ==========================================================

with st.expander("Dataset Diagnostics"):

    st.write("MASTER")
    st.write(list(master_df.columns))

    st.write("INDICES")
    st.write(list(indices_df.columns))

    st.write("THEMES")
    st.write(list(theme_df.columns))

    st.write("BENCHMARK")
    st.write(list(benchmark_df.columns))

# ==========================================================
# FOOTER
# ==========================================================

st.success(
    "Sprint 1.5 Executive Foundation Dashboard Completed Successfully"
)

st.info(
    "Ready for Sprint 2: Executive Dashboard Visualizations"
)
