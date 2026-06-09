# ==========================================================
# PAVEMENT PERFORMANCE MANAGEMENT DASHBOARD
# Sprint 1 - Core Engine & Data Architecture
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Pavement Performance Management Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# Works well in both Light and Dark Mode
# ==========================================================

st.markdown("""
<style>

.main-title {
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    padding: 10px;
}

.section-box {
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(128,128,128,0.3);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_data():

    master = pd.read_csv("data/clean_master.csv")

    multiselect = pd.read_csv(
        "data/multiselect_dataset.csv"
    )

    indices = pd.read_csv(
        "data/indices_dataset.csv"
    )

    themes = pd.read_csv(
        "data/theme_dataset.csv"
    )

    benchmark = pd.read_csv(
        "data/benchmark_dataset.csv"
    )

    return (
        master,
        multiselect,
        indices,
        themes,
        benchmark
    )

# ==========================================================
# LOAD DATASETS
# ==========================================================

try:

    master_df, multi_df, indices_df, theme_df, benchmark_df = load_data()

except Exception as e:

    st.error(f"Error loading datasets: {e}")
    st.stop()

# ==========================================================
# TITLE
# ==========================================================

st.markdown(
    """
    <div class='main-title'>
    Pavement Performance Management Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Pavement Performance Management Under Data Constraints: Perspectives of Practitioners in Kenya"
)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Dashboard Filters")

# Organization Filter

if "Agency" in master_df.columns:

    selected_orgs = st.sidebar.multiselect(
        "Organization",
        options=sorted(
            master_df["Agency"]
            .dropna()
            .unique()
        )
    )

else:
    selected_orgs = []

# Position Filter

position_col = None

for col in master_df.columns:

    if "position" in col.lower():

        position_col = col
        break

if position_col:

    selected_positions = st.sidebar.multiselect(
        "Position",
        options=sorted(
            master_df[position_col]
            .dropna()
            .unique()
        )
    )

else:
    selected_positions = []

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = master_df.copy()

if selected_orgs:

    filtered_df = filtered_df[
        filtered_df["Agency"]
        .isin(selected_orgs)
    ]

if position_col and selected_positions:

    filtered_df = filtered_df[
        filtered_df[position_col]
        .isin(selected_positions)
    ]

# ==========================================================
# KPI ENGINE
# ==========================================================

def calculate_kpis():

    kpis = {}

    kpis["Respondents"] = len(master_df)

    if "Agency" in master_df.columns:
        kpis["Organizations"] = (
            master_df["Agency"]
            .nunique()
        )
    else:
        kpis["Organizations"] = 0

    if "DMI" in indices_df.columns:
        kpis["DMI"] = round(
            indices_df["DMI"].mean(),
            1
        )
    else:
        kpis["DMI"] = 0

    if "FMI" in indices_df.columns:
        kpis["FMI"] = round(
            indices_df["FMI"].mean(),
            1
        )
    else:
        kpis["FMI"] = 0

    if "RRI" in indices_df.columns:
        kpis["RRI"] = round(
            indices_df["RRI"].mean(),
            1
        )
    else:
        kpis["RRI"] = 0

    if "DRI" in indices_df.columns:
        kpis["DRI"] = round(
            indices_df["DRI"].mean(),
            1
        )
    else:
        kpis["DRI"] = 0

    return kpis

# ==========================================================
# DISPLAY KPI CARDS
# ==========================================================

kpis = calculate_kpis()

st.subheader("Executive KPI Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Respondents",
        kpis["Respondents"]
    )

with c2:
    st.metric(
        "Organizations",
        kpis["Organizations"]
    )

with c3:
    st.metric(
        "Data Maturity Index",
        kpis["DMI"]
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Forecasting Maturity",
        kpis["FMI"]
    )

with c5:
    st.metric(
        "Reconstruction Readiness",
        kpis["RRI"]
    )

with c6:
    st.metric(
        "Digital Readiness",
        kpis["DRI"]
    )

# ==========================================================
# THEME ENGINE
# ==========================================================

THEMES = [
    "Data Systems & Databases",
    "Routine Data Collection & Monitoring",
    "Forecasting, AI & Analytics",
    "Capacity Building & Training",
    "Institutional Coordination & Policy",
    "Funding & Resource Allocation"
]

def calculate_theme_frequency():

    results = []

    for theme in THEMES:

        if theme in theme_df.columns:

            count = theme_df[theme].sum()

            results.append({
                "Theme": theme,
                "Mentions": count
            })

    return pd.DataFrame(results)

# ==========================================================
# THEME TABLE
# ==========================================================

st.subheader("Theme Frequency Summary")

theme_summary = calculate_theme_frequency()

if not theme_summary.empty:

    st.dataframe(
        theme_summary,
        use_container_width=True
    )

# ==========================================================
# BENCHMARK ENGINE
# ==========================================================

