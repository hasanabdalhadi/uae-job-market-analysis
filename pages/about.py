# ============================================================
# HJMI 2.0 — ABOUT & METHODOLOGY
# Hasan Job Market Intelligence
# ============================================================

import streamlit as st

from components.theme import (
    apply_theme,
    brand,
    page_header,
    footer,
)

from components.ui import (
    section_header,
    info_box,
    insight_card,
    data_status,
)

from services.data_service import (
    load_jobs,
    get_market_metrics,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="About & Methodology | HJMI",
    page_icon="ⓘ",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.45rem;
        padding-bottom: 2.2rem;
        max-width: 1450px;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.65rem;
    }

    .hjmi-method-card {
        height: 100%;
        padding: 17px 18px;
        border-radius: 16px;
        border: 1px solid rgba(148,163,184,0.12);
        background: linear-gradient(145deg, rgba(12,42,51,0.76), rgba(8,29,38,0.82));
    }

    .hjmi-method-step {
        color: #d8ad57;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 7px;
    }

    .hjmi-method-title {
        color: #f3f6f7;
        font-size: 14px;
        font-weight: 760;
        margin-bottom: 6px;
    }

    .hjmi-method-copy {
        color: #7f95a3;
        font-size: 10px;
        line-height: 1.65;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

df = load_jobs()
metrics = get_market_metrics(df) if not df.empty else None


# ============================================================
# HEADER
# ============================================================

page_header(
    "TRANSPARENT • DATA-DRIVEN • UAE FOCUSED",
    "About HJMI & Methodology",
    (
        "How Hasan Job Market Intelligence collects, structures and "
        "interprets UAE technology opportunity data."
    ),
)

if metrics:
    data_status(metrics["last_update"])


# ============================================================
# ABOUT
# ============================================================

section_header(
    "What is HJMI?",
    "A UAE-focused technology career and job-market intelligence platform.",
    "H",
)

info_box(
    "Hasan Job Market Intelligence",
    (
        "HJMI is developed by Hasan R. H. Abdalhadi. It combines job "
        "discovery with structured intelligence about roles, skills, "
        "locations, experience, graduate opportunities and salary disclosure, "
        "along with personal career tools such as profiles, recommendations, "
        "saved opportunities, application tracking and in-app alerts."
    ),
    "H",
)

mission_cols = st.columns(3)

with mission_cols[0]:
    insight_card(
        "1", "Discover", "Opportunities",
        "Explore technology opportunities represented in HJMI's latest UAE dataset."
    )

with mission_cols[1]:
    insight_card(
        "2", "Understand", "The Market",
        "Turn collected records into understandable signals about roles, skills and requirements."
    )

with mission_cols[2]:
    insight_card(
        "3", "Personalize", "Your Search",
        "Use career-profile information to compare your profile with structured HJMI job data."
    )


# ============================================================
# DATA SOURCE & PIPELINE
# ============================================================

section_header(
    "Data Source & Pipeline",
    "How external opportunity records become HJMI intelligence.",
    "⚙",
)

info_box(
    "Current external source: Jooble",
    (
        "HJMI currently uses the Jooble API as its external job-listing "
        "source. Results depend on configured UAE technology searches, "
        "Jooble's available coverage and HJMI's processing rules. HJMI "
        "does not claim to contain every technology vacancy in the UAE."
    ),
    "↗",
)

pipeline_cols = st.columns(4)

pipeline = [
    ("01", "Collect", "Request UAE technology opportunity records from the configured source."),
    ("02", "Normalize", "Organize titles, companies, locations, dates, salary text and source fields."),
    ("03", "Enrich", "Derive structured skills, experience and graduate-friendly signals."),
    ("04", "Analyze", "Use the processed dataset across discovery, intelligence and career tools."),
]

for col, (step, title, copy) in zip(pipeline_cols, pipeline):
    with col:
        st.markdown(
            f"""
            <div class="hjmi-method-card">
                <div class="hjmi-method-step">{step}</div>
                <div class="hjmi-method-title">{title}</div>
                <div class="hjmi-method-copy">{copy}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

info_box(
    "Automated updates",
    (
        "A scheduled GitHub Actions workflow retrieves current records, "
        "runs HJMI's preparation pipeline, validates the generated dataset "
        "and updates the repository when the data changes. The workflow is "
        "configured to run daily, although external API or workflow issues "
        "can affect individual updates."
    ),
    "↻",
)


# ============================================================
# DEFINITIONS
# ============================================================

section_header(
    "Core Data Definitions",
    "The most important labels to understand when reading HJMI.",
    "◇",
)

status_cols = st.columns(3)

with status_cols[0]:
    insight_card(
        "●", "Active", "Latest Collection",
        "The opportunity was returned in HJMI's latest collection."
    )

with status_cols[1]:
    insight_card(
        "✦", "New", "First Discovered",
        "HJMI first discovered the opportunity during the latest data update."
    )

with status_cols[2]:
    insight_card(
        "◷", "Historical", "Previously Observed",
        "The record is retained by HJMI but was not returned in the latest collection."
    )

info_box(
    "Observation states — not employer confirmations",
    (
        "Active does not independently guarantee that an employer is still "
        "accepting applications. Historical does not prove that a vacancy "
        "has closed. New means new to HJMI, not necessarily newly published "
        "by the employer."
    ),
    "ⓘ",
)


# ============================================================
# CLASSIFICATION METHODS
# ============================================================

section_header(
    "How HJMI Interprets Job Data",
    "Structured rules used to avoid unsupported assumptions.",
    "⚡",
)

method_tabs = st.tabs(
    ["Experience", "Graduate Friendly", "Skills", "Salary", "Market Trends"]
)

with method_tabs[0]:
    st.markdown(
        """
        HJMI looks for recognizable experience signals in the available
        job title and description and organizes them into descriptive
        categories such as **Fresh Graduate / Entry Level**, **0–1 Year**,
        **1–2 Years**, **2–3 Years**, **3–5 Years**, **5+ Years** and
        **Not Specified**.

        If no recognizable experience requirement is found, HJMI keeps the
        record as **Not Specified** rather than estimating a requirement.
        """
    )

with method_tabs[1]:
    st.markdown(
        """
        HJMI classifies a listing as graduate-friendly only when the
        available text contains an explicit early-career signal such as
        **fresh graduate**, **entry level**, **graduate trainee**,
        **no experience required**, or an experience requirement beginning
        at zero.

        A listing that is not classified as graduate-friendly may still
        accept graduates. Missing experience information alone is not enough
        for HJMI to classify it as graduate-friendly.
        """
    )

with method_tabs[2]:
    st.markdown(
        """
        HJMI extracts and organizes identifiable technology skills from
        processed opportunity records. Structured skill fields power skill
        intelligence, job matching and profile comparisons.

        A technology can still be relevant even when it is not present in
        HJMI's structured skill field, and different listings may use
        different names for similar technologies.
        """
    )

with method_tabs[3]:
    st.markdown(
        """
        HJMI treats salary as disclosed only when salary information is
        available in the collected source record. Missing salary is **not
        estimated**.

        The interface may display **"To be discussed after the interview"**
        as an HJMI presentation convention for missing salary information;
        this is not presented as employer-provided wording.

        HJMI avoids unsupported market averages or medians while source
        salary text is not normalized into directly comparable values.
        """
    )

with method_tabs[4]:
    st.markdown(
        """
        A single current snapshot is not treated as evidence that a role,
        skill, location or graduate market is rising or falling. Reliable
        trend claims require comparable observations collected consistently
        over time.

        HJMI retains fields such as first-seen, last-seen and opportunity
        status so its historical analysis can become stronger as the dataset
        grows.
        """
    )


# ============================================================
# CAREER INTELLIGENCE
# ============================================================

section_header(
    "Personal Career Intelligence",
    "What HJMI personalization means — and what it does not mean.",
    "🎯",
)

career_cols = st.columns(3)

with career_cols[0]:
    insight_card(
        "⚡", "Profile Match", "Structured Overlap",
        "Compares profile skills, role, specialization, experience and location with HJMI job data."
    )

with career_cols[1]:
    insight_card(
        "◇", "Recommendations", "Relevant Records",
        "Surfaces opportunities whose structured data overlaps with the user's career profile."
    )

with career_cols[2]:
    insight_card(
        "!", "Not a Hiring Score", "No Outcome Prediction",
        "HJMI match results do not represent employer interest, acceptance probability or hiring likelihood."
    )


# ============================================================
# INTEGRITY & LIMITATIONS
# ============================================================

section_header(
    "Data Integrity & Limitations",
    "Important context for interpreting HJMI analysis responsibly.",
    "✓",
)

integrity_cols = st.columns(3)

with integrity_cols[0]:
    insight_card(
        "✓", "No Invented", "Job Facts",
        "Missing salary, experience or other information is not silently replaced with unsupported values."
    )

with integrity_cols[1]:
    insight_card(
        "✓", "Clear", "Definitions",
        "HJMI documents the meaning of important platform labels and classifications."
    )

with integrity_cols[2]:
    insight_card(
        "✓", "Visible", "Limitations",
        "Dataset observations are separated from conclusions that would require broader evidence."
    )

with st.expander("View platform limitations", expanded=False):
    st.markdown(
        """
        - HJMI does not contain every technology job in the UAE.
        - External source coverage and behavior can change.
        - Search configuration affects which opportunities are returned.
        - Job descriptions can be incomplete or inconsistent.
        - Company, role and location naming can vary across source records.
        - Structured skills depend on what HJMI can identify from available data.
        - Salary information is frequently missing or inconsistently formatted.
        - Active and Historical are HJMI observation states, not employer confirmations.
        - Long-term trend analysis becomes more meaningful as comparable historical data grows.
        """
    )


# ============================================================
# AUTHOR / USE
# ============================================================

section_header(
    "Project & Use",
    "Independent development, transparent interpretation and responsible use.",
    "H",
)

author_cols = st.columns(2)

with author_cols[0]:
    info_box(
        "Project Author",
        (
            "HJMI is an independent project by Hasan R. H. Abdalhadi, "
            "a Computer Science Engineering student at BITS Pilani – Dubai Campus. "
            "The project combines software development, data analysis, "
            "information systems and digital product development."
        ),
        "H",
    )

with author_cols[1]:
    info_box(
        "Verify before applying",
        (
            "Users should review the original opportunity source and employer "
            "information before applying or making a career decision. HJMI "
            "does not guarantee vacancy availability, employer decisions, "
            "salary, interviews or hiring outcomes."
        ),
        "ⓘ",
    )

footer()
