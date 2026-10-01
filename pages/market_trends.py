# ============================================================
# HJMI 2.0 — MARKET TRENDS
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
    get_new_jobs,
    get_historical_jobs,
    get_graduate_jobs,
    get_market_metrics,
    skill_counts,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Market Trends | HJMI",
    page_icon="📈",
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
            MARKET TRENDS
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:20px;
        ">
            Track how HJMI's UAE technology opportunity
            dataset changes as new market observations
            are collected over time.
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
        "UAE TECHNOLOGY MARKET",
        "Market Trends",
        (
            "Track changes in technology opportunities "
            "as HJMI builds historical market data."
        ),
    )

    empty_state(
        title="Market trend data is unavailable",
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
new_jobs = get_new_jobs(df)
historical_jobs = get_historical_jobs(df)
graduate_jobs = get_graduate_jobs(active_jobs)


# Convert HJMI tracking dates safely.
tracking_df = df.copy()

tracking_df["_first_seen_dt"] = pd.to_datetime(
    tracking_df["first_seen"],
    errors="coerce",
    utc=True,
)

tracking_df["_last_seen_dt"] = pd.to_datetime(
    tracking_df["last_seen"],
    errors="coerce",
    utc=True,
)

valid_first_seen = tracking_df[
    tracking_df["_first_seen_dt"].notna()
].copy()


# ============================================================
# HEADER
# ============================================================

page_header(
    "UAE TECHNOLOGY MARKET INTELLIGENCE",
    "Market Trends 📈",
    (
        "Explore changes observed by HJMI as technology "
        "opportunities are collected over time, while clearly "
        "separating real historical evidence from analysis that "
        "requires a longer observation period."
    ),
)


data_status(
    metrics["last_update"]
)


info_box(
    "Important: what HJMI means by a trend",
    (
        "A real market trend requires observations across multiple "
        "points in time. HJMI will not treat a single current snapshot "
        "as proof that the UAE job market is increasing, decreasing "
        "or changing direction."
    ),
    "ⓘ",
)


# ============================================================
# CURRENT TRACKING METRICS
# ============================================================

metric_cols = st.columns(4)


with metric_cols[0]:

    market_metric(
        "💼",
        "Active Opportunities",
        f"{len(active_jobs):,}",
        (
            "Opportunities returned in the latest "
            "HJMI market collection."
        ),
    )


with metric_cols[1]:

    market_metric(
        "🆕",
        "Newly Discovered",
        f"{len(new_jobs):,}",
        (
            "Records first discovered by HJMI during "
            "the latest data update."
        ),
    )


with metric_cols[2]:

    market_metric(
        "◷",
        "Historical Records",
        f"{len(historical_jobs):,}",
        (
            "Records retained by HJMI but not returned "
            "in the latest collection."
        ),
    )


with metric_cols[3]:

    market_metric(
        "🎓",
        "Graduate Friendly",
        f"{len(graduate_jobs):,}",
        (
            "Active opportunities currently classified "
            "as graduate-friendly."
        ),
    )


# ============================================================
# HJMI OBSERVATION HISTORY
# ============================================================

section_header(
    "HJMI Observation History",
    (
        "When opportunities were first discovered by HJMI "
        "across the historical records currently retained."
    ),
    "📅",
)


if valid_first_seen.empty:

    empty_state(
        title="Historical dates are not available",
        message=(
            "HJMI does not currently have usable first-seen "
            "dates for temporal analysis."
        ),
        icon="📅",
    )

else:

    first_seen_daily = (
        valid_first_seen
        .assign(
            Observation_Date=valid_first_seen[
                "_first_seen_dt"
            ].dt.date
        )
        .groupby(
            "Observation_Date"
        )
        .size()
        .reset_index(
            name="Jobs First Discovered"
        )
        .sort_values(
            "Observation_Date"
        )
    )


    st.line_chart(
        first_seen_daily,
        x="Observation_Date",
        y="Jobs First Discovered",
        use_container_width=True,
    )


    info_box(
        "How to read this chart",
        (
            "This chart shows when HJMI first discovered records. "
            "It does not show the total number of UAE jobs created "
            "by employers on each date and should not be interpreted "
            "as employer hiring volume."
        ),
        "ⓘ",
    )


# ============================================================
# TRACKING PERIOD
# ============================================================

section_header(
    "Tracking Coverage",
    (
        "How much time is currently represented by HJMI's "
        "first-seen observations."
    ),
    "◷",
)


if valid_first_seen.empty:

    earliest_date = None
    latest_date = None
    tracking_days = 0

else:

    earliest_date = (
        valid_first_seen[
            "_first_seen_dt"
        ].min()
    )

    latest_date = (
        valid_first_seen[
            "_first_seen_dt"
        ].max()
    )

    tracking_days = max(
        (
            latest_date.date()
            - earliest_date.date()
        ).days + 1,
        1,
    )


coverage_cols = st.columns(3)


with coverage_cols[0]:

    insight_card(
        "◷",
        "Observation Window",
        f"{tracking_days:,} day(s)",
        (
            "Calendar span between the earliest and latest "
            "usable HJMI first-seen observations."
        ),
    )


with coverage_cols[1]:

    insight_card(
        "↓",
        "Earliest Observation",
        (
            earliest_date.strftime(
                "%d %b %Y"
            )
            if earliest_date is not None
            else "Not available"
        ),
        (
            "Earliest usable first-seen date currently "
            "retained in the dataset."
        ),
    )


with coverage_cols[2]:

    insight_card(
        "↑",
        "Latest Observation",
        (
            latest_date.strftime(
                "%d %b %Y"
            )
            if latest_date is not None
            else "Not available"
        ),
        (
            "Latest usable first-seen date currently "
            "retained in the dataset."
        ),
    )


# ============================================================
# CURRENT VS HISTORICAL
# ============================================================

section_header(
    "Current vs Historical Opportunity Records",
    (
        "A view of records returned in the latest collection "
        "compared with records retained from previous collections."
    ),
    "◇",
)


status_data = pd.DataFrame(
    {
        "Record Status": [
            "Active",
            "Historical",
        ],
        "Records": [
            len(active_jobs),
            len(historical_jobs),
        ],
    }
)


st.bar_chart(
    status_data,
    x="Record Status",
    y="Records",
    use_container_width=True,
)


info_box(
    "Historical is not confirmed closed",
    (
        "A Historical record is an opportunity that did not appear "
        "in HJMI's latest collection. This does not independently "
        "confirm that the employer has closed the vacancy."
    ),
    "ⓘ",
)


# ============================================================
# NEW OPPORTUNITIES
# ============================================================

section_header(
    "Latest Newly Discovered Opportunities",
    (
        "Opportunity records first discovered by HJMI "
        "during the latest update."
    ),
    "🆕",
)


info_box(
    "New does not mean posted today",
    (
        "HJMI's New label refers to first discovery by the platform. "
        "The employer may have published the opportunity earlier."
    ),
    "ⓘ",
)


if new_jobs.empty:

    empty_state(
        title="No newly discovered records",
        message=(
            "The latest collection did not introduce a job "
            "record that was new to HJMI's existing dataset."
        ),
        icon="✓",
    )

else:

    result_count(
        len(new_jobs),
        "newly discovered opportunities",
    )


    new_jobs_display = new_jobs.copy()

    new_jobs_display["_sort_date"] = pd.to_datetime(
        new_jobs_display["first_seen"],
        errors="coerce",
        utc=True,
    )

    new_jobs_display = (
        new_jobs_display
        .sort_values(
            "_sort_date",
            ascending=False,
            na_position="last",
        )
    )


    for _, job in (
        new_jobs_display
        .head(5)
        .iterrows()
    ):

        job_card(job)


# ============================================================
# SKILL SIGNALS
# ============================================================

section_header(
    "Current Skill Signals",
    (
        "Skills most frequently identified among active "
        "HJMI technology opportunities."
    ),
    "⚡",
)


active_skill_counts = skill_counts(
    active_jobs
)


if active_skill_counts.empty:

    empty_state(
        title="No skill signals available",
        message=(
            "HJMI did not identify structured skill "
            "information in the current active records."
        ),
        icon="⚡",
    )

else:

    current_skills = (
        active_skill_counts
        .head(12)
        .rename_axis("Skill")
        .reset_index(
            name="Active Opportunities"
        )
    )


    st.bar_chart(
        current_skills,
        x="Skill",
        y="Active Opportunities",
        use_container_width=True,
    )


    info_box(
        "Current signal, not yet a trend",
        (
            "This chart describes the current active dataset. "
            "HJMI needs comparable skill observations from multiple "
            "dates before it can reliably describe whether demand "
            "for a skill is rising or falling."
        ),
        "ⓘ",
    )


# ============================================================
# LOCATION SIGNALS
# ============================================================

section_header(
    "Current Location Signals",
    (
        "Location labels most represented among active "
        "technology opportunities."
    ),
    "📍",
)


location_counts = (
    active_jobs["location"]
    .replace("", pd.NA)
    .dropna()
    .value_counts()
    .head(12)
    .rename_axis("Location")
    .reset_index(
        name="Active Opportunities"
    )
)


if location_counts.empty:

    empty_state(
        title="No location signals available",
        message=(
            "No usable location information is currently "
            "available for market analysis."
        ),
        icon="📍",
    )

else:

    st.bar_chart(
        location_counts,
        x="Location",
        y="Active Opportunities",
        use_container_width=True,
    )


# ============================================================
# EXPERIENCE SIGNALS
# ============================================================

section_header(
    "Current Experience Signals",
    (
        "Experience classifications represented among "
        "active HJMI opportunities."
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
    active_jobs["experience_level"]
    .fillna("Not Specified")
    .value_counts()
    .reindex(
        experience_order,
        fill_value=0,
    )
    .rename_axis("Experience Level")
    .reset_index(
        name="Active Opportunities"
    )
)


st.bar_chart(
    experience_data,
    x="Experience Level",
    y="Active Opportunities",
    use_container_width=True,
)


# ============================================================
# GRADUATE SIGNALS
# ============================================================

section_header(
    "Graduate Market Signal",
    (
        "Current representation of explicitly graduate-friendly "
        "opportunities in the active HJMI dataset."
    ),
    "🎓",
)


non_graduate_count = (
    len(active_jobs)
    - len(graduate_jobs)
)


graduate_status = pd.DataFrame(
    {
        "Classification": [
            "Graduate Friendly",
            "Other / Not Explicitly Graduate Friendly",
        ],
        "Active Opportunities": [
            len(graduate_jobs),
            non_graduate_count,
        ],
    }
)


st.bar_chart(
    graduate_status,
    x="Classification",
    y="Active Opportunities",
    use_container_width=True,
)


info_box(
    "Graduate trend limitation",
    (
        "HJMI can describe the current number of opportunities "
        "classified as graduate-friendly. A reliable upward or "
        "downward graduate hiring trend requires repeated historical "
        "snapshots collected using a consistent method."
    ),
    "ⓘ",
)


# ============================================================
# WHAT CAN BE TRACKED NOW
# ============================================================

section_header(
    "Current Trend Readiness",
    (
        "What HJMI can already measure and what requires "
        "additional historical observations."
    ),
    "◇",
)


readiness_cols = st.columns(3)


with readiness_cols[0]:

    insight_card(
        "✓",
        "Available Now",
        "Opportunity History",
        (
            "HJMI retains first-seen, last-seen, Active, "
            "Historical and New information for job records."
        ),
    )


with readiness_cols[1]:

    insight_card(
        "◷",
        "Building Over Time",
        "Market Snapshots",
        (
            "Repeated daily collections will create stronger "
            "evidence for changes in roles, skills, locations "
            "and graduate opportunities."
        ),
    )


with readiness_cols[2]:

    insight_card(
        "→",
        "Future Analysis",
        "Reliable Trends",
        (
            "Once enough comparable history exists, HJMI can "
            "calculate changes between periods instead of "
            "relying on a single snapshot."
        ),
    )


# ============================================================
# FUTURE TREND ENGINE
# ============================================================

section_header(
    "HJMI Trend Intelligence Roadmap",
    (
        "The historical intelligence HJMI is designed "
        "to build as the dataset grows."
    ),
    "📈",
)


roadmap_data = pd.DataFrame(
    {
        "Intelligence Area": [
            "Opportunity Volume",
            "New Job Activity",
            "Skill Demand",
            "Location Activity",
            "Graduate Opportunities",
            "Experience Requirements",
            "Salary Transparency",
        ],
        "Current State": [
            "Current snapshot available",
            "First-seen tracking available",
            "Current signal available",
            "Current signal available",
            "Current signal available",
            "Current signal available",
            "Disclosure tracking available",
        ],
        "Future Trend Capability": [
            "Compare market snapshots over time",
            "Measure discovery activity by period",
            "Compare skill representation over time",
            "Compare location representation over time",
            "Track graduate-friendly representation",
            "Track experience requirement changes",
            "Track salary disclosure and validated values",
        ],
    }
)


st.dataframe(
    roadmap_data,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# METHODOLOGY
# ============================================================

section_header(
    "Market Trends Methodology",
    (
        "HJMI separates observed historical evidence "
        "from conclusions that the current data cannot support."
    ),
    "ⓘ",
)


info_box(
    "Why HJMI is conservative with trends",
    (
        "A change in one collection can result from search coverage, "
        "source availability, listing updates or genuine market "
        "movement. Strong trend analysis requires consistent "
        "collection over time and comparable historical snapshots. "
        "HJMI therefore avoids claiming that a role, skill or city "
        "is rising or falling until the data can support it."
    ),
    "ⓘ",
)


# ============================================================
# FOOTER
# ============================================================

footer()
