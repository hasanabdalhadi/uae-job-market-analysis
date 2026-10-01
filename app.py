import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# HJMI — HASAN JOB MARKET INTELLIGENCE
# UAE Job Market Intelligence Dashboard
# Developed by Hasan R. H. Abdalhadi
# ============================================================


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
# GLOBAL CSS
# ============================================================

st.html("""
<style>

:root {
    --bg-main: #06131f;
    --bg-deep: #04101b;
    --bg-card: #0b2030;
    --gold: #d7ad58;
    --gold-light: #f3d88d;
    --text-main: #f8fafc;
    --text-soft: #9aabba;
    --border: rgba(148, 163, 184, 0.14);
    --green: #00a86b;
}

/* ---------------- APP ---------------- */

.stApp {
    background:
        radial-gradient(
            circle at 88% 4%,
            rgba(0, 115, 47, 0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 10% 25%,
            rgba(37, 99, 235, 0.08),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #04101b 0%,
            #071827 50%,
            #06131f 100%
        );

    color: var(--text-main);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}


/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background:
        radial-gradient(
            circle at 50% 4%,
            rgba(0, 115, 47, 0.08),
            transparent 24%
        ),
        linear-gradient(
            180deg,
            #04121f,
            #061a25 55%,
            #04121f
        );

    border-right: 1px solid var(--border);
}


/* ---------------- LOGO ---------------- */

.hjmi-logo {
    text-align: center;
    padding: 22px 5px 25px;
}

.hjmi-logo-box {
    width: 110px;
    height: 110px;

    margin: 0 auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 30px;

    background:
        radial-gradient(
            circle at 35% 20%,
            rgba(255,255,255,0.07),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            rgba(212,168,83,0.10),
            rgba(5,20,32,0.98)
        );

    border: 1px solid rgba(212,168,83,0.28);

    box-shadow:
        0 16px 45px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.05);
}

.hjmi-h {
    font-family: Georgia, serif;
    font-size: 72px;
    font-weight: bold;

    background:
        linear-gradient(
            120deg,
            #fff4c7,
            #d4a853 40%,
            #ffffff 68%,
            #bd8733
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.uae-line {
    width: 76px;
    height: 4px;

    margin: 13px auto 11px;

    border-radius: 20px;

    background:
        linear-gradient(
            90deg,
            #ce1126 0%,
            #ce1126 25%,
            #ffffff 25%,
            #ffffff 50%,
            #00732f 50%,
            #00732f 75%,
            #111111 75%
        );
}

.hjmi-name {
    color: white;

    font-size: 18px;
    font-weight: 800;

    letter-spacing: 8px;

    padding-left: 8px;
}

.hjmi-small {
    margin-top: 7px;

    color: #7190a5;

    font-size: 8px;

    letter-spacing: 2.3px;
}


/* ---------------- HERO ---------------- */

.hero {
    position: relative;

    overflow: hidden;

    min-height: 335px;

    padding: 52px 50px;

    border-radius: 27px;

    border:
        1px solid rgba(212,168,83,0.24);

    background:
        radial-gradient(
            circle at 88% 28%,
            rgba(0,115,47,0.16),
            transparent 25%
        ),
        radial-gradient(
            circle at 72% 100%,
            rgba(37,99,235,0.12),
            transparent 30%
        ),
        linear-gradient(
            115deg,
            #04111f 0%,
            #072033 58%,
            #08333b 100%
        );

    box-shadow:
        0 22px 70px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

.hero::before {
    content: "";

    position: absolute;

    width: 430px;
    height: 430px;

    border-radius: 50%;

    border:
        1px solid rgba(212,168,83,0.12);

    right: -130px;
    top: -255px;
}

.hero::after {
    content: "";

    position: absolute;

    width: 290px;
    height: 290px;

    border-radius: 50%;

    border:
        1px solid rgba(0,168,107,0.11);

    right: 70px;
    bottom: -220px;
}

.hero-inner {
    position: relative;
    z-index: 2;
}

.hero-kicker {
    color: var(--gold);

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 4px;

    margin-bottom: 15px;
}

.hero-title {
    max-width: 1000px;

    color: white;

    font-size: clamp(37px, 4.2vw, 61px);
    font-weight: 850;

    line-height: 1.05;

    letter-spacing: 0.5px;
}

.hero-title span {
    background:
        linear-gradient(
            90deg,
            #d4a853,
            #fff0b3,
            #d4a853
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 11px;

    color: #cbd5e1;

    font-size: clamp(16px, 2vw, 24px);

    font-weight: 300;

    letter-spacing: 7px;
}

.hero-message {
    max-width: 850px;

    margin-top: 30px;

    color: #dbe4ee;

    font-size: 16px;

    font-style: italic;

    line-height: 1.8;
}

.hero-author {
    margin-top: 13px;

    color: var(--gold);

    font-size: 13px;

    letter-spacing: 2px;
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;

    gap: 9px;

    margin-top: 25px;
}

.hero-pill {
    padding: 8px 14px;

    border-radius: 30px;

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.08);

    color: #dce6ef;

    font-size: 11px;
}


/* ---------------- SECTION ---------------- */

.section-head {
    margin-top: 30px;
    margin-bottom: 17px;
}

.section-kicker {
    color: var(--gold);

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 3.5px;
}

.section-title {
    margin-top: 4px;

    color: #f8fafc;

    font-size: 27px;
    font-weight: 750;
}

.section-desc {
    margin-top: 4px;

    color: #8292a7;

    font-size: 13px;
}


/* ---------------- METRICS ---------------- */

.metric-box {
    min-height: 150px;

    padding: 22px;

    border-radius: 19px;

    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(37,99,235,0.08),
            transparent 35%
        ),
        linear-gradient(
            145deg,
            rgba(14,35,52,0.96),
            rgba(7,24,38,0.98)
        );

    border:
        1px solid rgba(148,163,184,0.13);

    box-shadow:
        0 12px 38px rgba(0,0,0,0.18);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

.metric-box:hover {
    transform: translateY(-2px);

    border-color:
        rgba(212,168,83,0.30);
}

.metric-icon {
    font-size: 26px;
}

.metric-label {
    margin-top: 10px;

    color: #91a3b6;

    font-size: 11px;

    letter-spacing: 0.8px;
}

.metric-number {
    margin-top: 3px;

    color: white;

    font-size: 31px;
    font-weight: 800;
}

.metric-note {
    margin-top: 6px;

    color: #64748b;

    font-size: 10px;
}


/* ---------------- FEATURE CARDS ---------------- */

.feature-card {
    min-height: 175px;

    padding: 24px;

    border-radius: 19px;

    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(0,168,107,0.05),
            transparent 35%
        ),
        linear-gradient(
            145deg,
            rgba(11,31,47,0.94),
            rgba(7,24,37,0.95)
        );

    border:
        1px solid rgba(148,163,184,0.12);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.12);
}

.feature-icon {
    font-size: 25px;
}

.feature-title {
    margin-top: 10px;

    color: white;

    font-size: 17px;
    font-weight: 700;
}

.feature-text {
    margin-top: 7px;

    color: #91a3b6;

    font-size: 13px;

    line-height: 1.7;
}


/* ---------------- STATUS ---------------- */

.status-card {
    margin-top: 20px;

    padding: 22px;

    border-radius: 17px;

    background:
        linear-gradient(
            90deg,
            rgba(212,168,83,0.07),
            rgba(16,185,129,0.035)
        );

    border:
        1px solid rgba(212,168,83,0.20);

    color: #dbe4ee;

    font-size: 13px;

    line-height: 1.7;
}

.status-card strong {
    color: #f7d98a;
}


/* ---------------- ABOUT ---------------- */

.about-card {
    min-height: 190px;

    padding: 25px;

    border-radius: 19px;

    background:
        linear-gradient(
            145deg,
            rgba(11,31,47,0.94),
            rgba(7,24,37,0.95)
        );

    border:
        1px solid rgba(148,163,184,0.12);
}

.about-title {
    color: white;

    font-size: 18px;
    font-weight: 700;

    margin-bottom: 10px;
}

.about-text {
    color: #91a3b6;

    font-size: 13px;

    line-height: 1.75;
}

.developer {
    margin-top: 18px;

    padding: 25px;

    border-radius: 19px;

    background:
        linear-gradient(
            120deg,
            rgba(212,168,83,0.06),
            rgba(7,28,43,0.94)
        );

    border:
        1px solid rgba(212,168,83,0.17);
}

.developer-name {
    color: white;

    font-size: 20px;
    font-weight: 700;
}

.developer-role {
    margin-top: 4px;

    color: var(--gold);

    font-size: 11px;

    letter-spacing: 2px;
}

.developer-details {
    margin-top: 10px;

    color: #91a3b6;

    font-size: 12px;

    line-height: 1.7;
}


/* ---------------- FOOTER ---------------- */

.hjmi-footer {
    margin-top: 50px;

    padding: 30px 10px 8px;

    text-align: center;

    border-top:
        1px solid rgba(148,163,184,0.12);

    color: #60768a;

    font-size: 11px;

    line-height: 1.9;
}

.footer-name {
    color: var(--gold);

    font-size: 13px;
    font-weight: 700;

    letter-spacing: 1px;
}


/* ---------------- STREAMLIT ---------------- */

div[data-testid="stDataFrame"] {
    border:
        1px solid rgba(148,163,184,0.12);

    border-radius: 16px;

    overflow: hidden;
}

hr {
    border-color:
        rgba(148,163,184,0.12) !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ---------------- RESPONSIVE ---------------- */

@media (max-width: 800px) {

    .hero {
        padding: 35px 25px;
    }

    .hero-title {
        font-size: 36px;
    }

    .hero-subtitle {
        letter-spacing: 3px;
    }

}

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="hjmi-logo">

        <div class="hjmi-logo-box">
            <div class="hjmi-h">H</div>
        </div>

        <div class="uae-line"></div>

        <div class="hjmi-name">
            HJMI
        </div>

        <div class="hjmi-small">
            HASAN JOB MARKET INTELLIGENCE
        </div>

    </div>
    """)

    st.markdown("### 🏠 Navigation")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Job Analysis",
            "Skills Analysis",
            "Location Analysis",
            "Salary Analysis",
            "Data Explorer",
            "About",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### 🎯 Project Focus")

    st.caption(
        "Exploring technology job-market data "
        "to transform raw information into clear "
        "and useful career insights."
    )

    st.divider()

    st.markdown("### 🇦🇪 UAE Focus")

    st.caption(
        "Technology • Data • Careers • Opportunities"
    )


