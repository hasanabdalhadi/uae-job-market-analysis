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


# ============================================================
# DESIGN
# ============================================================

apply_theme()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    brand()

    st.markdown(
        """
        <div style="
            color:#d8ad57;
            font-size:9px;
            font-weight:800;
            letter-spacing:2px;
            margin:5px 0 10px 0;
        ">
            ABOUT HJMI
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:20px;
        ">
            Understand how HJMI collects, processes,
            classifies and presents UAE technology
            job-market information.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DATA
# ============================================================

df = load_jobs()

if not df.empty:
    metrics = get_market_metrics(df)
else:
    metrics = None


# ============================================================
# HEADER
# ============================================================

page_header(
    "TRANSPARENT • DATA-DRIVEN • UAE FOCUSED",
    "About HJMI & Methodology",
    (
        "How Hasan Job Market Intelligence transforms collected "
        "UAE technology job listings into structured career and "
        "market intelligence."
    ),
)


if metrics:
    data_status(metrics["last_update"])


# ============================================================
# WHAT IS HJMI
# ============================================================

section_header(
    "What is HJMI?",
    (
        "A technology career and job-market intelligence "
        "project focused on the United Arab Emirates."
    ),
    "◇",
)


info_box(
    "Hasan Job Market Intelligence",
    (
        "HJMI is a data-analysis platform developed by "
        "Hasan R. H. Abdalhadi. It collects technology job "
        "opportunity data, structures it, and transforms it into "
        "clear intelligence about roles, skills, locations, "
        "experience requirements, graduate opportunities and "
        "salary transparency."
    ),
    "H",
)


mission_cols = st.columns(3)


with mission_cols[0]:

    insight_card(
        "1",
        "Discover",
        "Opportunities",
        (
            "Help users explore technology job opportunities "
            "represented in HJMI's UAE dataset."
        ),
    )


with mission_cols[1]:

    insight_card(
        "2",
        "Understand",
        "The Market",
        (
            "Turn collected job records into understandable "
            "signals about roles, skills and requirements."
        ),
    )


with mission_cols[2]:

    insight_card(
        "3",
        "Investigate",
        "Career Paths",
        (
            "Give students, graduates and professionals "
            "structured information they can use when "
            "researching career opportunities."
        ),
    )


# ============================================================
# DATA SOURCE
# ============================================================

section_header(
    "Data Source",
    (
        "Where HJMI currently obtains its external "
        "job-market records."
    ),
    "↗",
)


info_box(
    "Current external job source: Jooble",
    (
        "HJMI currently uses the Jooble API as its external "
        "job-listing data source. The automated collection process "
        "runs configured UAE technology searches and stores the "
        "returned records for further processing and analysis."
    ),
    "◇",
)


st.markdown(
    """
    **Current collection focus**

    - Software engineering and development
    - Data analysis, data science and data engineering
    - IT, cybersecurity, cloud, artificial intelligence
      and computer-science-related opportunities
    - United Arab Emirates
    """
)


info_box(
    "Coverage limitation",
    (
        "HJMI does not claim to contain every technology vacancy "
        "in the UAE. Results depend on the configured searches, "
        "the external source's coverage, returned records and "
        "HJMI's filtering process."
    ),
    "ⓘ",
)


# ============================================================
# DATA PIPELINE
# ============================================================

section_header(
    "How the Data Pipeline Works",
    (
        "The path from external job listings to "
        "HJMI intelligence."
    ),
    "⚙",
)


pipeline_cols = st.columns(4)


with pipeline_cols[0]:

    insight_card(
        "01",
        "Collect",
        "Job Records",
        (
            "HJMI requests UAE technology opportunity "
            "records from its configured external source."
        ),
    )


with pipeline_cols[1]:

    insight_card(
        "02",
        "Normalize",
        "The Data",
        (
            "Fields such as title, company, location, "
            "salary, dates and source information are "
            "organized into a consistent structure."
        ),
    )


with pipeline_cols[2]:

    insight_card(
        "03",
        "Enrich",
        "Market Signals",
        (
            "HJMI derives structured information such as "
            "skills, experience classifications and "
            "graduate-friendly indicators."
        ),
    )


with pipeline_cols[3]:

    insight_card(
        "04",
        "Analyze",
        "The Market",
        (
            "The processed dataset powers HJMI dashboards, "
            "filters, job exploration and intelligence views."
        ),
    )


# ============================================================
# AUTOMATION
# ============================================================

section_header(
    "Automated Updates",
    (
        "How HJMI keeps its dataset refreshed."
    ),
    "↻",
)


info_box(
    "Automated data workflow",
    (
        "HJMI uses an automated GitHub Actions workflow to run "
        "the data preparation pipeline on a scheduled basis. "
        "The workflow retrieves current records, processes the "
        "dataset, validates the generated output and updates "
        "the repository when the data changes."
    ),
    "⚙",
)


info_box(
    "Current schedule",
    (
        "The configured workflow is scheduled to run daily. "
        "External API availability, source behavior or workflow "
        "errors can affect whether a particular update succeeds."
    ),
    "◷",
)


# ============================================================
# STATUS DEFINITIONS
# ============================================================

section_header(
    "Opportunity Status Definitions",
    (
        "What HJMI means by Active, New and Historical."
    ),
    "◇",
)


status_cols = st.columns(3)


with status_cols[0]:

    insight_card(
        "●",
        "Active",
        "Latest Collection",
        (
            "The opportunity was returned in HJMI's "
            "latest collection process."
        ),
    )


with status_cols[1]:

    insight_card(
        "✦",
        "New",
        "First Discovered",
        (
            "HJMI first discovered the opportunity "
            "during the latest data update."
        ),
    )


with status_cols[2]:

    insight_card(
        "◷",
        "Historical",
        "Previously Observed",
        (
            "The opportunity is retained in HJMI's history "
            "but was not returned in the latest collection."
        ),
    )


info_box(
    "Important status limitation",
    (
        "Active does not independently guarantee that an employer "
        "is still accepting applications. Historical does not prove "
        "that a vacancy has been closed. These labels describe "
        "HJMI's observation of the source data."
    ),
    "ⓘ",
)


# ============================================================
# NEW DEFINITION
# ============================================================

section_header(
    "What Does 'New' Mean?",
    (
        "HJMI separates platform discovery time "
        "from employer publication time."
    ),
    "✦",
)


info_box(
    "New = new to HJMI",
    (
        "A New opportunity is a record that HJMI did not have "
        "in its previous stored dataset and discovered during "
        "the latest update. It does not necessarily mean the "
        "employer published the vacancy on that same day."
    ),
    "ⓘ",
)


# ============================================================
# EXPERIENCE
# ============================================================

section_header(
    "Experience Intelligence",
    (
        "How HJMI interprets experience requirements."
    ),
    "💼",
)


st.markdown(
    """
    HJMI searches the available job title and description for
    recognizable experience signals and organizes them into
    descriptive categories such as:

    - Fresh Graduate / Entry Level
    - 0–1 Year
    - 1–2 Years
    - 2–3 Years
    - 3–5 Years
    - 5+ Years
    - Not Specified
    """
)


info_box(
    "No invented experience requirement",
    (
        "When HJMI cannot identify a recognizable experience "
        "requirement from the available listing text, the record "
        "remains Not Specified rather than receiving an estimated "
        "experience level."
    ),
    "ⓘ",
)


# ============================================================
# GRADUATE CLASSIFICATION
# ============================================================

section_header(
    "Graduate-Friendly Classification",
    (
        "How HJMI identifies opportunities relevant "
        "to students and fresh graduates."
    ),
    "🎓",
)


info_box(
    "Graduate-friendly signals",
    (
        "HJMI looks for explicit early-career signals in the "
        "available listing text, such as fresh graduate, "
        "entry level, graduate trainee, no experience required "
        "or an experience requirement beginning at zero."
    ),
    "🎓",
)


info_box(
    "Classification limitation",
    (
        "A job that is not classified as graduate-friendly may "
        "still accept a fresh graduate. HJMI avoids automatically "
        "classifying every job with missing experience information "
        "as suitable for graduates."
    ),
    "ⓘ",
)


# ============================================================
# SKILLS
# ============================================================

section_header(
    "Skills Intelligence",
    (
        "How HJMI uses skill information."
    ),
    "⚡",
)


info_box(
    "Structured skill signals",
    (
        "HJMI extracts and organizes identified technology skills "
        "from the processed job records. These skills power analyses "
        "such as top represented skills, skill-related jobs, "
        "companies, locations and graduate opportunities."
    ),
    "⚡",
)


info_box(
    "Skill limitation",
    (
        "A skill may still be relevant to a role even when it is "
        "not present in HJMI's structured skills field. Different "
        "listings can also use different names or wording for "
        "similar technologies."
    ),
    "ⓘ",
)


# ============================================================
# SALARY
# ============================================================

section_header(
    "Salary Intelligence",
    (
        "How HJMI handles salary information responsibly."
    ),
    "💰",
)


info_box(
    "Disclosed salary",
    (
        "HJMI treats salary as disclosed only when salary "
        "information is available in the collected source record."
    ),
    "💰",
)


info_box(
    "Missing salary",
    (
        "When salary information is unavailable, HJMI does not "
        "invent an estimated salary. The interface displays "
        "'To be discussed after the interview' as an HJMI "
        "presentation convention for missing salary data."
    ),
    "◇",
)


info_box(
    "No unsupported salary averages",
    (
        "Until salary values are normalized and validated into "
        "comparable currencies, periods and ranges, HJMI does not "
        "calculate market averages, medians or salary ranges from "
        "incompatible source text."
    ),
    "ⓘ",
)


# ============================================================
# MARKET TRENDS
# ============================================================

section_header(
    "Market Trends",
    (
        "How HJMI separates current signals from "
        "real historical trends."
    ),
    "📈",
)


info_box(
    "A snapshot is not a trend",
    (
        "HJMI does not claim that a skill, role, location or "
        "graduate market is rising or falling based on one "
        "current snapshot. Reliable trend analysis requires "
        "comparable observations collected consistently over time."
    ),
    "📈",
)


info_box(
    "Historical development",
    (
        "HJMI already retains first-seen, last-seen and opportunity "
        "status information. As the historical dataset grows, "
        "additional snapshot-based trend analysis can be introduced."
    ),
    "◷",
)


# ============================================================
# DATA INTEGRITY
# ============================================================

section_header(
    "Data Integrity Principles",
    (
        "Rules HJMI follows when presenting job-market intelligence."
    ),
    "✓",
)


integrity_cols = st.columns(3)


with integrity_cols[0]:

    insight_card(
        "✓",
        "No Invented",
        "Job Facts",
        (
            "Missing experience, salary or other information "
            "is not silently replaced with unsupported values."
        ),
    )


with integrity_cols[1]:

    insight_card(
        "✓",
        "Clear",
        "Definitions",
        (
            "HJMI explains how labels such as Active, "
            "New, Historical and Graduate Friendly are used."
        ),
    )


with integrity_cols[2]:

    insight_card(
        "✓",
        "Visible",
        "Limitations",
        (
            "The platform distinguishes dataset observations "
            "from conclusions that require broader evidence."
        ),
    )


# ============================================================
# PLATFORM LIMITATIONS
# ============================================================

section_header(
    "Platform Limitations",
    (
        "Important context when interpreting HJMI analysis."
    ),
    "ⓘ",
)


st.markdown(
    """
    HJMI analysis should be interpreted with the following
    limitations in mind:

    - HJMI does not contain every technology job in the UAE.
    - External source coverage can change.
    - Search configuration affects which opportunities are returned.
    - Job descriptions may be incomplete or inconsistent.
    - Company and location names may appear in different formats.
    - Similar job titles may currently be counted separately.
    - Skills depend on what can be identified from available records.
    - Salary information is often missing or inconsistently formatted.
    - Active and Historical are HJMI observation states, not direct
      employer confirmations.
    - Long-term trend analysis requires a larger historical dataset.
    """
)


# ============================================================
# WHO HJMI IS FOR
# ============================================================

section_header(
    "Who HJMI is Designed For",
    (
        "Different users can investigate the same market "
        "from different perspectives."
    ),
    "◇",
)


audience_cols = st.columns(3)


with audience_cols[0]:

    insight_card(
        "🎓",
        "Students &",
        "Fresh Graduates",
        (
            "Explore early-career opportunities, skills, "
            "locations and experience requirements."
        ),
    )


with audience_cols[1]:

    insight_card(
        "💼",
        "Job",
        "Seekers",
        (
            "Search opportunities and investigate the "
            "market around roles, skills and locations."
        ),
    )


with audience_cols[2]:

    insight_card(
        "🏢",
        "Employers",
        "Future Platform",
        (
            "HJMI is designed to later support verified "
            "company profiles, direct job publishing and "
            "recruitment intelligence."
        ),
    )


# ============================================================
# FUTURE DEVELOPMENT
# ============================================================

section_header(
    "HJMI Platform Roadmap",
    (
        "The long-term direction of the project."
    ),
    "→",
)


st.markdown(
    """
    **HJMI 2.0 — Intelligence Platform**

    Market overview, job discovery, graduate intelligence,
    job intelligence, skills, locations, salaries and trends.

    **Future — Personalization**

    User accounts, career profiles, saved opportunities,
    application tracking, recommendations and job alerts.

    **Future — Verified Employer Platform**

    Company verification, employer profiles, direct job
    publishing, recruitment analytics and administrative review.
    """
)


# ============================================================
# PROJECT AUTHOR
# ============================================================

section_header(
    "Project Author",
    (
        "HJMI is an independent computer science and "
        "data-intelligence project."
    ),
    "H",
)


info_box(
    "Hasan R. H. Abdalhadi",
    (
        "Computer Science Engineering student at "
        "BITS Pilani – Dubai Campus. HJMI combines software, "
        "data analysis, information systems and digital "
        "product development into a practical UAE-focused project."
    ),
    "H",
)


# ============================================================
# DISCLAIMER
# ============================================================

section_header(
    "Use of HJMI Information",
    (
        "HJMI is designed as an information and "
        "career-research platform."
    ),
    "ⓘ",
)


info_box(
    "Verify before applying",
    (
        "Users should review the original opportunity source "
        "and employer information before making an application "
        "or career decision. HJMI provides structured market "
        "intelligence and does not guarantee vacancy availability, "
        "employer decisions, salary, interview outcomes or hiring."
    ),
    "ⓘ",
)


# ============================================================
# FOOTER
# ============================================================

footer()
