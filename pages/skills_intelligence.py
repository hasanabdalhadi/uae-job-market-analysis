# ============================================================
# HJMI 2.0 — SKILLS INTELLIGENCE
# Hasan Job Market Intelligence
# ============================================================

import pandas as pd
import plotly.express as px
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

from services.auth_service import (
    is_authenticated,
)

from services.career_profile_service import (
    get_career_profile,
    profile_ready_for_matching,
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
# CHART HELPERS
# ============================================================

def hjmi_horizontal_bar(
    data,
    label_col,
    value_col="Opportunities",
    *,
    height=None,
    max_items=10,
):
    """Render a clean HJMI horizontal ranking chart."""
    if data is None or data.empty:
        return

    chart_data = data[[label_col, value_col]].copy()
    chart_data[label_col] = chart_data[label_col].fillna("").astype(str).str.strip()
    chart_data[value_col] = pd.to_numeric(
        chart_data[value_col],
        errors="coerce",
    ).fillna(0)

    chart_data = chart_data[
        chart_data[label_col].ne("")
        & chart_data[value_col].gt(0)
    ]

    if chart_data.empty:
        return

    chart_data = (
        chart_data
        .sort_values(
            [value_col, label_col],
            ascending=[False, True],
        )
        .head(max_items)
        .sort_values(
            [value_col, label_col],
            ascending=[True, False],
        )
    )

    if height is None:
        height = max(340, 48 * len(chart_data) + 105)

    fig = px.bar(
        chart_data,
        x=value_col,
        y=label_col,
        orientation="h",
        text=value_col,
        custom_data=[label_col, value_col],
    )

    fig.update_traces(
        marker_color="#d8ad57",
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            f"<b>%{{customdata[0]}}</b><br>"
            f"{value_col}: %{{customdata[1]:,.0f}}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=55, t=10, b=45),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce7ef"),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#0b2433",
            font_color="#ffffff",
            bordercolor="#d8ad57",
        ),
        xaxis_title=value_col,
        yaxis_title=None,
        bargap=0.24,
    )

    max_value = float(chart_data[value_col].max())

    if max_value <= 10:
        tick_step = 1
    elif max_value <= 50:
        tick_step = 5
    elif max_value <= 100:
        tick_step = 10
    elif max_value <= 250:
        tick_step = 25
    else:
        tick_step = 50

    fig.update_xaxes(
        rangemode="tozero",
        gridcolor="rgba(120,145,160,0.18)",
        zeroline=False,
        tickmode="linear",
        tick0=0,
        dtick=tick_step,
        tickformat=",d",
    )

    fig.update_yaxes(
        showgrid=False,
        automargin=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": False,
        },
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
    .head(10)
    .rename_axis("Skill")
    .reset_index(name="Opportunities")
)


