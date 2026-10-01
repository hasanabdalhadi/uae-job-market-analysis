# ============================================================
# HJMI 2.0 — SKILLS INTELLIGENCE
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
    parse_skills,
    search_jobs,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Skills Intelligence | HJMI",
    page_icon="⚡",
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
            SKILLS INTELLIGENCE
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:20px;
        ">
            Explore technology skills and understand
            the roles, companies, locations and opportunities
            connected to them across the UAE market.
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
        "UAE TECHNOLOGY SKILLS",
        "Skills Intelligence",
        (
            "Explore technology skills represented "
            "across HJMI opportunities."
        ),
    )

    empty_state(
        title="Skills data is unavailable",
        message=(
            "HJMI could not load the current UAE "
            "technology job-market dataset."
        ),
        icon="⚠",
    )

    footer()

    st.stop()


# ============================================================
# DATA
# ============================================================

metrics = get_market_metrics(df)

active_jobs = get_active_jobs(df)

graduate_jobs = get_graduate_jobs(
    active_jobs
)

skills_rank = skill_counts(
    active_jobs
)


# ============================================================
# HEADER
# ============================================================

page_header(
    "UAE TECHNOLOGY SKILLS INTELLIGENCE",
    "Skills Intelligence ⚡",
    (
        "Understand which technology skills appear in HJMI's "
        "active UAE opportunities and explore the jobs, companies, "
        "locations and related skills connected to each one."
    ),
)


data_status(
    metrics["last_update"]
)


info_box(
    "What Skills Intelligence shows",
    (
        "Skill counts describe skills identified in the active "
        "job records currently represented by HJMI. They should "
        "be interpreted as signals from the collected dataset, "
        "not as a complete ranking of every skill demanded by "
        "every technology employer in the UAE."
    ),
    "ⓘ",
)


# ============================================================
# GENERAL SKILL METRICS
# ============================================================

jobs_with_skills = int(
    active_jobs["skills"]
    .fillna("")
    .astype(str)
    .str.strip()
    .ne("")
    .sum()
)


if len(active_jobs):

    jobs_with_skills_share = (
        jobs_with_skills
        / len(active_jobs)
        * 100
    )

else:

    jobs_with_skills_share = 0


graduate_skills = skill_counts(
    graduate_jobs
)


metric_cols = st.columns(4)


with metric_cols[0]:

    market_metric(
        "⚡",
        "Skills Identified",
        f'{metrics["skills"]:,}',
        (
            "Unique technology skills identified among "
            "active HJMI opportunity records."
        ),
    )


with metric_cols[1]:

    market_metric(
        "💼",
        "Jobs with Skill Data",
        f"{jobs_with_skills:,}",
        (
            "Active opportunities containing identified "
            "structured skill information."
        ),
    )


with metric_cols[2]:

    market_metric(
        "📊",
        "Skill Data Coverage",
        f"{jobs_with_skills_share:.1f}%",
        (
            "Share of active opportunity records currently "
            "containing identified skill information."
        ),
    )


with metric_cols[3]:

    market_metric(
        "🎓",
        "Graduate Skills",
        f"{len(graduate_skills):,}",
        (
            "Unique skills identified among currently "
            "graduate-friendly opportunities."
        ),
    )


# ============================================================
# TOP SKILLS
# ============================================================

section_header(
    "Skills Represented in the Market",
    (
        "Technology skills appearing most frequently among "
        "the active opportunity records currently analyzed by HJMI."
    ),
    "⚡",
)


if skills_rank.empty:

    empty_state(
        title="No structured skill information available",
        message=(
            "HJMI did not identify skill information in "
            "the current active opportunity records."
        ),
        icon="⚡",
    )

    footer()

    st.stop()


top_skills = (
    skills_rank
    .head(15)
    .rename_axis("Skill")
    .reset_index(name="Opportunities")
)


st.bar_chart(
    top_skills,
    x="Skill",
    y="Opportunities",
    use_container_width=True,
)


