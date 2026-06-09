
# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# SPRINT 1 + SPRINT 2 COMBINED
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Pavement Performance Management Dashboard",
    page_icon="📊",
    layout="wide"
)

DEVELOPER_MODE = False

THEME_DISPLAY_NAMES = {
    "Data_Systems_Databases":"Data Systems & Databases",
    "Routine_Data_Collection":"Routine Data Collection & Monitoring",
    "Forecasting_AI_Analytics":"Forecasting, AI & Analytics",
    "Capacity_Building_Training":"Capacity Building & Training",
    "Institutional_Coordination_Policy":"Institutional Coordination & Policy",
    "Funding_Resource_Allocation":"Funding & Resource Allocation"
}

# ==========================================================
# STYLING
# ==========================================================

st.markdown("""
<style>
.hero-title{text-align:center;font-size:46px;font-weight:800;}
.hero-subtitle{text-align:center;font-size:24px;color:#D97706;}
.section-title{font-size:28px;font-weight:700;margin-top:20px;}
.findings-box,.scope-box{padding:20px;border-radius:10px;border:1px solid #ddd;}
div[data-testid="metric-container"]{border:1px solid #ddd;border-radius:12px;padding:15px;}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_data():
    return (
        pd.read_csv("data/clean_master.csv"),
        pd.read_csv("data/multiselect_dataset.csv"),
        pd.read_csv("data/indices_dataset.csv"),
        pd.read_csv("data/theme_dataset.csv"),
        pd.read_csv("data/benchmark_dataset.csv")
    )

master_df, multi_df, indices_df, theme_df, benchmark_df = load_data()

agency_col = next((c for c in master_df.columns if "agency" in c.lower()), None)
position_col = next((c for c in master_df.columns if "position" in c.lower()), None)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Dashboard Filters")

selected_orgs = st.sidebar.multiselect(
    "Organization",
    sorted(master_df[agency_col].dropna().unique())
) if agency_col else []

filtered_df = master_df.copy()

if agency_col and selected_orgs:
    filtered_df = filtered_df[filtered_df[agency_col].isin(selected_orgs)]

# ==========================================================
# HELPERS
# ==========================================================

def safe_mean(df,col):
    try:
        return round(pd.to_numeric(df[col],errors="coerce").dropna().mean(),1)
    except:
        return 0

def gauge_chart(title,value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text":title},
        gauge={"axis":{"range":[0,100]}}
    ))
    fig.update_layout(height=300)
    return fig

# ==========================================================
# KPI ENGINE
# ==========================================================

responses=len(filtered_df)
organizations=filtered_df[agency_col].nunique() if agency_col else 0

dmi=safe_mean(indices_df,"DMI")
fmi=safe_mean(indices_df,"FMI")
rri=safe_mean(indices_df,"RRI")
dri=safe_mean(indices_df,"DRI")

# ==========================================================
# THEME ENGINE
# ==========================================================

theme_results=[]

for col in theme_df.columns:
    if col in THEME_DISPLAY_NAMES:
        theme_results.append({
            "Theme":THEME_DISPLAY_NAMES[col],
            "Mentions":int(pd.to_numeric(theme_df[col],errors="coerce").fillna(0).sum())
        })

theme_summary=pd.DataFrame(theme_results)

top_theme="Not Available"
if not theme_summary.empty:
    top_theme=theme_summary.sort_values("Mentions",ascending=False).iloc[0]["Theme"]

# ==========================================================
# HERO
# ==========================================================

st.markdown("<div class='hero-title'>Pavement Performance Management under Data Constraints</div>",unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Perspectives of Practitioners in Kenya</div>",unsafe_allow_html=True)

# ==========================================================
# RESEARCH SCOPE
# ==========================================================

st.markdown(f"""
<div class='scope-box'>
<h3>Research Scope</h3>
<ul>
<li>Responses: {responses}</li>
<li>Organizations: KeRRA, KURA, KeNHA, KRB, MTRD</li>
<li>Open Ended Questions: Q27 & Q28</li>
<li>Themes: 6</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# EXECUTIVE FINDINGS
# ==========================================================

st.markdown(f"""
<div class='findings-box'>
<h4>Executive Findings</h4>
<ul>
<li>{responses} respondents participated.</li>
<li>Dominant Theme: <b>{top_theme}</b></li>
<li>Digital Readiness Index: <b>{dri}</b></li>
</ul>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# KPI SUMMARY
# ==========================================================

st.markdown("<div class='section-title'>Executive KPI Summary</div>",unsafe_allow_html=True)

c1,c2,c3=st.columns(3)
c1.metric("Respondents",responses)
c2.metric("Organizations",organizations)
c3.metric("DMI",dmi)

c4,c5,c6=st.columns(3)
c4.metric("FMI",fmi)
c5.metric("RRI",rri)
c6.metric("DRI",dri)

# ==========================================================
# SPRINT 2 EXECUTIVE ANALYTICS
# ==========================================================

st.markdown("<div class='section-title'>Executive Analytics Dashboard</div>",unsafe_allow_html=True)

a,b=st.columns(2)

with a:
    if agency_col:
        agency_counts=filtered_df[agency_col].value_counts().reset_index()
        agency_counts.columns=["Agency","Responses"]
        st.plotly_chart(
            px.pie(agency_counts,names="Agency",values="Responses",hole=.55,title="Agency Distribution"),
            use_container_width=True
        )

with b:
    if not theme_summary.empty:
        st.plotly_chart(
            px.bar(theme_summary.sort_values("Mentions"),
                   x="Mentions",y="Theme",orientation="h",
                   title="Theme Frequency"),
            use_container_width=True
        )

if not theme_summary.empty:
    total=theme_summary["Mentions"].sum()
    if total>0:
        theme_summary["Percentage"]=theme_summary["Mentions"]/total*100
        st.plotly_chart(
            px.pie(theme_summary,names="Theme",values="Percentage",hole=.6,title="Theme Distribution"),
            use_container_width=True
        )

g1,g2=st.columns(2)
g1.plotly_chart(gauge_chart("DMI",dmi),use_container_width=True)
g2.plotly_chart(gauge_chart("FMI",fmi),use_container_width=True)

g3,g4=st.columns(2)
g3.plotly_chart(gauge_chart("RRI",rri),use_container_width=True)
g4.plotly_chart(gauge_chart("DRI",dri),use_container_width=True)

st.markdown("<div class='section-title'>National Readiness Summary</div>",unsafe_allow_html=True)

summary_df=pd.DataFrame({
    "Index":["DMI","FMI","RRI","DRI"],
    "Score":[dmi,fmi,rri,dri]
})
st.dataframe(summary_df,use_container_width=True)

st.markdown("<div class='section-title'>Organization Benchmarking</div>",unsafe_allow_html=True)

cols=[c for c in ["Agency","DMI","FMI","RRI","DRI","Overall_Score","Overall_Rank"] if c in benchmark_df.columns]
if cols:
    st.dataframe(benchmark_df[cols],use_container_width=True)

st.markdown("<div class='section-title'>Executive Insights</div>",unsafe_allow_html=True)

st.info(f"""
• Respondents: {responses}

• Organizations: {organizations}

• Dominant Theme: {top_theme}

• DMI: {dmi}

• FMI: {fmi}

• RRI: {rri}

• DRI: {dri}
""")

with st.expander("Dataset Health"):
    st.dataframe(pd.DataFrame({
        "Dataset":["Master","Multi-Select","Theme","Benchmark","Indices"],
        "Records":[len(master_df),len(multi_df),len(theme_df),len(benchmark_df),len(indices_df)]
    }),use_container_width=True)

if DEVELOPER_MODE:
    with st.expander("Developer Diagnostics"):
        st.write(master_df.columns)

st.success("Sprint 1 + Sprint 2 Dashboard Loaded Successfully")
