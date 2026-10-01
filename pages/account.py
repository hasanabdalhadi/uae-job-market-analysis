# ============================================================
# HJMI — MY HJMI
# Account • Recommended Jobs • Saved Jobs • Application Tracker
# ============================================================

import html

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
    save_job,
    get_saved_jobs,
    get_saved_jobs_count,
    remove_saved_job,
    is_job_saved,
)

from services.application_service import (
    add_application,
    get_applications,
    get_applications_count,
    update_application_status,
    update_application_notes,
    remove_application,
    is_application_tracked,
)

from services.career_profile_service import (
    get_career_profile,
    get_profile_completion,
    profile_ready_for_matching,
)

from services.data_service import (
    load_jobs,
)

from services.matching_service import (
    get_recommended_jobs,
    get_match_summary,
)

from services.job_alerts_service import (
    sync_smart_job_alerts,
    get_job_alerts,
    get_unread_job_alerts_count,
    mark_job_alert_read,
    mark_all_job_alerts_read,
    remove_job_alert,
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

    .hjmi-match-badge {
        display: inline-block;
        padding: 6px 10px;
        margin-top: 12px;
        margin-right: 6px;
        border-radius: 20px;
        background: rgba(216, 173, 87, 0.10);
        border: 1px solid rgba(216, 173, 87, 0.24);
        color: #d8ad57;
        font-size: 11px;
        font-weight: 800;
    }

    .hjmi-match-score {
        display: inline-block;
        padding: 6px 10px;
        margin-top: 12px;
        border-radius: 20px;
        background: rgba(53, 166, 148, 0.10);
        border: 1px solid rgba(53, 166, 148, 0.22);
        color: #72d6c5;
        font-size: 11px;
        font-weight: 800;
    }

    .hjmi-match-reason {
        color: #9cafb8;
        font-size: 12px;
        line-height: 1.7;
        margin-top: 12px;
    }

    .hjmi-skill-wrap {
        margin-top: 10px;
    }

    .hjmi-skill {
        display: inline-block;
        padding: 5px 9px;
        margin: 3px 4px 3px 0;
        border-radius: 14px;
        background: rgba(53, 166, 148, 0.09);
        border: 1px solid rgba(53, 166, 148, 0.18);
        color: #86d8cb;
        font-size: 10px;
        font-weight: 700;
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
# HELPERS
# ============================================================

def safe(value):

    if value is None:
        return ""

    return html.escape(
        str(value)
    )


def list_value(value):

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    return []


def render_match_skills(skills):

    skills = list_value(
        skills
    )

    if not skills:
        return ""

    skill_html = "".join(
        (
            '<span class="hjmi-skill">'
            f'{safe(skill)}'
            '</span>'
        )
        for skill in skills[:10]
    )

    return (
        '<div class="hjmi-skill-wrap">'
        f'{skill_html}'
        '</div>'
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
        saved_jobs_count = len(
            saved_jobs
        )


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
        applications_count = len(
            applications
        )


    # ========================================================
    # CAREER PROFILE
    # ========================================================

    try:
        career_profile = get_career_profile()
    except Exception:
        career_profile = None

    try:
        profile_completion = (
            get_profile_completion(
                career_profile
            )
            if career_profile
            else 0
        )
    except Exception:
        profile_completion = 0

    try:
        matching_ready = (
            profile_ready_for_matching(
                career_profile
            )
            if career_profile
            else False
        )
    except Exception:
        matching_ready = False


    # ========================================================
    # CAREER MATCH
    # ========================================================

    recommendations = None

    if matching_ready:

        try:

            jobs_df = load_jobs()

            recommendations = (
                get_recommended_jobs(
                    jobs_df,
                    career_profile,
                    only_active=True,
                )
            )

        except Exception:
            recommendations = None


    try:

        match_summary = (
            get_match_summary(
                recommendations
            )
        )

    except Exception:

        match_summary = {
            "total_matches": 0,
            "strong_matches": 0,
            "good_matches": 0,
            "skill_matches": 0,
        }


    recommendation_count = (
        match_summary.get(
            "total_matches",
            0,
        )
    )


    # ========================================================
    # SMART JOB ALERTS
    # ========================================================

    if matching_ready and recommendations is not None:
        try:
            sync_smart_job_alerts(recommendations)
        except Exception:
            pass

    try:
        job_alerts = get_job_alerts()
    except Exception:
        job_alerts = []

    try:
        unread_alerts_count = get_unread_job_alerts_count()
    except Exception:
        unread_alerts_count = sum(
            1 for alert in job_alerts
            if not alert.get("is_read", False)
        )


    # ========================================================
    # PAGE HEADER
    # ========================================================

    page_header(
        "MY HJMI",
        f"Welcome, {display_name}",
        (
            "Your personal career space for recommended "
            "opportunities, saved jobs and application tracking."
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
                {safe(display_name)}
            </div>

            <div style="
                color:#7f96a3;
                margin-top:6px;
                font-size:12px;
            ">
                {safe(email)}
            </div>

        </div>
        """
    )


    # ========================================================
    # ACCOUNT METRICS
    # ========================================================

    col1, col2, col3, col4, col5 = st.columns(
        5
    )


    with col1:

        st.metric(
            "Recommended",
            recommendation_count,
            help=(
                "Current HJMI opportunities matching "
                "signals from your Career Profile."
            ),
        )


    with col2:

        st.metric(
            "Saved Jobs",
            saved_jobs_count,
            help=(
                "Opportunities saved to your "
                "personal HJMI account."
            ),
        )


    with col3:

        st.metric(
            "Applications",
            applications_count,
            help=(
                "Applications currently tracked "
                "inside your HJMI workspace."
            ),
        )


    with col4:

        st.metric(
            "Alerts",
            unread_alerts_count,
            help=(
                "Unread Smart Job Alerts for newly discovered "
                "matching opportunities."
            ),
        )


    with col5:

        st.metric(
            "Profile",
            f"{profile_completion}%",
            help=(
                "Career Profile completion."
            ),
        )


    # ========================================================
    # WORKSPACE TABS
    # ========================================================

    (
        recommended_tab,
        alerts_tab,
        saved_tab,
        applications_tab,
    ) = st.tabs(
        [
            "◎ Recommended for You",
            f"🔔 Job Alerts ({unread_alerts_count})",
            "♡ Saved Jobs",
            "◉ Application Tracker",
        ]
    )


    # ========================================================
    # RECOMMENDED FOR YOU
    # ========================================================

    with recommended_tab:

        st.html(
            """
            <div class="hjmi-section-heading">
                Recommended for You
            </div>

            <div class="hjmi-section-subheading">
                Current UAE technology opportunities matched
                against signals in your HJMI Career Profile.
            </div>
            """
        )


        # ----------------------------------------------------
        # NO PROFILE
        # ----------------------------------------------------

        if not career_profile:

            st.html(
                """
                <div class="hjmi-empty">

                    <div class="hjmi-empty-title">
                        Create your Career Profile
                    </div>

                    <div class="hjmi-empty-text">
                        Add your specialization, skills,
                        experience, preferred locations and
                        target roles to activate HJMI Career Match.
                    </div>

                </div>
                """
            )

            st.page_link(
                "pages/career_profile.py",
                label="Create Career Profile",
                icon="🎯",
                use_container_width=True,
            )


        # ----------------------------------------------------
        # PROFILE NOT READY
        # ----------------------------------------------------

        elif not matching_ready:

            st.html(
                """
                <div class="hjmi-empty">

                    <div class="hjmi-empty-title">
                        Career Profile needs more information
                    </div>

                    <div class="hjmi-empty-text">
                        Add skills, a specialization or target
                        roles before HJMI can calculate
                        personalized opportunity matches.
                    </div>

                </div>
                """
            )

            st.page_link(
                "pages/career_profile.py",
                label="Update Career Profile",
                icon="🎯",
                use_container_width=True,
            )


        # ----------------------------------------------------
        # NO MATCHES
        # ----------------------------------------------------

        elif (
            recommendations is None
            or recommendations.empty
        ):

            st.html(
                """
                <div class="hjmi-empty">

                    <div class="hjmi-empty-title">
                        No current matches found
                    </div>

                    <div class="hjmi-empty-text">
                        HJMI did not find a current opportunity
                        meeting the Career Match rules for your
                        profile. Your profile remains active and
                        can be used again as the job dataset updates.
                    </div>

                </div>
                """
            )

            st.page_link(
                "pages/career_profile.py",
                label="Review Career Profile",
                icon="🎯",
                use_container_width=True,
            )


        # ----------------------------------------------------
        # MATCHES
        # ----------------------------------------------------

        else:

            summary_col1, summary_col2, summary_col3 = (
                st.columns(
                    3
                )
            )

            with summary_col1:

                st.metric(
                    "Total Matches",
                    match_summary.get(
                        "total_matches",
                        0,
                    ),
                )

            with summary_col2:

                st.metric(
                    "Strong Matches",
                    match_summary.get(
                        "strong_matches",
                        0,
                    ),
                )

            with summary_col3:

                st.metric(
                    "Good Matches",
                    match_summary.get(
                        "good_matches",
                        0,
                    ),
                )


            st.caption(
                "HJMI Match measures overlap between your "
                "Career Profile and available job data. "
                "It does not predict hiring or acceptance."
            )

            st.divider()


            # Show a manageable number initially
            display_limit = min(
                len(recommendations),
                25,
            )

            for index in range(
                display_limit
            ):

                job = (
                    recommendations
                    .iloc[index]
                    .to_dict()
                )


                job_title = (
                    job.get(
                        "job_title_display",
                        "",
                    )
                    or job.get(
                        "job_title",
                        "",
                    )
                    or "Untitled Opportunity"
                )


                company = (
                    job.get(
                        "company_display",
                        "",
                    )
                    or job.get(
                        "company",
                        "",
                    )
                    or "Company not specified"
                )


                location = (
                    job.get(
                        "location_display",
                        "",
                    )
                    or job.get(
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


                job_identifier = (
                    str(job_url).strip()
                    or (
                        f"{job_title}|"
                        f"{company}|"
                        f"{location}"
                    )
                )


                match_score = (
                    job.get(
                        "hjmi_match_score",
                        0,
                    )
                    or 0
                )


                match_label = (
                    job.get(
                        "hjmi_match_label",
                        "",
                    )
                    or "Profile Match"
                )


                matched_skills = list_value(
                    job.get(
                        "hjmi_matched_skills",
                        [],
                    )
                )


                match_reasons = list_value(
                    job.get(
                        "hjmi_match_reasons",
                        [],
                    )
                )


                experience_label = (
                    job.get(
                        "hjmi_experience_label",
                        "",
                    )
                    or ""
                )


                reasons_text = (
                    " • ".join(
                        str(reason)
                        for reason
                        in match_reasons
                    )
                )


                if not reasons_text:
                    reasons_text = (
                        "Profile signals matched "
                        "this opportunity."
                    )


                skills_html = (
                    render_match_skills(
                        matched_skills
                    )
                )


                st.html(
                    f"""
                    <div class="hjmi-job-card">

                        <div class="hjmi-job-title">
                            {safe(job_title)}
                        </div>

                        <div class="hjmi-job-company">
                            {safe(company)}
                        </div>

                        <div class="hjmi-job-location">
                            📍 {safe(location)}
                        </div>

                        <div>
                            <span class="hjmi-match-badge">
                                {safe(match_label)}
                            </span>

                            <span class="hjmi-match-score">
                                HJMI Match {safe(match_score)}%
                            </span>
                        </div>

                        <div class="hjmi-match-reason">
                            Why this matched:
                            {safe(reasons_text)}
                        </div>

                        {skills_html}

                    </div>
                    """
                )


                if experience_label:

                    st.caption(
                        f"Experience signal: "
                        f"{experience_label}"
                    )


                # --------------------------------------------
                # CURRENT SAVED / TRACKED STATE
                # --------------------------------------------

                try:

                    already_saved = (
                        is_job_saved(
                            job_identifier
                        )
                    )

                except Exception:

                    already_saved = False


                try:

                    already_tracked = (
                        is_application_tracked(
                            job_identifier
                        )
                    )

                except Exception:

                    already_tracked = False


                action_col1, action_col2, action_col3 = (
                    st.columns(
                        [2, 1, 1]
                    )
                )


                # --------------------------------------------
                # VIEW JOB
                # --------------------------------------------

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
                            key=(
                                f"recommended_no_link_"
                                f"{index}"
                            ),
                            disabled=True,
                            use_container_width=True,
                        )


                # --------------------------------------------
                # SAVE JOB
                # --------------------------------------------

                with action_col2:

                    if already_saved:

                        st.button(
                            "✓ Saved",
                            key=(
                                f"recommended_saved_"
                                f"{index}"
                            ),
                            disabled=True,
                            use_container_width=True,
                        )

                    else:

                        if st.button(
                            "♡ Save",
                            key=(
                                f"recommended_save_"
                                f"{index}"
                            ),
                            use_container_width=True,
                        ):
                            result = save_job(
                                job_id=job_identifier,
                                job_title=job_title,
                                company=company,
                                location=location,
                                job_url=job_url,
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
                                else bool(
                                    result
                                )
                            )

                            if success:

                                st.toast(
                                    "✓ Saved to My HJMI"
                                )

                                st.rerun()

                            else:

                                message = (
                                    result.get(
                                        "message",
                                        (
                                            "HJMI could not "
                                            "save this job."
                                        ),
                                    )
                                    if isinstance(
                                        result,
                                        dict,
                                    )
                                    else (
                                        "HJMI could not "
                                        "save this job."
                                    )
                                )

                                st.error(
                                    message
                                )


                # --------------------------------------------
                # TRACK APPLICATION
                # --------------------------------------------

                with action_col3:

                    if already_tracked:

                        st.button(
                            "✓ Tracked",
                            key=(
                                f"recommended_tracked_"
                                f"{index}"
                            ),
                            disabled=True,
                            use_container_width=True,
                        )

                    else:

                        if st.button(
                            "Track",
                            key=(
                                f"recommended_track_"
                                f"{index}"
                            ),
                            use_container_width=True,
                        ):

                            result = add_application(
                                job_id=job_identifier,
                                job_title=job_title,
                                company=company,
                                location=location,
                                job_url=job_url,
                                status="Applied",
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
                                else bool(
                                    result
                                )
                            )

                            if success:

                                st.toast(
                                    "✓ Application added "
                                    "to your tracker."
                                )

                                st.rerun()

                            else:

                                message = (
                                    result.get(
                                        "message",
                                        (
                                            "HJMI could not "
                                            "track this application."
                                        ),
                                    )
                                    if isinstance(
                                        result,
                                        dict,
                                    )
                                    else (
                                        "HJMI could not "
                                        "track this application."
                                    )
                                )

                                st.error(
                                    message
                                )


                st.divider()


            if len(
                recommendations
            ) > display_limit:

                st.info(
                    (
                        f"Showing the first "
                        f"{display_limit} of "
                        f"{len(recommendations)} "
                        f"current profile matches."
                    )
                )


    # ========================================================
    # SMART JOB ALERTS
    # ========================================================

    with alerts_tab:

        st.html(
            """
            <div class="hjmi-section-heading">
                Smart Job Alerts
            </div>

            <div class="hjmi-section-subheading">
                Newly discovered HJMI opportunities that match
                signals in your Career Profile.
            </div>
            """
        )

        st.caption(
            "Alerts use HJMI discovery time and Career Profile "
            "overlap. They do not predict hiring or acceptance."
        )

        if unread_alerts_count > 0:
            if st.button(
                "Mark All as Read",
                key="mark_all_job_alerts_read",
                use_container_width=True,
            ):
                if mark_all_job_alerts_read():
                    st.toast("All job alerts marked as read.")
                    st.rerun()
                else:
                    st.error("HJMI could not update your alerts.")

        if not job_alerts:

            st.html(
                """
                <div class="hjmi-empty">
                    <div class="hjmi-empty-title">
                        No new job alerts yet
                    </div>
                    <div class="hjmi-empty-text">
                        Your alert baseline is active. Future newly
                        discovered opportunities matching your Career
                        Profile can appear here.
                    </div>
                </div>
                """
            )

        else:

            for index, alert in enumerate(job_alerts):

                alert_id = alert.get("id")
                job_title = alert.get("job_title", "") or "Untitled Opportunity"
                company = alert.get("company", "") or "Company not specified"
                location = alert.get("location", "") or "Location not specified"
                job_url = alert.get("job_url", "") or ""
                match_score = alert.get("match_score", 0) or 0
                match_label = alert.get("match_label", "") or "Profile Match"
                matched_skills = list_value(alert.get("matched_skills", []))
                match_reasons = list_value(alert.get("match_reasons", []))
                is_read = bool(alert.get("is_read", False))

                reasons_text = " • ".join(
                    str(reason) for reason in match_reasons
                ) or "Profile signals matched this opportunity."

                skills_html = render_match_skills(matched_skills)
                read_label = "Read" if is_read else "New Alert"

                st.html(
                    f"""
                    <div class="hjmi-job-card">
                        <div class="hjmi-job-title">{safe(job_title)}</div>
                        <div class="hjmi-job-company">{safe(company)}</div>
                        <div class="hjmi-job-location">📍 {safe(location)}</div>
                        <div>
                            <span class="hjmi-match-badge">{safe(read_label)}</span>
                            <span class="hjmi-match-badge">{safe(match_label)}</span>
                            <span class="hjmi-match-score">HJMI Match {safe(match_score)}%</span>
                        </div>
                        <div class="hjmi-match-reason">
                            Why this matched: {safe(reasons_text)}
                        </div>
                        {skills_html}
                    </div>
                    """
                )

                alert_col1, alert_col2, alert_col3 = st.columns([2, 1, 1])

                with alert_col1:
                    if job_url:
                        st.link_button(
                            "View Job",
                            job_url,
                            use_container_width=True,
                        )
                    else:
                        st.button(
                            "Job Link Unavailable",
                            key=f"alert_no_link_{alert_id}_{index}",
                            disabled=True,
                            use_container_width=True,
                        )

                with alert_col2:
                    if is_read:
                        st.button(
                            "✓ Read",
                            key=f"alert_read_{alert_id}_{index}",
                            disabled=True,
                            use_container_width=True,
                        )
                    elif st.button(
                        "Mark Read",
                        key=f"mark_alert_read_{alert_id}_{index}",
                        use_container_width=True,
                    ):
                        if mark_job_alert_read(alert_id):
                            st.toast("Job alert marked as read.")
                            st.rerun()
                        else:
                            st.error("HJMI could not update this alert.")

                with alert_col3:
                    if st.button(
                        "Remove",
                        key=f"remove_alert_{alert_id}_{index}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        if remove_job_alert(alert_id):
                            st.toast("Job alert removed.")
                            st.rerun()
                        else:
                            st.error("HJMI could not remove this alert.")

                st.divider()


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
                        Explore Find Jobs or your personalized
                        recommendations and save opportunities
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

            for index, job in enumerate(
                saved_jobs
            ):

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
                            {safe(job_title)}
                        </div>

                        <div class="hjmi-job-company">
                            {safe(company)}
                        </div>

                        <div class="hjmi-job-location">
                            📍 {safe(location)}
                        </div>

                    </div>
                    """
                )


                action_col1, action_col2 = (
                    st.columns(
                        [3, 1]
                    )
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
                            key=(
                                f"saved_no_link_"
                                f"{index}"
                            ),
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
                            else bool(
                                result
                            )
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
                        add it to your tracker from Find Jobs
                        or Recommended for You.
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

                application_id = (
                    application.get(
                        "id"
                    )
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


                if (
                    current_status
                    not in status_options
                ):
                    current_status = "Applied"


                st.html(
                    f"""
                    <div class="hjmi-job-card">

                        <div class="hjmi-job-title">
                            {safe(job_title)}
                        </div>

                        <div class="hjmi-job-company">
                            {safe(company)}
                        </div>

                        <div class="hjmi-job-location">
                            📍 {safe(location)}
                        </div>

                        <div class="hjmi-tracker-status">
                            {safe(current_status)}
                        </div>

                    </div>
                    """
                )


                tracker_col1, tracker_col2 = (
                    st.columns(
                        [2, 1]
                    )
                )


                # --------------------------------------------
                # STATUS
                # --------------------------------------------

                with tracker_col1:

                    selected_status = st.selectbox(
                        "Application Status",
                        options=status_options,
                        index=status_options.index(
                            current_status
                        ),
                        key=(
                            f"application_status_"
                            f"{application_id}_"
                            f"{index}"
                        ),
                    )


                with tracker_col2:

                    st.write("")
                    st.write("")

                    if st.button(
                        "Update Status",
                        key=(
                            f"update_status_"
                            f"{application_id}_"
                            f"{index}"
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


                # --------------------------------------------
                # NOTES
                # --------------------------------------------

                notes = st.text_area(
                    "Notes",
                    value=current_notes,
                    placeholder=(
                        "Add interview dates, recruiter notes, "
                        "follow-up reminders or other details..."
                    ),
                    key=(
                        f"application_notes_"
                        f"{application_id}_"
                        f"{index}"
                    ),
                    height=100,
                )


                if st.button(
                    "Save Notes",
                    key=(
                        f"save_notes_"
                        f"{application_id}_"
                        f"{index}"
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


                # --------------------------------------------
                # JOB / REMOVE ACTIONS
                # --------------------------------------------

                (
                    job_action_col1,
                    job_action_col2,
                ) = st.columns(
                    [3, 1]
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
                                f"{application_id}_"
                                f"{index}"
                            ),
                            disabled=True,
                            use_container_width=True,
                        )


                with job_action_col2:

                    if st.button(
                        "Remove",
                        key=(
                            f"remove_application_"
                            f"{application_id}_"
                            f"{index}"
                        ),
                        use_container_width=True,
                        type="secondary",
                    ):

                        success = (
                            remove_application(
                                application_id
                            )
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
    # WORKSPACE INFORMATION
    # ========================================================

    info_box(
        "Your HJMI Workspace",
        (
            "Career Match uses your approved Career Profile "
            "to identify relevant opportunities from the HJMI "
            "job dataset. Match information represents profile "
            "and job-data overlap, not hiring probability."
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
        Career Match, saved jobs, application tracking,
        career preferences and personalized opportunities.
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

        login_submit = (
            st.form_submit_button(
                "Sign In",
                use_container_width=True,
                type="primary",
            )
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

        signup_password_confirm = (
            st.text_input(
                "Confirm password",
                type="password",
                placeholder=(
                    "Enter your password again"
                ),
            )
        )

        terms = st.checkbox(
            (
                "I understand that HJMI uses my account "
                "information to provide account features."
            )
        )

        signup_submit = (
            st.form_submit_button(
                "Create Account",
                use_container_width=True,
                type="primary",
            )
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
