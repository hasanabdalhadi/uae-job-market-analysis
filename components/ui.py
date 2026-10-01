# ============================================================
# HJMI 2.0 — REUSABLE UI COMPONENTS
# Hasan Job Market Intelligence
# ============================================================

import html
import streamlit as st


# ============================================================
# HELPERS
# ============================================================

def safe(value, fallback="Not specified"):
    """Escape dynamic text before rendering it as HTML."""

    if value is None:
        return fallback

    text = str(value).strip()

    if not text or text.lower() in {
        "nan",
        "none",
        "null",
        "n/a",
    }:
        return fallback

    return html.escape(text)


def safe_url(value):
    """Allow only normal web URLs for clickable links."""

    if value is None:
        return None

    url = str(value).strip()

    if url.startswith("https://") or url.startswith("http://"):
        return html.escape(url, quote=True)

    return None


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(title, description=None, icon=None):
    """Reusable section heading."""

    icon_html = f"{safe(icon)} " if icon else ""

    description_html = ""

    if description:
        description_html = f"""
        <div style="
            color:#70859a;
            font-size:12px;
            line-height:1.7;
            margin-top:5px;
            max-width:900px;
        ">
            {safe(description)}
        </div>
        """

    st.html(
        f"""
        <div style="margin:34px 0 17px 0;">

            <div style="
                color:#ffffff;
                font-size:22px;
                font-weight:760;
                letter-spacing:-0.02em;
            ">
                {icon_html}{safe(title)}
            </div>

            {description_html}

        </div>
        """
    )


# ============================================================
# INFORMATION BOX
# ============================================================

def info_box(title, text, icon="ⓘ"):
    """Explain a metric, feature, chart or definition."""

    st.html(
        f"""
        <div class="hjmi-explainer">

            <strong>
                {safe(icon)} {safe(title)}
            </strong>

            <br>

            {safe(text)}

        </div>
        """
    )


# ============================================================
# MARKET METRIC
# ============================================================

def market_metric(icon, label, value, explanation=""):
    """Render one HJMI market metric."""

    st.html(
        f"""
        <div class="hjmi-metric">

            <div class="hjmi-metric-top">

                <div class="hjmi-metric-icon">
                    {safe(icon)}
                </div>

                <div
                    class="hjmi-info"
                    title="{safe(explanation)}"
                >
                    ⓘ
                </div>

            </div>

            <div class="hjmi-metric-label">
                {safe(label)}
            </div>

            <div class="hjmi-metric-value">
                {safe(value)}
            </div>

            <div class="hjmi-metric-note">
                {safe(explanation)}
            </div>

        </div>
        """
    )


# ============================================================
# BADGES
# ============================================================

def badge(text, badge_type="active"):
    """Return reusable HJMI badge HTML."""

    allowed_types = {
        "active",
        "new",
        "graduate",
        "verified",
    }

    if badge_type not in allowed_types:
        badge_type = "active"

    return (
        f'<span class="hjmi-badge '
        f'hjmi-badge-{badge_type}">'
        f'{safe(text)}'
        f'</span>'
    )


def job_status_badge(status):
    """Return the appropriate job status badge."""

    status = str(status).strip()

    if status == "New Opportunity":
        return badge(
            "🆕 New Opportunity",
            "new",
        )

    if status == "Active":
        return badge(
            "● Active",
            "active",
        )

    return (
        '<span class="hjmi-badge" '
        'style="'
        'color:#9aaabd;'
        'background:rgba(148,163,184,0.08);'
        'border:1px solid rgba(148,163,184,0.15);'
        '">'
        'Historical'
        '</span>'
    )


# ============================================================
# JOB CARD
# ============================================================

