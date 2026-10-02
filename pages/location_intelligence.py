# ============================================================
# HJMI 2.0 — LOCATION INTELLIGENCE
# Hasan Job Market Intelligence
# ============================================================

import pandas as pd
import streamlit as st
import plotly.express as px

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
    get_market_metrics,
    skill_counts,
)



# ============================================================
# LOCATION NORMALIZATION + CHART HELPERS
# ============================================================

UAE_EMIRATE_ALIASES = {
    "dubai": "Dubai", "abu dhabi": "Abu Dhabi", "abu-dhabi": "Abu Dhabi",
    "abudhabi": "Abu Dhabi", "sharjah": "Sharjah", "ajman": "Ajman",
    "umm al quwain": "Umm Al Quwain", "umm al-quwain": "Umm Al Quwain",
    "umm al qaiwain": "Umm Al Quwain", "uaq": "Umm Al Quwain",
    "ras al khaimah": "Ras Al Khaimah", "ras al-khaimah": "Ras Al Khaimah",
    "rak": "Ras Al Khaimah", "fujairah": "Fujairah",
    "al ain": "Al Ain", "al-ain": "Al Ain",
}
UAE_WIDE_LABELS = {"uae", "u.a.e", "u.a.e.", "united arab emirates",
                   "united arab emirate", "emirates"}

def normalize_location_label(value):
    if pd.isna(value):
        return ""
    raw = " ".join(str(value).strip().split())
    if not raw:
        return ""
    lowered = " ".join(raw.lower().replace(",", " ").split())
    if lowered in UAE_WIDE_LABELS:
        return "UAE-wide / Unspecified"
    stripped = lowered
    for suffix in (" united arab emirates", " uae", " u.a.e.", " u.a.e"):
        if stripped.endswith(suffix):
            stripped = stripped[:-len(suffix)].strip(" ,-")
    if stripped in UAE_EMIRATE_ALIASES:
        return UAE_EMIRATE_ALIASES[stripped]
    if lowered in UAE_EMIRATE_ALIASES:
        return UAE_EMIRATE_ALIASES[lowered]
    return raw

def normalized_text_counts(series):
    cleaned = series.fillna("").astype(str).map(lambda x: " ".join(x.strip().split()))
    cleaned = cleaned[cleaned.ne("")]
    if cleaned.empty:
        return pd.Series(dtype="int64")
    frame = pd.DataFrame({"label": cleaned})
    frame["key"] = frame["label"].str.casefold()
    grouped = frame.groupby("key", sort=False)
    counts = grouped.size()
    labels = grouped["label"].agg(
        lambda values: max(values.tolist(),
                           key=lambda x: (sum(ch.isupper() for ch in x), len(x)))
    )
    return pd.Series(counts.values, index=labels.values, dtype="int64").sort_values(ascending=False)

def hjmi_horizontal_bar(data, label_col, value_col="Opportunities", *, max_items=8, height=None):
    if data is None or data.empty:
        return
    chart_data = data[[label_col, value_col]].copy()
    chart_data[value_col] = pd.to_numeric(chart_data[value_col], errors="coerce").fillna(0)
    chart_data = chart_data[chart_data[value_col] > 0]
    chart_data = chart_data.sort_values(value_col, ascending=False).head(max_items)
    if chart_data.empty:
        return
    chart_data = chart_data.iloc[::-1]
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
    if height is None:
        height = max(260, min(430, 80 + len(chart_data) * 38))
    fig = px.bar(chart_data, x=value_col, y=label_col, orientation="h",
                 text=value_col, custom_data=[label_col, value_col])
    fig.update_traces(marker_color="#d8ad57", texttemplate="%{text:,.0f}",
                      textposition="outside", cliponaxis=False,
                      hovertemplate=f"<b>%{{customdata[0]}}</b><br>{value_col}: %{{customdata[1]:,.0f}}<extra></extra>")
    fig.update_layout(height=height, margin=dict(l=8, r=42, t=8, b=35),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#eaf2f8"), xaxis_title=value_col,
                      yaxis_title=None, showlegend=False)
    fig.update_xaxes(rangemode="tozero", gridcolor="rgba(117,139,157,0.16)",
                     zeroline=False, tickmode="linear", tick0=0,
                     dtick=tick_step, tickformat=",d")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False, "displaylogo": False,
                            "responsive": True, "scrollZoom": False})

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Location Intelligence | HJMI",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN
# ============================================================

