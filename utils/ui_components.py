# ==========================================================
# SHARED UI COMPONENTS
# Professional Research Analytics Dashboard Theme
#
# Save this file as:
# utils/ui_components.py
# ==========================================================

import html
import streamlit as st


def _safe(value):
    """Safely convert any value to escaped text for HTML rendering."""
    return html.escape(str(value))


def apply_dashboard_theme():
    """
    Applies the shared dashboard shell/theme.
    Call this after st.set_page_config() and after any page-specific CSS.
    """

    st.markdown(
        """
<style>

/* ==========================================================
   STREAMLIT HEADER / WHITE STRIP FIX
   ========================================================== */

html, body, [data-testid="stAppViewContainer"] {
    background: #07111F !important;
}

header[data-testid="stHeader"] {
    background: #07111F !important;
}

div[data-testid="stToolbar"] {
    visibility: hidden !important;
    height: 0rem !important;
    position: fixed !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

/* ==========================================================
   GLOBAL APP SHELL
   ========================================================== */

.stApp {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.16), transparent 26%),
        radial-gradient(circle at top right, rgba(217,119,6,0.12), transparent 24%),
        linear-gradient(180deg, #07111F 0%, #0B1220 42%, #0F172A 100%);
    color: #E5E7EB;
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 3rem;
    max-width: 1480px;
}

/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111F 0%, #0B1220 100%);
    border-right: 1px solid rgba(148,163,184,0.20);
}

section[data-testid="stSidebar"] * {
    color: #CBD5E1;
}

/* ==========================================================
   TYPOGRAPHY
   ========================================================== */

h1, h2, h3, h4 {
    color: #F8FAFC;
    letter-spacing: -0.02em;
}

p, li, span, label {
    color: #CBD5E1;
}

hr {
    border-color: rgba(148,163,184,0.20);
}

/* ==========================================================
   TOP STATUS BAR
   ========================================================== */

.dashboard-topbar {
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    gap:12px;
    padding:12px 14px;
    border:1px solid rgba(148,163,184,0.22);
    border-radius:16px;
    background:rgba(15,23,42,0.90);
    box-shadow:0 12px 32px rgba(0,0,0,0.22);
    margin-bottom:16px;
}

.dashboard-topbar-left {
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    align-items:center;
    flex:1;
}

.dashboard-chip {
    display:inline-flex;
    align-items:center;
    gap:7px;
    padding:7px 10px;
    border-radius:999px;
    background:rgba(30,41,59,0.94);
    border:1px solid rgba(148,163,184,0.24);
    font-size:13px;
    font-weight:600;
    color:#E2E8F0;
    white-space:nowrap;
}

.dashboard-chip strong {
    color:#FFFFFF;
}

.dashboard-actions {
    display:flex;
    gap:8px;
    align-items:center;
    flex-shrink:0;
}

.dashboard-action {
    width:34px;
    height:34px;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    border-radius:10px;
    background:rgba(30,41,59,0.94);
    border:1px solid rgba(148,163,184,0.25);
    color:#E5E7EB;
    font-size:15px;
}

/* ==========================================================
   HERO
   ========================================================== */

.hero-badge {
    background:rgba(217,119,6,0.12) !important;
    border:1px solid rgba(217,119,6,0.65) !important;
    color:#FDBA74 !important;
    box-shadow:0 0 0 4px rgba(217,119,6,0.08);
}

.hero-title {
    color:#F8FAFC !important;
    text-shadow:0 18px 45px rgba(0,0,0,0.35);
}

.hero-subtitle {
    color:#FDBA74 !important;
}

.hero-description {
    color:#CBD5E1 !important;
}

/* ==========================================================
   BADGES AND STORY STRIP
   ========================================================== */

.badge-row {
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    justify-content:center;
    margin-top:14px;
    margin-bottom:10px;
}

.status-badge {
    display:inline-flex;
    align-items:center;
    gap:7px;
    padding:7px 11px;
    border-radius:999px;
    font-size:12px;
    font-weight:800;
    letter-spacing:0.04em;
    color:#E5E7EB;
    background:rgba(30,41,59,0.92);
    border:1px solid rgba(148,163,184,0.22);
}

.status-badge.blue {
    border-color:rgba(37,99,235,0.65);
    color:#BFDBFE;
}

.status-badge.green {
    border-color:rgba(5,150,105,0.65);
    color:#BBF7D0;
}

.status-badge.amber {
    border-color:rgba(217,119,6,0.65);
    color:#FED7AA;
}

.status-badge.purple {
    border-color:rgba(124,58,237,0.65);
    color:#DDD6FE;
}

.story-strip {
    display:grid;
    grid-template-columns: repeat(3, 1fr);
    gap:12px;
    margin:18px 0 18px 0;
}

.story-item {
    padding:14px 16px;
    border-radius:16px;
    background:rgba(15,23,42,0.82);
    border:1px solid rgba(148,163,184,0.22);
}

.story-label {
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:0.10em;
    color:#94A3B8;
    font-weight:800;
    margin-bottom:6px;
}

.story-value {
    color:#F8FAFC;
    font-weight:700;
    line-height:1.35;
}

/* ==========================================================
   CARDS, METRICS AND WIDGETS
   ========================================================== */

div[data-testid="metric-container"] {
    background:rgba(15,23,42,0.86) !important;
    border:1px solid rgba(148,163,184,0.22) !important;
    border-radius:18px !important;
    box-shadow:0 12px 28px rgba(0,0,0,0.18);
}

div[data-testid="metric-container"] label,
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color:#94A3B8 !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color:#F8FAFC !important;
}

.scope-box,
.findings-box,
.note-box,
.theme-highlight-box {
    background:rgba(15,23,42,0.82) !important;
    border:1px solid rgba(148,163,184,0.22) !important;
    color:#CBD5E1 !important;
    box-shadow:0 12px 28px rgba(0,0,0,0.18);
}

.scope-box h3,
.findings-box h4,
.note-box b,
.theme-highlight-box b {
    color:#F8FAFC !important;
}

.findings-box {
    border-left:6px solid #F59E0B !important;
}

.note-box {
    border-left:5px solid #2563EB !important;
}

.theme-highlight-box {
    border-left:5px solid #7C3AED !important;
}

.section-title {
    color:#F8FAFC !important;
    font-size:28px !important;
    font-weight:800 !important;
    margin-top:34px !important;
    margin-bottom:16px !important;
    padding:12px 14px;
    border-left:5px solid #38BDF8;
    border-radius:12px;
    background:rgba(15,23,42,0.68);
    border-top:1px solid rgba(148,163,184,0.18);
    border-bottom:1px solid rgba(148,163,184,0.12);
}

.stPlotlyChart {
    border:1px solid rgba(148,163,184,0.20);
    border-radius:18px;
    padding:10px;
    background:rgba(15,23,42,0.70);
    box-shadow:0 12px 28px rgba(0,0,0,0.15);
}

[data-testid="stDataFrame"] {
    border:1px solid rgba(148,163,184,0.20);
    border-radius:16px;
    overflow:hidden;
}

[data-testid="stAlert"] {
    border-radius:16px;
    border:1px solid rgba(148,163,184,0.22);
}

/* ==========================================================
   RESPONSIVE
   ========================================================== */

@media (max-width: 900px) {
    .dashboard-topbar {
        flex-direction:column;
        align-items:flex-start;
    }

    .story-strip {
        grid-template-columns:1fr;
    }
}

</style>
""",
        unsafe_allow_html=True
    )