# ============================================================
# DATA
# ============================================================

DATA_FILE = Path(
    "data/uae_tech_jobs_clean.csv"
)


@st.cache_data
def load_data():

    if not DATA_FILE.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(DATA_FILE)

    except Exception:
        return pd.DataFrame()


df = load_data()


def normalize_boolean_series(series):
    """Normalize boolean values loaded from CSV safely."""
    return (
        series.fillna(False).astype(str).str.strip().str.lower()
        .isin(["true", "1", "yes", "y"])
    )


if not df.empty:
    if "is_active" in df.columns:
        df["is_active"] = normalize_boolean_series(df["is_active"])
    else:
        df["is_active"] = True

    if "is_new" in df.columns:
        df["is_new"] = normalize_boolean_series(df["is_new"])
    else:
        df["is_new"] = False

    if "status" not in df.columns:
        df["status"] = df["is_active"].map({True: "Active", False: "Inactive"})

    active_df = df[df["is_active"]].copy()
    inactive_df = df[~df["is_active"]].copy()
else:
    active_df = pd.DataFrame()
    inactive_df = pd.DataFrame()


# ============================================================
# COMPONENTS
# ============================================================

def section(
    kicker,
    title,
    description,
):

    st.html(
        f"""
        <div class="section-head">

            <div class="section-kicker">
                {kicker}
            </div>

            <div class="section-title">
                {title}
            </div>

            <div class="section-desc">
                {description}
            </div>

        </div>
        """
    )


