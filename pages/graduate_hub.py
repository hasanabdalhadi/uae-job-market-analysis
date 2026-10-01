# ============================================================
# HJMI 2.0 — GRADUATE HUB
# Hasan Job Market Intelligence
# ============================================================

import pandas as pd
import streamlit as st

from components.theme import (
    apply_theme,
    brand,
    page_header,
    footer,
)

from components.ui import (
    market_metric,
    section_header,
    info_box,
    insight_card,
    job_card,
    empty_state,
    data_status,
    result_count,
)

from services.data_service import (
    load_jobs,
    get_active_jobs,
    get_graduate_jobs,
    get_market_metrics,
    skill_counts,
    search_jobs,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Graduate Hub | HJMI",
    page_icon="🎓",
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
            GRADUATE HUB
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:20px;
        ">
            Career intelligence designed for students,
            fresh graduates and early-career technology talent
            exploring opportunities across the UAE.
        </div>

        <div style="
            padding:14px;
            border-radius:14px;
            background:rgba(216,173,87,0.05);
            border:1px solid rgba(216,173,87,0.12);
        ">
            <div style="
                color:#f2d58b;
                font-size:10px;
                font-weight:750;
            ">
                🎓 Graduate Focus
            </div>

            <div style="
                color:#71879a;
                font-size:9px;
                line-height:1.7;
                margin-top:6px;
            ">
                Opportunities • Skills • Experience •
                Companies • Locations
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

df = load_jobs()


if df.empty:

    page_header(
        "EARLY-CAREER INTELLIGENCE",
        "Graduate Hub",
        (
            "Technology career intelligence for students "
            "and fresh graduates in the UAE."
        ),
    )

    empty_state(
        title="Graduate market data is unavailable",
        message=(
            "HJMI could not load the current UAE technology "
            "job-market dataset."
        ),
        icon="⚠",
    )

    footer()

    st.stop()


# ============================================================
# DATA VIEWS
# ============================================================

metrics = get_market_metrics(df)

active_jobs = get_active_jobs(df)

graduate_jobs = get_graduate_jobs(active_jobs)


# ============================================================
# HEADER
# ============================================================

page_header(
    "HJMI EARLY-CAREER INTELLIGENCE",
    "Graduate Hub 🎓",
    (
        "A dedicated career intelligence space for students, "
        "fresh graduates and early-career candidates exploring "
        "technology opportunities in the UAE."
    ),
)


data_status(
    metrics["last_update"]
)


# ============================================================
# DEFINITION
# ============================================================

info_box(
    "How HJMI identifies graduate-friendly opportunities",
    (
        "HJMI looks for explicit signals in the available listing "
        "text, such as fresh graduate, entry level, graduate trainee, "
        "no experience required or an experience requirement beginning "
        "at zero. Jobs with no stated experience requirement are not "
        "automatically classified as graduate-friendly."
    ),
    "🎓",
)


# ============================================================
# GRADUATE METRICS
# ============================================================

graduate_count = len(
    graduate_jobs
)

active_count = len(
    active_jobs
)


if active_count:

    graduate_share = (
        graduate_count
        / active_count
        * 100
    )

else:

    graduate_share = 0


graduate_companies = (
    graduate_jobs["company"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


graduate_locations = (
    graduate_jobs["location"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


metric_cols = st.columns(4)


with metric_cols[0]:

    market_metric(
        "🎓",
        "Graduate Opportunities",
        f"{graduate_count:,}",
        (
            "Active opportunities currently identified "
            "as fresh-graduate or entry-level friendly."
        ),
    )


with metric_cols[1]:

    market_metric(
        "📊",
        "Graduate Market Share",
        f"{graduate_share:.1f}%",
        (
            "Share of active HJMI opportunities currently "
            "classified as graduate-friendly."
        ),
    )


with metric_cols[2]:

    market_metric(
        "🏢",
        "Graduate Companies",
        f"{graduate_companies:,}",
        (
            "Unique companies represented among identified "
            "graduate-friendly opportunities."
        ),
    )


with metric_cols[3]:

    market_metric(
        "📍",
        "Graduate Locations",
        f"{graduate_locations:,}",
        (
            "Unique UAE location labels represented among "
            "graduate-friendly opportunities."
        ),
    )


# ============================================================
# EMPTY GRADUATE DATA
# ============================================================

if graduate_jobs.empty:

    section_header(
        "Current Graduate Market",
        (
            "HJMI only labels an opportunity as graduate-friendly "
            "when the available listing provides a relevant signal."
        ),
        "🎓",
    )

    empty_state(
        title="No explicitly graduate-friendly jobs identified",
        message=(
            "The current active dataset does not contain an explicit "
            "fresh-graduate or entry-level signal that meets HJMI's "
            "classification rules. This does not mean there are no "
            "other jobs that a graduate could apply for."
        ),
        icon="🎓",
    )

    footer()

    st.stop()


# ============================================================
# GRADUATE MARKET SNAPSHOT
# ============================================================

section_header(
    "Graduate Market Snapshot",
    (
        "A quick view of the roles, skills, companies and "
        "locations represented in the current graduate-friendly "
        "technology market."
    ),
    "◈",
)


# ------------------------------------------------------------
# TOP GRADUATE ROLE
# ------------------------------------------------------------

role_counts = (
    graduate_jobs["job_title"]
    .replace("", pd.NA)
    .dropna()
    .value_counts()
)


if not role_counts.empty:

    top_role = role_counts.index[0]
    top_role_count = int(
        role_counts.iloc[0]
    )

else:

    top_role = "Not available"
    top_role_count = 0


# ------------------------------------------------------------
# TOP GRADUATE SKILL
# ------------------------------------------------------------

graduate_skill_counts = skill_counts(
    graduate_jobs
)


if not graduate_skill_counts.empty:

    top_skill = (
        graduate_skill_counts.index[0]
    )

    top_skill_count = int(
        graduate_skill_counts.iloc[0]
    )

else:

    top_skill = "Not available"
    top_skill_count = 0


# ------------------------------------------------------------
# TOP GRADUATE COMPANY
# ------------------------------------------------------------

company_counts = (
    graduate_jobs["company"]
    .replace("", pd.NA)
    .dropna()
    .value_counts()
)


if not company_counts.empty:

    top_company = company_counts.index[0]

    top_company_count = int(
        company_counts.iloc[0]
    )

else:

    top_company = "Not available"
    top_company_count = 0


# ------------------------------------------------------------
# TOP GRADUATE LOCATION
# ------------------------------------------------------------

location_counts = (
    graduate_jobs["location"]
    .replace("", pd.NA)
    .dropna()
    .value_counts()
)


if not location_counts.empty:

    top_location = (
        location_counts.index[0]
    )

    top_location_count = int(
        location_counts.iloc[0]
    )

else:

    top_location = "Not available"
    top_location_count = 0


snapshot_cols = st.columns(4)


with snapshot_cols[0]:

    insight_card(
        "💻",
        "Most Represented Role",
        top_role,
        (
            f"{top_role_count:,} graduate-friendly listing(s) "
            "currently use this exact title."
        ),
    )


with snapshot_cols[1]:

    insight_card(
        "⚡",
        "Leading Graduate Skill",
        top_skill,
        (
            f"{top_skill_count:,} graduate-friendly listing(s) "
            "include this identified skill."
        ),
    )


with snapshot_cols[2]:

    insight_card(
        "🏢",
        "Most Represented Company",
        top_company,
        (
            f"{top_company_count:,} graduate-friendly listing(s) "
            "are currently associated with this company."
        ),
    )


with snapshot_cols[3]:

    insight_card(
        "📍",
        "Leading Graduate Location",
        top_location,
        (
            f"{top_location_count:,} graduate-friendly listing(s) "
            "currently use this location label."
        ),
    )


# ============================================================
# GRADUATE SKILLS
# ============================================================

section_header(
    "Skills for Graduate Opportunities",
    (
        "Skills identified in the currently represented "
        "graduate-friendly technology opportunities."
    ),
    "⚡",
)


info_box(
    "How to use this section",
    (
        "This is not a list of skills every graduate must have. "
        "It shows skills identified in the graduate-friendly job "
        "records currently represented in HJMI and can help users "
        "understand what employers are mentioning in these listings."
    ),
    "ⓘ",
)


if graduate_skill_counts.empty:

    empty_state(
        title="No graduate skill data available",
        message=(
            "HJMI did not identify structured skill information "
            "in the current graduate-friendly records."
        ),
        icon="⚡",
    )

else:

    top_graduate_skills = (
        graduate_skill_counts
        .head(10)
        .rename_axis("Skill")
        .reset_index(name="Opportunities")
    )

    st.bar_chart(
        top_graduate_skills,
        x="Skill",
        y="Opportunities",
        use_container_width=True,
    )


# ============================================================
# GRADUATE SKILL GAP
# ============================================================

section_header(
    "Graduate Skill Gap Explorer",
    (
        "Choose a skill to see how it connects to current "
        "graduate-friendly opportunities."
    ),
    "🎯",
)


available_skills = list(
    graduate_skill_counts.index
)


if available_skills:

    selected_skill = st.selectbox(
        "Select a graduate-market skill",
        available_skills,
    )


    skill_jobs = search_jobs(
        graduate_jobs,
        skill=selected_skill,
    )


    skill_share = (
        len(skill_jobs)
        / len(graduate_jobs)
        * 100
    )


    skill_roles = (
        skill_jobs["job_title"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    skill_companies = (
        skill_jobs["company"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    skill_locations = (
        skill_jobs["location"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    skill_metric_cols = st.columns(4)


    with skill_metric_cols[0]:

        market_metric(
            "💼",
            "Matching Opportunities",
            f"{len(skill_jobs):,}",
            (
                f"Graduate-friendly opportunities currently "
                f"identified with {selected_skill}."
            ),
        )


    with skill_metric_cols[1]:

        market_metric(
            "📊",
            "Graduate Job Share",
            f"{skill_share:.1f}%",
            (
                "Share of the current graduate-friendly "
                "market represented by this skill."
            ),
        )


    with skill_metric_cols[2]:

        market_metric(
            "💻",
            "Related Roles",
            f"{skill_roles:,}",
            (
                "Unique job-title labels represented among "
                "the matching opportunities."
            ),
        )


    with skill_metric_cols[3]:

        market_metric(
            "🏢",
            "Related Companies",
            f"{skill_companies:,}",
            (
                "Unique companies represented among the "
                "matching graduate opportunities."
            ),
        )


    st.caption(
        f"{selected_skill} currently appears across "
        f"{skill_locations:,} UAE location label(s) in the "
        "graduate-friendly dataset."
    )


# ============================================================
# EXPERIENCE INTELLIGENCE
# ============================================================

section_header(
    "Early-Career Experience Requirements",
    (
        "How HJMI currently classifies experience requirements "
        "within the graduate-friendly dataset."
    ),
    "💼",
)


experience_counts = (
    graduate_jobs[
        "experience_level"
    ]
    .fillna("Not Specified")
    .value_counts()
    .rename_axis("Experience Level")
    .reset_index(name="Opportunities")
)


if experience_counts.empty:

    empty_state(
        title="Experience information unavailable",
        message=(
            "No experience classifications are available "
            "for the current graduate dataset."
        ),
        icon="💼",
    )

else:

    st.bar_chart(
        experience_counts,
        x="Experience Level",
        y="Opportunities",
        use_container_width=True,
    )


info_box(
    "Experience classification",
    (
        "HJMI extracts experience requirements only when they "
        "can be identified from the available listing text. "
        "When a requirement cannot be identified, it remains "
        "Not Specified rather than being estimated."
    ),
    "ⓘ",
)


# ============================================================
# COMPANIES HIRING GRADUATES
# ============================================================

section_header(
    "Companies Represented in Graduate Hiring",
    (
        "Companies currently represented among HJMI's "
        "graduate-friendly technology opportunities."
    ),
    "🏢",
)


top_companies = (
    company_counts
    .head(10)
    .rename_axis("Company")
    .reset_index(name="Opportunities")
)


if top_companies.empty:

    empty_state(
        title="Company data unavailable",
        message=(
            "No company information is available for the "
            "current graduate-friendly records."
        ),
        icon="🏢",
    )

else:

    st.bar_chart(
        top_companies,
        x="Company",
        y="Opportunities",
        use_container_width=True,
    )


# ============================================================
# LOCATIONS
# ============================================================

section_header(
    "Graduate Opportunity Locations",
    (
        "UAE location labels currently represented among "
        "graduate-friendly technology opportunities."
    ),
    "📍",
)


top_locations = (
    location_counts
    .head(10)
    .rename_axis("Location")
    .reset_index(name="Opportunities")
)


if top_locations.empty:

    empty_state(
        title="Location data unavailable",
        message=(
            "No location information is available for "
            "the current graduate-friendly records."
        ),
        icon="📍",
    )

else:

    st.bar_chart(
        top_locations,
        x="Location",
        y="Opportunities",
        use_container_width=True,
    )


# ============================================================
# GRADUATE JOB EXPLORER
# ============================================================

section_header(
    "Explore Graduate Opportunities",
    (
        "Search the currently identified graduate-friendly "
        "technology opportunities."
    ),
    "⌕",
)


graduate_search = st.text_input(
    "Search graduate opportunities",
    placeholder=(
        "Search role, company, location, skill or keyword..."
    ),
)


filtered_graduate_jobs = search_jobs(
    graduate_jobs,
    search_text=graduate_search,
)


result_count(
    len(filtered_graduate_jobs),
    "graduate-friendly opportunities",
)


if filtered_graduate_jobs.empty:

    empty_state(
        title="No matching graduate opportunities",
        message=(
            "Try a broader search term or clear the search "
            "field to view all identified graduate opportunities."
        ),
        icon="⌕",
    )

else:

    display_limit = min(
        len(filtered_graduate_jobs),
        10,
    )


    for _, job in (
        filtered_graduate_jobs
        .head(display_limit)
        .iterrows()
    ):

        job_card(job)


    if len(filtered_graduate_jobs) > display_limit:

        st.caption(
            f"Showing {display_limit:,} of "
            f"{len(filtered_graduate_jobs):,} matching "
            "graduate-friendly opportunities."
        )


# ============================================================
# GRADUATE GUIDANCE
# ============================================================

section_header(
    "How to Use Graduate Intelligence",
    (
        "HJMI is designed to help graduates investigate the "
        "market rather than make career decisions for them."
    ),
    "◇",
)


guidance_cols = st.columns(3)


with guidance_cols[0]:

    insight_card(
        "1",
        "Discover",
        "Opportunities",
        (
            "Explore jobs whose available listing information "
            "shows an early-career or graduate-friendly signal."
        ),
    )


with guidance_cols[1]:

    insight_card(
        "2",
        "Understand",
        "Requirements",
        (
            "Compare the skills and experience requirements "
            "appearing across current graduate opportunities."
        ),
    )


with guidance_cols[2]:

    insight_card(
        "3",
        "Prepare",
        "Your Profile",
        (
            "Use the market evidence as one input when deciding "
            "which skills, roles and opportunities to investigate."
        ),
    )


# ============================================================
# METHODOLOGY
# ============================================================

info_box(
    "Important limitation",
    (
        "Graduate-friendly classification is based on the text "
        "available to HJMI from each listing. A role that is not "
        "marked graduate-friendly may still accept a fresh graduate, "
        "and an identified graduate-friendly listing may contain "
        "other requirements that candidates should review before "
        "applying."
    ),
    "ⓘ",
)


# ============================================================
# FOOTER
# ============================================================

footer()
