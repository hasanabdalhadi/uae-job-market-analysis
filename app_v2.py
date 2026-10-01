# ============================================================
# HJMI 2.1 — APPLICATION ENTRY POINT
# Hasan Job Market Intelligence
# ============================================================

import streamlit as st

from services.auth_service import (
    is_authenticated,
    get_current_user,
    get_user_display_name,
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

account_page = st.Page(
    "pages/account.py",
    title="My HJMI",
    icon="👤",
)

about_page = st.Page(
    "pages/about.py",
    title="About & Methodology",
    icon="ℹ️",
)


# ============================================================
# HIDDEN ROUTER
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
        account_page,
        about_page,
    ],
    position="hidden",
)


# ============================================================
# AUTH STATE
# ============================================================

authenticated = is_authenticated()

if authenticated:
    current_user = get_current_user()
    display_name = get_user_display_name()
else:
    current_user = None
    display_name = None


# ============================================================
# GLOBAL SIDEBAR STYLE
# ============================================================

st.html(
    """
    <style>

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071923 0%,
                #071c27 55%,
                #061720 100%
            );
        border-right: 1px solid rgba(216, 173, 87, 0.10);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.5rem;
    }

    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.35rem;
    }

    .hjmi-brand {
        padding: 12px 4px 16px 4px;
        margin-bottom: 2px;
    }

    .hjmi-brand-row {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .hjmi-brand-logo {
        width: 48px;
        height: 48px;
        min-width: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 13px;

        background:
            linear-gradient(
                145deg,
                #173944,
                #0b242d
            );

        border: 1px solid rgba(216, 173, 87, 0.45);

        box-shadow:
            0 10px 25px rgba(0, 0, 0, 0.24);

        color: #e2b95e;

        font-family: Georgia, serif;
        font-size: 27px;
        font-weight: 700;
    }

    .hjmi-brand-short {
        color: #f7f8f8;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: 3px;
        line-height: 1;
    }

    .hjmi-brand-full {
        margin-top: 6px;

        color: #d8ad57;

        font-size: 7px;
        font-weight: 700;

        letter-spacing: 1.25px;
        line-height: 1.5;
    }

    .hjmi-uae-stripe {
        width: 100%;
        height: 3px;

        display: flex;

        margin-top: 16px;

        border-radius: 100px;
        overflow: hidden;

        opacity: 0.95;
    }

    .hjmi-uae-stripe span {
        flex: 1;
        height: 100%;
    }

    .hjmi-red {
        background: #d53d45;
    }

    .hjmi-green {
        background: #24965a;
    }

    .hjmi-white {
        background: #e9eeee;
    }

    .hjmi-black {
        background: #11171c;
    }

    .hjmi-nav-heading {
        margin:
            17px 5px 5px 5px;

        color: #698391;

        font-size: 8px;
        font-weight: 800;

        letter-spacing: 1.8px;
    }

    .hjmi-account-card {
        margin:
            5px 0 6px 0;

        padding: 13px;

        border-radius: 13px;

        border:
            1px solid rgba(216, 173, 87, 0.15);

        background:
            linear-gradient(
                145deg,
                rgba(14, 46, 55, 0.80),
                rgba(9, 31, 40, 0.82)
            );
    }

    .hjmi-account-small {
        color: #d8ad57;

        font-size: 7px;
        font-weight: 800;

        letter-spacing: 1.4px;

        margin-bottom: 5px;
    }

    .hjmi-account-title {
        color: #f4f6f7;

        font-size: 12px;
        font-weight: 700;

        margin-bottom: 5px;
    }

    .hjmi-account-description {
        color: #78909d;

        font-size: 9px;
        line-height: 1.6;
    }

    .hjmi-account-email {
        color: #698391;

        font-size: 8px;
        line-height: 1.5;

        margin-top: 5px;

        word-break: break-word;
    }

    .hjmi-version {
        margin:
            18px 5px 8px 5px;

        color: #49636f;

        font-size: 8px;

        letter-spacing: 1.2px;
    }

    </style>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # HJMI BRAND — TOP
    # --------------------------------------------------------

    st.html(
        """
        <div class="hjmi-brand">

            <div class="hjmi-brand-row">

                <div class="hjmi-brand-logo">
                    H
                </div>

                <div>

                    <div class="hjmi-brand-short">
                        HJMI
                    </div>

                    <div class="hjmi-brand-full">
                        HASAN JOB MARKET INTELLIGENCE
                    </div>

                </div>

            </div>

            <div class="hjmi-uae-stripe">
                <span class="hjmi-red"></span>
                <span class="hjmi-green"></span>
                <span class="hjmi-white"></span>
                <span class="hjmi-black"></span>
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # CAREER DISCOVERY
    # --------------------------------------------------------

    st.html(
        """
        <div class="hjmi-nav-heading">
            CAREER DISCOVERY
        </div>
        """
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

    st.html(
        """
        <div class="hjmi-nav-heading">
            MARKET INTELLIGENCE
        </div>
        """
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
    # MY HJMI
    # --------------------------------------------------------

    st.html(
        """
        <div class="hjmi-nav-heading">
            MY HJMI
        </div>
        """
    )

    if authenticated:

        user_email = getattr(
            current_user,
            "email",
            "",
        ) or ""

        st.html(
            f"""
            <div class="hjmi-account-card">

                <div class="hjmi-account-small">
                    ACCOUNT ACTIVE
                </div>

                <div class="hjmi-account-title">
                    {display_name}
                </div>

                <div class="hjmi-account-description">
                    Your personal HJMI career workspace.
                </div>

                <div class="hjmi-account-email">
                    {user_email}
                </div>

            </div>
            """
        )

        st.page_link(
            account_page,
            label="My HJMI",
            icon="👤",
            use_container_width=True,
        )

    else:

        st.html(
            """
            <div class="hjmi-account-card">

                <div class="hjmi-account-small">
                    PERSONAL CAREER SPACE
                </div>

                <div class="hjmi-account-title">
                    Your HJMI Account
                </div>

                <div class="hjmi-account-description">
                    Save opportunities, track applications,
                    manage your career profile and receive
                    personalized job alerts.
                </div>

            </div>
            """
        )

        st.page_link(
            account_page,
            label="Sign In",
            icon="🔐",
            use_container_width=True,
        )

        st.page_link(
            account_page,
            label="Create Account",
            icon="➕",
            use_container_width=True,
        )


    # --------------------------------------------------------
    # PLATFORM
    # --------------------------------------------------------

    st.html(
        """
        <div class="hjmi-nav-heading">
            PLATFORM
        </div>
        """
    )

    st.page_link(
        about_page,
        label="About & Methodology",
        icon="ℹ️",
    )


    # --------------------------------------------------------
    # VERSION
    # --------------------------------------------------------

    st.html(
        """
        <div class="hjmi-version">
            HJMI 2.1 • UAE MARKET INTELLIGENCE 🇦🇪
        </div>
        """
    )


# ============================================================
# RUN PAGE
# ============================================================

navigation.run()