def metric(
    icon,
    label,
    value,
    note,
):

    st.html(
        f"""
        <div class="metric-box">

            <div class="metric-icon">
                {icon}
            </div>

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-number">
                {value}
            </div>

            <div class="metric-note">
                {note}
            </div>

        </div>
        """
    )


def pending():

    st.html("""
    <div class="status-card">

        🛠️
        <strong>
            Data pipeline ready.
        </strong>

        <br><br>

        The HJMI interface is active.
        Market statistics and visualizations
        will appear after the UAE technology
        dataset has been processed and validated.

        <br><br>

        No placeholder market statistics are
        presented as real results.

    </div>
    """)


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-inner">

        <div class="hero-kicker">
            ◇ DATA ANALYSIS PROJECT • UNITED ARAB EMIRATES
        </div>

        <div class="hero-title">
            UAE JOB MARKET
            <span>INTELLIGENCE</span>
            🇦🇪
        </div>

        <div class="hero-subtitle">
            DATA • TECHNOLOGY • OPPORTUNITIES
        </div>

        <div class="hero-message">
            “Turning job market data into clear insights
            that help people understand where technology
            opportunities are heading.”
        </div>

        <div class="hero-author">
            — Hasan R. H. Abdalhadi —
        </div>

        <div class="hero-pills">

            <div class="hero-pill">
                📍 UAE Tech Opportunities
            </div>

            <div class="hero-pill">
                📊 Data-Driven Analysis
            </div>

            <div class="hero-pill">
                💻 Computer Science
            </div>

        </div>

    </div>

