# ============================================================
# HJMI 2.0 — DESIGN SYSTEM
# Hasan Job Market Intelligence
# ============================================================

import streamlit as st


def apply_theme():
    """Apply the global HJMI 2.0 visual design system."""

    st.html("""
    <style>

    /* ========================================================
       HJMI 2.0 — DESIGN TOKENS
       ======================================================== */

    :root {
        --hjmi-bg: #04111c;
        --hjmi-bg-soft: #071927;
        --hjmi-surface: #0a1d2c;
        --hjmi-surface-2: #0d2435;
        --hjmi-surface-3: #102b3d;

        --hjmi-gold: #d8ad57;
        --hjmi-gold-light: #f2d58b;
        --hjmi-gold-soft: rgba(216, 173, 87, 0.12);

        --hjmi-green: #00a86b;
        --hjmi-green-soft: rgba(0, 168, 107, 0.12);

        --hjmi-blue: #4c8dff;
        --hjmi-blue-soft: rgba(76, 141, 255, 0.12);

        --hjmi-red: #ce1126;

        --hjmi-text: #f8fafc;
        --hjmi-text-soft: #a8b7c7;
        --hjmi-text-muted: #70859a;

        --hjmi-border: rgba(148, 163, 184, 0.14);
        --hjmi-border-gold: rgba(216, 173, 87, 0.25);

        --hjmi-radius-sm: 12px;
        --hjmi-radius: 18px;
        --hjmi-radius-lg: 26px;

        --hjmi-shadow:
            0 18px 50px rgba(0, 0, 0, 0.22);
    }


    /* ========================================================
       GLOBAL APP
       ======================================================== */

    html {
        scroll-behavior: smooth;
    }

    .stApp {
        color: var(--hjmi-text);

        background:
            radial-gradient(
                circle at 92% 3%,
                rgba(0, 168, 107, 0.09),
                transparent 24%
            ),
            radial-gradient(
                circle at 8% 35%,
                rgba(76, 141, 255, 0.07),
                transparent 27%
            ),
            linear-gradient(
                135deg,
                #03101a 0%,
                #061725 48%,
                #04131f 100%
            );
    }


    /* ========================================================
       MAIN CONTENT WIDTH
       ======================================================== */

    .block-container {
        max-width: 1720px;

        padding-top: 1.5rem;
        padding-left: 2.4rem;
        padding-right: 2.4rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       TYPOGRAPHY
       ======================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: var(--hjmi-text);
        letter-spacing: -0.02em;
    }

    p {
        color: var(--hjmi-text-soft);
    }

    a {
        transition: 0.2s ease;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(216, 173, 87, 0.07),
                transparent 22%
            ),
            linear-gradient(
                180deg,
                #04131f 0%,
                #061a28 52%,
                #04131f 100%
            );

        border-right:
            1px solid var(--hjmi-border);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.5rem;
    }


    /* ========================================================
       HJMI BRAND
       ======================================================== */

    .hjmi-brand {
        padding:
            24px 14px 28px;

        text-align: center;
    }

    .hjmi-brand-mark {
        width: 92px;
        height: 92px;

        margin:
            0 auto 14px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 26px;

        background:
            radial-gradient(
                circle at 30% 20%,
                rgba(255,255,255,0.08),
                transparent 30%
            ),
            linear-gradient(
                145deg,
                rgba(216,173,87,0.13),
                rgba(5,22,34,0.98)
            );

        border:
            1px solid rgba(216,173,87,0.30);

        box-shadow:
            0 18px 45px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .hjmi-brand-h {
        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 61px;
        font-weight: 700;

        line-height: 1;

        background:
            linear-gradient(
                120deg,
                #fff3c4,
                #d8ad57 38%,
                #ffffff 67%,
                #b77d2d
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hjmi-uae-line {
        width: 68px;
        height: 4px;

        margin:
            0 auto 13px;

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

    .hjmi-brand-name {
        color: white;

        font-size: 17px;
        font-weight: 800;

        letter-spacing: 7px;

        padding-left: 7px;
    }

    .hjmi-brand-sub {
        margin-top: 7px;

        color: #72899d;

        font-size: 8px;

        letter-spacing: 2px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hjmi-hero {
        position: relative;

        overflow: hidden;

        min-height: 360px;

        padding:
            58px 56px;

        border-radius:
            var(--hjmi-radius-lg);

        border:
            1px solid var(--hjmi-border-gold);

        background:
            radial-gradient(
                circle at 88% 20%,
                rgba(0,168,107,0.16),
                transparent 27%
            ),
            radial-gradient(
                circle at 67% 110%,
                rgba(76,141,255,0.12),
                transparent 31%
            ),
            linear-gradient(
                115deg,
                #04111e 0%,
                #072034 58%,
                #07353d 100%
            );

        box-shadow:
            0 24px 70px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .hjmi-hero::before {
        content: "";

        position: absolute;

        width: 470px;
        height: 470px;

        right: -145px;
        top: -280px;

        border-radius: 50%;

        border:
            1px solid rgba(216,173,87,0.13);
    }

    .hjmi-hero::after {
        content: "";

        position: absolute;

        width: 300px;
        height: 300px;

        right: 100px;
        bottom: -230px;

        border-radius: 50%;

        border:
            1px solid rgba(0,168,107,0.12);
    }

    .hjmi-hero-content {
        position: relative;
        z-index: 2;

        max-width: 1050px;
    }

    .hjmi-eyebrow {
        color: var(--hjmi-gold);

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 4px;

        margin-bottom: 16px;
    }

    .hjmi-hero-title {
        color: white;

        max-width: 1100px;

        font-size:
            clamp(40px, 4.6vw, 67px);

        font-weight: 850;

        line-height: 1.03;

        letter-spacing: -1px;
    }

    .hjmi-gradient-text {
        background:
            linear-gradient(
                90deg,
                #d8ad57,
                #fff0b0,
                #d8ad57
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hjmi-hero-subtitle {
        margin-top: 13px;

        color: #cbd5e1;

        font-size:
            clamp(15px, 1.8vw, 22px);

        font-weight: 300;

        letter-spacing: 6px;
    }

    .hjmi-hero-description {
        max-width: 830px;

        margin-top: 28px;

        color: #c8d5e1;

        font-size: 15px;

        line-height: 1.8;
    }

    .hjmi-hero-pills {
        display: flex;
        flex-wrap: wrap;

        gap: 9px;

        margin-top: 25px;
    }

    .hjmi-pill {
        padding:
            8px 14px;

        border-radius: 999px;

        color: #dce7f0;

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.08);

        font-size: 11px;
    }


    /* ========================================================
       PAGE HEADER
       ======================================================== */

    .hjmi-page-header {
        margin-top: 31px;
        margin-bottom: 19px;
    }

    .hjmi-page-kicker {
        color: var(--hjmi-gold);

        font-size: 10px;
        font-weight: 800;

        letter-spacing: 3.5px;
    }

    .hjmi-page-title {
        margin-top: 5px;

        color: white;

        font-size:
            clamp(25px, 2.4vw, 34px);

        font-weight: 760;
    }

    .hjmi-page-description {
        max-width: 950px;

        margin-top: 6px;

        color: var(--hjmi-text-muted);

        font-size: 13px;

        line-height: 1.7;
    }


    /* ========================================================
       EXPLAINER
       ======================================================== */

    .hjmi-explainer {
        margin:
            12px 0 22px;

        padding:
            17px 19px;

        border-radius:
            15px;

        background:
            linear-gradient(
                90deg,
                rgba(76,141,255,0.075),
                rgba(0,168,107,0.045)
            );

        border:
            1px solid rgba(76,141,255,0.16);

        color: #b7c7d6;

        font-size: 12px;

        line-height: 1.7;
    }

    .hjmi-explainer strong {
        color: #e6eef5;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .hjmi-metric {
        min-height: 154px;

        padding:
            22px;

        border-radius:
            var(--hjmi-radius);

        background:
            radial-gradient(
                circle at 100% 0%,
                rgba(76,141,255,0.08),
                transparent 38%
            ),
            linear-gradient(
                145deg,
                rgba(13,37,54,0.97),
                rgba(6,24,37,0.98)
            );

        border:
            1px solid var(--hjmi-border);

        box-shadow:
            0 12px 35px rgba(0,0,0,0.15);

        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease;
    }

    .hjmi-metric:hover {
        transform:
            translateY(-3px);

        border-color:
            rgba(216,173,87,0.32);

        box-shadow:
            0 17px 42px rgba(0,0,0,0.22);
    }

    .hjmi-metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .hjmi-metric-icon {
        font-size: 26px;
    }

    .hjmi-info {
        color: #647b90;

        font-size: 12px;
    }

    .hjmi-metric-label {
        margin-top: 13px;

        color: #8fa3b6;

        font-size: 10px;

        letter-spacing: 1px;

        text-transform: uppercase;
    }

    .hjmi-metric-value {
        margin-top: 3px;

        color: white;

        font-size: 32px;
        font-weight: 820;
    }

    .hjmi-metric-note {
        margin-top: 6px;

        color: #667c91;

        font-size: 10px;

        line-height: 1.5;
    }


    /* ========================================================
       GENERAL CARDS
       ======================================================== */

    .hjmi-card {
        padding:
            23px;

        border-radius:
            var(--hjmi-radius);

        background:
            radial-gradient(
                circle at 100% 0%,
                rgba(0,168,107,0.045),
                transparent 35%
            ),
            linear-gradient(
                145deg,
                rgba(11,31,47,0.96),
                rgba(7,24,37,0.97)
            );

        border:
            1px solid var(--hjmi-border);

        box-shadow:
            0 12px 34px rgba(0,0,0,0.12);
    }

    .hjmi-card-title {
        color: white;

        font-size: 16px;
        font-weight: 720;
    }

    .hjmi-card-subtitle {
        margin-top: 6px;

        color: var(--hjmi-text-muted);

        font-size: 12px;

        line-height: 1.65;
    }


    /* ========================================================
       JOB CARD
       ======================================================== */

    .hjmi-job-card {
        margin-bottom: 13px;

        padding:
            21px 22px;

        border-radius:
            var(--hjmi-radius);

        background:
            linear-gradient(
                145deg,
                rgba(12,34,50,0.98),
                rgba(7,25,38,0.98)
            );

        border:
            1px solid var(--hjmi-border);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.11);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    .hjmi-job-card:hover {
        transform:
            translateY(-2px);

        border-color:
            rgba(216,173,87,0.30);
    }

    .hjmi-job-title {
        color: white;

        font-size: 17px;
        font-weight: 720;
    }

    .hjmi-job-company {
        margin-top: 4px;

        color: var(--hjmi-gold);

        font-size: 12px;
    }

    .hjmi-job-meta {
        display: flex;
        flex-wrap: wrap;

        gap: 8px;

        margin-top: 13px;
    }

    .hjmi-job-tag {
        padding:
            6px 10px;

        border-radius: 999px;

        color: #b8c7d4;

        background:
            rgba(255,255,255,0.04);

        border:
            1px solid rgba(255,255,255,0.07);

        font-size: 10px;
    }


    /* ========================================================
       STATUS BADGES
       ======================================================== */

    .hjmi-badge {
        display: inline-flex;
        align-items: center;

        padding:
            5px 9px;

        border-radius:
            999px;

        font-size: 9px;
        font-weight: 750;

        letter-spacing: 0.5px;
    }

    .hjmi-badge-new {
        color: #b8ffe0;

        background:
            rgba(0,168,107,0.13);

        border:
            1px solid rgba(0,168,107,0.22);
    }

    .hjmi-badge-active {
        color: #c6dcff;

        background:
            rgba(76,141,255,0.12);

        border:
            1px solid rgba(76,141,255,0.20);
    }

    .hjmi-badge-graduate {
        color: #ffe7a7;

        background:
            rgba(216,173,87,0.12);

        border:
            1px solid rgba(216,173,87,0.22);
    }

    .hjmi-badge-verified {
        color: #b9f6dc;

        background:
            rgba(0,168,107,0.11);

        border:
            1px solid rgba(0,168,107,0.22);
    }


    /* ========================================================
       STATUS / NOTICE CARD
       ======================================================== */

    .hjmi-status {
        margin:
            18px 0;

        padding:
            19px 20px;

        border-radius:
            16px;

        background:
            linear-gradient(
                90deg,
                rgba(216,173,87,0.07),
                rgba(0,168,107,0.035)
            );

        border:
            1px solid rgba(216,173,87,0.19);

        color: #cbd8e3;

        font-size: 12px;

        line-height: 1.75;
    }

    .hjmi-status strong {
        color: var(--hjmi-gold-light);
    }


    /* ========================================================
       STREAMLIT BUTTONS
       ======================================================== */

    div.stButton > button,
    div.stLinkButton > a {
        min-height: 42px;

        border-radius:
            12px !important;

        border:
            1px solid rgba(216,173,87,0.24) !important;

        background:
            linear-gradient(
                135deg,
                rgba(216,173,87,0.14),
                rgba(8,31,46,0.95)
            ) !important;

        color:
            #f4e1ae !important;

        font-weight:
            650 !important;

        transition:
            0.2s ease !important;
    }

    div.stButton > button:hover,
    div.stLinkButton > a:hover {
        border-color:
            rgba(216,173,87,0.48) !important;

        transform:
            translateY(-1px);

        box-shadow:
            0 8px 22px rgba(0,0,0,0.18);
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background:
            rgba(8,29,44,0.90) !important;

        border-color:
            var(--hjmi-border) !important;

        border-radius:
            12px !important;
    }

    div[data-baseweb="input"] input {
        color:
            white !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        color:
            #8297aa !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color:
            var(--hjmi-gold-light) !important;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {
        overflow: hidden;

        border-radius:
            16px;

        border:
            1px solid var(--hjmi-border);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.12);
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    details {
        border:
            1px solid var(--hjmi-border) !important;

        border-radius:
            14px !important;

        background:
            rgba(8,29,44,0.65) !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color:
            var(--hjmi-border) !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .hjmi-footer {
        margin-top: 55px;

        padding:
            32px 12px 12px;

        text-align: center;

        border-top:
            1px solid var(--hjmi-border);

        color:
            #61788d;

        font-size:
            10px;

        line-height:
            1.9;
    }

    .hjmi-footer-brand {
        color:
            var(--hjmi-gold);

        font-size:
            12px;

        font-weight:
            750;

        letter-spacing:
            1.3px;
    }


    /* ========================================================
       REMOVE STREAMLIT CHROME
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       RESPONSIVE — TABLET
       ======================================================== */

    @media (max-width: 1100px) {

        .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        .hjmi-hero {
            padding:
                46px 38px;
        }

    }


    /* ========================================================
       RESPONSIVE — MOBILE
       ======================================================== */

    @media (max-width: 760px) {

        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hjmi-hero {
            min-height: auto;

            padding:
                35px 24px;

            border-radius:
                20px;
        }

        .hjmi-hero-title {
            font-size:
                37px;
        }

        .hjmi-hero-subtitle {
            font-size:
                14px;

            letter-spacing:
                3px;
        }

        .hjmi-hero-description {
            font-size:
                13px;
        }

        .hjmi-metric {
            min-height:
                135px;
        }

        .hjmi-metric-value {
            font-size:
                27px;
        }

        .hjmi-job-meta {
            gap:
                6px;
        }

    }


    /* ========================================================
       SMALL MOBILE
       ======================================================== */

    @media (max-width: 480px) {

        .hjmi-hero-title {
            font-size:
                32px;
        }

        .hjmi-page-title {
            font-size:
                25px;
        }

        .hjmi-hero {
            padding:
                30px 20px;
        }

    }

    </style>
    """)