def job_card(row, show_description=False):
    """
    Render a professional HJMI job opportunity card.

    Expected row fields come from services/data_service.py.
    """

    title = safe(
        row.get("job_title_display"),
        "Job title not specified",
    )

    company = safe(
        row.get("company_display"),
        "Company not specified",
    )

    location = safe(
        row.get("location_display"),
        "UAE location not specified",
    )

    experience = safe(
        row.get("experience_display"),
        "Not specified",
    )

    salary = safe(
        row.get("salary_display"),
        "To be discussed after the interview",
    )

    skills = safe(
        row.get("skills"),
        "Skills not specified",
    )

    status = row.get(
        "job_status",
        "Historical",
    )

    publication_date = safe(
        row.get("publication_date_display"),
        "Not available",
    )

    first_seen = safe(
        row.get("first_seen_display"),
        "Not available",
    )

    job_url = safe_url(
        row.get("job_url")
    )

    graduate_friendly = bool(
        row.get(
            "fresh_graduate_friendly",
            False,
        )
    )

    description_html = ""

    if show_description:

        description = safe(
            row.get("description"),
            "No description available.",
        )

        if len(description) > 650:
            description = (
                description[:650].rstrip()
                + "..."
            )

        description_html = f"""
        <div style="
            margin-top:16px;
            padding-top:14px;
            border-top:1px solid rgba(148,163,184,0.10);
            color:#8fa3b6;
            font-size:11px;
            line-height:1.75;
        ">
            {description}
        </div>
        """

    graduate_badge = ""

    if graduate_friendly:
        graduate_badge = badge(
            "🎓 Fresh Graduate Friendly",
            "graduate",
        )

    apply_html = ""

    if job_url:
        apply_html = f"""
        <a
            href="{job_url}"
            target="_blank"
            rel="noopener noreferrer"
            style="
                text-decoration:none;
                color:#f2d58b;
                font-size:11px;
                font-weight:700;
                padding:9px 14px;
                border-radius:10px;
                border:1px solid rgba(216,173,87,0.25);
                background:rgba(216,173,87,0.08);
            "
        >
            View Opportunity ↗
        </a>
        """

    st.html(
        f"""
        <div class="hjmi-job-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:20px;
                flex-wrap:wrap;
            ">

                <div style="
                    flex:1;
                    min-width:240px;
                ">

                    <div class="hjmi-job-title">
                        {title}
                    </div>

                    <div class="hjmi-job-company">
                        {company}
                    </div>

                </div>

                <div style="
                    display:flex;
                    gap:7px;
                    flex-wrap:wrap;
                    justify-content:flex-end;
                ">
                    {job_status_badge(status)}
                    {graduate_badge}
                </div>

            </div>

            <div class="hjmi-job-meta">

                <div class="hjmi-job-tag">
                    📍 {location}
                </div>

                <div class="hjmi-job-tag">
                    💼 {experience}
                </div>

                <div class="hjmi-job-tag">
                    💰 {salary}
                </div>

            </div>

            <div style="
                margin-top:14px;
                color:#8398aa;
                font-size:11px;
                line-height:1.65;
            ">
                <strong style="color:#aab9c6;">
                    Skills:
                </strong>
                {skills}
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:15px;
                flex-wrap:wrap;
                margin-top:17px;
            ">

                <div style="
                    color:#60778c;
                    font-size:10px;
                    line-height:1.6;
                ">
                    Published: {publication_date}
                    &nbsp; • &nbsp;
                    First seen by HJMI: {first_seen}
                </div>

                {apply_html}

            </div>

            {description_html}

        </div>
        """
    )


# ============================================================
# EMPTY STATE
# ============================================================

def empty_state(
    title="No opportunities found",
    message=(
        "Try changing your filters or search terms "
        "to discover more opportunities."
    ),
    icon="⌕",
):
    """Render a polished empty state."""

    st.html(
        f"""
        <div style="
            text-align:center;
            padding:55px 25px;
            border-radius:20px;
            border:1px solid rgba(148,163,184,0.13);
            background:rgba(8,29,44,0.55);
            margin:18px 0;
        ">

            <div style="
                font-size:34px;
                margin-bottom:12px;
            ">
                {safe(icon)}
            </div>

            <div style="
                color:#ffffff;
                font-size:17px;
                font-weight:700;
            ">
                {safe(title)}
            </div>

            <div style="
                color:#70859a;
                font-size:12px;
                margin-top:7px;
                line-height:1.7;
            ">
                {safe(message)}
            </div>

        </div>
        """
    )