</div>
""")


# ============================================================
# CALCULATE REAL METRICS
# ============================================================

if df.empty:
    active_jobs = "—"
    new_jobs = "—"
    jobs_collected = "—"
    unique_titles = "—"
    skills_total = "—"
    location_total = "—"
    last_updated = "Not available"
else:
    active_jobs = f"{len(active_df):,}"
    new_jobs = f"{int(df['is_new'].sum()):,}"
    jobs_collected = f"{len(df):,}"
    market_df = active_df if not active_df.empty else df

    unique_titles = f"{market_df['job_title'].nunique():,}" if "job_title" in market_df.columns else "—"

    if "location" in market_df.columns:
        valid_locations = market_df["location"].replace("", pd.NA).dropna()
        location_total = f"{valid_locations.nunique():,}"
    else:
        location_total = "—"

    if "skills" in market_df.columns:
        skill_set = set()
        for item in market_df["skills"].dropna():
            for skill in str(item).split(","):
                skill = skill.strip()
                if skill:
                    skill_set.add(skill)
        skills_total = f"{len(skill_set):,}"
    else:
        skills_total = "—"

    update_column = "last_seen" if "last_seen" in df.columns else ("fetched_at" if "fetched_at" in df.columns else None)
    if update_column:
        update_values = pd.to_datetime(df[update_column], errors="coerce", utc=True).dropna()
        last_updated = update_values.max().strftime("%d %b %Y • %H:%M UTC") if not update_values.empty else "Not available"
    else:
        last_updated = "Not available"


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    section(
        "✦ MARKET OVERVIEW",
        "UAE Technology Job Market",
        "A data-driven view of technology "
        "opportunities represented in the dataset.",
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric("💼", "ACTIVE JOBS", active_jobs, "Seen in the latest market check")

    with c2:
        metric("🆕", "NEW JOBS", new_jobs, "First discovered in the latest update")

    with c3:
        metric("📚", "JOBS COLLECTED", jobs_collected, "Historical technology jobs stored")

    with c4:
        metric("📍", "UAE LOCATIONS", location_total, "Active locations represented")

    st.html(
        f"""
        <div class="status-card">
            🔄 <strong>Last Data Update:</strong> {last_updated}
            <br><br>
            🧑‍💻 <strong>Active Job Titles:</strong> {unique_titles}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            ⚡ <strong>Skills Identified:</strong> {skills_total}
        </div>
        """
    )

    section(
        "◈ INTELLIGENCE CENTER",
        "Explore the Market",
        "Explore jobs, skills, locations "
        "and career information from different perspectives.",
    )

    a, b, c = st.columns(3)

    with a:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                📈
            </div>

            <div class="feature-title">
                Job Analysis
            </div>

            <div class="feature-text">
                Explore technology roles and patterns
                represented across the UAE job-market data.
            </div>

        </div>
        """)

    with b:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                ⚡
            </div>

            <div class="feature-title">
                Skills Intelligence
            </div>

            <div class="feature-text">
                Discover programming languages,
                technologies and technical skills
                identified from job information.
            </div>

        </div>
        """)

    with c:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                📍
            </div>

            <div class="feature-title">
                Location Insights
            </div>

            <div class="feature-text">
                Understand where technology
                opportunities represented in the
                dataset are located across the UAE.
            </div>

        </div>
        """)

    if df.empty:
        pending()


