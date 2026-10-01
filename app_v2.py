# ============================================================
# HJMI 2.1 — APPLICATION ENTRY POINT
# Hasan Job Market Intelligence
# ============================================================

import streamlit as st


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
# PAGE DEFINITIONS
# ============================================================

home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True,
)

find_jobs_page = st.Page(
    "pages/find_jobs.py",
    title="Find Jobs",
    icon="🔎",
)

graduate_hub_page = st.Page(
    "pages/graduate_hub.py",
    title="Graduate Hub",
    icon="🎓",
)

job_intelligence_page = st.Page(
    "pages/job_intelligence.py",
    title="Job Intelligence",
    icon="💼",
)

skills_intelligence_page = st.Page(
    "pages/skills_intelligence.py",
    title="Skills Intelligence",
    icon="⚡",
)

location_intelligence_page = st.Page(
    "pages/location_intelligence.py",
    title="Location Intelligence",
    icon="📍",
)

salary_intelligence_page = st.Page(
    "pages/salary_intelligence.py",
    title="Salary Intelligence",
    icon="💰",
)

market_trends_page = st.Page(
    "pages/market_trends.py",
    title="Market Trends",
    icon="📈",
)

about_page = st.Page(
    "pages/about.py",
    title="About & Methodology",
    icon="ℹ️",
)


# ============================================================
# ROUTER
# Hidden because we are building our own premium sidebar.
# ============================================================

navigation = st.navigation(
    [
        home_page,
        find_jobs_page,
        graduate_hub_page,
        job_intelligence_page,
        skills_intelligence_page,
        location_intelligence_page,
        salary_intelligence_page,
        market_trends_page,
        about_page,
    ],
    position="hidden",
)


# ============================================================
# SIDEBAR DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* Sidebar spacing */
    section[data-testid="stSidebar"] > div {
        padding-top: 0.8rem;
    }

    /* HJMI main brand */
    .hjmi-main-brand {
        padding: 14px 8px 18px 8px;
        margin-bottom: 4px;
    }

    .hjmi-logo-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hjmi-logo {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;

        background:
            linear-gradient(
                145deg,
                #183c46,
                #0d242d
            );

        border: 1px solid rgba(216, 173, 87, 0.45);

        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.24);

        color: #e1b85f;

        font-size: 23px;
        font-weight: 800;
    }

    .hjmi-name {
        color: #f5f7f8;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.8px;
        line-height: 1.1;
    }

    .hjmi-full-name {
        margin-top: 4px;
        color: #d8ad57;
        font-size: 7.5px;
        font-weight: 700;
        letter-spacing: 1.3px;
        line-height: 1.4;
    }

    .hjmi-uae-line {
        display: flex;
        height: 3px;
        width: 100%;
        margin-top: 15px;
        overflow: hidden;
        border-radius: 20px;
    }

    .hjmi-uae-red {
        width: 25%;
        background: #d93c3c;
    }

    .hjmi-uae-green {
        width: 25%;
        background: #2f9e62;
    }

    .hjmi-uae-white {
        width: 25%;
        background: #e9eef0;
    }

    .hjmi-uae-black {
        width: 25%;
        background: #12181d;
    }

    .hjmi-nav-label {
        margin:
            16px 8px 7px 8px;

        color: #6f8797;

        font-size: 8px;
        font-weight: 800;

        letter-spacing: 1.7px;
    }

    .hjmi-account-box {
        margin-top: 20px;
        padding: 14px;

        border:
            1px solid rgba(216, 173, 87, 0.15);

        border-radius: 14px;

        background:
            rgba(15, 42, 50, 0.55);
    }

    .hjmi-account-title {
        color: #f1f5f6;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .hjmi-account-text {
        color: #718997;
        font-size: 9px;
        line-height: 1.6;
    }

    .hjmi-version {
        margin:
            20px 8px 5px 8px;

        color: #506774;

        font-size: 8px;
        letter-spacing: 1px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CUSTOM SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND — ALWAYS AT THE TOP
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hjmi-main-brand">

            <div class="hjmi-logo-row">

                <div class="hjmi-logo">
                    H
                </div>

                <div>

                    <div class="hjmi-name">
                        HJMI
                    </div>

                    <div class="hjmi-full-name">
                        HASAN JOB MARKET INTELLIGENCE
                    </div>

                </div>

            </div>

            <div class="hjmi-uae-line">
                <div class="hjmi-uae-red"></div>
                <div class="hjmi-uae-green"></div>
                <div class="hjmi-uae-white"></div>
                <div class="hjmi-uae-black"></div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CAREER DISCOVERY
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hjmi-nav-label">
            CAREER DISCOVERY
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link(
        home_page,
        label="Home",
        icon="🏠",
    )

    st.page_link(
        find_jobs_page,
        label="Find Jobs",
        icon="🔎",
    )

    st.page_link(
        graduate_hub_page,
        label="Graduate Hub",
        icon="🎓",
    )


    # --------------------------------------------------------
    # MARKET INTELLIGENCE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hjmi-nav-label">
            MARKET INTELLIGENCE
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link(
        job_intelligence_page,
        label="Job Intelligence",
        icon="💼",
    )

    st.page_link(
        skills_intelligence_page,
        label="Skills Intelligence",
        icon="⚡",
    )

    st.page_link(
        location_intelligence_page,
        label="Location Intelligence",
        icon="📍",
    )

    st.page_link(
        salary_intelligence_page,
        label="Salary Intelligence",
        icon="💰",
    )

    st.page_link(
        market_trends_page,
        label="Market Trends",
        icon="📈",
    )


    # --------------------------------------------------------
    # MY HJMI — ACCOUNT PREVIEW
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hjmi-nav-label">
            MY HJMI
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hjmi-account-box">

            <div class="hjmi-account-title">
                Your Career Space
            </div>

            <div class="hjmi-account-text">
                Sign in to save jobs, track applications
                and personalize your HJMI experience.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.button(
        "Sign In",
        use_container_width=True,
        key="hjmi_signin_preview",
    )

    st.button(
        "Create Account",
        use_container_width=True,
        key="hjmi_signup_preview",
    )


    # --------------------------------------------------------
    # PLATFORM
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hjmi-nav-label">
            PLATFORM
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link(
        about_page,
        label="About & Methodology",
        icon="ℹ️",
    )


    # --------------------------------------------------------
    # VERSION
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hjmi-version">
            HJMI 2.1 • UAE 🇦🇪
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RUN SELECTED PAGE
# ============================================================

navigation.run()