def render_top_status_bar(
    items=None,
    dataset_status="Interim Dataset",
    responses=None,
    agencies=None,
    theme_framework="Aligned",
    refresh_status="Final Refresh Pending",
    show_actions=True
):
    """
    Render a flexible top status bar.

    Supports BOTH formats:

    1. New format:
       render_top_status_bar([
           ("📦", "Dataset", "Interim Dataset"),
           ("👥", "Responses", 81)
       ])

    2. Old format:
       render_top_status_bar(
           dataset_status="Interim Dataset",
           responses=81,
           agencies=5
       )
    """

    if items is None:
        response_text = "N/A" if responses is None else responses
        agency_text = "N/A" if agencies is None else agencies

        items = [
            ("📦", "Dataset", dataset_status),
            ("👥", "Responses", response_text),
            ("🏢", "Agencies", agency_text),
            ("🧩", "Themes", theme_framework),
            ("🔄", "Status", refresh_status)
        ]

    chip_html = ""

    for item in items:
        if len(item) == 3:
            icon, label, value = item
        else:
            icon, label, value = "•", "Item", item

        chip_html += (
            '<div class="dashboard-chip">'
            f'{_safe(icon)} {_safe(label)}: '
            f'<strong>{_safe(value)}</strong>'
            '</div>'
        )

    actions_html = ""

    if show_actions:
        actions_html = """
<div class="dashboard-actions">
    <div class="dashboard-action" title="Settings">⚙</div>
    <div class="dashboard-action" title="Refresh pending">↻</div>
    <div class="dashboard-action" title="Export ready">⇩</div>
    <div class="dashboard-action" title="Method notes">ⓘ</div>
</div>
"""

    st.markdown(
        f"""
<div class="dashboard-topbar">
    <div class="dashboard-topbar-left">
        {chip_html}
    </div>
    {actions_html}
</div>
""",
        unsafe_allow_html=True
    )


def render_status_badges(badges):
    """
    badges can be a list of strings or tuples: ("TEXT", "blue")
    supported colours: blue, green, amber, purple
    """

    badge_html = ""
    colour_cycle = ["blue", "green", "amber", "purple"]

    for i, badge in enumerate(badges):
        if isinstance(badge, tuple):
            text, colour = badge
        else:
            text = badge
            colour = colour_cycle[i % len(colour_cycle)]

        badge_html += (
            f'<span class="status-badge {_safe(colour)}">'
            f'{_safe(text)}</span>'
        )

    st.markdown(
        f'<div class="badge-row">{badge_html}</div>',
        unsafe_allow_html=True
    )


def render_story_strip(domain, evidence, decision_use):
    st.markdown(
        f"""
<div class="story-strip">
    <div class="story-item">
        <div class="story-label">Research Domain</div>
        <div class="story-value">{_safe(domain)}</div>
    </div>
    <div class="story-item">
        <div class="story-label">Evidence Base</div>
        <div class="story-value">{_safe(evidence)}</div>
    </div>
    <div class="story-item">
        <div class="story-label">Decision Use</div>
        <div class="story-value">{_safe(decision_use)}</div>
    </div>
</div>
""",
        unsafe_allow_html=True
    )
