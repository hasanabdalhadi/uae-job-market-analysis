# ============================================================
# HJMI 2.0 — JOB INTELLIGENCE
# Hasan Job Market Intelligence
# ============================================================

import pandas as pd
import plotly.graph_objects as go
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
    get_market_metrics,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Job Intelligence | HJMI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN
# ============================================================

apply_theme()


# ============================================================
# CHART HELPERS
# ============================================================

def horizontal_bar_chart(
    data,
    label_col,
    value_col,
    height=420,
    max_items=10,
):
    """Render a clean HJMI horizontal ranking chart."""

    chart_data = data.copy()

    if max_items:
        chart_data = chart_data.head(max_items)

    chart_data[value_col] = pd.to_numeric(
        chart_data[value_col],
        errors="coerce",
    ).fillna(0)

    chart_data = chart_data.sort_values(
        value_col,
        ascending=True,
    )

    fig = go.Figure(
        go.Bar(
            x=chart_data[value_col],
            y=chart_data[label_col],
            orientation="h",
            text=chart_data[value_col].astype(int),
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                + value_col
                + ": %{x}<extra></extra>"
            ),
        )
    )

    max_value = chart_data[value_col].max()

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=45, t=10, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#0b2631",
            font_size=12,
        ),
        xaxis=dict(
            title=value_col,
            rangemode="tozero",
            gridcolor="rgba(127,150,163,0.14)",
            zeroline=False,
            fixedrange=True,
            range=[
                0,
                max(1, float(max_value) * 1.18),
            ],
        ),
        yaxis=dict(
            title="",
            fixedrange=True,
            automargin=True,
        ),
        font=dict(
            color="#d9e3e7",
            size=12,
        ),
    )

    fig.update_traces(
        marker=dict(
            color="#d8ad57",
            line=dict(
                color="rgba(216,173,87,0.35)",
                width=1,
            ),
        ),
        textfont=dict(
            color="#d9e3e7",
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
        },
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
            JOB INTELLIGENCE
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:20px;
        ">
            Analyze roles, companies, categories,
            experience requirements and opportunity
            patterns across the UAE technology market.
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
        "Job Intelligence",
        (
            "Analyze roles, employers and opportunity "
            "patterns across the HJMI dataset."
        ),
    )

    empty_state(
        title="Job intelligence data is unavailable",
        message=(
            "HJMI could not load the current UAE "
            "technology job-market dataset."
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

historical_jobs = get_historical_jobs(df)


# ============================================================
# HEADER
# ============================================================

page_header(
    "UAE TECHNOLOGY MARKET INTELLIGENCE",
    "Job Intelligence",
    (
        "Explore the roles, companies, categories and experience "
        "requirements represented in HJMI's UAE technology "
        "job-market data."
    ),
)


data_status(
    metrics["last_update"]
)


info_box(
    "What this page measures",
    (
        "Job Intelligence describes the opportunities represented "
        "in HJMI's collected dataset. Counts and rankings reflect "
        "the available HJMI records rather than the entire UAE "
        "employment market."
    ),
    "ⓘ",
)


# ============================================================
# MARKET METRICS
# ============================================================

metric_cols = st.columns(4)


with metric_cols[0]:

    market_metric(
        "💼",
        "Active Opportunities",
        f"{len(active_jobs):,}",
        (
            "Technology opportunities seen in the "
            "latest HJMI market collection."
        ),
    )


with metric_cols[1]:

    market_metric(
        "🆕",
        "New Opportunities",
        f"{len(new_jobs):,}",
        (
            "Opportunities first discovered by HJMI "
            "during the latest update."
        ),
    )


with metric_cols[2]:

    market_metric(
        "◷",
        "Historical Records",
        f"{len(historical_jobs):,}",
        (
            "Records retained by HJMI but not returned "
            "in the latest market collection."
        ),
    )


with metric_cols[3]:

    market_metric(
        "🏢",
        "Active Companies",
        f'{metrics["companies"]:,}',
        (
            "Unique company names represented among "
            "active HJMI opportunities."
        ),
    )


# ============================================================
# MARKET SNAPSHOT
# ============================================================

section_header(
    "Job Market Snapshot",
    (
        "Quick signals from the currently active technology "
        "opportunities represented in HJMI."
    ),
    "◈",
)


# ------------------------------------------------------------
# ROLE COUNTS
# ------------------------------------------------------------

role_counts = (
    active_jobs["job_title"]
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
# COMPANY COUNTS
# ------------------------------------------------------------

company_counts = (
    active_jobs["company"]
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
# CATEGORY COUNTS
# ------------------------------------------------------------

category_counts = (
    active_jobs["category"]
    .replace("", pd.NA)
    .dropna()
    .value_counts()
)


if not category_counts.empty:

    top_category = category_counts.index[0]
    top_category_count = int(
        category_counts.iloc[0]
    )

else:

    top_category = "Not available"
    top_category_count = 0


# ------------------------------------------------------------
# EXPERIENCE COUNTS
# ------------------------------------------------------------

experience_counts = (
    active_jobs["experience_level"]
    .fillna("Not Specified")
    .value_counts()
)


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
            f"{top_role_count:,} active listing(s) "
            "currently use this exact job-title label."
        ),
    )


with snapshot_cols[1]:

    insight_card(
        "🏢",
        "Most Represented Company",
        top_company,
        (
            f"{top_company_count:,} active opportunity "
            "record(s) are associated with this company."
        ),
    )


with snapshot_cols[2]:

    insight_card(
        "◇",
        "Leading Category",
        top_category,
        (
            f"{top_category_count:,} active opportunity "
            "record(s) currently use this category label."
        ),
    )


with snapshot_cols[3]:

    insight_card(
        "💼",
        "Most Common Experience",
        top_experience,
        (
            f"{top_experience_count:,} active listing(s) "
            "currently fall into this HJMI classification."
        ),
    )


# ============================================================
# TOP ROLES
# ============================================================

section_header(
    "Top Roles",
    (
        "The job-title labels appearing most frequently "
        "among active HJMI opportunities."
    ),
    "💻",
)


with st.expander("How HJMI counts roles"):
    st.caption(
        "HJMI counts exact job-title labels. Similar titles such as "
        "Software Engineer and Software Developer may therefore appear "
        "separately rather than being automatically merged."
    )


top_roles = (
    role_counts
    .head(10)
    .rename_axis("Job Role")
    .reset_index(name="Opportunities")
)


if top_roles.empty:

    empty_state(
        title="Role data unavailable",
        message=(
            "No usable job-title information is available "
            "in the current active dataset."
        ),
        icon="💻",
    )

else:

    horizontal_bar_chart(
        top_roles,
        "Job Role",
        "Opportunities",
        height=390,
        max_items=10,
    )


# ============================================================
# COMPANIES HIRING
# ============================================================

section_header(
    "Companies Hiring",
    (
        "Companies most represented among active technology "
        "opportunities currently collected by HJMI."
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
            "No usable company information is available "
            "in the current active dataset."
        ),
        icon="🏢",
    )

else:

    horizontal_bar_chart(
        top_companies,
        "Company",
        "Opportunities",
        height=390,
        max_items=10,
    )


# ============================================================
# EXPERIENCE INTELLIGENCE
# ============================================================

section_header(
    "Experience Requirements",
    (
        "HJMI classifications based on experience information "
        "identified in the available listing text."
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


experience_table = (
    active_jobs["experience_level"]
    .fillna("Not Specified")
    .value_counts()
    .reindex(
        experience_order,
        fill_value=0,
    )
    .rename_axis("Experience Level")
    .reset_index(name="Opportunities")
)


horizontal_bar_chart(
    experience_table,
    "Experience Level",
    "Opportunities",
    height=340,
    max_items=None,
)


with st.expander("How HJMI classifies experience"):
    st.caption(
        "HJMI extracts experience only when a recognizable requirement "
        "appears in the available listing text. Missing requirements "
        "remain Not Specified instead of being estimated."
    )


# ============================================================
# JOB CATEGORIES
# ============================================================

section_header(
    "Job Categories",
    (
        "Category labels represented across active "
        "technology opportunities."
    ),
    "◇",
)


top_categories = (
    category_counts
    .head(10)
    .rename_axis("Category")
    .reset_index(name="Opportunities")
)


if top_categories.empty:

    empty_state(
        title="Category data unavailable",
        message=(
            "No structured category information is available "
            "for the current active records."
        ),
        icon="◇",
    )

else:

    horizontal_bar_chart(
        top_categories,
        "Category",
        "Opportunities",
        height=390,
        max_items=10,
    )


# ============================================================
# NEW ROLE INTELLIGENCE
# ============================================================

section_header(
    "New Opportunity Intelligence",
    (
        "Roles represented among opportunities first discovered "
        "during HJMI's latest market update."
    ),
    "🆕",
)


with st.expander("What does New mean?"):
    st.caption(
        "New refers to when HJMI first discovered the record. "
        "It does not necessarily represent the employer's original "
        "publication date."
    )


if new_jobs.empty:

    empty_state(
        title="No newly discovered opportunities",
        message=(
            "The latest collection did not introduce a record "
            "that was new to HJMI's existing dataset."
        ),
        icon="✓",
    )

else:

    new_role_counts = (
        new_jobs["job_title"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(10)
        .rename_axis("New Role")
        .reset_index(name="Opportunities")
    )


    if not new_role_counts.empty:

        horizontal_bar_chart(
            new_role_counts,
            "New Role",
            "Opportunities",
            height=360,
            max_items=10,
        )


    result_count(
        len(new_jobs),
        "newly discovered opportunities",
    )


    for _, job in (
        new_jobs
        .head(5)
        .iterrows()
    ):

        job_card(job)


# ============================================================
# ACTIVE VS HISTORICAL
# ============================================================

section_header(
    "Active vs Historical Records",
    (
        "Understand the current state of the records "
        "retained by HJMI."
    ),
    "◷",
)


status_data = pd.DataFrame(
    {
        "Status": [
            "Active",
            "Historical",
        ],
        "Records": [
            len(active_jobs),
            len(historical_jobs),
        ],
    }
)


horizontal_bar_chart(
    status_data,
    "Status",
    "Records",
    height=230,
    max_items=None,
)


with st.expander("What does Historical mean?"):
    st.caption(
        "Historical means the opportunity was retained by HJMI but "
        "did not appear in the latest collection. This alone does not "
        "prove that the employer closed the vacancy."
    )


# ============================================================
# ROLE EXPLORER
# ============================================================

section_header(
    "Role Explorer",
    (
        "Choose a job title to investigate the companies, "
        "locations and current opportunities connected to it."
    ),
    "⌕",
)


available_roles = sorted(
    role_counts.index.tolist(),
    key=lambda value: str(value).lower(),
)


if not available_roles:

    empty_state(
        title="No roles available to explore",
        message=(
            "The current active dataset does not contain "
            "usable job-title information."
        ),
        icon="⌕",
    )

else:

    selected_role = st.selectbox(
        "Select a role",
        available_roles,
    )


    role_jobs = active_jobs[
        active_jobs["job_title"]
        == selected_role
    ].copy()


    role_companies = (
        role_jobs["company"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    role_locations = (
        role_jobs["location"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    role_graduate_jobs = int(
        role_jobs[
            "fresh_graduate_friendly"
        ].sum()
    )


    role_salary_jobs = int(
        role_jobs[
            "salary_disclosed"
        ].sum()
    )


    role_metric_cols = st.columns(4)


    with role_metric_cols[0]:

        market_metric(
            "💼",
            "Opportunities",
            f"{len(role_jobs):,}",
            (
                "Active opportunities currently using "
                "this exact job-title label."
            ),
        )


    with role_metric_cols[1]:

        market_metric(
            "🏢",
            "Companies",
            f"{role_companies:,}",
            (
                "Unique companies represented for "
                "the selected role."
            ),
        )


    with role_metric_cols[2]:

        market_metric(
            "📍",
            "Locations",
            f"{role_locations:,}",
            (
                "Unique UAE location labels represented "
                "for the selected role."
            ),
        )


    with role_metric_cols[3]:

        market_metric(
            "🎓",
            "Graduate Friendly",
            f"{role_graduate_jobs:,}",
            (
                "Selected-role listings currently classified "
                "as fresh-graduate friendly."
            ),
        )


    st.caption(
        f"{role_salary_jobs:,} selected-role opportunity "
        "record(s) currently include salary information."
    )


    result_count(
        len(role_jobs),
        "matching active opportunities",
    )


    for _, job in (
        role_jobs
        .head(10)
        .iterrows()
    ):

        job_card(job)


    if len(role_jobs) > 10:

        st.caption(
            f"Showing 10 of {len(role_jobs):,} "
            "matching active opportunities."
        )


# ============================================================
# CURRENT OPPORTUNITIES
# ============================================================

section_header(
    "Latest Active Opportunities",
    (
        "A sample of technology opportunities represented "
        "in HJMI's latest market collection."
    ),
    "↗",
)


if active_jobs.empty:

    empty_state(
        title="No active opportunities available",
        message=(
            "No active records are currently represented "
            "in the HJMI dataset."
        ),
        icon="💼",
    )

else:

    latest_active = active_jobs.copy()

    latest_active["_sort_date"] = pd.to_datetime(
        latest_active["first_seen"],
        errors="coerce",
        utc=True,
    )


    latest_active = latest_active.sort_values(
        "_sort_date",
        ascending=False,
        na_position="last",
    )


    for _, job in (
        latest_active
        .head(5)
        .iterrows()
    ):

        job_card(job)


# ============================================================
# METHODOLOGY
# ============================================================

section_header(
    "Job Intelligence Methodology",
    (
        "HJMI keeps analysis tied to the information "
        "available in its collected records."
    ),
    "ⓘ",
)


info_box(
    "Market representation",
    (
        "HJMI analyzes the jobs returned through its configured "
        "collection process. Results should be interpreted as "
        "signals from the HJMI dataset rather than a complete "
        "census of every technology vacancy in the UAE."
    ),
    "ⓘ",
)


# ============================================================
# FOOTER
# ============================================================

footer()