hjmi_horizontal_bar(
    top_skills,
    "Skill",
    max_items=10,
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
# PERSONAL SKILL INTELLIGENCE
# ============================================================

def _profile_list(value):
    """Normalize Supabase profile list values without changing stored data."""
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return []
        return [item.strip() for item in cleaned.replace(";", ",").split(",") if item.strip()]
    return [str(value).strip()] if str(value).strip() else []


def _canonical_skill_map(skill_index):
    return {
        str(skill).strip().lower(): str(skill).strip()
        for skill in skill_index
        if str(skill).strip()
    }


def _skill_opportunity_counts(jobs, skill_names):
    """Count active records containing each canonical skill."""
    wanted = {str(skill).strip().lower(): str(skill).strip() for skill in skill_names}
    counts = {label: 0 for label in wanted.values()}
    if jobs is None or jobs.empty or "skills" not in jobs.columns:
        return counts

    for value in jobs["skills"]:
        present = {str(skill).strip().lower() for skill in parse_skills(value)}
        for key, label in wanted.items():
            if key in present:
                counts[label] += 1
    return counts


st.markdown("---")
section_header(
    "My Skill Intelligence",
    (
        "Compare your Career Profile with the skills currently represented "
        "across HJMI's active UAE opportunity records."
    ),
    "◎",
)

if not is_authenticated():
    info_box(
        "Personal intelligence is available with an HJMI account",
        (
            "Sign in and complete your Career Profile to compare your skills "
            "with the current HJMI market dataset and identify evidence-based "
            "skill gaps for your target roles."
        ),
        "🔐",
    )
else:
    try:
        career_profile = get_career_profile()
    except Exception:
        career_profile = None

    if not career_profile:
        info_box(
            "Complete your Career Profile",
            (
                "Add your skills and target roles in My HJMI to unlock your "
                "personal market coverage, shared skills and skill-gap analysis."
            ),
            "◎",
        )
    else:
        profile_skills = _profile_list(career_profile.get("skills", []))
        target_roles = _profile_list(career_profile.get("target_roles", []))
        market_skill_map = _canonical_skill_map(skills_rank.index)

        shared_skills = []
        for skill in profile_skills:
            canonical = market_skill_map.get(skill.lower())
            if canonical and canonical not in shared_skills:
                shared_skills.append(canonical)

        coverage = (
            len(shared_skills) / len(profile_skills) * 100
            if profile_skills
            else 0
        )

        # Skill gaps are derived only from active jobs that match a target-role
        # phrase. If no target role is available, we deliberately avoid calling
        # broad market popularity a personal gap.
        target_jobs = active_jobs.iloc[0:0].copy()
        if target_roles:
            target_mask = pd.Series(False, index=active_jobs.index)
            titles = active_jobs["job_title"].fillna("").astype(str)
            for role in target_roles:
                target_mask = target_mask | titles.str.contains(
                    str(role), case=False, regex=False, na=False
                )
            target_jobs = active_jobs[target_mask].copy()

        target_skill_counter = {}
        if not target_jobs.empty:
            for value in target_jobs["skills"]:
                for skill in parse_skills(value):
                    label = market_skill_map.get(str(skill).strip().lower(), str(skill).strip())
                    if label:
                        target_skill_counter[label] = target_skill_counter.get(label, 0) + 1

        profile_skill_keys = {skill.lower() for skill in profile_skills}
        missing_skills = [
            (skill, count)
            for skill, count in sorted(
                target_skill_counter.items(), key=lambda item: item[1], reverse=True
            )
            if skill.lower() not in profile_skill_keys
        ][:5]

        shared_counts = _skill_opportunity_counts(active_jobs, shared_skills)
        strongest_shared = sorted(
            shared_counts.items(), key=lambda item: item[1], reverse=True
        )

        personal_cols = st.columns(3)
        with personal_cols[0]:
            market_metric(
                "◎",
                "Your Market Coverage",
                f"{coverage:.0f}%",
                "Share of your listed profile skills represented in the current active HJMI dataset.",
            )
        with personal_cols[1]:
            market_metric(
                "✓",
                "Shared Market Skills",
                f"{len(shared_skills):,}",
                "Skills in your Career Profile that are also represented in current active HJMI opportunities.",
            )
        with personal_cols[2]:
            market_metric(
                "△",
                "Target-Role Skill Gaps",
                f"{len(missing_skills):,}" if target_roles and not target_jobs.empty else "—",
                "Top structured skills found in matching target-role records but not listed in your profile.",
            )

        compare_left, compare_right = st.columns(2)

        with compare_left:
            st.markdown("### Profile vs UAE Market")
            if not profile_skills:
                st.caption("Add skills to your Career Profile to start the comparison.")
            elif shared_skills:
                shared_text = " • ".join(shared_skills[:10])
                st.success(f"Shared skills: {shared_text}")
                if strongest_shared:
                    strongest_text = " • ".join(
                        f"{skill} ({count})" for skill, count in strongest_shared[:5]
                    )
                    st.caption(
                        "Strongest current market representation among your shared skills: "
                        + strongest_text
                    )
            else:
                st.info(
                    "None of your currently listed profile skills are represented in HJMI's structured active-skill field yet."
                )

        with compare_right:
            st.markdown("### Skill Gap Intelligence")
            if not target_roles:
                st.caption(
                    "Add at least one target role to your Career Profile to calculate role-specific skill gaps."
                )
            elif target_jobs.empty:
                st.caption(
                    "HJMI does not currently have active records whose job titles match your target roles closely enough for a reliable gap comparison."
                )
            elif missing_skills:
                for skill, count in missing_skills:
                    st.markdown(f"**{skill}** — appears in {count:,} matching target-role record(s)")
                st.caption(
                    "These are dataset gaps, not hiring requirements. Learning a skill does not guarantee a job or a higher match score."
                )
            else:
                st.success(
                    "No additional structured skill gaps were identified from the current active records matching your target roles."
                )

        info_box(
            "How personal skill intelligence is calculated",
            (
                "HJMI compares the skills saved in your Career Profile with its current structured active-job data. "
                "Skill gaps are limited to active records whose job titles match your target-role phrases. "
                "The result is a dataset comparison, not a prediction of hiring success or a complete statement of employer requirements."
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

    hjmi_horizontal_bar(
        top_skill_roles,
        "Job Role",
        max_items=10,
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

    hjmi_horizontal_bar(
        top_skill_companies,
        "Company",
        max_items=10,
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

    hjmi_horizontal_bar(
        top_skill_locations,
        "Location",
        max_items=10,
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


    hjmi_horizontal_bar(
        related_skills_df,
        "Related Skill",
        max_items=10,
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


hjmi_horizontal_bar(
    experience_data,
    "Experience Level",
    max_items=7,
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


hjmi_horizontal_bar(
    salary_data,
    "Salary Status",
    max_items=2,
    height=300,
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
