# ============================================================
# HJMI 2.0 — SALARY INTELLIGENCE
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
    get_market_metrics,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Salary Intelligence | HJMI",
    page_icon="💰",
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
            SALARY INTELLIGENCE
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:20px;
        ">
            Explore salary transparency across UAE
            technology opportunities without inventing
            or estimating missing salary information.
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
        "UAE TECHNOLOGY COMPENSATION",
        "Salary Intelligence",
        (
            "Explore salary information available "
            "across HJMI opportunity records."
        ),
    )

    empty_state(
        title="Salary data is unavailable",
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

salary_jobs = active_jobs[
    active_jobs["salary_disclosed"]
].copy()

undisclosed_jobs = active_jobs[
    ~active_jobs["salary_disclosed"]
].copy()


# ============================================================
# HEADER
# ============================================================

page_header(
    "UAE TECHNOLOGY SALARY INTELLIGENCE",
    "Salary Intelligence 💰",
    (
        "Understand salary transparency across active UAE "
        "technology opportunities while keeping disclosed "
        "salary information separate from missing salary data."
    ),
)


data_status(
    metrics["last_update"]
)


info_box(
    "HJMI salary principle",
    (
        "HJMI does not invent a salary when an employer or source "
        "listing does not provide one. Missing salary information "
        "is displayed as 'To be discussed after the interview' "
        "rather than being replaced with an estimated market value."
    ),
    "💰",
)


# ============================================================
# SALARY METRICS
# ============================================================

active_count = len(active_jobs)
salary_count = len(salary_jobs)
undisclosed_count = len(undisclosed_jobs)


if active_count:

    disclosure_rate = (
        salary_count
        / active_count
        * 100
    )

else:

    disclosure_rate = 0


salary_companies = (
    salary_jobs["company"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


salary_locations = (
    salary_jobs["location"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


metric_cols = st.columns(4)


with metric_cols[0]:

    market_metric(
        "💰",
        "Salary Disclosed",
        f"{salary_count:,}",
        (
            "Active opportunity records currently "
            "containing salary information."
        ),
    )


with metric_cols[1]:

    market_metric(
        "📊",
        "Disclosure Rate",
        f"{disclosure_rate:.1f}%",
        (
            "Share of active HJMI opportunities currently "
            "containing salary information."
        ),
    )


with metric_cols[2]:

    market_metric(
        "◇",
        "Salary Not Disclosed",
        f"{undisclosed_count:,}",
        (
            "Active records where HJMI does not have "
            "salary information from the source listing."
        ),
    )


with metric_cols[3]:

    market_metric(
        "🏢",
        "Companies with Salary Data",
        f"{salary_companies:,}",
        (
            "Unique companies represented among records "
            "with disclosed salary information."
        ),
    )


# ============================================================
# TRANSPARENCY OVERVIEW
# ============================================================

section_header(
    "Salary Transparency Overview",
    (
        "How often salary information appears in the "
        "active opportunity records represented by HJMI."
    ),
    "◈",
)


salary_status_data = pd.DataFrame(
    {
        "Salary Status": [
            "Salary Disclosed",
            "Not Disclosed",
        ],
        "Opportunities": [
            salary_count,
            undisclosed_count,
        ],
    }
)


st.bar_chart(
    salary_status_data,
    x="Salary Status",
    y="Opportunities",
    use_container_width=True,
)


info_box(
    "What 'Not Disclosed' means",
    (
        "It means salary information is not available in the "
        "HJMI record. HJMI does not assume why the information "
        "is missing and does not create a replacement salary."
    ),
    "ⓘ",
)


# ============================================================
# SALARY DATA SNAPSHOT
# ============================================================

section_header(
    "Salary Data Snapshot",
    (
        "A descriptive view of where disclosed salary "
        "information currently appears in the dataset."
    ),
    "💰",
)


if salary_jobs.empty:

    empty_state(
        title="No disclosed salary records available",
        message=(
            "The current active dataset does not contain "
            "salary information that HJMI can analyze."
        ),
        icon="💰",
    )

else:

    company_counts = (
        salary_jobs["company"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
    )


    location_counts = (
        salary_jobs["location"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
    )


    role_counts = (
        salary_jobs["job_title"]
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


    if not location_counts.empty:

        top_location = location_counts.index[0]
        top_location_count = int(
            location_counts.iloc[0]
        )

    else:

        top_location = "Not available"
        top_location_count = 0


    if not role_counts.empty:

        top_role = role_counts.index[0]
        top_role_count = int(
            role_counts.iloc[0]
        )

    else:

        top_role = "Not available"
        top_role_count = 0


    snapshot_cols = st.columns(4)


    with snapshot_cols[0]:

        insight_card(
            "💼",
            "Salary Records",
            f"{salary_count:,}",
            (
                "Active opportunity records containing "
                "salary information."
            ),
        )


    with snapshot_cols[1]:

        insight_card(
            "💻",
            "Most Represented Role",
            top_role,
            (
                f"{top_role_count:,} salary-disclosed record(s) "
                "currently use this exact job-title label."
            ),
        )


    with snapshot_cols[2]:

        insight_card(
            "🏢",
            "Most Represented Company",
            top_company,
            (
                f"{top_company_count:,} salary-disclosed record(s) "
                "are currently associated with this company."
            ),
        )


    with snapshot_cols[3]:

        insight_card(
            "📍",
            "Leading Location",
            top_location,
            (
                f"{top_location_count:,} salary-disclosed record(s) "
                "currently use this location label."
            ),
        )


# ============================================================
# SALARY BY LOCATION
# ============================================================

section_header(
    "Salary Transparency by Location",
    (
        "Locations represented among active opportunities "
        "that currently contain salary information."
    ),
    "📍",
)


if salary_jobs.empty:

    empty_state(
        title="Location salary analysis unavailable",
        message=(
            "No disclosed salary records are currently "
            "available for location analysis."
        ),
        icon="📍",
    )

else:

    salary_by_location = (
        salary_jobs["location"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(12)
        .rename_axis("Location")
        .reset_index(name="Salary-Disclosed Jobs")
    )


    if salary_by_location.empty:

        empty_state(
            title="No salary location data available",
            message=(
                "The salary-disclosed records do not contain "
                "usable location information."
            ),
            icon="📍",
        )

    else:

        st.bar_chart(
            salary_by_location,
            x="Location",
            y="Salary-Disclosed Jobs",
            use_container_width=True,
        )


# ============================================================
# SALARY BY ROLE
# ============================================================

section_header(
    "Salary Transparency by Role",
    (
        "Job-title labels most represented among active "
        "records that contain salary information."
    ),
    "💻",
)


if salary_jobs.empty:

    empty_state(
        title="Role salary analysis unavailable",
        message=(
            "No disclosed salary records are currently "
            "available for role analysis."
        ),
        icon="💻",
    )

else:

    salary_by_role = (
        salary_jobs["job_title"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(15)
        .rename_axis("Job Role")
        .reset_index(name="Salary-Disclosed Jobs")
    )


    if not salary_by_role.empty:

        st.bar_chart(
            salary_by_role,
            x="Job Role",
            y="Salary-Disclosed Jobs",
            use_container_width=True,
        )


# ============================================================
# SALARY BY COMPANY
# ============================================================

section_header(
    "Salary Transparency by Company",
    (
        "Companies most represented among active records "
        "that currently contain salary information."
    ),
    "🏢",
)


if salary_jobs.empty:

    empty_state(
        title="Company salary analysis unavailable",
        message=(
            "No disclosed salary records are currently "
            "available for company analysis."
        ),
        icon="🏢",
    )

else:

    salary_by_company = (
        salary_jobs["company"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(15)
        .rename_axis("Company")
        .reset_index(name="Salary-Disclosed Jobs")
    )


    if not salary_by_company.empty:

        st.bar_chart(
            salary_by_company,
            x="Company",
            y="Salary-Disclosed Jobs",
            use_container_width=True,
        )


# ============================================================
# SALARY BY EXPERIENCE
# ============================================================

section_header(
    "Salary Transparency by Experience",
    (
        "Experience classifications represented among active "
        "records that contain salary information."
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


if salary_jobs.empty:

    salary_experience = pd.DataFrame(
        {
            "Experience Level": experience_order,
            "Salary-Disclosed Jobs": [0] * len(
                experience_order
            ),
        }
    )

else:

    salary_experience = (
        salary_jobs["experience_level"]
        .fillna("Not Specified")
        .value_counts()
        .reindex(
            experience_order,
            fill_value=0,
        )
        .rename_axis("Experience Level")
        .reset_index(name="Salary-Disclosed Jobs")
    )


st.bar_chart(
    salary_experience,
    x="Experience Level",
    y="Salary-Disclosed Jobs",
    use_container_width=True,
)


# ============================================================
# ACTUAL SALARY RECORDS
# ============================================================

section_header(
    "Explore Disclosed Salary Records",
    (
        "Review active opportunities where the collected "
        "source record includes salary information."
    ),
    "↗",
)


if salary_jobs.empty:

    empty_state(
        title="No disclosed salaries to display",
        message=(
            "HJMI currently has no active opportunity "
            "with usable salary information."
        ),
        icon="💰",
    )

else:

    salary_search = st.text_input(
        "Search salary-disclosed opportunities",
        placeholder=(
            "Search job title, company, location or salary..."
        ),
    )


    filtered_salary_jobs = salary_jobs.copy()


    if salary_search.strip():

        query = salary_search.strip().lower()

        searchable = (
            filtered_salary_jobs["job_title"].fillna("")
            + " "
            + filtered_salary_jobs["company"].fillna("")
            + " "
            + filtered_salary_jobs["location"].fillna("")
            + " "
            + filtered_salary_jobs["salary_display"].fillna("")
        ).str.lower()


        filtered_salary_jobs = filtered_salary_jobs[
            searchable.str.contains(
                query,
                regex=False,
                na=False,
            )
        ]


    result_count(
        len(filtered_salary_jobs),
        "salary-disclosed opportunities",
    )


    if filtered_salary_jobs.empty:

        empty_state(
            title="No salary records match your search",
            message=(
                "Try a broader search term or clear "
                "the search field."
            ),
            icon="⌕",
        )

    else:

        display_limit = min(
            len(filtered_salary_jobs),
            10,
        )


        for _, job in (
            filtered_salary_jobs
            .head(display_limit)
            .iterrows()
        ):

            job_card(job)


        if len(filtered_salary_jobs) > display_limit:

            st.caption(
                f"Showing {display_limit:,} of "
                f"{len(filtered_salary_jobs):,} "
                "salary-disclosed opportunities."
            )


# ============================================================
# JOBS WITHOUT DISCLOSED SALARY
# ============================================================

section_header(
    "Opportunities Without Disclosed Salary",
    (
        "Active opportunities where salary information "
        "is not available in the HJMI source record."
    ),
    "◇",
)


info_box(
    "HJMI display convention",
    (
        "For these records, HJMI displays "
        "'Salary: To be discussed after the interview'. "
        "This is an HJMI presentation convention for missing "
        "salary data and should not be interpreted as a direct "
        "statement from the employer."
    ),
    "ⓘ",
)


result_count(
    len(undisclosed_jobs),
    "opportunities without disclosed salary",
)


if not undisclosed_jobs.empty:

    for _, job in (
        undisclosed_jobs
        .head(5)
        .iterrows()
    ):

        job_card(job)


    if len(undisclosed_jobs) > 5:

        st.caption(
            f"Showing 5 of {len(undisclosed_jobs):,} "
            "opportunities without disclosed salary."
        )


# ============================================================
# FUTURE SALARY ANALYTICS
# ============================================================

section_header(
    "Salary Intelligence Roadmap",
    (
        "What HJMI can analyze as salary data becomes "
        "more structured and reliable."
    ),
    "◇",
)


roadmap_cols = st.columns(3)


with roadmap_cols[0]:

    insight_card(
        "1",
        "Normalize",
        "Salary Formats",
        (
            "Convert reliable disclosed salary values into "
            "consistent AED periods without changing the "
            "original source information."
        ),
    )


with roadmap_cols[1]:

    insight_card(
        "2",
        "Compare",
        "Comparable Records",
        (
            "Analyze salary ranges by role, location and "
            "experience only when enough comparable records "
            "are available."
        ),
    )


with roadmap_cols[2]:

    insight_card(
        "3",
        "Track",
        "Salary Trends",
        (
            "Measure changes over time after HJMI builds "
            "sufficient historical salary observations."
        ),
    )


# ============================================================
# METHODOLOGY
# ============================================================

section_header(
    "Salary Intelligence Methodology",
    (
        "Salary analysis is intentionally conservative "
        "to avoid presenting unsupported compensation figures."
    ),
    "ⓘ",
)


info_box(
    "Current limitation",
    (
        "HJMI currently treats the source salary field as "
        "descriptive text. Salary formats may differ by currency, "
        "period, range and wording. Until those values are "
        "normalized and validated, HJMI does not calculate "
        "average, median, minimum or maximum market salaries."
    ),
    "ⓘ",
)


# ============================================================
# FOOTER
# ============================================================

footer()