# ============================================================
# JOB ANALYSIS
# ============================================================

elif page == "Job Analysis":

    section(
        "✦ JOB ANALYSIS",
        "Technology Roles & Market Patterns",
        "Explore technology-related roles "
        "identified in the processed dataset.",
    )

    if df.empty:

        pending()

    elif "job_title" in df.columns:

        analysis_df = active_df if not active_df.empty else df

        top_jobs = (
            analysis_df["job_title"]
            .dropna()
            .value_counts()
            .head(15)
        )

        st.markdown("#### 📊 Most Represented Job Titles")

        st.bar_chart(
            top_jobs,
            horizontal=True,
        )


# ============================================================
# SKILLS
# ============================================================

elif page == "Skills Analysis":

    section(
        "◈ SKILLS INTELLIGENCE",
        "Technology Skills",
        "Explore technologies and technical "
        "skills identified in job information.",
    )

    if df.empty:

        pending()

    elif "skills" in df.columns:

        analysis_df = active_df if not active_df.empty else df

        skills = (
            analysis_df["skills"]
            .dropna()
            .str.split(",")
            .explode()
            .str.strip()
        )

        skills = skills[
            skills != ""
        ]

        top_skills = (
            skills
            .value_counts()
            .head(15)
        )

        st.markdown(
            "#### ⚡ Most Frequently Identified Skills"
        )

        st.bar_chart(
            top_skills,
            horizontal=True,
        )


# ============================================================
# LOCATION
# ============================================================

elif page == "Location Analysis":

    section(
        "⌖ LOCATION INTELLIGENCE",
        "Where Are the Opportunities?",
        "Explore the geographic distribution "
        "of technology roles represented in the dataset.",
    )

    if df.empty:

        pending()

    elif "location" in df.columns:

        analysis_df = active_df if not active_df.empty else df

        locations = (
            analysis_df["location"]
            .replace("", pd.NA)
            .dropna()
            .value_counts()
            .head(15)
        )

        st.markdown(
            "#### 📍 Most Represented Locations"
        )

        st.bar_chart(
            locations,
            horizontal=True,
        )


# ============================================================
# SALARY
# ============================================================

