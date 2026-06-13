# ==========================================================
# SHARED DASHBOARD NAVIGATION
# Applies grouped navigation consistently across all dashboard pages.
# ==========================================================

import streamlit as st


def apply_sidebar_navigation(current_page="Executive Dashboard"):
    """
    Renders the same grouped sidebar navigation on every page.
    Also hides Streamlit's default multipage navigation to avoid duplication.
    The styling is adaptive for light and dark mode.
    """

    st.markdown(
        """
<style>

/* ==========================================================
   Hide Streamlit default multipage navigation
   ========================================================== */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"]{
    display:none !important;
    visibility:hidden !important;
    height:0 !important;
    max-height:0 !important;
    overflow:hidden !important;
}

/* ==========================================================
   Light/Dark adaptive variables
   ========================================================== */
:root{
    --nav-title-text:#111827;
    --nav-muted-text:#374151;
    --nav-panel-bg:rgba(243,244,246,0.88);
    --nav-panel-border:rgba(17,24,39,0.13);
    --nav-link-text:#1F2937;
    --nav-link-hover-bg:rgba(37,99,235,0.08);
    --nav-filter-text:#111827;
    --nav-input-bg:#FFFFFF;
    --nav-input-text:#111827;
    --nav-placeholder:#4B5563;
    --nav-expander-bg:rgba(249,250,251,0.92);
}

@media (prefers-color-scheme: dark){
    :root{
        --nav-title-text:#F9FAFB;
        --nav-muted-text:#D1D5DB;
        --nav-panel-bg:rgba(17,24,39,0.88);
        --nav-panel-border:rgba(229,231,235,0.18);
        --nav-link-text:#F3F4F6;
        --nav-link-hover-bg:rgba(96,165,250,0.16);
        --nav-filter-text:#F9FAFB;
        --nav-input-bg:#111827;
        --nav-input-text:#F9FAFB;
        --nav-placeholder:#D1D5DB;
        --nav-expander-bg:rgba(15,23,42,0.92);
    }
}

/* ==========================================================
   Sidebar menu title and caption
   ========================================================== */
section[data-testid="stSidebar"] .sidebar-nav-title{
    font-size:18px;
    font-weight:800;
    margin-top:4px;
    margin-bottom:6px;
    letter-spacing:0.2px;
    color:var(--nav-title-text) !important;
}

section[data-testid="stSidebar"] .sidebar-nav-caption{
    font-size:12px;
    color:var(--nav-muted-text) !important;
    margin-bottom:10px;
    line-height:1.35;
}

/* ==========================================================
   Expander group headings
   ========================================================== */
section[data-testid="stSidebar"] details{
    background:var(--nav-expander-bg) !important;
    border:1px solid var(--nav-panel-border) !important;
    border-radius:10px !important;
    margin-bottom:8px !important;
}

section[data-testid="stSidebar"] details summary,
section[data-testid="stSidebar"] details summary *,
section[data-testid="stSidebar"] details p{
    color:var(--nav-title-text) !important;
    font-weight:700 !important;
}

/* ==========================================================
   Page links
   ========================================================== */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a *,
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] *{
    color:var(--nav-link-text) !important;
    text-decoration:none !important;
    font-weight:600 !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover{
    background:var(--nav-link-hover-bg) !important;
    border-radius:8px !important;
}

/* ==========================================================
   Filter title and multiselect visibility
   Fixes "Choose options" readability in dark mode.
   ========================================================== */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label *,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *{
    color:var(--nav-filter-text) !important;
}

/* Multiselect/select control */
section[data-testid="stSidebar"] [data-baseweb="select"] > div{
    background-color:var(--nav-input-bg) !important;
    color:var(--nav-input-text) !important;
    border-color:var(--nav-panel-border) !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] input,
section[data-testid="stSidebar"] [data-baseweb="select"] div,
section[data-testid="stSidebar"] [data-baseweb="select"] span{
    color:var(--nav-input-text) !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] input::placeholder{
    color:var(--nav-placeholder) !important;
    opacity:1 !important;
}

/* Dropdown menu items */
div[data-baseweb="popover"] *,
ul[role="listbox"] *,
li[role="option"] *{
    color:var(--nav-input-text) !important;
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

    def is_group(group_pages):

        return current_page in group_pages

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

    st.sidebar.markdown(
        "<div class='sidebar-nav-title'>▦ Dashboard Menu</div>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "<div class='sidebar-nav-caption'>Grouped pages are shown below. Open a section to move across the dashboard.</div>",
        unsafe_allow_html=True
    )

    with st.sidebar.expander(
        "▤ Executive Overview",
        expanded=is_group(executive_pages)
    ):

        page_link(
            "Executive Dashboard.py",
            "▦ Executive Dashboard"
        )

        page_link(
            "pages/01_Respondent_Profile.py",
            "☷ Respondent Profile"
        )

    with st.sidebar.expander(
        "◇ Maturity Analysis",
        expanded=is_group(maturity_pages)
    ):

        page_link(
            "pages/02_Data_Maturity_Analysis.py",
            "◈ Data Maturity Analysis"
        )

        page_link(
            "pages/03_Forecasting_Maturity.py",
            "⌁ Forecasting Maturity Analysis"
        )

        page_link(
            "pages/04_Reconstruction_Readiness.py",
            "▱ Reconstruction Readiness Analysis"
        )

        page_link(
            "pages/05_Digital_Readiness.py",
            "◌ Digital Readiness Analysis"
        )

    with st.sidebar.expander(
        "⊞ Question Analytics",
        expanded=is_group(question_pages)
    ):

        page_link(
            "pages/06_Data_Practices_Questions.py",
            "☰ Data Practices Questions"
        )

        page_link(
            "pages/07_Forecasting_Questions.py",
            "⌕ Forecasting Questions"
        )

        page_link(
            "pages/08_Reconstruction_and_Modelling_Questions.py",
            "◇ Reconstruction & Modelling Questions"
        )

        page_link(
            "pages/09_Digital_Readiness_Questions.py",
            "◍ Digital Readiness Questions"
        )

    with st.sidebar.expander(
        "✧ Strategic Insights",
        expanded=is_group(strategic_pages)
    ):

        page_link(
            "pages/10_Open_Ended_Insights.py",
            "◆ Open Ended Insights"
        )

        page_link(
            "pages/11_Benchmarking_and_Gap_Analysis.py",
            "▧ Benchmarking & Gap Analysis"
        )

        page_link(
            "pages/12_Strategic_Roadmap.py",
            "⌂ Strategic Roadmap"
        )

        page_link(
            "pages/13_Key_Findings_and_Recommendations.py",
            "★ Key Findings & Recommendations"
        )

    st.sidebar.divider()