apply_theme()
st.markdown(
    """<style>
    div[data-testid="stVerticalBlock"] { gap: 0.75rem; }
    div[data-testid="stPlotlyChart"] { margin-bottom: 0.25rem; }
    </style>""",
    unsafe_allow_html=True,
)


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
            LOCATION INTELLIGENCE
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:20px;
        ">
            Explore where UAE technology opportunities
            are represented and understand the roles,
            skills and companies connected to each location.
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
        "UAE TECHNOLOGY LOCATIONS",
        "Location Intelligence",
        (
            "Explore the geographic distribution of "
            "technology opportunities represented in HJMI."
        ),
    )

    empty_state(
        title="Location data is unavailable",
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


location_series = (
    active_jobs["location"]
    .fillna("")
    .astype(str)
    .map(normalize_location_label)
)

location_jobs = active_jobs[location_series.ne("")].copy()
location_jobs["location_display"] = location_series.loc[location_jobs.index]

location_counts = location_jobs["location_display"].value_counts()


# ============================================================
# HEADER
# ============================================================

page_header(
    "UAE TECHNOLOGY LOCATION INTELLIGENCE",
    "Location Intelligence 📍",
    (
        "Explore where active technology opportunities are "
        "represented across the UAE and investigate the roles, "
        "skills, companies and experience requirements connected "
        "to each location."
    ),
)


data_status(
    metrics["last_update"]
)


info_box(
    "How to read Location Intelligence",
    (
        "HJMI standardizes only clear UAE location variants, such as "
        "country suffixes and obvious emirate-name aliases. Broad labels "
        "such as United Arab Emirates are shown as UAE-wide / Unspecified. "
        "Ambiguous districts or place names are preserved rather than guessed."
    ),
    "ⓘ",
)


# ============================================================
# LOCATION METRICS
# ============================================================

jobs_with_location = len(
    location_jobs
)


if len(active_jobs):

    location_coverage = (
        jobs_with_location
        / len(active_jobs)
        * 100
    )

else:

    location_coverage = 0


unique_locations = (
    location_jobs["location_display"]
    .nunique()
)


if not location_counts.empty:

    leading_location = (
        location_counts.index[0]
    )

    leading_location_count = int(
        location_counts.iloc[0]
    )

else:

    leading_location = "Not available"
    leading_location_count = 0


metric_cols = st.columns(4)


with metric_cols[0]:

    market_metric(
        "📍",
        "Location Labels",
        f"{unique_locations:,}",
        (
            "Unique location labels represented among "
            "active HJMI opportunities."
        ),
    )


with metric_cols[1]:

    market_metric(
        "💼",
        "Jobs with Location",
        f"{jobs_with_location:,}",
        (
            "Active opportunities currently containing "
            "usable location information."
        ),
    )


with metric_cols[2]:

    market_metric(
        "📊",
        "Location Coverage",
        f"{location_coverage:.1f}%",
        (
            "Share of active HJMI opportunities currently "
            "containing location information."
        ),
    )


with metric_cols[3]:

    market_metric(
        "◉",
        "Leading Location",
        leading_location,
        (
            f"{leading_location_count:,} active opportunity "
            "record(s) currently use this location label."
        ),
    )


# ============================================================
# UAE LOCATION DISTRIBUTION
# ============================================================

section_header(
    "UAE Opportunity Distribution",
    (
        "Location labels appearing most frequently among "
        "active technology opportunities represented in HJMI."
    ),
    "📍",
)


if location_counts.empty:

    empty_state(
        title="No location information available",
        message=(
            "The current active dataset does not contain "
            "usable location information."
        ),
        icon="📍",
    )

    footer()
    st.stop()


top_locations = (
    location_counts
    .head(10)
    .rename_axis("Location")
    .reset_index(name="Opportunities")
)


hjmi_horizontal_bar(top_locations, "Location", "Opportunities", max_items=10)


info_box(
    "Location distribution",
    (
        "A larger count means more active HJMI opportunity "
        "records currently use that location label. This does "
        "not measure the total number of technology jobs that "
        "exist in the city or emirate."
    ),
    "ⓘ",
)


# ============================================================
# LOCATION EXPLORER
# ============================================================

section_header(
    "Location Explorer",
    (
        "Choose a location to investigate its current "
        "technology opportunity profile."
    ),
    "⌕",
)


available_locations = sorted(
    location_counts.index.tolist(),
    key=lambda value: str(value).lower(),
)


selected_location = st.selectbox(
    "Select a UAE location",
    available_locations,
)


selected_jobs = location_jobs[
    location_jobs["location_display"] == selected_location
].copy()


selected_job_count = len(
    selected_jobs
)


if len(active_jobs):

    selected_share = (
        selected_job_count
        / len(active_jobs)
        * 100
    )

else:

    selected_share = 0


selected_companies = (
    selected_jobs["company"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


selected_roles = (
    selected_jobs["job_title"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


selected_graduate_jobs = selected_jobs[
    selected_jobs[
        "fresh_graduate_friendly"
    ]
].copy()


selected_salary_jobs = int(
    selected_jobs[
        "salary_disclosed"
    ].sum()
)


location_metric_cols = st.columns(4)


with location_metric_cols[0]:

    market_metric(
        "💼",
        "Opportunities",
        f"{selected_job_count:,}",
        (
            "Active HJMI opportunities currently "
            "represented in the selected location."
        ),
    )


with location_metric_cols[1]:

    market_metric(
        "📊",
        "Dataset Opportunity Share",
        f"{selected_share:.1f}%",
        (
            "Share of active HJMI dataset records "
            "represented by this normalized location."
        ),
    )


with location_metric_cols[2]:

    market_metric(
        "🏢",
        "Companies",
        f"{selected_companies:,}",
        (
            "Unique companies represented among "
            "opportunities in this location."
        ),
    )


with location_metric_cols[3]:

    market_metric(
        "🎓",
        "Graduate Friendly",
        f"{len(selected_graduate_jobs):,}",
        (
            "Selected-location opportunities currently "
            "classified as graduate-friendly."
        ),
    )


# ============================================================
# LOCATION SNAPSHOT
# ============================================================

section_header(
    f"{selected_location} Market Snapshot",
    (
        "A quick view of the technology opportunity profile "
        "currently represented for this location."
    ),
    "◈",
)


role_counts = normalized_text_counts(selected_jobs["job_title"])
company_counts = normalized_text_counts(selected_jobs["company"])


selected_skill_counts = skill_counts(
    selected_jobs
)


experience_counts = (
    selected_jobs["experience_level"]
    .fillna("Not Specified")
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


if not selected_skill_counts.empty:

    top_skill = (
        selected_skill_counts.index[0]
    )

    top_skill_count = int(
        selected_skill_counts.iloc[0]
    )

else:

    top_skill = "Not available"
    top_skill_count = 0


if not company_counts.empty:

    top_company = (
        company_counts.index[0]
    )

    top_company_count = int(
        company_counts.iloc[0]
    )

else:

    top_company = "Not available"
    top_company_count = 0


if not experience_counts.empty:

    top_experience = (
        experience_counts.index[0]
    )

    top_experience_count = int(
        experience_counts.iloc[0]
    )

else:

    top_experience = "Not available"
    top_experience_count = 0


snapshot_cols = st.columns(4)


with snapshot_cols[0]:

    insight_card(
        "💻",
        "Most Represented Role",
        top_role,
        (
            f"{top_role_count:,} selected-location listing(s) "
            "currently use this exact title."
        ),
    )


with snapshot_cols[1]:

    insight_card(
        "⚡",
        "Leading Skill",
        top_skill,
        (
            f"{top_skill_count:,} selected-location listing(s) "
            "currently include this identified skill."
        ),
    )


with snapshot_cols[2]:

    insight_card(
        "🏢",
        "Most Represented Company",
        top_company,
        (
            f"{top_company_count:,} selected-location listing(s) "
            "are associated with this company."
        ),
    )


with snapshot_cols[3]:

    insight_card(
        "💼",
        "Most Common Experience",
        top_experience,
        (
            f"{top_experience_count:,} selected-location listing(s) "
            "currently fall into this HJMI classification."
        ),
    )


# ============================================================
# ROLES BY LOCATION
# ============================================================

section_header(
    f"Roles in {selected_location}",
    (
        "Job-title labels most frequently represented among "
        "active opportunities in the selected location."
    ),
    "💻",
)


top_roles = (
    role_counts
    .head(8)
    .rename_axis("Job Role")
    .reset_index(name="Opportunities")
)


if top_roles.empty:

    empty_state(
        title="No role information available",
        message=(
            "No usable job-title information is currently "
            "available for this location."
        ),
        icon="💻",
    )

else:

    hjmi_horizontal_bar(top_roles, "Job Role", "Opportunities", max_items=8)


# ============================================================
# SKILLS BY LOCATION
# ============================================================

section_header(
    f"Skills in {selected_location}",
    (
        "Technology skills identified most frequently among "
        "active opportunities in the selected location."
    ),
    "⚡",
)


top_skills = (
    selected_skill_counts
    .head(8)
    .rename_axis("Skill")
    .reset_index(name="Opportunities")
)


if top_skills.empty:

    empty_state(
        title="No structured skill information available",
        message=(
            "HJMI did not identify structured skills in "
            "the current opportunities for this location."
        ),
        icon="⚡",
    )

else:

    hjmi_horizontal_bar(top_skills, "Skill", "Opportunities", max_items=8)


# ============================================================
# COMPANIES BY LOCATION
# ============================================================

section_header(
    f"Companies Represented in {selected_location}",
    (
        "Companies appearing most frequently among active "
        "HJMI opportunities in the selected location."
    ),
    "🏢",
)


top_companies = (
    company_counts
    .head(8)
    .rename_axis("Company")
    .reset_index(name="Opportunities")
)


if top_companies.empty:

    empty_state(
        title="No company information available",
        message=(
            "No usable company information is currently "
            "available for this location."
        ),
        icon="🏢",
    )

else:

    hjmi_horizontal_bar(top_companies, "Company", "Opportunities", max_items=8)


# ============================================================
# EXPERIENCE BY LOCATION
# ============================================================

section_header(
    f"Experience Requirements in {selected_location}",
    (
        "HJMI experience classifications represented among "
        "active opportunities in the selected location."
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
    selected_jobs["experience_level"]
    .fillna("Not Specified")
    .value_counts()
    .reindex(
        experience_order,
        fill_value=0,
    )
    .rename_axis("Experience Level")
    .reset_index(name="Opportunities")
)


hjmi_horizontal_bar(experience_data, "Experience Level", "Opportunities", max_items=7, height=300)


info_box(
    "Experience information",
    (
        "HJMI does not estimate missing experience requirements. "
        "When the available listing text does not provide a "
        "recognizable requirement, the record remains "
        "Not Specified."
    ),
    "ⓘ",
)


# ============================================================
# GRADUATE OPPORTUNITIES
# ============================================================

section_header(
    f"Graduate Opportunities in {selected_location}",
    (
        "Early-career opportunities currently identified "
        "for the selected location."
    ),
    "🎓",
)


if selected_graduate_jobs.empty:

    empty_state(
        title="No explicit graduate-friendly matches",
        message=(
            "HJMI currently has no active record in this location "
            "that meets its explicit fresh-graduate or entry-level "
            "classification rules. Other jobs may still accept "
            "graduates."
        ),
        icon="🎓",
    )

else:

    graduate_roles = (
        selected_graduate_jobs[
            "job_title"
        ]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    graduate_companies = (
        selected_graduate_jobs[
            "company"
        ]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    graduate_skills = skill_counts(
        selected_graduate_jobs
    )


    graduate_cols = st.columns(3)


    with graduate_cols[0]:

        market_metric(
            "🎓",
            "Graduate Opportunities",
            f"{len(selected_graduate_jobs):,}",
            (
                "Active selected-location opportunities "
                "classified as graduate-friendly."
            ),
        )


    with graduate_cols[1]:

        market_metric(
            "💻",
            "Graduate Roles",
            f"{graduate_roles:,}",
            (
                "Unique job-title labels represented among "
                "graduate-friendly opportunities."
            ),
        )


    with graduate_cols[2]:

        market_metric(
            "🏢",
            "Graduate Companies",
            f"{graduate_companies:,}",
            (
                "Unique companies represented among "
                "graduate-friendly opportunities."
            ),
        )


    if not graduate_skills.empty:

        graduate_skills_df = (
            graduate_skills
            .head(10)
            .rename_axis("Skill")
            .reset_index(
                name="Graduate Opportunities"
            )
        )


        hjmi_horizontal_bar(graduate_skills_df, "Skill", "Graduate Opportunities", max_items=8)


# ============================================================
# SALARY AVAILABILITY
# ============================================================

section_header(
    f"Salary Availability in {selected_location}",
    (
        "How often salary information is available in "
        "the selected location's opportunity records."
    ),
    "💰",
)


salary_not_disclosed = (
    selected_job_count
    - selected_salary_jobs
)


salary_data = pd.DataFrame(
    {
        "Salary Status": [
            "Salary Disclosed",
            "Not Disclosed",
        ],
        "Opportunities": [
            selected_salary_jobs,
            salary_not_disclosed,
        ],
    }
)


hjmi_horizontal_bar(salary_data, "Salary Status", "Opportunities", max_items=2, height=260)


info_box(
    "Salary information",
    (
        "HJMI only treats salary as disclosed when salary "
        "information exists in the collected job record. "
        "It does not create an estimated salary for listings "
        "where the source does not provide one."
    ),
    "💰",
)


# ============================================================
# OPPORTUNITIES
# ============================================================

section_header(
    f"Explore Opportunities in {selected_location}",
    (
        "Browse active technology opportunities currently "
        "represented for the selected location."
    ),
    "↗",
)


result_count(
    len(selected_jobs),
    "matching active opportunities",
)


if selected_jobs.empty:

    empty_state(
        title="No matching opportunities",
        message=(
            "No active HJMI opportunities are currently "
            "represented for this location."
        ),
        icon="⌕",
    )

else:

    latest_jobs = selected_jobs.copy()

    latest_jobs["_sort_date"] = pd.to_datetime(
        latest_jobs["first_seen"],
        errors="coerce",
        utc=True,
    )

    latest_jobs = latest_jobs.sort_values(
        "_sort_date",
        ascending=False,
        na_position="last",
    )


    display_limit = min(
        len(latest_jobs),
        10,
    )


    for _, job in (
        latest_jobs
        .head(display_limit)
        .iterrows()
    ):

        job_card(job)


    if len(latest_jobs) > display_limit:

        st.caption(
            f"Showing {display_limit:,} of "
            f"{len(latest_jobs):,} active opportunities "
            f"currently represented in {selected_location}."
        )


# ============================================================
# METHODOLOGY
# ============================================================

section_header(
    "Location Intelligence Methodology",
    (
        "HJMI keeps geographic analysis tied to location "
        "information available in the collected job records."
    ),
    "ⓘ",
)


info_box(
    "Important limitation",
    (
        "Location labels can vary between listings. HJMI normalizes only "
        "clear UAE variants and country suffixes. Broad UAE-only records are "
        "kept as UAE-wide / Unspecified, while ambiguous districts and place "
        "names remain separate so the platform does not invent geography."
    ),
    "ⓘ",
)


# ============================================================
# FOOTER
# ============================================================

footer()