info_box(
    "Reading the chart",
    (
        "A higher count means the skill was identified in more "
        "active HJMI opportunity records. One job may contain "
        "multiple skills and therefore contribute to multiple "
        "skill counts."
    ),
    "ⓘ",
)


# ============================================================
# SKILL EXPLORER
# ============================================================

section_header(
    "Skill Explorer",
    (
        "Select a skill to investigate its current connection "
        "to UAE technology opportunities."
    ),
    "⌕",
)


available_skills = list(
    skills_rank.index
)


selected_skill = st.selectbox(
    "Select a technology skill",
    available_skills,
)


skill_jobs = search_jobs(
    active_jobs,
    skill=selected_skill,
)


skill_job_count = len(
    skill_jobs
)


if len(active_jobs):

    market_share = (
        skill_job_count
        / len(active_jobs)
        * 100
    )

else:

    market_share = 0


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


skill_roles = (
    skill_jobs["job_title"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


skill_graduate_jobs = skill_jobs[
    skill_jobs[
        "fresh_graduate_friendly"
    ]
].copy()


skill_metric_cols = st.columns(4)


with skill_metric_cols[0]:

    market_metric(
        "💼",
        "Matching Opportunities",
        f"{skill_job_count:,}",
        (
            f"Active HJMI opportunities currently "
            f"identified with {selected_skill}."
        ),
    )


with skill_metric_cols[1]:

    market_metric(
        "📊",
        "Active Market Share",
        f"{market_share:.1f}%",
        (
            "Share of active HJMI opportunities currently "
            "represented by the selected skill."
        ),
    )


with skill_metric_cols[2]:

    market_metric(
        "🏢",
        "Companies",
        f"{skill_companies:,}",
        (
            "Unique companies represented among opportunities "
            "connected to the selected skill."
        ),
    )


with skill_metric_cols[3]:

    market_metric(
        "🎓",
        "Graduate Opportunities",
        f"{len(skill_graduate_jobs):,}",
        (
            "Matching opportunities currently classified "
            "as fresh-graduate or entry-level friendly."
        ),
    )


# ============================================================
# SELECTED SKILL SNAPSHOT
# ============================================================

section_header(
    f"{selected_skill} Market Snapshot",
    (
        "A closer look at the roles, companies and locations "
        "currently connected to this skill."
    ),
    "◈",
)


# ------------------------------------------------------------
# TOP ROLE
# ------------------------------------------------------------

role_counts = (
    skill_jobs["job_title"]
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
# TOP COMPANY
# ------------------------------------------------------------

company_counts = (
    skill_jobs["company"]
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
# TOP LOCATION
# ------------------------------------------------------------

location_counts = (
    skill_jobs["location"]
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
            f"{top_role_count:,} matching listing(s) "
            "currently use this exact job-title label."
        ),
    )


with snapshot_cols[1]:

    insight_card(
        "🏢",
        "Most Represented Company",
        top_company,
        (
            f"{top_company_count:,} matching opportunity "
            "record(s) are associated with this company."
        ),
    )


with snapshot_cols[2]:

    insight_card(
        "📍",
        "Leading Location",
        top_location,
        (
            f"{top_location_count:,} matching opportunity "
            "record(s) use this location label."
        ),
    )


with snapshot_cols[3]:

    insight_card(
        "◇",
        "Related Roles",
        f"{skill_roles:,}",
        (
            "Unique job-title labels currently represented "
            "among opportunities containing this skill."
        ),
    )


# ============================================================
# RELATED ROLES
# ============================================================

section_header(
    f"Roles Using {selected_skill}",
    (
        "Job-title labels represented among active "
        "opportunities connected to the selected skill."
    ),
    "💻",
)


top_skill_roles = (
    role_counts
    .head(12)
    .rename_axis("Job Role")
    .reset_index(name="Opportunities")
)


if top_skill_roles.empty:

    empty_state(
        title="No related roles available",
        message=(
            "HJMI could not identify related job-title "
            "information for this skill."
        ),
        icon="💻",
    )

else:

    st.bar_chart(
        top_skill_roles,
        x="Job Role",
        y="Opportunities",
        use_container_width=True,
    )


# ============================================================
# COMPANIES USING SELECTED SKILL
# ============================================================

section_header(
    f"Companies Seeking {selected_skill}",
    (
        "Companies represented among active opportunities "
        "currently connected to the selected skill."
    ),
    "🏢",
)


top_skill_companies = (
    company_counts
    .head(12)
    .rename_axis("Company")
    .reset_index(name="Opportunities")
)


if top_skill_companies.empty:

    empty_state(
        title="No company information available",
        message=(
            "No usable company information is currently "
            "available for this selected skill."
        ),
        icon="🏢",
    )

else:

    st.bar_chart(
        top_skill_companies,
        x="Company",
        y="Opportunities",
        use_container_width=True,
    )


# ============================================================
# LOCATION INTELLIGENCE FOR SKILL
# ============================================================

section_header(
    f"Where {selected_skill} Appears",
    (
        "UAE location labels represented among opportunities "
        "currently connected to the selected skill."
    ),
    "📍",
)


top_skill_locations = (
    location_counts
    .head(10)
    .rename_axis("Location")
    .reset_index(name="Opportunities")
)


if top_skill_locations.empty:

    empty_state(
        title="No location information available",
        message=(
            "No usable location information is currently "
            "available for this selected skill."
        ),
        icon="📍",
    )

else:

    st.bar_chart(
        top_skill_locations,
        x="Location",
        y="Opportunities",
        use_container_width=True,
    )


# ============================================================
# CO-OCCURRING SKILLS
# ============================================================

section_header(
    f"Skills Appearing with {selected_skill}",
    (
        "Other identified skills appearing in the same "
        "active opportunity records as the selected skill."
    ),
    "🔗",
)


related_skill_counter = {}


for skills_value in skill_jobs["skills"]:

    job_skills = parse_skills(
        skills_value
    )

    normalized_selected = (
        str(selected_skill)
        .strip()
        .lower()
    )

    for skill in job_skills:

        if (
            skill.strip().lower()
            == normalized_selected
        ):
            continue

        related_skill_counter[
            skill
        ] = (
            related_skill_counter
            .get(skill, 0)
            + 1
        )


if related_skill_counter:

    related_skills_df = pd.DataFrame(
        sorted(
            related_skill_counter.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:12],
        columns=[
            "Related Skill",
            "Opportunities",
        ],
    )


    st.bar_chart(
        related_skills_df,
        x="Related Skill",
        y="Opportunities",
        use_container_width=True,
    )


else:

    empty_state(
        title="No related skills identified",
        message=(
            "The current matching records do not contain "
            "other structured skills alongside the selected skill."
        ),
        icon="🔗",
    )


info_box(
    "What co-occurring skills mean",
    (
        "These skills appear in the same HJMI opportunity records "
        "as the selected skill. This does not prove that every "
        "employer requires the skills together, but it can help "
        "users investigate common combinations in the dataset."
    ),
    "ⓘ",
)


# ============================================================
# GRADUATE SKILL INTELLIGENCE
# ============================================================

section_header(
    f"{selected_skill} for Fresh Graduates",
    (
        "Graduate-friendly opportunities currently connected "
        "to the selected technology skill."
    ),
    "🎓",
)


if skill_graduate_jobs.empty:

    empty_state(
        title=(
            "No graduate-friendly matches identified"
        ),
        message=(
            f"HJMI currently has no active opportunity that is "
            f"both identified with {selected_skill} and explicitly "
            "classified as fresh-graduate friendly."
        ),
        icon="🎓",
    )

else:

    graduate_company_count = (
        skill_graduate_jobs["company"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    graduate_location_count = (
        skill_graduate_jobs["location"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    graduate_role_count = (
        skill_graduate_jobs["job_title"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    graduate_cols = st.columns(3)


    with graduate_cols[0]:

        market_metric(
            "💻",
            "Graduate Roles",
            f"{graduate_role_count:,}",
            (
                "Unique job-title labels represented among "
                "graduate-friendly matches."
            ),
        )


    with graduate_cols[1]:

        market_metric(
            "🏢",
            "Graduate Companies",
            f"{graduate_company_count:,}",
            (
                "Unique companies represented among "
                "graduate-friendly matches."
            ),
        )


    with graduate_cols[2]:

        market_metric(
            "📍",
            "Graduate Locations",
            f"{graduate_location_count:,}",
            (
                "Unique UAE location labels represented among "
                "graduate-friendly matches."
            ),
        )


# ============================================================
# EXPERIENCE PROFILE
# ============================================================

section_header(
    f"Experience Profile for {selected_skill}",
    (
        "HJMI experience classifications represented among "
        "matching active opportunities."
    ),
    "💼",
)


experience_order = [
    "Fresh Graduate / Entry Level",
    "0–1 Year",
    "1–2 Years",
    "2–3 Years",
    "3–5 Years",
    "5+ Years",
    "Not Specified",
]


experience_data = (
    skill_jobs["experience_level"]
    .fillna("Not Specified")
    .value_counts()
    .reindex(
        experience_order,
        fill_value=0,
    )
    .rename_axis("Experience Level")
    .reset_index(name="Opportunities")
)


st.bar_chart(
    experience_data,
    x="Experience Level",
    y="Opportunities",
    use_container_width=True,
)


# ============================================================
# SALARY AVAILABILITY
# ============================================================

section_header(
    f"Salary Availability for {selected_skill}",
    (
        "How often salary information is available in the "
        "matching opportunity records."
    ),
    "💰",
)


salary_disclosed = int(
    skill_jobs[
        "salary_disclosed"
    ].sum()
)


salary_not_disclosed = (
    len(skill_jobs)
    - salary_disclosed
)


salary_data = pd.DataFrame(
    {
        "Salary Status": [
            "Salary Disclosed",
            "Not Disclosed",
        ],
        "Opportunities": [
            salary_disclosed,
            salary_not_disclosed,
        ],
    }
)


st.bar_chart(
    salary_data,
    x="Salary Status",
    y="Opportunities",
    use_container_width=True,
)


info_box(
    "Salary transparency",
    (
        "HJMI does not create estimated salaries for jobs where "
        "the source listing does not provide salary information. "
        "Those opportunities are displayed as 'To be discussed "
        "after the interview'."
    ),
    "💰",
)


# ============================================================
# MATCHING OPPORTUNITIES
# ============================================================

section_header(
    f"Opportunities Requiring {selected_skill}",
    (
        "Explore active job records currently connected "
        "to the selected skill."
    ),
    "↗",
)


result_count(
    len(skill_jobs),
    "matching active opportunities",
)


if skill_jobs.empty:

    empty_state(
        title="No matching opportunities found",
        message=(
            "No active HJMI opportunity currently matches "
            "the selected skill."
        ),
        icon="⌕",
    )

else:

    display_limit = min(
        len(skill_jobs),
        10,
    )


    for _, job in (
        skill_jobs
        .head(display_limit)
        .iterrows()
    ):

        job_card(job)


    if len(skill_jobs) > display_limit:

        st.caption(
            f"Showing {display_limit:,} of "
            f"{len(skill_jobs):,} matching opportunities."
        )


# ============================================================
# METHODOLOGY
# ============================================================

section_header(
    "Skills Intelligence Methodology",
    (
        "HJMI keeps skill analysis tied to information "
        "identified in its collected job records."
    ),
    "ⓘ",
)


info_box(
    "Important limitation",
    (
        "A skill may be relevant to a job even when it is not "
        "identified in HJMI's structured skills field, and skill "
        "names may appear in different forms across listings. "
        "The analysis therefore describes the structured HJMI "
        "dataset rather than every possible skill relationship."
    ),
    "ⓘ",
)


# ============================================================
# FOOTER
# ============================================================

footer()