def brand():
    """Render the HJMI sidebar brand."""

    st.html("""
    <div class="hjmi-brand">

        <div class="hjmi-brand-mark">
            <div class="hjmi-brand-h">H</div>
        </div>

        <div class="hjmi-uae-line"></div>

        <div class="hjmi-brand-name">
            HJMI
        </div>

        <div class="hjmi-brand-sub">
            HASAN JOB MARKET INTELLIGENCE
        </div>

    </div>
    """)


def hero():
    """Render the main HJMI 2.0 hero."""

    st.html("""
    <div class="hjmi-hero">

        <div class="hjmi-hero-content">

            <div class="hjmi-eyebrow">
                ◇ UAE TECHNOLOGY CAREER INTELLIGENCE
            </div>

            <div class="hjmi-hero-title">
                Find Opportunities.
                <br>
                Understand the
                <span class="hjmi-gradient-text">
                    Market.
                </span>
            </div>

            <div class="hjmi-hero-subtitle">
                DATA • CAREERS • TECHNOLOGY
            </div>

            <div class="hjmi-hero-description">
                HJMI transforms UAE technology job-market data
                into practical insights for students, fresh graduates
                and professionals — helping users discover opportunities,
                understand employer requirements and make more informed
                career decisions.
            </div>

            <div class="hjmi-hero-pills">

                <div class="hjmi-pill">
                    🎓 Fresh Graduate Focus
                </div>

                <div class="hjmi-pill">
                    💼 Job Intelligence
                </div>

                <div class="hjmi-pill">
                    ⚡ Skills Intelligence
                </div>

                <div class="hjmi-pill">
                    🇦🇪 UAE Market
                </div>

            </div>

        </div>

    </div>
    """)


