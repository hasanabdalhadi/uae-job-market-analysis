# ============================================================
# HJMI 2.0 — HOME & MARKET OVERVIEW
# Hasan Job Market Intelligence
# ============================================================

import pandas as pd
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

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.2rem;
        max-width: 1450px;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.70rem;
    }

    .hjmi-home-hero {
        position: relative;
        overflow: hidden;
        padding: 34px 36px;
        margin: 4px 0 12px 0;
        border-radius: 24px;
        border: 1px solid rgba(216,173,87,0.18);
        background:
            radial-gradient(circle at 88% 12%, rgba(216,173,87,0.12), transparent 30%),
            linear-gradient(135deg, rgba(13,45,55,0.96), rgba(6,25,34,0.98));
        box-shadow: 0 20px 55px rgba(0,0,0,0.20);
    }

    .hjmi-home-kicker {
        color: #d8ad57;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2.2px;
        margin-bottom: 12px;
    }

    .hjmi-home-title {
        color: #f7f9fa;
        font-size: clamp(32px, 4vw, 54px);
        line-height: 1.04;
        font-weight: 820;
        letter-spacing: -1.7px;
        max-width: 900px;
    }

    .hjmi-home-title span {
        color: #e2b95e;
    }

    .hjmi-home-copy {
        color: #a8bac6;
        font-size: 14px;
        line-height: 1.75;
        max-width: 820px;
        margin-top: 16px;
    }

    .hjmi-home-proof {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 22px;
    }

    .hjmi-home-pill {
        color: #c9d6dd;
        font-size: 10px;
        font-weight: 650;
        padding: 7px 10px;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.13);
        background: rgba(255,255,255,0.025);
    }

    .hjmi-section-note {
        color: #758b9d;
        font-size: 11px;
        line-height: 1.7;
        margin: -3px 0 5px 0;
    }

    .hjmi-start-card {
        height: 100%;
        min-height: 142px;
        padding: 18px;
        border-radius: 17px;
        border: 1px solid rgba(148,163,184,0.12);
        background: linear-gradient(145deg, rgba(12,42,51,0.82), rgba(8,29,38,0.86));
    }

    .hjmi-start-label {
        color: #d8ad57;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }

    .hjmi-start-title {
        color: #f2f5f6;
        font-size: 15px;
        font-weight: 760;
        margin-bottom: 7px;
    }

    .hjmi-start-copy {
        color: #7f95a3;
        font-size: 10px;
        line-height: 1.65;
    }


    @media (max-width: 800px) {
        .hjmi-home-hero {
            padding: 25px 22px;
            border-radius: 19px;
        }

        .hjmi-home-title {
            font-size: 34px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD MARKET DATA
# ============================================================

df = load_jobs()

if df.empty:
    st.markdown(
        """
        <div class="hjmi-home-hero">
            <div class="hjmi-home-kicker">UAE TECHNOLOGY CAREER INTELLIGENCE</div>
            <div class="hjmi-home-title">
                Understand the market.<br>
                <span>Build a stronger career.</span>
            </div>
            <div class="hjmi-home-copy">
                HJMI connects UAE technology job discovery with market and
                career intelligence in one focused platform.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    empty_state(
        title="Market data is currently unavailable",
        message=(
            "HJMI could not load the UAE technology job-market dataset. "
            "Please check the data pipeline and try again."
        ),
        icon="⚠",
    )
    footer()
    st.stop()


metrics = get_market_metrics(df)
active_jobs = get_active_jobs(df)
new_jobs = get_new_jobs(df)
graduate_jobs = get_graduate_jobs(active_jobs)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hjmi-home-hero">
        <div class="hjmi-home-kicker">HASAN JOB MARKET INTELLIGENCE • UAE</div>
        <div class="hjmi-home-title">
            Understand the market.<br>
            <span>Build a stronger career.</span>
        </div>
        <div class="hjmi-home-copy">
            HJMI brings UAE technology opportunities, skills, graduate
            intelligence and personalized career tools into one platform —
            helping you move from job searching to informed career discovery.
        </div>
        <div class="hjmi-home-proof">
            <div class="hjmi-home-pill">Live market collection</div>
            <div class="hjmi-home-pill">Career intelligence</div>
            <div class="hjmi-home-pill">Graduate focused</div>
            <div class="hjmi-home-pill">No invented salary data</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

data_status(metrics["last_update"])


# ============================================================
# LIVE MARKET SNAPSHOT
# ============================================================

section_header(
    "Live UAE Market Snapshot",
    "The latest technology opportunity records currently represented by HJMI.",
    "◈",
)

metric_cols = st.columns(4)

with metric_cols[0]:
    market_metric(
        "💼",
        "Active Opportunities",
        f'{metrics["active_jobs"]:,}',
        "Returned in HJMI's latest market collection.",
    )

with metric_cols[1]:
    market_metric(
        "🆕",
        "Newly Discovered",
        f'{metrics["new_jobs"]:,}',
        "First discovered by HJMI in the latest update.",
    )

with metric_cols[2]:
    market_metric(
        "🎓",
        "Graduate Friendly",
        f'{metrics["graduate_jobs"]:,}',
        "Active records with an identified early-career signal.",
    )

with metric_cols[3]:
    market_metric(
        "🏢",
        "Companies",
        f'{metrics["companies"]:,}',
        "Unique companies represented among active records.",
    )


# ============================================================
# CURRENT MARKET SIGNALS
# ============================================================

def normalized_counts(series):
    cleaned = series.fillna("").astype(str).map(lambda x: " ".join(x.strip().split()))
    cleaned = cleaned[cleaned.ne("")]
    if cleaned.empty:
        return None
    frame = cleaned.to_frame("label")
    frame["key"] = frame["label"].str.casefold()
    grouped = frame.groupby("key", sort=False)
    counts = grouped.size()
    labels = grouped["label"].agg(
        lambda values: max(
            values.tolist(),
            key=lambda x: (sum(ch.isupper() for ch in x), len(x)),
        )
    )
    return counts.set_axis(labels.values).sort_values(ascending=False)


role_counts = normalized_counts(active_jobs["job_title"]) if not active_jobs.empty else None
location_counts = normalized_counts(active_jobs["location"]) if not active_jobs.empty else None
skills_rank = skill_counts(active_jobs)

top_role = role_counts.index[0] if role_counts is not None and not role_counts.empty else "Not available"
top_role_count = int(role_counts.iloc[0]) if role_counts is not None and not role_counts.empty else 0

top_location = (
    location_counts.index[0]
    if location_counts is not None and not location_counts.empty
    else "Not available"
)
top_location_count = (
    int(location_counts.iloc[0])
    if location_counts is not None and not location_counts.empty
    else 0
)

top_skill = skills_rank.index[0] if not skills_rank.empty else "Not available"
top_skill_count = int(skills_rank.iloc[0]) if not skills_rank.empty else 0

graduate_share = (
    len(graduate_jobs) / len(active_jobs) * 100
    if len(active_jobs) > 0
    else 0
)

section_header(
    "Current Market Signals",
    "Quick context from the latest active HJMI dataset — descriptive signals, not market forecasts.",
    "⚡",
)

signal_cols = st.columns(4)

with signal_cols[0]:
    insight_card(
        "💻",
        "Most Represented Role",
        top_role,
        f"{top_role_count:,} active record(s) currently use this job-title label.",
    )

with signal_cols[1]:
    insight_card(
        "⚡",
        "Most Identified Skill",
        top_skill,
        f"{top_skill_count:,} active record(s) include this identified skill.",
    )

with signal_cols[2]:
    insight_card(
        "📍",
        "Leading Location",
        top_location,
        f"{top_location_count:,} active record(s) currently use this location label.",
    )

with signal_cols[3]:
    insight_card(
        "🎓",
        "Graduate Dataset Share",
        f"{graduate_share:.1f}%",
        "Share of active HJMI records classified as graduate-friendly.",
    )


# ============================================================
# START WITH HJMI
# ============================================================

section_header(
    "Start with HJMI",
    "Choose the path that matches what you want to do next.",
    "→",
)

start_cols = st.columns(3)

with start_cols[0]:
    with st.container(border=True):
        st.markdown(
            """
            <div class="hjmi-start-label">DISCOVER</div>
            <div class="hjmi-start-title">Find UAE Tech Opportunities</div>
            <div class="hjmi-start-copy">
                Search active opportunities by role, company, location,
                skill and experience.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(
            "pages/find_jobs.py",
            label="Explore Jobs",
            icon="🔎",
            use_container_width=True,
        )

with start_cols[1]:
    with st.container(border=True):
        st.markdown(
            """
            <div class="hjmi-start-label">PERSONALIZE</div>
            <div class="hjmi-start-title">Build Your Career Intelligence</div>
            <div class="hjmi-start-copy">
                Create your career profile to unlock profile matching,
                recommendations and your personal HJMI workspace.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(
            "pages/career_profile.py",
            label="Build Career Profile",
            icon="🎯",
            use_container_width=True,
        )

with start_cols[2]:
    with st.container(border=True):
        st.markdown(
            """
            <div class="hjmi-start-label">EARLY CAREER</div>
            <div class="hjmi-start-title">Explore Graduate Intelligence</div>
            <div class="hjmi-start-copy">
                Focus on explicitly identified graduate-friendly opportunities,
                skills, experience and employers.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(
            "pages/graduate_hub.py",
            label="Open Graduate Hub",
            icon="🎓",
            use_container_width=True,
        )


# ============================================================
# NEW OPPORTUNITIES — COMPACT PREVIEW
# ============================================================

st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

section_header(
    "Latest Discoveries",
    "A small preview of opportunities first discovered by HJMI in the latest update.",
    "🆕",
)

if new_jobs.empty:
    empty_state(
        title="No newly discovered opportunities in this update",
        message=(
            "No record in the latest collection was new to HJMI's existing dataset. "
            "Active opportunities remain available in Find Jobs."
        ),
        icon="✓",
    )
else:
    new_jobs_display = new_jobs.copy()

    if "first_seen" in new_jobs_display.columns:
        new_jobs_display["_sort_date"] = pd.to_datetime(
            new_jobs_display["first_seen"],
            errors="coerce",
            utc=True,
        )
        new_jobs_display = new_jobs_display.sort_values(
            "_sort_date",
            ascending=False,
            na_position="last",
        )

    for _, job in new_jobs_display.head(3).iterrows():
        job_card(job)


st.caption(
    "'Newly Discovered' means first seen by HJMI in the latest update; "
    "it does not necessarily mean the employer posted the vacancy that day."
)


# ============================================================
# PLATFORM INTELLIGENCE — COMPACT
# ============================================================

section_header(
    "Explore Market Intelligence",
    "Go deeper into the parts of the UAE technology market that matter to your search.",
    "◇",
)

area_cols = st.columns(4)

with area_cols[0]:
    feature_card(
        "💼",
        "Jobs",
        "Explore roles, companies and experience requirements in the active dataset.",
        "JOB INTELLIGENCE",
    )
    st.page_link("pages/job_intelligence.py", label="Open", icon="💼", use_container_width=True)

with area_cols[1]:
    feature_card(
        "⚡",
        "Skills",
        "See which structured skills appear across current technology opportunities.",
        "SKILLS INTELLIGENCE",
    )
    st.page_link("pages/skills_intelligence.py", label="Open", icon="⚡", use_container_width=True)

with area_cols[2]:
    feature_card(
        "📍",
        "Locations",
        "Understand how active opportunity records are represented across UAE locations.",
        "LOCATION INTELLIGENCE",
    )
    st.page_link("pages/location_intelligence.py", label="Open", icon="📍", use_container_width=True)

with area_cols[3]:
    feature_card(
        "📈",
        "Trends",
        "Review HJMI discovery history and current signals without overstating trends.",
        "MARKET TRENDS",
    )
    st.page_link("pages/market_trends.py", label="Open", icon="📈", use_container_width=True)


# ============================================================
# TRUST & METHODOLOGY
# ============================================================

with st.expander("How HJMI interprets its data", expanded=False):
    st.markdown(
        """
        **Active** means the opportunity was returned in HJMI's latest collection;
        it is not an independent confirmation that the employer still has the
        vacancy open.

        **Newly Discovered** means HJMI first saw the record during the latest
        update; it does not necessarily mean the employer posted it that day.

        **Historical** means the record is retained by HJMI but was not returned
        in the latest collection; this alone does not prove that the vacancy closed.

        **Graduate Friendly** is assigned only when available listing text contains
        an early-career signal. Missing experience information is not automatically
        treated as graduate-friendly.

        HJMI does not invent missing salary values.
        """
    )
    st.page_link(
        "pages/about.py",
        label="Read About & Methodology",
        icon="ℹ️",
        use_container_width=True,
    )


footer()
