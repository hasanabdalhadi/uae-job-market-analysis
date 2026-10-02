# ============================================================
# HJMI 2.0 — SALARY INTELLIGENCE
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
)



# ============================================================
# SALARY DISPLAY HELPERS
# ============================================================

def normalized_text_counts(series):
    """Collapse case/spacing duplicates without changing the underlying records."""
    cleaned = series.fillna("").astype(str).map(lambda x: " ".join(x.strip().split()))
    cleaned = cleaned[cleaned.ne("")]
    if cleaned.empty:
        return pd.Series(dtype="int64")
    frame = pd.DataFrame({"label": cleaned})
    frame["key"] = frame["label"].str.casefold()
    grouped = frame.groupby("key", sort=False)
    counts = grouped.size()
    labels = grouped["label"].agg(
        lambda values: max(
            values.tolist(),
            key=lambda x: (sum(ch.isupper() for ch in x), len(x)),
        )
    )
    return pd.Series(counts.values, index=labels.values, dtype="int64").sort_values(ascending=False)


def hjmi_horizontal_bar(data, label_col, value_col="Opportunities", *, max_items=8, height=None):
    """Compact HJMI count chart. This visualizes records, not salary amounts."""
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
        height = max(250, min(410, 75 + len(chart_data) * 38))
    fig = px.bar(
        chart_data, x=value_col, y=label_col, orientation="h",
        text=value_col, custom_data=[label_col, value_col],
    )
    fig.update_traces(
        marker_color="#d8ad57",
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=f"<b>%{{customdata[0]}}</b><br>{value_col}: %{{customdata[1]:,.0f}}<extra></extra>",
    )
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=42, t=8, b=35),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#eaf2f8"),
        xaxis_title=value_col,
        yaxis_title=None,
        showlegend=False,
    )
    fig.update_xaxes(
        rangemode="tozero",
        gridcolor="rgba(117,139,157,0.16)",
        zeroline=False,
        tickmode="linear",
        tick0=0,
        dtick=tick_step,
        tickformat=",d",
    )
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "displaylogo": False,
                "responsive": True, "scrollZoom": False},
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


hjmi_horizontal_bar(
    salary_status_data,
    "Salary Status",
    "Opportunities",
    max_items=2,
    height=250,
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
    "Salary Disclosure Snapshot",
    (
        "A descriptive view of where salary-disclosed records "
        "currently appear in the dataset."
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

    company_counts = normalized_text_counts(
        salary_jobs["company"]
    )


    location_counts = (
        salary_jobs["location"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
    )


    role_counts = normalized_text_counts(
        salary_jobs["job_title"]
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
    "Salary Disclosure Coverage by Location",
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
        .head(8)
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

        hjmi_horizontal_bar(
            salary_by_location,
            "Location",
            "Salary-Disclosed Jobs",
            max_items=8,
        )


# ============================================================
# SALARY BY ROLE
# ============================================================

section_header(
    "Salary Disclosure Coverage by Role",
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
        role_counts
        .head(8)
        .rename_axis("Job Role")
        .reset_index(name="Salary-Disclosed Jobs")
    )


    if not salary_by_role.empty:

        hjmi_horizontal_bar(
            salary_by_role,
            "Job Role",
            "Salary-Disclosed Jobs",
            max_items=8,
        )


# ============================================================
# SALARY BY COMPANY
# ============================================================

section_header(
    "Salary Disclosure Coverage by Company",
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
        company_counts
        .head(8)
        .rename_axis("Company")
        .reset_index(name="Salary-Disclosed Jobs")
    )


    if not salary_by_company.empty:

        hjmi_horizontal_bar(
            salary_by_company,
            "Company",
            "Salary-Disclosed Jobs",
            max_items=8,
        )


# ============================================================
# SALARY BY EXPERIENCE
# ============================================================

section_header(
    "Salary Disclosure Coverage by Experience",
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


hjmi_horizontal_bar(
    salary_experience,
    "Experience Level",
    "Salary-Disclosed Jobs",
    max_items=7,
    height=300,
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

with st.expander("Future salary analytics", expanded=False):
    st.markdown(
        """
        HJMI will add salary-range comparisons only after disclosed values can be
        normalized reliably across currency, pay period and range formats. Until
        then, this page measures **salary disclosure coverage**, not compensation
        levels, and does not estimate missing salaries.
        """
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
