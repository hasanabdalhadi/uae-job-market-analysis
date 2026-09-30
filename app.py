import streamlit as st
import pandas as pd
from pathlib import Path
from textwrap import dedent


# ============================================================
# HJMI — HASAN JOB MARKET INTELLIGENCE
# UAE Job Market Data Analysis Dashboard
# Developed by Hasan R. H. Abdalhadi
# ============================================================


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HJMI | UAE Job Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML HELPER
# Prevents Streamlit from displaying HTML as a code block
# ============================================================

def html(content):
    st.markdown(
        dedent(content).strip(),
        unsafe_allow_html=True,
    )


# ============================================================
# GLOBAL DESIGN
# ============================================================

html("""
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 88% 3%,
            rgba(0, 115, 47, 0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 12% 20%,
            rgba(37, 99, 235, 0.09),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #04101c 0%,
            #071827 48%,
            #06131f 100%
        );

    color: #f8fafc;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background:
        radial-gradient(
            circle at 50% 5%,
            rgba(0, 115, 47, 0.08),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #04121f 0%,
            #061a25 50%,
            #04121f 100%
        );

    border-right: 1px solid rgba(148, 163, 184, 0.13);
}

section[data-testid="stSidebar"] > div {
    padding-top: 0.8rem;
}


/* ==========================================================
   LOGO
   ========================================================== */

.logo-box {
    text-align: center;
    padding: 20px 5px 24px 5px;
}

.logo-circle {
    width: 108px;
    height: 108px;

    margin: auto;

    border-radius: 30px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            145deg,
            rgba(212,168,83,0.10),
            rgba(5,20,32,0.95)
        );

    border: 1px solid rgba(212,168,83,0.25);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.05);
}

.logo-letter {
    font-family: Georgia, serif;
    font-size: 72px;
    font-weight: bold;
    line-height: 1;

    background:
        linear-gradient(
            120deg,
            #fff4c7 5%,
            #d4a853 40%,
            #ffffff 70%,
            #c5943c 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    filter:
        drop-shadow(
            0 4px 10px rgba(212,168,83,0.18)
        );
}

.logo-uae-line {
    width: 75px;
    height: 4px;

    margin: 12px auto 11px auto;

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
            #000000 75%
        );
}

.logo-name {
    color: #ffffff;

    font-size: 19px;
    font-weight: 800;

    letter-spacing: 8px;

    margin-left: 8px;
}

.logo-description {
    margin-top: 7px;

    color: #7190a5;

    font-size: 8px;

    letter-spacing: 2.4px;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    position: relative;
    overflow: hidden;

    min-height: 330px;

    padding: 52px 48px 42px 48px;

    margin-bottom: 28px;

    border-radius: 26px;

    border:
        1px solid rgba(212,168,83,0.24);

    background:
        radial-gradient(
            circle at 87% 30%,
            rgba(0,115,47,0.15),
            transparent 25%
        ),
        radial-gradient(
            circle at 68% 100%,
            rgba(37,99,235,0.12),
            transparent 30%
        ),
        linear-gradient(
            115deg,
            rgba(4,16,28,0.99) 0%,
            rgba(7,31,46,0.97) 55%,
            rgba(8,47,54,0.94) 100%
        );

    box-shadow:
        0 22px 70px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

.hero::before {
    content: "";

    position: absolute;

    width: 420px;
    height: 420px;

    border-radius: 50%;

    border:
        1px solid rgba(212,168,83,0.11);

    right: -125px;
    top: -250px;
}

.hero::after {
    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    border-radius: 50%;

    border:
        1px solid rgba(16,185,129,0.10);

    right: 80px;
    bottom: -210px;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-kicker {
    color: #d4a853;

    font-size: 11px;
    font-weight: 700;

    letter-spacing: 4px;

    margin-bottom: 15px;
}

.hero-title {
    margin: 0;

    color: #ffffff;

    font-size: clamp(36px, 4vw, 59px);

    font-weight: 800;

    line-height: 1.05;

    letter-spacing: 1px;
}

.gold {
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

    font-size: clamp(16px, 2vw, 25px);

    font-weight: 300;

    letter-spacing: 7px;
}

.mission {
    max-width: 850px;

    margin-top: 29px;

    color: #dbe4ee;

    font-size: 16px;

    font-style: italic;

    line-height: 1.8;
}

.author {
    margin-top: 14px;

    color: #d4a853;

    font-size: 13px;

    letter-spacing: 2px;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;

    gap: 9px;

    margin-top: 25px;
}

.hero-tag {
    padding: 8px 14px;

    border-radius: 30px;

    color: #dce6ef;

    font-size: 11px;

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.08);
}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.section {
    margin-top: 29px;
    margin-bottom: 17px;
}

.section-kicker {
    color: #d4a853;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 3.5px;
}

.section-title {
    color: #f8fafc;

    font-size: 26px;
    font-weight: 750;

    margin-top: 4px;
}

.section-description {
    color: #8292a7;

    font-size: 13px;

    margin-top: 4px;
}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

.metric-card {
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
}

.metric-icon {
    font-size: 26px;
    margin-bottom: 10px;
}

.metric-label {
    color: #91a3b6;

    font-size: 11px;

    letter-spacing: 0.8px;
}

.metric-value {
    color: #ffffff;

    font-size: 31px;
    font-weight: 800;

    margin-top: 3px;
}

.metric-note {
    color: #64748b;

    font-size: 10px;

    margin-top: 6px;
}


/* ==========================================================
   INFORMATION CARDS
   ========================================================== */

.info-card {
    min-height: 170px;

    padding: 24px;

    border-radius: 19px;

    background:
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

.info-card h3 {
    color: #ffffff;

    font-size: 17px;

    margin-top: 0;
    margin-bottom: 9px;
}

.info-card p {
    color: #91a3b6;

    font-size: 13px;

    line-height: 1.7;
}


/* ==========================================================
   STATUS / EMPTY STATE
   ========================================================== */

.status-card {
    margin-top: 19px;

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


/* ==========================================================
   ABOUT DEVELOPER
   ========================================================== */

.developer-card {
    padding: 26px;

    margin-top: 18px;

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
    color: #ffffff;

    font-size: 19px;

    font-weight: 700;
}

.developer-role {
    color: #d4a853;

    font-size: 12px;

    letter-spacing: 1px;

    margin-top: 5px;
}

.developer-text {
    color: #91a3b6;

    font-size: 12px;

    line-height: 1.7;

    margin-top: 10px;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {
    margin-top: 50px;

    padding: 30px 15px 8px 15px;

    text-align: center;

    border-top:
        1px solid rgba(148,163,184,0.12);

    color: #60768a;

    font-size: 11px;

    line-height: 1.9;
}

.footer-brand {
    color: #d4a853;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 1px;
}


/* ==========================================================
   STREAMLIT COMPONENTS
   ========================================================== */

div[data-testid="stPlotlyChart"] {
    background:
        rgba(8,25,39,0.65);

    border:
        1px solid rgba(148,163,184,0.10);

    border-radius: 19px;

    padding: 5px;
}

div[data-testid="stDataFrame"] {
    border:
        1px solid rgba(148,163,184,0.12);

    border-radius: 16px;

    overflow: hidden;
}

div[role="radiogroup"] label {
    padding-top: 3px;
    padding-bottom: 3px;
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


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 800px) {

    .hero {
        padding: 34px 25px;
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

    html("""
    <div class="logo-box">

        <div class="logo-circle">
            <div class="logo-letter">H</div>
        </div>

        <div class="logo-uae-line"></div>

        <div class="logo-name">
            HJMI
        </div>

        <div class="logo-description">
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

    st.markdown("---")

    st.markdown("### 🎯 Project Focus")

    st.caption(
        "Exploring technology job-market data to transform "
        "raw information into clear and useful career insights."
    )

    st.markdown("---")

    st.markdown("### 🇦🇪 UAE Focus")

    st.caption(
        "Technology • Data • Careers • Opportunities"
    )


# ============================================================
# DATA
# ============================================================

CLEAN_DATA_FILE = Path(
    "data/uae_tech_jobs_clean.csv"
)


@st.cache_data
def load_data():

    if not CLEAN_DATA_FILE.exists():
        return pd.DataFrame()

    try:

        return pd.read_csv(
            CLEAN_DATA_FILE
        )

    except Exception:

        return pd.DataFrame()


df = load_data()


# ============================================================
# COMPONENT FUNCTIONS
# ============================================================

def section_header(
    kicker,
    title,
    description,
):

    html(f"""
    <div class="section">

        <div class="section-kicker">
            {kicker}
        </div>

        <div class="section-title">
            {title}
        </div>

        <div class="section-description">
            {description}
        </div>

    </div>
    """)


def metric_card(
    icon,
    label,
    value,
    note,
):

    html(f"""
    <div class="metric-card">

        <div class="metric-icon">
            {icon}
        </div>

        <div class="metric-label">
            {label}
        </div>

        <div class="metric-value">
            {value}
        </div>

        <div class="metric-note">
            {note}
        </div>

    </div>
    """)


def data_pending():

    html("""
    <div class="status-card">

        🛠️ <strong>Data pipeline ready.</strong>

        <br><br>

        The dashboard interface is active.
        Market statistics and visualizations will appear
        after the UAE technology dataset has been processed
        and validated.

        <br><br>

        No placeholder market statistics are being presented
        as real results.

    </div>
    """)


# ============================================================
# HERO
# ============================================================

html("""
<div class="hero">

    <div class="hero-content">

        <div class="hero-kicker">
            ◇ DATA ANALYSIS PROJECT • UNITED ARAB EMIRATES
        </div>

        <div class="hero-title">
            UAE JOB MARKET
            <span class="gold">INTELLIGENCE</span>
            🇦🇪
        </div>

        <div class="hero-subtitle">
            DATA • TECHNOLOGY • OPPORTUNITIES
        </div>

        <div class="mission">
            “Turning job market data into clear insights
            that help people understand where technology
            opportunities are heading.”
        </div>

        <div class="author">
            — Hasan R. H. Abdalhadi —
        </div>

        <div class="hero-tags">

            <div class="hero-tag">
                📍 UAE Tech Opportunities
            </div>

            <div class="hero-tag">
                📊 Data-Driven Analysis
            </div>

            <div class="hero-tag">
                💻 Computer Science
            </div>

        </div>

    </div>

</div>
""")


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    section_header(
        "✦ MARKET OVERVIEW",
        "UAE Technology Job Market",
        "A data-driven overview of technology opportunities "
        "represented in the project dataset.",
    )

    col1, col2, col3, col4 = st.columns(4)

    if df.empty:

        total_jobs = "—"
        unique_titles = "—"
        skills_count = "—"
        locations_count = "—"

    else:

        total_jobs = f"{len(df):,}"

        unique_titles = (
            f"{df['job_title'].nunique():,}"
            if "job_title" in df.columns
            else "—"
        )

        if "skills" in df.columns:

            all_skills = set()

            for value in df["skills"].dropna():

                for skill in str(value).split(","):

                    skill = skill.strip()

                    if skill:
                        all_skills.add(skill)

            skills_count = f"{len(all_skills):,}"

        else:

            skills_count = "—"

        locations_count = (
            f"{df['location'].nunique():,}"
            if "location" in df.columns
            else "—"
        )

    with col1:

        metric_card(
            "💼",
            "TOTAL UAE TECH JOBS",
            total_jobs,
            "Validated records in the dataset",
        )

    with col2:

        metric_card(
            "🧑‍💻",
            "UNIQUE JOB TITLES",
            unique_titles,
            "Technology roles identified",
        )

    with col3:

        metric_card(
            "⚡",
            "SKILLS IDENTIFIED",
            skills_count,
            "Technical skills detected",
        )

    with col4:

        metric_card(
            "📍",
            "UAE LOCATIONS",
            locations_count,
            "Locations represented",
        )

    section_header(
        "◈ INTELLIGENCE CENTER",
        "Explore the Market",
        "Different perspectives on jobs, skills, "
        "locations and career opportunities.",
    )

    a, b, c = st.columns(3)

    with a:

        html("""
        <div class="info-card">

            <h3>📈 Job Analysis</h3>

            <p>
                Explore technology roles, job categories
                and patterns found across the UAE
                job-market dataset.
            </p>

        </div>
        """)

    with b:

        html("""
        <div class="info-card">

            <h3>⚡ Skills Intelligence</h3>

            <p>
                Discover programming languages,
                platforms and technologies appearing
                across technology-related roles.
            </p>

        </div>
        """)

    with c:

        html("""
        <div class="info-card">

            <h3>📍 Location Insights</h3>

            <p>
                Understand how opportunities represented
                in the dataset are distributed across
                UAE locations.
            </p>

        </div>
        """)

    if df.empty:
        data_pending()


# ============================================================
# JOB ANALYSIS
# ============================================================

elif page == "Job Analysis":

    section_header(
        "✦ JOB ANALYSIS",
        "Technology Roles & Market Patterns",
        "Explore job titles and technology-related "
        "roles identified in the dataset.",
    )

    if df.empty:

        data_pending()

    else:

        st.success(
            f"Dataset active — {len(df):,} "
            "validated records loaded."
        )

        if "job_title" in df.columns:

            top_titles = (
                df["job_title"]
                .dropna()
                .value_counts()
                .head(15)
            )

            st.bar_chart(top_titles)


# ============================================================
# SKILLS ANALYSIS
# ============================================================

elif page == "Skills Analysis":

    section_header(
        "◈ SKILLS INTELLIGENCE",
        "In-Demand Technology Skills",
        "Explore technologies and technical skills "
        "identified from the available job information.",
    )

    if df.empty:

        data_pending()

    else:

        if "skills" in df.columns:

            skills = (
                df["skills"]
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

            st.bar_chart(top_skills)

        else:

            data_pending()


# ============================================================
# LOCATION ANALYSIS
# ============================================================

elif page == "Location Analysis":

    section_header(
        "⌖ LOCATION INTELLIGENCE",
        "Where Are the Opportunities?",
        "Explore locations represented across "
        "the UAE technology-job dataset.",
    )

    if df.empty:

        data_pending()

    else:

        if "location" in df.columns:

            locations = (
                df["location"]
                .replace("", pd.NA)
                .dropna()
                .value_counts()
                .head(15)
            )

            st.bar_chart(locations)

        else:

            data_pending()


# ============================================================
# SALARY ANALYSIS
# ============================================================

elif page == "Salary Analysis":

    section_header(
        "◇ SALARY INTELLIGENCE",
        "Compensation Insights",
        "Salary analysis is shown only when the "
        "source data provides sufficiently usable "
        "compensation information.",
    )

    if df.empty:

        data_pending()

    elif "salary" not in df.columns:

        data_pending()

    else:

        html("""
        <div class="status-card">

            💰 <strong>Salary data detected.</strong>

            <br><br>

            Compensation values will be normalized
            and validated before salary comparisons
            are displayed.

        </div>
        """)


# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    section_header(
        "⌕ DATA EXPLORER",
        "Explore the Dataset",
        "Inspect the processed records used by HJMI.",
    )

    if df.empty:

        data_pending()

    else:

        search = st.text_input(
            "🔎 Search dataset",
            placeholder=(
                "Search job title, company, "
                "location or skill..."
            ),
        )

        filtered_df = df.copy()

        if search:

            search_lower = search.lower()

            mask = filtered_df.astype(
                str
            ).apply(
                lambda row:
                row.str.lower()
                .str.contains(
                    search_lower,
                    regex=False,
                )
                .any(),
                axis=1,
            )

            filtered_df = filtered_df[
                mask
            ]

        st.caption(
            f"{len(filtered_df):,} records displayed"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    section_header(
        "✦ ABOUT HJMI",
        "Hasan Job Market Intelligence",
        "A Computer Science and data-analysis project "
        "focused on technology opportunities in the UAE.",
    )

    left, right = st.columns([1.3, 1])

    with left:

        html("""
        <div class="info-card">

            <h3>🎯 Project Purpose</h3>

            <p>
                HJMI explores job-market data and
                transforms raw information into clearer
                insights about technology roles, skills,
                locations and career opportunities
                represented in the UAE dataset.
            </p>

            <p>
                The project combines data acquisition,
                cleaning, analysis, visualization and
                dashboard development into one
                practical workflow.
            </p>

        </div>
        """)

    with right:

        html("""
        <div class="info-card">

            <h3>🧰 Technology Stack</h3>

            <p>
                🐍 Python<br>
                📊 Pandas<br>
                📈 Data Visualization<br>
                🖥️ Streamlit<br>
                🗃️ Open Data<br>
                💻 GitHub
            </p>

        </div>
        """)

    html("""
    <div class="developer-card">

        <div class="developer-name">
            Hasan R. H. Abdalhadi
        </div>

        <div class="developer-role">
            COMPUTER SCIENCE ENGINEERING
        </div>

        <div class="developer-text">
            BITS Pilani – Dubai Campus<br>
            Information Systems • Software • Data •
            Digital Technologies
        </div>

    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

html("""
<div class="footer">

    <div class="footer-brand">
        HJMI — HASAN JOB MARKET INTELLIGENCE
    </div>

    UAE Job Market Data Analysis

    <br>

    Python • Pandas • Data Visualization • Streamlit • GitHub

    <br><br>

    Designed & Developed by
    <strong style="color:#d6dde5;">
        Hasan R. H. Abdalhadi
    </strong>

</div>
""")
