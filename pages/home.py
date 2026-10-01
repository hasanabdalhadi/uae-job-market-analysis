# ============================================================
# HJMI 2.0 — HOME & MARKET OVERVIEW
# Hasan Job Market Intelligence
# ============================================================

import streamlit as st

from components.theme import (
    apply_theme,
    brand,
    hero,
    page_header,
    footer,
)

from components.ui import (
    market_metric,
    section_header,
    info_box,
    insight_card,
    feature_card,
    job_card,
    empty_state,
    data_status,
)

from services.data_service import (
    load_jobs,
    get_active_jobs,
    get_new_jobs,
    get_graduate_jobs,
    get_market_metrics,
    skill_counts,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HJMI | UAE Job Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

apply_theme()


# ============================================================
# SIDEBAR BRAND
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
            MARKET INTELLIGENCE
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            color:#a7bac8;
            font-size:12px;
            line-height:2.1;
        ">
            ◈ Market Overview<br>
            ◇ Find Jobs<br>
            ◇ Graduate Hub<br>
            ◇ Job Intelligence<br>
            ◇ Skills Intelligence<br>
            ◇ Location Intelligence<br>
            ◇ Salary Intelligence<br>
            ◇ Market Trends
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            margin-top:26px;
            padding-top:18px;
            border-top:1px solid rgba(148,163,184,0.12);
        ">
            <div style="
                color:#d8ad57;
                font-size:9px;
                font-weight:800;
                letter-spacing:2px;
                margin-bottom:10px;
            ">
                HJMI PLATFORM
            </div>

            <div style="
                color:#6f8598;
                font-size:11px;
                line-height:2;
            ">
                My HJMI<br>
                Saved Jobs<br>
                Applications<br>
                Job Alerts<br>
                Employer Portal
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            margin-top:28px;
            padding:14px;
            border-radius:13px;
            background:rgba(216,173,87,0.05);
            border:1px solid rgba(216,173,87,0.12);
        ">
            <div style="
                color:#d8ad57;
                font-size:9px;
                font-weight:800;
                letter-spacing:1px;
            ">
                HJMI 2.0
            </div>

            <div style="
                color:#71879a;
                font-size:9px;
                line-height:1.6;
                margin-top:5px;
            ">
                UAE Technology Career Intelligence Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD MARKET DATA
# ============================================================

df = load_jobs()


# ============================================================
# DATA AVAILABILITY
# ============================================================

if df.empty:

    hero()

    empty_state(
        title="Market data is currently unavailable",
        message=(
            "HJMI could not load the UAE technology job-market "
            "dataset. Please check the data pipeline and try again."
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

new_jobs = get_new_jobs(df)

graduate_jobs = get_graduate_jobs(active_jobs)


# ============================================================
# HERO
# ============================================================

hero()


# ============================================================
# DATA STATUS
# ============================================================

data_status(
    metrics["last_update"]
)


# ============================================================
# MARKET OVERVIEW
# ============================================================

page_header(
    "LIVE UAE TECHNOLOGY MARKET",
    "Market Overview",
    (
        "A clear snapshot of the technology opportunities currently "
        "represented in HJMI's latest UAE market collection."
    ),
)


info_box(
    "How to read this dashboard",
    (
        "HJMI collects technology opportunities from its configured "
        "market source and analyzes the latest dataset. 'Active' means "
        "the opportunity appeared in the latest HJMI collection. It "
        "does not independently guarantee that the employer has not "
        "changed or closed the vacancy since collection."
    ),
    "ⓘ",
)


# ============================================================
# PRIMARY METRICS
# ============================================================

metric_cols = st.columns(4)

with metric_cols[0]:

    market_metric(
        "💼",
        "Active Opportunities",
        f'{metrics["active_jobs"]:,}',
        (
            "Technology opportunities seen in the latest "
            "HJMI market collection."
        ),
    )


with metric_cols[1]:

    market_metric(
        "🆕",
        "New Opportunities",
        f'{metrics["new_jobs"]:,}',
        (
            "Opportunities first discovered by HJMI "
            "during the latest data update."
        ),
    )


with metric_cols[2]:

    market_metric(
        "🎓",
        "Graduate Opportunities",
        f'{metrics["graduate_jobs"]:,}',
        (
            "Active listings identified from their available "
            "text as fresh-graduate or entry-level friendly."
        ),
    )


with metric_cols[3]:

    market_metric(
        "🏢",
        "Companies",
        f'{metrics["companies"]:,}',
        (
            "Unique companies represented among active "
            "HJMI opportunities."
        ),
    )


st.write("")


secondary_cols = st.columns(4)

with secondary_cols[0]:

    market_metric(
        "📍",
        "Locations",
        f'{metrics["locations"]:,}',
        (
            "Unique UAE location labels represented in "
            "the active market dataset."
        ),
    )


with secondary_cols[1]:

    market_metric(
        "⚡",
        "Skills Identified",
        f'{metrics["skills"]:,}',
        (
            "Unique technology skills identified in "
            "active HJMI job records."
        ),
    )


with secondary_cols[2]:

    market_metric(
        "💰",
        "Salary Disclosed",
        f'{metrics["salary_disclosed"]:,}',
        (
            "Active opportunities where salary information "
            "is available in the source data."
        ),
    )


with secondary_cols[3]:

    market_metric(
        "🗂️",
        "Market Records",
        f'{metrics["jobs_collected"]:,}',
        (
            "Total active and historical UAE technology "
            "records currently retained by HJMI."
        ),
    )


# ============================================================
# MARKET SNAPSHOT
# ============================================================

section_header(
    "Market Snapshot",
    (
        "Quick signals from the latest active UAE technology "
        "opportunities represented in HJMI."
    ),
    "◈",
)


# ------------------------------------------------------------
# TOP ROLE
# ------------------------------------------------------------

if not active_jobs.empty:

    top_roles = (
        active_jobs["job_title"]
        .replace("", None)
        .dropna()
        .value_counts()
    )

else:
    top_roles = None


if (
    top_roles is not None
    and not top_roles.empty
):
    top_role = top_roles.index[0]
    top_role_count = int(top_roles.iloc[0])

else:
    top_role = "Not available"
    top_role_count = 0


# ------------------------------------------------------------
# TOP LOCATION
# ------------------------------------------------------------

if not active_jobs.empty:

    top_locations = (
        active_jobs["location"]
        .replace("", None)
        .dropna()
        .value_counts()
    )

else:
    top_locations = None


if (
    top_locations is not None
    and not top_locations.empty
):
    top_location = top_locations.index[0]
    top_location_count = int(
        top_locations.iloc[0]
    )

else:
    top_location = "Not available"
    top_location_count = 0


# ------------------------------------------------------------
# TOP SKILL
# ------------------------------------------------------------

skills_rank = skill_counts(
    active_jobs
)


if not skills_rank.empty:

    top_skill = skills_rank.index[0]
    top_skill_count = int(
        skills_rank.iloc[0]
    )

else:
    top_skill = "Not available"
    top_skill_count = 0


# ------------------------------------------------------------
# GRADUATE SHARE
# ------------------------------------------------------------

if len(active_jobs) > 0:

    graduate_share = (
        len(graduate_jobs)
        / len(active_jobs)
        * 100
    )

else:
    graduate_share = 0


snapshot_cols = st.columns(4)


with snapshot_cols[0]:

    insight_card(
        "💻",
        "Most Represented Role",
        top_role,
        (
            f"{top_role_count:,} active listing(s) currently "
            "use this exact job-title label."
        ),
    )


with snapshot_cols[1]:

    insight_card(
        "📍",
        "Leading Location",
        top_location,
        (
            f"{top_location_count:,} active opportunity record(s) "
            "currently use this location label."
        ),
    )


with snapshot_cols[2]:

    insight_card(
        "⚡",
        "Most Identified Skill",
        top_skill,
        (
            f"{top_skill_count:,} active listing(s) in the "
            "current dataset include this identified skill."
        ),
    )


with snapshot_cols[3]:

    insight_card(
        "🎓",
        "Graduate-Friendly Share",
        f"{graduate_share:.1f}%",
        (
            "Share of active listings currently classified "
            "by HJMI as fresh-graduate or entry-level friendly."
        ),
    )


# ============================================================
# GRADUATE FOCUS
# ============================================================

section_header(
    "Fresh Graduate Focus",
    (
        "A dedicated view for students and recent graduates "
        "starting their technology careers in the UAE."
    ),
    "🎓",
)


graduate_feature_cols = st.columns(3)


with graduate_feature_cols[0]:

    feature_card(
        "🎯",
        "Entry-Level Discovery",
        (
            "Identify opportunities whose available listing text "
            "indicates fresh-graduate, entry-level or zero-year "
            "experience suitability."
        ),
        "GRADUATE HUB",
    )


with graduate_feature_cols[1]:

    feature_card(
        "⚡",
        "Graduate Skill Intelligence",
        (
            "Understand which technical skills appear across "
            "the graduate-friendly opportunities represented "
            "in HJMI."
        ),
        "SKILL GAP",
    )


with graduate_feature_cols[2]:

    feature_card(
        "🏢",
        "Graduate Hiring Market",
        (
            "Explore companies, roles and UAE locations "
            "represented among identified graduate-friendly "
            "technology opportunities."
        ),
        "CAREER INTELLIGENCE",
    )


# ============================================================
# LATEST NEW OPPORTUNITIES
# ============================================================

section_header(
    "New Opportunities",
    (
        "Technology opportunities first discovered by HJMI "
        "during the latest market update."
    ),
    "🆕",
)


info_box(
    "What does New mean?",
    (
        "'New' means HJMI first discovered the opportunity "
        "during the latest collection. It does not necessarily "
        "mean the employer originally published the vacancy today."
    ),
    "ⓘ",
)


if new_jobs.empty:

    empty_state(
        title="No newly discovered opportunities in this update",
        message=(
            "The latest HJMI collection did not identify a job "
            "that was new to the existing dataset. Active "
            "opportunities remain available in the market."
        ),
        icon="✓",
    )

else:

    new_jobs_display = new_jobs.copy()

    if "publication_date" in new_jobs_display.columns:

        new_jobs_display[
            "_sort_date"
        ] = st.session_state.get(
            "_unused",
            None,
        )

        new_jobs_display[
            "_sort_date"
        ] = (
            new_jobs_display[
                "publication_date"
            ]
        )

        new_jobs_display = (
            new_jobs_display
            .sort_values(
                "_sort_date",
                ascending=False,
            )
        )

    for _, job in (
        new_jobs_display
        .head(5)
        .iterrows()
    ):

        job_card(job)


# ============================================================
# GRADUATE OPPORTUNITIES PREVIEW
# ============================================================

section_header(
    "Graduate Opportunities Preview",
    (
        "A sample of active opportunities currently identified "
        "as suitable for fresh graduates or entry-level candidates."
    ),
    "🎓",
)


if graduate_jobs.empty:

    empty_state(
        title="No graduate-friendly listings identified",
        message=(
            "HJMI did not find an explicit fresh-graduate or "
            "entry-level signal in the currently active listings. "
            "Jobs without a stated experience requirement are "
            "not automatically classified as graduate-friendly."
        ),
        icon="🎓",
    )

else:

    for _, job in (
        graduate_jobs
        .head(5)
        .iterrows()
    ):

        job_card(job)


# ============================================================
# HJMI INTELLIGENCE AREAS
# ============================================================

section_header(
    "Explore HJMI Intelligence",
    (
        "HJMI 2.0 is designed to connect job discovery with "
        "market understanding rather than showing vacancies alone."
    ),
    "◇",
)


area_row_1 = st.columns(4)


with area_row_1[0]:

    feature_card(
        "⌕",
        "Find Jobs",
        (
            "Search active UAE technology opportunities "
            "using role, company, location, skill and "
            "experience filters."
        ),
        "DISCOVER",
    )


with area_row_1[1]:

    feature_card(
        "🎓",
        "Graduate Hub",
        (
            "Focus on entry-level opportunities, graduate "
            "skills and early-career market signals."
        ),
        "START YOUR CAREER",
    )


with area_row_1[2]:

    feature_card(
        "💼",
        "Job Intelligence",
        (
            "Understand roles, companies and experience "
            "requirements represented in the market."
        ),
        "ANALYZE",
    )


with area_row_1[3]:

    feature_card(
        "⚡",
        "Skills Intelligence",
        (
            "Explore skills appearing in opportunities and "
            "the roles, companies and locations connected "
            "to them."
        ),
        "SKILLS",
    )


st.write("")


area_row_2 = st.columns(4)


with area_row_2[0]:

    feature_card(
        "📍",
        "Location Intelligence",
        (
            "Explore how technology opportunities are "
            "distributed across UAE location labels."
        ),
        "UAE",
    )


with area_row_2[1]:

    feature_card(
        "💰",
        "Salary Intelligence",
        (
            "Analyze disclosed salary information without "
            "inventing values for listings where salary "
            "is unavailable."
        ),
        "COMPENSATION",
    )


with area_row_2[2]:

    feature_card(
        "📈",
        "Market Trends",
        (
            "Track how the HJMI dataset changes as new "
            "market snapshots are collected over time."
        ),
        "TRENDS",
    )


with area_row_2[3]:

    feature_card(
        "🏢",
        "Employer Platform",
        (
            "Future HJMI modules will support verified "
            "company profiles, direct opportunities and "
            "employer analytics."
        ),
        "PLATFORM ROADMAP",
    )


# ============================================================
# METHODOLOGY NOTE
# ============================================================

section_header(
    "Understanding HJMI Data",
    (
        "Transparency is part of the platform. Market labels "
        "describe what HJMI observed in its collected dataset."
    ),
    "ⓘ",
)


info_box(
    "Active Opportunities",
    (
        "An Active opportunity is a job returned in the latest "
        "HJMI market collection. HJMI does not independently "
        "confirm the vacancy's status directly with the employer."
    ),
    "●",
)


info_box(
    "Historical Opportunities",
    (
        "A Historical opportunity is retained in HJMI's dataset "
        "but was not returned in the latest collection. This does "
        "not by itself prove that the employer closed the vacancy."
    ),
    "◷",
)


info_box(
    "Fresh Graduate Classification",
    (
        "HJMI classifies a listing as graduate-friendly only when "
        "the available listing text contains a relevant signal, "
        "such as fresh graduate, entry level, no experience "
        "required or an experience requirement beginning at zero."
    ),
    "🎓",
)


# ============================================================
# FOOTER
# ============================================================

footer()
