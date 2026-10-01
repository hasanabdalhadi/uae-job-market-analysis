# ============================================================
# HJMI — ACCOUNT
# Sign In • Create Account • Account Management
# ============================================================

import streamlit as st

from components.theme import (
    apply_theme,
    page_header,
    footer,
)

from components.ui import (
    info_box,
)

from services.auth_service import (
    sign_up,
    sign_in,
    sign_out,
    is_authenticated,
    get_current_user,
    get_user_display_name,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="My HJMI | Account",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN
# ============================================================

apply_theme()


st.html(
    """
    <style>

    .hjmi-auth-wrap {
        max-width: 620px;
        margin: 0 auto;
    }

    .hjmi-auth-intro {
        text-align: center;
        margin: 10px auto 28px auto;
        max-width: 620px;
        color: #8298a5;
        font-size: 14px;
        line-height: 1.8;
    }

    .hjmi-auth-status {
        padding: 18px 20px;
        margin: 18px 0;
        border-radius: 16px;
        border: 1px solid rgba(216, 173, 87, 0.18);
        background: rgba(12, 40, 49, 0.65);
    }

    .hjmi-auth-status-title {
        color: #d8ad57;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.3px;
        margin-bottom: 7px;
    }

    .hjmi-auth-status-value {
        color: #f3f6f7;
        font-size: 17px;
        font-weight: 700;
    }

    </style>
    """
)


# ============================================================
# AUTHENTICATED USER
# ============================================================

if is_authenticated():

    user = get_current_user()
    display_name = get_user_display_name()

    page_header(
        "MY HJMI",
        f"Welcome, {display_name}",
        (
            "Your personal career space for saved opportunities, "
            "applications, job alerts and career preferences."
        ),
    )

    email = getattr(
        user,
        "email",
        "Not available",
    )

    st.html(
        f"""
        <div class="hjmi-auth-status">

            <div class="hjmi-auth-status-title">
                SIGNED IN
            </div>

            <div class="hjmi-auth-status-value">
                {display_name}
            </div>

            <div style="
                color:#7f96a3;
                margin-top:6px;
                font-size:12px;
            ">
                {email}
            </div>

        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Saved Jobs",
            "0",
            help="Saved opportunities will appear here.",
        )

    with col2:
        st.metric(
            "Applications",
            "0",
            help="Application tracking will appear here.",
        )

    with col3:
        st.metric(
            "Job Alerts",
            "0",
            help="Personalized alerts will appear here.",
        )

    st.info(
        "Your account is active. Saved Jobs, Applications and "
        "Job Alerts will be connected to your HJMI profile next."
    )

    if st.button(
        "Sign Out",
        use_container_width=True,
        type="secondary",
    ):
        sign_out()
        st.rerun()

    footer()
    st.stop()


# ============================================================
# SIGN IN / CREATE ACCOUNT
# ============================================================

page_header(
    "MY HJMI",
    "Your Career Space",
    (
        "Sign in to personalize your HJMI experience, "
        "or create an account to start building your "
        "career workspace."
    ),
)


st.html(
    """
    <div class="hjmi-auth-intro">
        Your HJMI account will become the central place for
        saved jobs, application tracking, career preferences
        and personalized opportunity alerts.
    </div>
    """
)


sign_in_tab, create_account_tab = st.tabs(
    [
        "Sign In",
        "Create Account",
    ]
)


# ============================================================
# SIGN IN
# ============================================================

with sign_in_tab:

    st.subheader("Welcome back")

    with st.form(
        "hjmi_sign_in_form",
        clear_on_submit=False,
    ):

        login_email = st.text_input(
            "Email",
            placeholder="name@example.com",
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        login_submit = st.form_submit_button(
            "Sign In",
            use_container_width=True,
            type="primary",
        )

    if login_submit:

        with st.spinner("Signing in..."):

            result = sign_in(
                login_email,
                login_password,
            )

        if result["success"]:

            st.success(
                result["message"]
            )

            st.rerun()

        else:

            st.error(
                result["message"]
            )


# ============================================================
# CREATE ACCOUNT
# ============================================================

with create_account_tab:

    st.subheader("Create your HJMI account")

    with st.form(
        "hjmi_create_account_form",
        clear_on_submit=False,
    ):

        full_name = st.text_input(
            "Full name",
            placeholder="Your full name",
        )

        signup_email = st.text_input(
            "Email",
            placeholder="name@example.com",
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
        )

        signup_password_confirm = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Enter your password again",
        )

        terms = st.checkbox(
            (
                "I understand that HJMI uses my account "
                "information to provide account features."
            )
        )

        signup_submit = st.form_submit_button(
            "Create Account",
            use_container_width=True,
            type="primary",
        )

    if signup_submit:

        if not full_name.strip():

            st.error(
                "Please enter your full name."
            )

        elif signup_password != signup_password_confirm:

            st.error(
                "The passwords do not match."
            )

        elif not terms:

            st.error(
                "Please confirm the account information notice."
            )

        else:

            with st.spinner(
                "Creating your HJMI account..."
            ):

                result = sign_up(
                    signup_email,
                    signup_password,
                    full_name,
                )

            if result["success"]:

                st.success(
                    result["message"]
                )

                info_box(
                    "Confirm your email",
                    (
                        "Open the confirmation email sent by "
                        "HJMI/Supabase and confirm your address. "
                        "After confirmation, return to HJMI and "
                        "sign in with your email and password."
                    ),
                    "✉",
                )

            else:

                st.error(
                    result["message"]
                )


# ============================================================
# ACCOUNT SECURITY NOTE
# ============================================================

st.divider()

info_box(
    "Account Security",
    (
        "HJMI authentication is handled through Supabase. "
        "Passwords are not stored inside the HJMI GitHub "
        "repository or job-market CSV files."
    ),
    "🔒",
)


# ============================================================
# FOOTER
# ============================================================

footer()
