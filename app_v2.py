# ============================================================
# HJMI 2.0 — APPLICATION ENTRY POINT
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
# HJMI 2.0 NAVIGATION
# ============================================================

pages = {
    "HJMI Intelligence": [
        st.Page(
            "pages/home.py",
            title="Home",
            icon="🏠",
            default=True,
        ),
        st.Page(
            "pages/find_jobs.py",
            title="Find Jobs",
            icon="🔎",
        ),
        st.Page(
            "pages/graduate_hub.py",
            title="Graduate Hub",
            icon="🎓",
        ),
    ],

    "Market Intelligence": [
        st.Page(
            "pages/job_intelligence.py",
            title="Job Intelligence",
            icon="💼",
        ),
        st.Page(
            "pages/skills_intelligence.py",
            title="Skills Intelligence",
            icon="⚡",
        ),
        st.Page(
            "pages/location_intelligence.py",
            title="Location Intelligence",
            icon="📍",
        ),
        st.Page(
            "pages/salary_intelligence.py",
            title="Salary Intelligence",
            icon="💰",
        ),
        st.Page(
            "pages/market_trends.py",
            title="Market Trends",
            icon="📈",
        ),
    ],

    "Platform": [
        st.Page(
            "pages/about.py",
            title="About & Methodology",
            icon="ℹ️",
        ),
    ],
}


# ============================================================
# RUN NAVIGATION
# ============================================================

navigation = st.navigation(
    pages,
    position="sidebar",
    expanded=True,
)

navigation.run()
