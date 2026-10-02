# ============================================================
# HJMI — CAREER PROFILE
# Career Profile • CV Intelligence • Career Match
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
    is_authenticated,
)

from services.career_profile_service import (
    get_career_profile,
    save_career_profile,
    get_profile_completion,
    profile_ready_for_matching,
)

from services.cv_service import (
    analyze_cv,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Career Profile | HJMI",
    page_icon="◈",
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

    .hjmi-profile-card {
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(216, 173, 87, 0.16);
        background: rgba(9, 31, 40, 0.58);
        margin-bottom: 12px;
    }

    .hjmi-profile-label {
        color: #d8ad57;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.4px;
        margin-bottom: 7px;
    }

    .hjmi-profile-value {
        color: #f3f6f7;
        font-size: 20px;
        font-weight: 750;
    }

    .hjmi-profile-description {
        color: #7f96a3;
        font-size: 12px;
        line-height: 1.7;
        margin-top: 7px;
    }

    .hjmi-cv-card {
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(216, 173, 87, 0.16);
        background:
            linear-gradient(
                145deg,
                rgba(9, 31, 40, 0.72),
                rgba(7, 25, 34, 0.78)
            );
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .hjmi-cv-label {
        color: #d8ad57;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.4px;
        margin-bottom: 6px;
    }

    .hjmi-cv-value {
        color: #f3f6f7;
        font-size: 14px;
        line-height: 1.7;
    }

    </style>
    """
)


# ============================================================
# HELPERS
# ============================================================

def safe(value):
    return html.escape(
        str(value or "")
    )


def merge_unique(
    original,
    new_values,
):
    result = []
    seen = set()

    for value in (
        list(original or [])
        + list(new_values or [])
    ):

        value = str(
            value or ""
        ).strip()

        if not value:
            continue

        key = value.lower()

        if key in seen:
            continue

        seen.add(key)
        result.append(value)

    return result


# ============================================================
# AUTH CHECK
# ============================================================

if not is_authenticated():

    page_header(
        "HJMI CAREER MATCH",
        "Career Profile",
        (
            "Build your career profile so HJMI can identify "
            "opportunities that match your skills and interests."
        ),
    )

    info_box(
        "Sign in required",
        (
            "Your Career Profile is connected to your personal "
            "HJMI account. Sign in to My HJMI before creating "
            "or editing your profile."
        ),
        "🔐",
    )

    st.page_link(
        "pages/account.py",
        label="Go to My HJMI",
        icon="👤",
        use_container_width=True,
    )

    footer()

    st.stop()


# ============================================================
# LOAD PROFILE
# ============================================================

profile = get_career_profile() or {}

completion = get_profile_completion(
    profile
)


# ============================================================
# HEADER
# ============================================================

page_header(
    "HJMI CAREER MATCH",
    "Career Profile",
    (
        "Build your career profile manually or use CV Intelligence "
        "to identify skills and career information from your CV."
    ),
)


# ============================================================
# PROFILE STATUS
# ============================================================

status_col1, status_col2 = st.columns(
    2
)


with status_col1:

    st.metric(
        "Profile Completion",
        f"{completion}%",
    )


with status_col2:

    if profile_ready_for_matching(
        profile
    ):

        st.metric(
            "Matching Status",
            "Ready",
        )

    else:

        st.metric(
            "Matching Status",
            "Profile Required",
        )


st.progress(
    completion / 100
)


# ============================================================
# EXPLANATION
# ============================================================

info_box(
    "How HJMI Profile Match works",
    (
        "Your Career Profile will be compared with technology "
        "opportunities in the HJMI UAE dataset. Jobs do not need "
        "to match every skill. Partial skill overlap, target roles, "
        "specialization, experience and location can all contribute "
        "to identifying relevant opportunities."
    ),
    "◈",
)


# ============================================================
# EXISTING PROFILE VALUES
# ============================================================

specialization_value = str(
    profile.get(
        "specialization",
        "",
    )
    or ""
)


target_roles_value = profile.get(
    "target_roles",
    []
) or []


skills_value = profile.get(
    "skills",
    []
) or []


experience_value = str(
    profile.get(
        "experience_level",
        "",
    )
    or ""
)


locations_value = profile.get(
    "preferred_locations",
    []
) or []


# ============================================================
# CAREER PROFILE FORM
# ============================================================

st.markdown(
    "## Your Career Information"
)

st.caption(
    "You can update these details whenever your skills "
    "or career goals change."
)


with st.form(
    "hjmi_career_profile_form"
):

    specialization = st.text_input(
        "Specialization / Field of Study",
        value=specialization_value,
        placeholder=(
            "Example: Computer Science, Software Engineering, "
            "Data Science..."
        ),
        help=(
            "Your academic specialization or main "
            "professional field."
        ),
    )


    target_roles_text = st.text_area(
        "Target Job Roles",
        value=", ".join(
            target_roles_value
        ),
        placeholder=(
            "Software Engineer, Data Analyst, "
            "Web Developer, IT Support"
        ),
        help=(
            "Separate multiple roles with commas."
        ),
        height=90,
    )


    skills_text = st.text_area(
        "Skills",
        value=", ".join(
            skills_value
        ),
        placeholder=(
            "Python, Java, SQL, JavaScript, HTML, CSS, "
            "MySQL, Data Analysis"
        ),
        help=(
            "Add all skills that HJMI should consider "
            "when matching jobs to your profile."
        ),
        height=120,
    )


    experience_options = [
        "Not Specified",
        "Fresh Graduate / Entry Level",
        "0–1 Year",
        "1–2 Years",
        "2–3 Years",
        "3–5 Years",
        "5+ Years",
    ]


    if (
        experience_value
        in experience_options
    ):

        experience_index = (
            experience_options.index(
                experience_value
            )
        )

    else:

        experience_index = 0


    experience_level = st.selectbox(
        "Experience Level",
        options=experience_options,
        index=experience_index,
    )


    preferred_locations_text = st.text_area(
        "Preferred UAE Locations",
        value=", ".join(
            locations_value
        ),
        placeholder=(
            "Dubai, Abu Dhabi, Sharjah, Remote"
        ),
        help=(
            "Separate multiple locations with commas."
        ),
        height=90,
    )


    save_profile = (
        st.form_submit_button(
            "Save Career Profile",
            use_container_width=True,
            type="primary",
        )
    )


# ============================================================
# SAVE MANUAL PROFILE
# ============================================================

if save_profile:

    target_roles = merge_unique(
        [],
        [
            value.strip()
            for value in target_roles_text.split(",")
            if value.strip()
        ],
    )


    skills = merge_unique(
        [],
        [
            value.strip()
            for value in skills_text.split(",")
            if value.strip()
        ],
    )


    preferred_locations = merge_unique(
        [],
        [
            value.strip()
            for value in preferred_locations_text.split(",")
            if value.strip()
        ],
    )


    result = save_career_profile(
        specialization=specialization,
        target_roles=target_roles,
        skills=skills,
        experience_level=experience_level,
        preferred_locations=preferred_locations,
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


# ============================================================
# CURRENT PROFILE SUMMARY
# ============================================================

if profile:

    st.divider()

    st.markdown(
        "## Current Profile"
    )


    summary_col1, summary_col2 = (
        st.columns(2)
    )


    with summary_col1:

        st.html(
            f"""
            <div class="hjmi-profile-card">

                <div class="hjmi-profile-label">
                    SPECIALIZATION
                </div>

                <div class="hjmi-profile-value">
                    {
                        safe(
                            specialization_value
                            or "Not specified"
                        )
                    }
                </div>

                <div class="hjmi-profile-description">
                    Your primary academic or professional field.
                </div>

            </div>
            """
        )


    with summary_col2:

        st.html(
            f"""
            <div class="hjmi-profile-card">

                <div class="hjmi-profile-label">
                    EXPERIENCE
                </div>

                <div class="hjmi-profile-value">
                    {
                        safe(
                            experience_value
                            or "Not specified"
                        )
                    }
                </div>

                <div class="hjmi-profile-description">
                    Experience level used for job matching.
                </div>

            </div>
            """
        )


    st.markdown(
        "### Target Roles"
    )

    if target_roles_value:

        st.write(
            ", ".join(target_roles_value)
        )

    else:

        st.caption(
            "No target roles added yet."
        )


    st.markdown(
        "### Skills"
    )

    if skills_value:

        st.write(
            ", ".join(skills_value)
        )

    else:

        st.caption(
            "No skills added yet."
        )


    st.markdown(
        "### Preferred Locations"
    )

    if locations_value:

        st.write(
            ", ".join(locations_value)
        )

    else:

        st.caption(
            "No preferred locations added yet."
        )


# ============================================================
# CV INTELLIGENCE
# ============================================================

st.divider()

st.markdown(
    "## CV Intelligence"
)

st.caption(
    "Upload a text-based PDF CV. HJMI will analyze it locally "
    "during this session and show you the detected information "
    "before anything is added to your Career Profile."
)


info_box(
    "Your CV stays under your control",
    (
        "Uploading a CV does not automatically replace your Career "
        "Profile. HJMI first shows the detected information. "
        "You decide whether to apply it to your profile."
    ),
    "📄",
)


uploaded_cv = st.file_uploader(
    "Upload CV",
    type=["pdf"],
    accept_multiple_files=False,
    help=(
        "PDF only. Text-based PDFs work best. "
        "Scanned image-only CVs may not contain readable text."
    ),
)


if uploaded_cv is not None:

    current_cv_name = uploaded_cv.name
    previous_cv_name = st.session_state.get("hjmi_cv_file_name")

    if previous_cv_name and previous_cv_name != current_cv_name:
        st.session_state.pop("hjmi_cv_analysis", None)
        st.session_state.pop("hjmi_cv_file_name", None)

    file_size = (
        len(
            uploaded_cv.getvalue()
        )
        / 1024
    )

    file_col1, file_col2 = (
        st.columns(2)
    )


    with file_col1:

        st.metric(
            "Selected CV",
            uploaded_cv.name,
        )


    with file_col2:

        st.metric(
            "File Size",
            f"{file_size:.1f} KB",
        )


    analyze_button = st.button(
        "Analyze CV",
        type="primary",
        use_container_width=True,
    )


    if analyze_button:

        with st.spinner(
            "HJMI is analyzing your CV..."
        ):

            analysis = analyze_cv(
                uploaded_cv
            )


        if analysis["success"]:

            st.session_state[
                "hjmi_cv_analysis"
            ] = analysis

            st.session_state[
                "hjmi_cv_file_name"
            ] = uploaded_cv.name

            st.toast(
                "CV analysis completed."
            )

        else:

            st.session_state.pop(
                "hjmi_cv_analysis",
                None,
            )

            st.error(
                analysis["message"]
            )


# ============================================================
# CV ANALYSIS RESULTS
# ============================================================

cv_analysis = st.session_state.get(
    "hjmi_cv_analysis"
)


if cv_analysis:

    st.markdown(
        "### CV Analysis Results"
    )

    st.caption(
        "Review the detected information before applying it "
        "to your Career Profile."
    )


    cv_col1, cv_col2 = st.columns(
        2
    )


    with cv_col1:

        st.html(
            f"""
            <div class="hjmi-cv-card">

                <div class="hjmi-cv-label">
                    DETECTED SPECIALIZATION
                </div>

                <div class="hjmi-cv-value">
                    {
                        safe(
                            cv_analysis.get(
                                "specialization"
                            )
                            or "Not detected"
                        )
                    }
                </div>

            </div>
            """
        )


    with cv_col2:

        st.html(
            f"""
            <div class="hjmi-cv-card">

                <div class="hjmi-cv-label">
                    DETECTED EXPERIENCE LEVEL
                </div>

                <div class="hjmi-cv-value">
                    {
                        safe(
                            cv_analysis.get(
                                "experience_level"
                            )
                            or "Not Specified"
                        )
                    }
                </div>

            </div>
            """
        )


    pages = cv_analysis.get(
        "pages",
        0,
    )

    skills_detected = cv_analysis.get(
        "skills",
        [],
    ) or []

    roles_detected = cv_analysis.get(
        "target_roles",
        [],
    ) or []


    metric1, metric2, metric3 = (
        st.columns(3)
    )


    with metric1:

        st.metric(
            "PDF Pages",
            pages,
        )


    with metric2:

        st.metric(
            "Skills Detected",
            len(
                skills_detected
            ),
        )


    with metric3:

        st.metric(
            "Role Signals",
            len(
                roles_detected
            ),
        )


    # --------------------------------------------------------
    # CONTACT INFORMATION
    # --------------------------------------------------------

    st.markdown(
        "#### Detected Contact Information"
    )


    contact_email = (
        cv_analysis.get(
            "email",
            "",
        )
        or "Not detected"
    )

    contact_phone = (
        cv_analysis.get(
            "phone",
            "",
        )
        or "Not detected"
    )

    linkedin = (
        cv_analysis.get(
            "linkedin",
            "",
        )
        or "Not detected"
    )

    github = (
        cv_analysis.get(
            "github",
            "",
        )
        or "Not detected"
    )


    contact1, contact2 = st.columns(
        2
    )


    with contact1:

        st.write(
            f"**Email:** {contact_email}"
        )

        st.write(
            f"**Phone:** {contact_phone}"
        )


    with contact2:

        st.write(
            f"**LinkedIn:** {linkedin}"
        )

        st.write(
            f"**GitHub:** {github}"
        )


    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    st.markdown(
        "#### Detected Skills"
    )


    if skills_detected:

        st.write(
            " • ".join(
                skills_detected
            )
        )

    else:

        st.caption(
            "No skills from the current HJMI skill catalog "
            "were detected in this CV."
        )


    # --------------------------------------------------------
    # ROLE SIGNALS
    # --------------------------------------------------------

    st.markdown(
        "#### Detected Career / Role Signals"
    )


    if roles_detected:

        st.write(
            " • ".join(
                roles_detected
            )
        )

    else:

        st.caption(
            "No specific target-role signals were detected."
        )


    # --------------------------------------------------------
    # REVIEW / EDIT BEFORE APPLYING
    # --------------------------------------------------------

    st.markdown(
        "### Review Before Applying"
    )

    st.caption(
        "You can edit the detected information below. "
        "Only the values you approve here will be added "
        "to your Career Profile."
    )


    detected_specialization = (
        cv_analysis.get(
            "specialization",
            "",
        )
        or specialization_value
    )


    detected_experience = (
        cv_analysis.get(
            "experience_level",
            "Not Specified",
        )
        or "Not Specified"
    )


    if (
        detected_experience
        not in experience_options
    ):

        detected_experience = (
            "Not Specified"
        )


    detected_experience_index = (
        experience_options.index(
            detected_experience
        )
    )


    with st.form(
        "hjmi_cv_review_form"
    ):

        reviewed_specialization = (
            st.text_input(
                "Specialization",
                value=(
                    detected_specialization
                ),
            )
        )


        reviewed_roles = (
            st.text_area(
                "Target Roles / Role Signals",
                value=", ".join(
                    roles_detected
                ),
                height=90,
                help=(
                    "You can remove, add or edit roles "
                    "before applying them."
                ),
            )
        )


        reviewed_skills = (
            st.text_area(
                "Skills Detected from CV",
                value=", ".join(
                    skills_detected
                ),
                height=140,
                help=(
                    "Review the detected skills carefully. "
                    "You can remove incorrect skills or add "
                    "skills that HJMI did not detect."
                ),
            )
        )


        reviewed_experience = (
            st.selectbox(
                "Experience Level",
                options=experience_options,
                index=(
                    detected_experience_index
                ),
            )
        )


        st.caption(
            "Your existing preferred UAE locations will not "
            "be changed by CV analysis."
        )


        apply_cv = (
            st.form_submit_button(
                "Apply CV Data to Career Profile",
                type="primary",
                use_container_width=True,
            )
        )


    # --------------------------------------------------------
    # APPLY APPROVED CV DATA
    # --------------------------------------------------------

    if apply_cv:

        approved_roles = [
            value.strip()
            for value in
            reviewed_roles.split(",")
            if value.strip()
        ]


        approved_skills = [
            value.strip()
            for value in
            reviewed_skills.split(",")
            if value.strip()
        ]


        merged_roles = merge_unique(
            target_roles_value,
            approved_roles,
        )


        merged_skills = merge_unique(
            skills_value,
            approved_skills,
        )


        final_specialization = (
            reviewed_specialization.strip()
            or specialization_value
        )


        final_experience = (
            reviewed_experience
        )


        if (
            final_experience
            == "Not Specified"
            and experience_value
        ):

            final_experience = (
                experience_value
            )


        result = save_career_profile(
            specialization=(
                final_specialization
            ),
            target_roles=merged_roles,
            skills=merged_skills,
            experience_level=(
                final_experience
            ),
            preferred_locations=(
                locations_value
            ),
        )


        if result["success"]:

            st.session_state.pop(
                "hjmi_cv_analysis",
                None,
            )

            st.session_state.pop(
                "hjmi_cv_file_name",
                None,
            )

            st.toast(
                "Approved CV information added to your Career Profile."
            )

            st.rerun()

        else:

            st.error(
                result["message"]
            )


    # --------------------------------------------------------
    # RAW TEXT PREVIEW
    # --------------------------------------------------------

    with st.expander(
        "View extracted CV text"
    ):

        st.caption(
            "This is the text HJMI could read from the PDF. "
            "It is shown for transparency and troubleshooting."
        )

        st.text_area(
            "Extracted CV Text",
            value=cv_analysis.get(
                "text",
                "",
            ),
            height=300,
            disabled=True,
        )


# ============================================================
# MATCHING PREVIEW
# ============================================================

st.divider()

st.markdown(
    "## Personalized Opportunities"
)

info_box(
    "Career Match is available",
    (
        "HJMI can use the Career Profile you approved — including manual "
        "information and approved CV-derived skills — to compare your "
        "profile with structured UAE opportunity data. Results describe "
        "profile relevance and do not predict employer interest or hiring."
    ),
    "◎",
)

st.page_link(
    "pages/account.py",
    label="Open My HJMI Recommendations",
    icon="🎯",
    use_container_width=True,
)


# ============================================================
# FOOTER
# ============================================================

footer()