def page_header(kicker, title, description):
    """Render a consistent page heading."""

    st.html(
        f"""
        <div class="hjmi-page-header">

            <div class="hjmi-page-kicker">
                {kicker}
            </div>

            <div class="hjmi-page-title">
                {title}
            </div>

            <div class="hjmi-page-description">
                {description}
            </div>

        </div>
        """
    )


def explainer(title, text):
    """Explain what a page, chart or feature does."""

    st.html(
        f"""
        <div class="hjmi-explainer">
            💡 <strong>{title}</strong>
            <br>
            {text}
        </div>
        """
    )


def metric_card(icon, label, value, note=""):
    """Render a HJMI metric card."""

    st.html(
        f"""
        <div class="hjmi-metric">

            <div class="hjmi-metric-top">

                <div class="hjmi-metric-icon">
                    {icon}
                </div>

                <div class="hjmi-info">
                    ⓘ
                </div>

            </div>

            <div class="hjmi-metric-label">
                {label}
            </div>

            <div class="hjmi-metric-value">
                {value}
            </div>

            <div class="hjmi-metric-note">
                {note}
            </div>

        </div>
        """
    )


def status_card(content):
    """Render an informational status card."""

    st.html(
        f"""
        <div class="hjmi-status">
            {content}
        </div>
        """
    )


def footer():
    """Render the HJMI footer."""

    st.html("""
    <div class="hjmi-footer">

        <div class="hjmi-footer-brand">
            HJMI — HASAN JOB MARKET INTELLIGENCE
        </div>

        UAE Technology Career Intelligence Platform

        <br>

        Data • Jobs • Skills • Graduate Opportunities

        <br><br>

        Designed & Developed by
        Hasan R. H. Abdalhadi

    </div>
    """)
