# ============================================================
# HJMI — ACCOUNT
# Sign In • Create Account • Saved Jobs • Application Tracker
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

from services.saved_jobs_service import (
    get_saved_jobs,
    get_saved_jobs_count,
    remove_saved_job,
)

from services.application_service import (
    get_applications,
    get_applications_count,
    update_application_status,
    update_application_notes,
    remove_application,
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
        margin: 18px 0 24px 0;
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

    .hjmi-section-heading {
        margin-top: 30px;
        margin-bottom: 6px;
        color: #f3f6f7;
        font-size: 24px;
        font-weight: 800;
    }

    .hjmi-section-subheading {
        color: #78909d;
        font-size: 13px;
        line-height: 1.7;
        margin-bottom: 18px;
    }

    .hjmi-job-card {
        padding: 18px 20px;
        margin: 0 0 10px 0;
        border-radius: 15px;
        border: 1px solid rgba(216, 173, 87, 0.14);
        background:
            linear-gradient(
                145deg,
                rgba(12, 40, 49, 0.72),
                rgba(8, 29, 38, 0.78)
            );
    }

    .hjmi-job-title {
        color: #f4f6f7;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .hjmi-job-company {
        color: #d8ad57;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .hjmi-job-location {
        color: #7f96a3;
        font-size: 11px;
    }

    .hjmi-empty {
        padding: 28px 22px;
        margin-top: 15px;
        border-radius: 16px;
        text-align: center;
        border: 1px dashed rgba(216, 173, 87, 0.20);
        background: rgba(9, 31, 40, 0.42);
    }

    .hjmi-empty-title {
        color: #f3f6f7;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .hjmi-empty-text {
        color: #78909d;
        font-size: 12px;
        line-height: 1.7;
    }

    .hjmi-tracker-status {
        display: inline-block;
        padding: 6px 10px;
        margin-top: 10px;
        border-radius: 20px;
        background: rgba(216, 173, 87, 0.10);
        border: 1px solid rgba(216, 173, 87, 0.20);
        color: #d8ad57;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.4px;
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

    email = getattr(
        user,
        "email",
        "Not available",
    )


    # ========================================================
    # SAVED JOB DATA
    # ========================================================

    try:
        saved_jobs = get_saved_jobs()
    except Exception:
        saved_jobs = []

    try:
        saved_jobs_count = get_saved_jobs_count()
    except Exception:
        saved_jobs_count = len(saved_jobs)


    # ========================================================
    # APPLICATION DATA
    # ========================================================

    try:
        applications = get_applications()
    except Exception:
        applications = []

    try:
        applications_count = get_applications_count()
    except Exception:
        applications_count = len(applications)


    # ========================================================
    # PAGE HEADER
    # ========================================================

    page_header(
        "MY HJMI",
        f"Welcome, {display_name}",
        (
            "Your personal career space for saved opportunities, "
            "applications, job alerts and career preferences."
        ),
    )


    # ========================================================
    # ACCOUNT STATUS
    # ========================================================

    st.html(
        f"""
        <div class="hjmi-auth-status">

            <div class="hjmi-auth-status-title">
                ACCOUNT ACTIVE
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


    # ========================================================
    # ACCOUNT METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Saved Jobs",
            saved_jobs_count,
            help=(
                "Opportunities saved to your "
                "personal HJMI account."
            ),
        )

    with col2:

        st.metric(
            "Applications",
            applications_count,
            help=(
                "Applications currently tracked "
                "inside your HJMI workspace."
            ),
        )

    with col3:

        st.metric(
            "Job Alerts",
            "0",
            help=(
                "Personalized job alerts will be "
                "available in a future HJMI update."
            ),
        )


    # ========================================================
    # WORKSPACE TABS
    # ========================================================

    saved_tab, applications_tab = st.tabs(
        [
            "♡ Saved Jobs",
            "◉ Application Tracker",
        ]
    )


    # ========================================================
    # SAVED JOBS
    # ========================================================

    with saved_tab:

        st.html(
            """
            <div class="hjmi-section-heading">
                Saved Jobs
            </div>

            <div class="hjmi-section-subheading">
                Opportunities you saved while exploring the
                UAE technology job market.
            </div>
            """
        )


        if not saved_jobs:

            st.html(
                """
                <div class="hjmi-empty">

                    <div class="hjmi-empty-title">
                        No saved jobs yet
                    </div>

                    <div class="hjmi-empty-text">
                        Explore Find Jobs and save opportunities
                        you want to review later.
                    </div>

                </div>
                """
            )

            st.page_link(
                "pages/find_jobs.py",
                label="Explore Jobs",
                icon="🔎",
                use_container_width=True,
            )

        else:

            for index, job in enumerate(saved_jobs):

                job_id = str(
                    job.get(
                        "job_id",
                        "",
                    )
                )

                job_title = (
                    job.get(
                        "job_title",
                        "",
                    )
                    or "Untitled Opportunity"
                )

                company = (
                    job.get(
                        "company",
                        "",
                    )
                    or "Company not specified"
                )

                location = (
                    job.get(
                        "location",
                        "",
                    )
                    or "Location not specified"
                )

                job_url = (
                    job.get(
                        "job_url",
                        "",
                    )
                    or ""
                )


                st.html(
                    f"""
                    <div class="hjmi-job-card">

                        <div class="hjmi-job-title">
                            {job_title}
                        </div>

                        <div class="hjmi-job-company">
                            {company}
                        </div>

                        <div class="hjmi-job-location">
                            📍 {location}
                        </div>

                    </div>
                    """
                )


                action_col1, action_col2 = st.columns(
                    [3, 1]
                )


                with action_col1:

                    if job_url:

                        st.link_button(
                            "View Job",
                            job_url,
                            use_container_width=True,
                        )

                    else:

                        st.button(
                            "Job Link Unavailable",
                            key=f"no_link_{index}",
                            disabled=True,
                            use_container_width=True,
                        )


                with action_col2:

                    if st.button(
                        "Remove",
                        key=(
                            f"remove_saved_"
                            f"{job_id}_{index}"
                        ),
                        use_container_width=True,
                        type="secondary",
                    ):

                        result = remove_saved_job(
                            job_id
                        )

                        success = (
                            result.get(
                                "success",
                                False,
                            )
                            if isinstance(
                                result,
                                dict,
                            )
                            else bool(result)
                        )

                        if success:

                            st.toast(
                                "Job removed from My HJMI."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "HJMI could not remove "
                                "this saved job."
                            )


                st.divider()


    # ========================================================
    # APPLICATION TRACKER
    # ========================================================

    with applications_tab:

        st.html(
            """
            <div class="hjmi-section-heading">
                Application Tracker
            </div>

            <div class="hjmi-section-subheading">
                Track your progress after applying for
                opportunities you discover through HJMI.
            </div>
            """
        )


        if not applications:

            st.html(
                """
                <div class="hjmi-empty">

                    <div class="hjmi-empty-title">
                        No applications tracked yet
                    </div>

                    <div class="hjmi-empty-text">
                        When you apply for an opportunity,
                        add it to your tracker from Find Jobs.
                    </div>

                </div>
                """
            )

            st.page_link(
                "pages/find_jobs.py",
                label="Find Opportunities",
                icon="🔎",
                use_container_width=True,
            )

        else:

            status_options = [
                "Applied",
                "Interview",
                "Offer",
                "Rejected",
                "Withdrawn",
            ]


            for index, application in enumerate(
                applications
            ):

                application_id = application.get(
                    "id"
                )

                job_title = (
                    application.get(
                        "job_title",
                        "",
                    )
                    or "Untitled Opportunity"
                )

                company = (
                    application.get(
                        "company",
                        "",
                    )
                    or "Company not specified"
                )

                location = (
                    application.get(
                        "location",
                        "",
                    )
                    or "Location not specified"
                )

                job_url = (
                    application.get(
                        "job_url",
                        "",
                    )
                    or ""
                )

                current_status = (
                    application.get(
                        "status",
                        "Applied",
                    )
                    or "Applied"
                )

                current_notes = (
                    application.get(
                        "notes",
                        "",
                    )
                    or ""
                )


                if current_status not in status_options:
                    current_status = "Applied"


                st.html(
                    f"""
                    <div class="hjmi-job-card">

                        <div class="hjmi-job-title">
                            {job_title}
                        </div>

                        <div class="hjmi-job-company">
                            {company}
                        </div>

                        <div class="hjmi-job-location">
                            📍 {location}
                        </div>

                        <div class="hjmi-tracker-status">
                            {current_status}
                        </div>

                    </div>
                    """
                )


                tracker_col1, tracker_col2 = st.columns(
                    [2, 1]
                )


                # ============================================
                # STATUS
                # ============================================

                with tracker_col1:

                    selected_status = st.selectbox(
                        "Application Status",
                        options=status_options,
                        index=status_options.index(
                            current_status
                        ),
                        key=(
                            f"application_status_"
                            f"{application_id}_{index}"
                        ),
                    )


                with tracker_col2:

                    st.write("")

                    st.write("")

                    if st.button(
                        "Update Status",
                        key=(
                            f"update_status_"
                            f"{application_id}_{index}"
                        ),
                        use_container_width=True,
                    ):

                        result = (
                            update_application_status(
                                application_id,
                                selected_status,
                            )
                        )

                        if result["success"]:

                            st.toast(
                                result["message"]
                            )

                            st.rerun()

                        else:

                            st.error(
                                result["message"]
                            )


                # ============================================
                # NOTES
                # ============================================

                notes = st.text_area(
                    "Notes",
                    value=current_notes,
                    placeholder=(
                        "Add interview dates, recruiter notes, "
                        "follow-up reminders or other details..."
                    ),
                    key=(
                        f"application_notes_"
                        f"{application_id}_{index}"
                    ),
                    height=100,
                )


                if st.button(
                    "Save Notes",
                    key=(
                        f"save_notes_"
                        f"{application_id}_{index}"
                    ),
                    use_container_width=True,
                ):

                    result = (
                        update_application_notes(
                            application_id,
                            notes,
                        )
                    )

                    if result["success"]:

                        st.toast(
                            result["message"]
                        )

                    else:

                        st.error(
                            result["message"]
                        )


                # ============================================
                # JOB / REMOVE ACTIONS
                # ============================================

                job_action_col1, job_action_col2 = (
                    st.columns(
                        [3, 1]
                    )
                )


                with job_action_col1:

                    if job_url:

                        st.link_button(
                            "View Job",
                            job_url,
                            use_container_width=True,
                        )

                    else:

                        st.button(
                            "Job Link Unavailable",
                            key=(
                                f"application_no_link_"
                                f"{application_id}_{index}"
                            ),
                            disabled=True,
                            use_container_width=True,
                        )


                with job_action_col2:

                    if st.button(
                        "Remove",
                        key=(
                            f"remove_application_"
                            f"{application_id}_{index}"
                        ),
                        use_container_width=True,
                        type="secondary",
                    ):

                        success = remove_application(
                            application_id
                        )

                        if success:

                            st.toast(
                                "Application removed "
                                "from your tracker."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "HJMI could not remove "
                                "this application."
                            )


                st.divider()


    # ========================================================
    # ACCOUNT ROADMAP
    # ========================================================

    info_box(
        "Your HJMI Workspace",
        (
            "Saved Jobs and Application Tracker are connected "
            "to your HJMI account. Job alerts and career "
            "preferences will be added as the platform develops."
        ),
        "👤",
    )


    # ========================================================
    # SIGN OUT
    # ========================================================

    st.divider()

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
        Your HJMI account is your personal space for
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

    st.subheader(
        "Welcome back"
    )

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

        with st.spinner(
            "Signing in..."
        ):

            result = sign_in(
                login_email,
                login_password,
            )


        if result["success"]:

            st.success(
                result["message"]
            )

            st.info(
                "Sign in completed. Your HJMI session "
                "is being saved."
            )

        else:

            st.error(
                result["message"]
            )


# ============================================================
# CREATE ACCOUNT
# ============================================================

with create_account_tab:

    st.subheader(
        "Create your HJMI account"
    )

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

        elif (
            signup_password
            != signup_password_confirm
        ):

            st.error(
                "The passwords do not match."
            )

        elif not terms:

            st.error(
                "Please confirm the account "
                "information notice."
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
