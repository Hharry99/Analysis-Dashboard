# ==========================================================
# SHARED DASHBOARD NAVIGATION
# Clean grouped sidebar navigation for all dashboard pages.
# ==========================================================

import streamlit as st


def apply_sidebar_navigation(current_page="Executive Dashboard"):
    """
    Renders grouped dashboard navigation.
    Designed to remain readable in light and dark mode.
    """

    st.markdown(
        """
<style>

/* Hide Streamlit default multipage list */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"]{
    display:none !important;
    visibility:hidden !important;
    height:0 !important;
    max-height:0 !important;
    overflow:hidden !important;
}

/* Sidebar menu title */
section[data-testid="stSidebar"] .sidebar-nav-title{
    font-size:21px !important;
    font-weight:900 !important;
    margin-top:6px !important;
    margin-bottom:8px !important;
    color:#F9FAFB !important;
    line-height:1.25 !important;
}

section[data-testid="stSidebar"] .sidebar-nav-caption{
    font-size:13px !important;
    font-weight:600 !important;
    color:#E5E7EB !important;
    margin-bottom:12px !important;
    line-height:1.45 !important;
}

/* Expander outer container */
section[data-testid="stSidebar"] div[data-testid="stExpander"]{
    border:1px solid rgba(255,255,255,0.18) !important;
    border-radius:12px !important;
    margin-bottom:10px !important;
    overflow:hidden !important;
    background:rgba(15,23,42,0.60) !important;
}

/* Expander header / summary.
   This is the important fix: when expanded, the group title stays visible. */
section[data-testid="stSidebar"] div[data-testid="stExpander"] details summary,
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary,
section[data-testid="stSidebar"] details summary{
    background:#F3F4F6 !important;
    color:#111827 !important;
    min-height:44px !important;
    padding:10px 13px !important;
    border-radius:10px 10px 0 0 !important;
    font-size:16px !important;
    font-weight:900 !important;
    line-height:1.25 !important;
}

/* Force every element inside the expander header to be visible */
section[data-testid="stSidebar"] div[data-testid="stExpander"] details summary *,
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary *,
section[data-testid="stSidebar"] details summary *{
    color:#111827 !important;
    fill:#111827 !important;
    stroke:#111827 !important;
    font-size:16px !important;
    font-weight:900 !important;
}

/* Page links */
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] *,
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a *{
    color:#F9FAFB !important;
    font-size:15.8px !important;
    font-weight:800 !important;
    line-height:1.25 !important;
    text-decoration:none !important;
}

/* Page link spacing */
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]{
    padding:8px 10px !important;
    border-radius:9px !important;
    margin-bottom:3px !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover{
    background:rgba(255,255,255,0.12) !important;
}

/* Filter header */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label *,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *{
    color:#F9FAFB !important;
}

/* Filter multiselect/select box:
   Use a white input background so "Choose options" stays readable in dark mode. */
section[data-testid="stSidebar"] [data-baseweb="select"] > div{
    background:#FFFFFF !important;
    color:#111827 !important;
    border:1px solid rgba(17,24,39,0.25) !important;
    border-radius:9px !important;
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

/* Dropdown options */
div[data-baseweb="popover"] *,
ul[role="listbox"] *,
li[role="option"] *{
    color:#111827 !important;
}

/* Make expander arrow visible */
section[data-testid="stSidebar"] svg{
    color:inherit !important;
}

</style>
""",
        unsafe_allow_html=True
    )

    def page_link(page, label):

        try:

            st.page_link(
                page,
                label=label
            )

        except Exception:

            st.markdown(
                f"- {label}"
            )

    executive_pages = [
        "Executive Dashboard",
        "Respondent Profile"
    ]

    maturity_pages = [
        "Data Maturity Analysis",
        "Forecasting Maturity Analysis",
        "Reconstruction Readiness Analysis",
        "Digital Readiness Analysis"
    ]

    question_pages = [
        "Data Practices Questions",
        "Forecasting Questions",
        "Reconstruction & Modelling Questions",
        "Digital Readiness Questions"
    ]

    strategic_pages = [
        "Open Ended Insights",
        "Benchmarking & Gap Analysis",
        "Strategic Roadmap",
        "Key Findings & Recommendations"
    ]

    def expanded(group_pages):

        return current_page in group_pages

    st.sidebar.markdown(
        "<div class='sidebar-nav-title'>▦ Dashboard Menu</div>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "<div class='sidebar-nav-caption'>Grouped pages are shown below. Open a section to move across the dashboard.</div>",
        unsafe_allow_html=True
    )

    with st.sidebar.expander(
        "▤  Executive Overview",
        expanded=expanded(executive_pages)
    ):

        page_link(
            "Executive Dashboard.py",
            "▦  Executive Dashboard"
        )

        page_link(
            "pages/01_Respondent_Profile.py",
            "☷  Respondent Profile"
        )

    with st.sidebar.expander(
        "◇  Maturity Analysis",
        expanded=expanded(maturity_pages)
    ):

        page_link(
            "pages/02_Data_Maturity_Analysis.py",
            "◈  Data Maturity Analysis"
        )

        page_link(
            "pages/03_Forecasting_Maturity.py",
            "⌁  Forecasting Maturity Analysis"
        )

        page_link(
            "pages/04_Reconstruction_Readiness.py",
            "▰  Reconstruction Readiness Analysis"
        )

        page_link(
            "pages/05_Digital_Readiness.py",
            "◌  Digital Readiness Analysis"
        )

    with st.sidebar.expander(
        "⊞  Question Analytics",
        expanded=expanded(question_pages)
    ):

        page_link(
            "pages/06_Data_Practices_Questions.py",
            "☰  Data Practices Questions"
        )

        page_link(
            "pages/07_Forecasting_Questions.py",
            "⌕  Forecasting Questions"
        )

        page_link(
            "pages/08_Reconstruction_and_Modelling_Questions.py",
            "◇  Reconstruction & Modelling Questions"
        )

        page_link(
            "pages/09_Digital_Readiness_Questions.py",
            "◍  Digital Readiness Questions"
        )

    with st.sidebar.expander(
        "✧  Strategic Insights",
        expanded=expanded(strategic_pages)
    ):

        page_link(
            "pages/10_Open_Ended_Insights.py",
            "◆  Open Ended Insights"
        )

        page_link(
            "pages/11_Benchmarking_and_Gap_Analysis.py",
            "▧  Benchmarking & Gap Analysis"
        )

        page_link(
            "pages/12_Strategic_Roadmap.py",
            "⌂  Strategic Roadmap"
        )

        page_link(
            "pages/13_Key_Findings_and_Recommendations.py",
            "★  Key Findings & Recommendations"
        )

    st.sidebar.divider()