def organization_rankings():

    if benchmark_df.empty:
        return pd.DataFrame()

    benchmark = benchmark_df.copy()

    required_cols = [
        "DMI",
        "FMI",
        "RRI",
        "DRI"
    ]

    missing = [
        c for c in required_cols
        if c not in benchmark.columns
    ]

    if missing:
        return pd.DataFrame()

    benchmark["Overall Score"] = (

        benchmark["DMI"]
        + benchmark["FMI"]
        + benchmark["RRI"]
        + benchmark["DRI"]

    ) / 4

    benchmark = benchmark.sort_values(
        "Overall Score",
        ascending=False
    )

    return benchmark

# ==========================================================
# BENCHMARK TABLE
# ==========================================================

st.subheader("Organization Benchmark Ranking")

ranking_df = organization_rankings()

if not ranking_df.empty:

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

else:

    st.info(
        "Benchmark dataset not yet populated."
    )

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.success(
    "Sprint 1 Completed Successfully"
)

st.info(
    "Next Step: Build Executive Dashboard Visualizations (Sprint 2)"
)# Welcome to Sourcery! We're here to be your pair programmer anytime you're
# working in VS Code.

# To get started log into your Sourcery account. Click on the Sourcery logo
# (the hexagon) on your VS Code sidebar and click the login button, or open
# the command palette (Ctrl/Cmd+Shift+P) and execute `Sourcery: Login`.

# Let's start looking at how you can get a code review from Sourcery.

# The `Review` tab allows you to get a code review straight away in your IDE
# - You can always get a review of the current file
# - If in Git you can review your current set of uncommitted changes, 
#   or your current branch compared to the default branch

# If you want reviews when you open a PR, you can add Sourcery to your GitHub or GitLab repos.


# Now let's move on to the `Chat` tab.

# Above each function you'll see a few commands - these are Code Lenses that
# you can use to interact with Sourcery. Try clicking on "Ask Sourcery" and
# asking it to update the code to use `dateutil`. The answer will appear in
# the Sourcery sidebar chat.

def days_between_dates(date1, date2):
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()
    delta = d2 - d1
    return delta.days


# With the Ask Sourcery command or the chat in the sidebar you can ask Sourcery
# questions, have it write new code for you, or update existing code.

# Sourcery also has a series of "recipes" to do different things with code.
# Try clicking the Generate Docstrings lens above this next function:

def calculate_weighted_moving_average(prices, weights):
    if not prices or not weights:
        raise ValueError("Both prices and weights must be provided.")
    
    if len(weights) > len(prices):
        raise ValueError("Length of weights must be less than or equal to length of prices.")
    
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    
    wma = []
    for i in range(len(prices) - len(weights) + 1):
        weighted_sum = sum(prices[i + j] * normalized_weights[j] for j in range(len(weights)))
        wma.append(weighted_sum)
    
    return wma

# Now try clicking Generate Tests or Explain Code for the same function!

# There is also a recipe for generating diagrams.
# You can access this by clicking Ask Sourcery and choosing it from the 
# dropdown or by selecting a section of code and clicking the recipes button 
# in the sidebar.

# In your code you'll also see sections start to get underlined.
# This means Sourcery has a suggestion to improve it.

def refactoring_example(spellbook):
    result = []
    for spell in spellbook:
        if spell.is_awesome:
            result.append(spell)
    print(result)

# Hover over the underlined code to see details of the changes including a diff.

# You can accept Sourcery's changes with the quick fix action. Put your cursor
# on the highlighted line and click on the lightbulb. 
# 
# Or use the quick-fix hotkey (Ctrl .) or (Cmd .)  and then choose 
# "Sourcery - Convert for loop...". This will instantly replace the code with 
# the improved version.

# The Problems pane (Ctrl/Cmd+Shift+M) shows all of Sourcery's suggestions.

# Sourcery also provides code metrics for each function to give you insight into
# code quality - hover over the function definition below to see this report.

def magical_hoist(magic):
    if is_powerful(magic):
        result = 'Magic'
    else:
        print("Not powerful.")
        result = 'Magic'
    print(result)

# What if we don't want to make the change Sourcery suggests?

# You can skip/ignore changes from Sourcery in a few ways:

# 1) In the quick fix menu choose "Sourcery - Skip suggested refactoring"
#    This adds a comment to the function telling Sourcery not to make the change.

# 2) In the quick fix menu choose "Sourcery - Never show me this refactoring"
#    This tells Sourcery to never suggest this type of suggestion. This config
#    is stored in a configuration file on your machine.

# 3) Click on the Sourcery button in the Status Bar (typically the bottom of
#    the VS Code window) to bring up the Sourcery Hub. Click on "Settings" and
#    then you can toggle individual rule types on or off

# For more details check out our documentation here:
# https://docs.sourcery.ai/

# If you want to play around a bit more, here are some more examples of Sourcery's in-line suggestions.
# These include cases where Sourcery has chained together suggestions to come
# up with more powerful refactorings.

def find_more(magicks):
    powerful_magic = []
    for magic in magicks:
        if not is_powerful(magic):
            continue
        powerful_magic.append(magic)
    return powerful_magic


def is_powerful(magic):
    if magic == 'Sourcery':
        return True
    elif magic == 'More Sourcery':
        return True
    else:
        return False


def print_all(spells: list):
    for i in range(len(spells)):
        print(spells[i])
