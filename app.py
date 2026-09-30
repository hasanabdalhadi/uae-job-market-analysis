import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

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
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Main App ---------- */

    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(15, 118, 110, 0.12), transparent 25%),
            radial-gradient(circle at 15% 20%, rgba(37, 99, 235, 0.10), transparent 28%),
            linear-gradient(135deg, #06111d 0%, #071827 45%, #07131f 100%);
        color: #f8fafc;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #06111d 0%, #071b25 55%, #06111d 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.14);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    /* ---------- HJMI Logo ---------- */

    .logo-box {
        text-align: center;
        padding: 25px 10px 22px 10px;
        margin-bottom: 20px;
    }

    .logo-mark {
        font-size: 70px;
        line-height: 1;
        font-weight: 800;
        font-family: Georgia, serif;
        background: linear-gradient(
            120deg,
            #f8fafc 20%,
            #d4a853 45%,
            #f7d98a 65%,
            #ffffff 85%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -4px;
        filter: drop-shadow(0 0 14px rgba(212, 168, 83, 0.15));
    }

    .logo-line {
        width: 70px;
        height: 3px;
        margin: 10px auto;
        background: linear-gradient(90deg, #ce1126, #ffffff, #00732f);
        border-radius: 20px;
    }

    .logo-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 7px;
        margin-top: 8px;
    }

    .logo-subtitle {
        color: #94a3b8;
        font-size: 9px;
        letter-spacing: 2.5px;
        margin-top: 5px;
    }

    /* ---------- Hero ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 42px 42px 38px 42px;
        margin-bottom: 24px;
        border: 1px solid rgba(212, 168, 83, 0.24);
        border-radius: 24px;

        background:
            linear-gradient(
                110deg,
                rgba(4, 18, 32, 0.98) 0%,
                rgba(7, 30, 45, 0.96) 55%,
                rgba(10, 49, 57, 0.90) 100%
            );

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 330px;
        height: 330px;
        border: 1px solid rgba(212, 168, 83, 0.14);
        border-radius: 50%;
        right: -100px;
        top: -180px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        border: 1px solid rgba(16, 185, 129, 0.10);
        border-radius: 50%;
        right: 30px;
        bottom: -170px;
    }

    .eyebrow {
        color: #d4a853;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 4px;
        margin-bottom: 13px;
    }

    .hero h1 {
        margin: 0;
        color: #ffffff;
        font-size: 49px;
        line-height: 1.05;
        letter-spacing: 1px;
    }

    .hero h1 span {
        background: linear-gradient(90deg, #d4a853, #f7d98a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero h2 {
        margin: 8px 0 22px 0;
        color: #cbd5e1;
        font-size: 26px;
        font-weight: 300;
        letter-spacing: 8px;
    }

    .mission {
        max-width: 900px;
        color: #dbe4ee;
        font-size: 17px;
        font-style: italic;
        line-height: 1.7;
        margin-bottom: 15px;
    }

    .author {
        color: #d4a853;
        font-size: 13px;
        letter-spacing: 2px;
    }

    .uae-pill {
        display: inline-block;
        margin-top: 22px;
        padding: 8px 15px;
        border-radius: 50px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.09);
        color: #e2e8f0;
        font-size: 12px;
    }

    /* ---------- Section Titles ---------- */

    .section-heading {
        margin-top: 24px;
        margin-bottom: 17px;
    }

    .section-kicker {
        color: #d4a853;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 3px;
        margin-bottom: 4px;
    }

    .section-title {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 700;
        margin: 0;
    }

    .section-description {
        color: #8292a7;
        font-size: 13px;
        margin-top: 4px;
    }

    /* ---------- Metric Cards ---------- */

    .metric-card {
        min-height: 145px;
        padding: 22px;
        border-radius: 18px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 35, 52, 0.96),
                rgba(8, 25, 39, 0.96)
            );
        border: 1px solid rgba(148, 163, 184, 0.13);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.16);
        transition: 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(212, 168, 83, 0.28);
    }

    .metric-icon {
        font-size: 25px;
        margin-bottom: 12px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 12px;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        margin-top: 3px;
    }

    .metric-note {
        color: #64748b;
        font-size: 11px;
        margin-top: 5px;
    }

    /* ---------- Information Cards ---------- */

    .info-card {
        min-height: 150px;
        padding: 22px;
        margin-bottom: 10px;
        border-radius: 18px;
        background: rgba(10, 29, 44, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.12);
    }

    .info-card h3 {
        color: #ffffff;
        font-size: 17px;
        margin-top: 0;
        margin-bottom: 8px;
    }

    .info-card p {
        color: #94a3b8;
        line-height: 1.65;
        font-size: 13px;
    }

    /* ---------- Status ---------- */

    .status-box {
        padding: 17px 20px;
        border-radius: 15px;
        margin: 12px 0 20px 0;
        background: rgba(212, 168, 83, 0.07);
        border: 1px solid rgba(212, 168, 83, 0.20);
        color: #dbe4ee;
        font-size: 13px;
    }

    /* ---------- Footer ---------- */

    .footer {
        margin-top: 45px;
        padding: 28px 15px 10px 15px;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
        text-align: center;
        color: #64748b;
        font-size: 12px;
        line-height: 1.8;
    }

    .footer strong {
        color: #d4a853;
    }

    /* ---------- Streamlit Components ---------- */

    div[data-testid="stPlotlyChart"] {
        background: rgba(8, 25, 39, 0.60);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 18px;
        padding: 5px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 15px;
        overflow: hidden;
    }

    .stSelectbox label,
    .stMultiSelect label {
        color: #cbd5e1 !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR BRANDING
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo-box">
            <div class="logo-mark">H</div>
            <div class="logo-line"></div>
            <div class="logo-title">HJMI</div>
            <div class="logo-subtitle">
                HASAN JOB MARKET INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🏠 Navigation")

    page = st.radio(
        "Explore",
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
        "Exploring technology job-market data to transform raw "
        "information into clear and useful career insights."
    )

    st.markdown("---")

    st.markdown("**🇦🇪 United Arab Emirates**")
    st.caption("Technology • Data • Careers • Insights")

# ============================================================
# DATA
# ============================================================

DATA_FILE = Path("data/arab_jobs_raw.csv")


@st.cache_data
def load_local_data():
    if DATA_FILE.exists():
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()


df = load_local_data()

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="eyebrow">
            ◇ DATA ANALYSIS PROJECT • UNITED ARAB EMIRATES
        </div>

        <h1>
            UAE JOB MARKET <span>INTELLIGENCE</span> 🇦🇪
        </h1>

        <h2>DATA • TECHNOLOGY • OPPORTUNITIES</h2>

        <div class="mission">
            “Turning job market data into clear insights that help people
            understand where technology opportunities are heading.”
        </div>

        <div class="author">
            — Hasan R. H. Abdalhadi —
        </div>

        <div class="uae-pill">
            📍 UAE Tech Opportunities &nbsp; • &nbsp;
            📊 Data-Driven Analysis
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================


def section_header(kicker, title, description):
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            <div class="section-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon, label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_chart_message():
    st.markdown(
        """
        <div class="status-box">
            🛠️ <strong>Data preparation in progress.</strong><br><br>
            This dashboard is connected to the project data pipeline.
            Metrics and visualizations will appear after the UAE dataset
            has been downloaded, cleaned, and validated.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    section_header(
        "✦ MARKET OVERVIEW",
        "UAE Technology Job Market",
        "A clear overview of the dataset and the insights produced by the analysis.",
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "💼",
            "TOTAL UAE TECH JOBS",
            "—",
            "Calculated from validated data",
        )

    with col2:
        metric_card(
            "🧑‍💻",
            "UNIQUE JOB TITLES",
            "—",
            "Technology roles identified",
        )

    with col3:
        metric_card(
            "⚡",
            "SKILLS IDENTIFIED",
            "—",
            "Extracted from job information",
        )

    with col4:
        metric_card(
            "📍",
            "UAE LOCATIONS",
            "—",
            "Locations represented in data",
        )

    section_header(
        "◈ INTELLIGENCE CENTER",
        "Explore the Market",
        "Each section focuses on a different part of the UAE technology job market.",
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            """
            <div class="info-card">
                <h3>📈 Job Analysis</h3>
                <p>
                    Explore technology roles, job categories, and patterns
                    found across the UAE job market dataset.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            """
            <div class="info-card">
                <h3>⚡ Skills Intelligence</h3>
                <p>
                    Identify technical skills and technologies appearing
                    across technology-related job opportunities.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            """
            <div class="info-card">
                <h3>📍 Location Insights</h3>
                <p>
                    Understand how technology opportunities are distributed
                    across cities and locations in the UAE.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    empty_chart_message()

# ============================================================
# JOB ANALYSIS
# ============================================================

elif page == "Job Analysis":

    section_header(
        "✦ JOB ANALYSIS",
        "Technology Roles & Market Patterns",
        "Explore the structure and distribution of technology jobs in the dataset.",
    )

    if df.empty:
        empty_chart_message()

    else:
        st.success("Dataset loaded successfully.")

        st.write("Rows available:", len(df))

        st.dataframe(
            df.head(25),
            use_container_width=True,
            hide_index=True,
        )

# ============================================================
# SKILLS ANALYSIS
# ============================================================

elif page == "Skills Analysis":

    section_header(
        "◈ SKILLS ANALYSIS",
        "In-Demand Technology Skills",
        "Discover which technical skills appear most frequently in job opportunities.",
    )

    empty_chart_message()

# ============================================================
# LOCATION ANALYSIS
# ============================================================

elif page == "Location Analysis":

    section_header(
        "⌖ LOCATION ANALYSIS",
        "Where Are the Opportunities?",
        "Explore the geographic distribution of technology jobs across the UAE.",
    )

    empty_chart_message()

# ============================================================
# SALARY ANALYSIS
# ============================================================

elif page == "Salary Analysis":

    section_header(
        "◇ SALARY ANALYSIS",
        "Compensation Insights",
        "Salary insights will only be displayed when reliable salary data is available.",
    )

    empty_chart_message()

# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    section_header(
        "⌕ DATA EXPLORER",
        "Explore the Dataset",
        "Inspect the data used to generate the dashboard insights.",
    )

    if df.empty:
        empty_chart_message()

    else:
        st.write(f"**Available records:** {len(df):,}")
        st.write(f"**Available columns:** {len(df.columns)}")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    section_header(
        "✦ ABOUT THE PROJECT",
        "Hasan Job Market Intelligence",
        "A portfolio data-analysis project focused on technology opportunities in the UAE.",
    )

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown(
            """
            <div class="info-card">
                <h3>🎯 Project Purpose</h3>
                <p>
                    HJMI was created to explore job-market data and transform
                    raw information into clear insights about technology roles,
                    skills, locations, and career opportunities in the UAE.
                </p>
                <p>
                    The project combines data collection, cleaning, analysis,
                    visualization, and dashboard development in one practical
                    data-analysis workflow.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="info-card">
                <h3>🧰 Technology</h3>
                <p>
                    🐍 Python<br>
                    📊 Pandas<br>
                    📈 Plotly<br>
                    🖥️ Streamlit<br>
                    🗃️ Open Data<br>
                    💻 GitHub
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="info-card">
            <h3>👨‍💻 Developer</h3>
            <p>
                <strong style="color:#ffffff;">Hasan R. H. Abdalhadi</strong><br>
                Computer Science Engineering<br>
                BITS Pilani – Dubai Campus
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <strong>HJMI — Hasan Job Market Intelligence</strong><br>

        UAE Job Market Data Analysis • Python • Pandas • Plotly • Streamlit<br>

        Designed & Developed by Hasan R. H. Abdalhadi

    </div>
    """,
    unsafe_allow_html=True,
)