elif page == "Salary Analysis":

    section(
        "◇ SALARY INTELLIGENCE",
        "Compensation Insights",
        "Compensation analysis is presented only when reliable salary information is available in the source data.",
    )

    if df.empty or "salary" not in df.columns:
        pending()
    else:
        salary_values = df["salary"].fillna("").astype(str).str.strip()
        salary_values = salary_values[~salary_values.str.lower().isin(["", "nan", "none", "null"])]

        if salary_values.empty:
            st.html("""
            <div class="status-card">
                💰 <strong>Reliable salary data is not currently available.</strong>
                <br><br>
                HJMI does not estimate or fabricate compensation values. Salary analysis will appear when reliable salary information is available in the source data.
            </div>
            """)
        else:
            st.html(f"""
            <div class="status-card">
                💰 <strong>Salary information detected in {len(salary_values):,} job records.</strong>
                <br><br>
                Salary values require normalization and validation before meaningful comparisons are presented.
            </div>
            """)


# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    section(
        "⌕ DATA EXPLORER",
        "Explore the Dataset",
        "Search and inspect active and historical technology job records used by HJMI.",
    )

    if df.empty:
        pending()
    else:
        filter_col, search_col = st.columns([1, 2])

        with filter_col:
            status_filter = st.selectbox(
                "📌 Job status",
                ["Active Jobs", "All Jobs", "Inactive Jobs", "New Jobs"],
            )

        with search_col:
            search = st.text_input(
                "🔎 Search dataset",
                placeholder="Search job title, company, location or skill...",
            )

        if status_filter == "Active Jobs":
            filtered = df[df["is_active"]].copy()
        elif status_filter == "Inactive Jobs":
            filtered = df[~df["is_active"]].copy()
        elif status_filter == "New Jobs":
            filtered = df[df["is_new"]].copy()
        else:
            filtered = df.copy()

        if search:
            search_lower = search.lower()
            mask = filtered.astype(str).apply(
                lambda row: row.str.lower().str.contains(search_lower, regex=False).any(),
                axis=1,
            )
            filtered = filtered[mask]

        st.caption(f"{len(filtered):,} records displayed")

        preferred_columns = [
            "status", "is_new", "job_title", "company", "location",
            "skills", "salary", "publication_date", "first_seen",
            "last_seen", "job_url", "source",
        ]
        display_columns = [c for c in preferred_columns if c in filtered.columns]

        st.dataframe(
            filtered[display_columns],
            width="stretch",
            hide_index=True,
        )


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    section(
        "✦ ABOUT HJMI",
        "Hasan Job Market Intelligence",
        "A Computer Science and data-analysis "
        "project focused on technology "
        "opportunities in the UAE.",
    )

    left, right = st.columns([1.3, 1])

    with left:

        st.html("""
        <div class="about-card">

            <div class="about-title">
                🎯 Project Purpose
            </div>

            <div class="about-text">

                HJMI explores job-market data and
                transforms raw information into
                clearer insights about technology
                roles, skills, locations and career
                opportunities represented in the UAE.

                <br><br>

                The project combines data acquisition,
                cleaning, analysis, visualization
                and dashboard development into one
                practical workflow.

            </div>

        </div>
        """)

    with right:

        st.html("""
        <div class="about-card">

            <div class="about-title">
                🧰 Technology Stack
            </div>

            <div class="about-text">

                🐍 Python
                <br><br>
                📊 Pandas
                <br><br>
                📈 Data Visualization
                <br><br>
                🖥️ Streamlit
                <br><br>
                💻 GitHub

            </div>

        </div>
        """)

    st.html("""
    <div class="developer">

        <div class="developer-name">
            Hasan R. H. Abdalhadi
        </div>

        <div class="developer-role">
            COMPUTER SCIENCE ENGINEERING
        </div>

        <div class="developer-details">

            BITS Pilani – Dubai Campus

            <br>

            Information Systems • Software •
            Data • Digital Technologies

        </div>

    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="hjmi-footer">

    <div class="footer-name">
        HJMI — HASAN JOB MARKET INTELLIGENCE
    </div>

    UAE Job Market Data Analysis

    <br>

    Python • Pandas • Data Visualization •
    Streamlit • GitHub

    <br><br>

    Designed & Developed by
    Hasan R. H. Abdalhadi

</div>
""")