# ============================================================
# INSIGHT CARD
# ============================================================

def insight_card(icon, title, value, description):
    """Render a market insight card."""

    st.html(
        f"""
        <div class="hjmi-card">

            <div style="
                font-size:24px;
                margin-bottom:12px;
            ">
                {safe(icon)}
            </div>

            <div class="hjmi-card-title">
                {safe(title)}
            </div>

            <div style="
                color:#f2d58b;
                font-size:23px;
                font-weight:800;
                margin-top:7px;
            ">
                {safe(value)}
            </div>

            <div class="hjmi-card-subtitle">
                {safe(description)}
            </div>

        </div>
        """
    )


# ============================================================
# FEATURE CARD
# ============================================================

def feature_card(icon, title, description, label=None):
    """Render cards used for HJMI platform features."""

    label_html = ""

    if label:
        label_html = f"""
        <div style="
            display:inline-block;
            margin-top:14px;
            padding:5px 9px;
            border-radius:999px;
            color:#f2d58b;
            background:rgba(216,173,87,0.08);
            border:1px solid rgba(216,173,87,0.16);
            font-size:9px;
            font-weight:700;
        ">
            {safe(label)}
        </div>
        """

    st.html(
        f"""
        <div class="hjmi-card"
             style="min-height:185px;">

            <div style="
                font-size:28px;
                margin-bottom:15px;
            ">
                {safe(icon)}
            </div>

            <div class="hjmi-card-title">
                {safe(title)}
            </div>

            <div class="hjmi-card-subtitle">
                {safe(description)}
            </div>

            {label_html}

        </div>
        """
    )


# ============================================================
# SALARY DISPLAY
# ============================================================

def salary_notice():
    """Explain HJMI salary presentation."""

    info_box(
        "How salary information works",
        (
            "HJMI displays salary information when it is available "
            "in the source listing. When an employer does not provide "
            "a salary, HJMI does not invent or estimate one; the "
            "opportunity is displayed as 'To be discussed after the "
            "interview'."
        ),
        "💰",
    )


# ============================================================
# DATA STATUS
# ============================================================

def data_status(last_update):
    """Render latest market data status."""

    st.html(
        f"""
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;
            flex-wrap:wrap;
            padding:13px 16px;
            margin:12px 0 23px 0;
            border-radius:13px;
            background:rgba(0,168,107,0.055);
            border:1px solid rgba(0,168,107,0.13);
        ">

            <div style="
                color:#a9bdcb;
                font-size:10px;
            ">
                <span style="color:#69d5a5;">
                    ●
                </span>

                HJMI Market Data
            </div>

            <div style="
                color:#667f92;
                font-size:10px;
            ">
                Last update:
                {safe(last_update)}
            </div>

        </div>
        """
    )


# ============================================================
# RESULT COUNT
# ============================================================

def result_count(count, label="opportunities"):
    """Show number of matching results."""

    st.html(
        f"""
        <div style="
            color:#7d92a5;
            font-size:11px;
            margin:8px 0 15px 0;
        ">
            Showing
            <strong style="color:#f2d58b;">
                {safe(count)}
            </strong>
            {safe(label)}
        </div>
        """
    )


# ============================================================
# DEVELOPMENT LABEL
# ============================================================

def coming_soon(title, description):
    """Placeholder for later HJMI platform modules."""

    st.html(
        f"""
        <div class="hjmi-card"
             style="
                text-align:center;
                padding:50px 25px;
             ">

            <div style="
                color:#d8ad57;
                font-size:10px;
                font-weight:800;
                letter-spacing:3px;
            ">
                HJMI PLATFORM DEVELOPMENT
            </div>

            <div style="
                color:white;
                font-size:22px;
                font-weight:750;
                margin-top:10px;
            ">
                {safe(title)}
            </div>

            <div style="
                color:#70859a;
                font-size:12px;
                line-height:1.7;
                max-width:650px;
                margin:10px auto 0 auto;
            ">
                {safe(description)}
            </div>

        </div>
        """
    )
