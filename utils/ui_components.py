# ==========================================================
# SHARED UI COMPONENTS
# Professional Research Analytics Dashboard Theme
# ==========================================================

import html
import streamlit as st


def apply_dashboard_theme():
    """
    Applies a reusable dashboard shell/theme across pages.
    Place this near the top of every Streamlit page after st.set_page_config().
    """

    st.markdown(
        """
<style>

/* GLOBAL APP SHELL */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.16), transparent 26%),
        radial-gradient(circle at top right, rgba(217,119,6,0.12), transparent 24%),
        linear-gradient(180deg, #07111F 0%, #0B1220 42%, #0F172A 100%);
    color: #E5E7EB;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1480px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111F 0%, #0B1220 100%);
    border-right: 1px solid rgba(148,163,184,0.20);
}

section[data-testid="stSidebar"] * {
    color: #CBD5E1;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #CBD5E1;
}

/* TYPOGRAPHY */
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

/* TOP STATUS BAR */
.dashboard-topbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    padding:12px 14px;
    border:1px solid rgba(148,163,184,0.22);
    border-radius:16px;
    background:rgba(15,23,42,0.86);
    box-shadow:0 12px 32px rgba(0,0,0,0.22);
    margin-bottom:16px;
}

.dashboard-topbar-left {
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    align-items:center;
}

.dashboard-chip {
    display:inline-flex;
    align-items:center;
    gap:7px;
    padding:7px 10px;
    border-radius:999px;
    background:rgba(30,41,59,0.92);
    border:1px solid rgba(148,163,184,0.22);
    font-size:13px;
    font-weight:600;
    color:#E2E8F0;
}

.dashboard-chip strong {
    color:#FFFFFF;
}

.dashboard-actions {
    display:flex;
    gap:8px;
    align-items:center;
}

.dashboard-action {
    width:34px;
    height:34px;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    border-radius:10px;
    background:rgba(30,41,59,0.90);
    border:1px solid rgba(148,163,184,0.25);
    color:#E5E7EB;
    font-size:15px;
}

/* HERO */
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

/* BADGES AND STORY STRIP */
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

/* CARDS, METRICS AND WIDGETS */
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

/* ALERTS */
[data-testid="stAlert"] {
    border-radius:16px;
    border:1px solid rgba(148,163,184,0.22);
    background:rgba(15,23,42,0.78);
}

/* RESPONSIVE */
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
    dataset_status="Interim Dataset",
    responses=None,
    agencies=None,
    theme_framework="Aligned",
    refresh_status="Final Refresh Pending"
):
    response_text = "N/A" if responses is None else f"{responses}"
    agency_text = "N/A" if agencies is None else f"{agencies}"

    st.markdown(
        f"""
<div class="dashboard-topbar">
    <div class="dashboard-topbar-left">
        <div class="dashboard-chip">📦 Dataset: <strong>{html.escape(dataset_status)}</strong></div>
        <div class="dashboard-chip">👥 Responses: <strong>{html.escape(response_text)}</strong></div>
        <div class="dashboard-chip">🏢 Agencies: <strong>{html.escape(agency_text)}</strong></div>
        <div class="dashboard-chip">🧩 Themes: <strong>{html.escape(theme_framework)}</strong></div>
        <div class="dashboard-chip">🔄 Status: <strong>{html.escape(refresh_status)}</strong></div>
    </div>
    <div class="dashboard-actions">
        <div class="dashboard-action" title="Settings">⚙</div>
        <div class="dashboard-action" title="Refresh pending">↻</div>
        <div class="dashboard-action" title="Export ready">⇩</div>
        <div class="dashboard-action" title="Method notes">ⓘ</div>
    </div>
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
            f'<span class="status-badge {html.escape(colour)}">'
            f'{html.escape(str(text))}</span>'
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
        <div class="story-value">{html.escape(domain)}</div>
    </div>
    <div class="story-item">
        <div class="story-label">Evidence Base</div>
        <div class="story-value">{html.escape(evidence)}</div>
    </div>
    <div class="story-item">
        <div class="story-label">Decision Use</div>
        <div class="story-value">{html.escape(decision_use)}</div>
    </div>
</div>
""",
        unsafe_allow_html=True
    )
