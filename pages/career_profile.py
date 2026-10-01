# ============================================================
# HJMI — CAREER PROFILE
# Personal Career Intelligence
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
    is_authenticated,
)

from services.career_profile_service import (
    get_career_profile,
    save_career_profile,
    get_profile_completion,
    profile_ready_for_matching,
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
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(216, 173, 87, 0.16);
        background: rgba(9, 31, 40, 0.58);
        margin-bottom: 20px;
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

    </style>
    """
)


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
        "Tell HJMI about your specialization, skills, career "
        "interests and preferred locations. This information "
        "will power personalized job matching."
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
    "How HJMI Career Match will work",
    (
        "HJMI will compare your Career Profile with technology "
        "opportunities in the UAE job dataset. A job does not "
        "need to match every skill in your profile. Even partial "
        "skill overlap can make an opportunity relevant."
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

    # --------------------------------------------------------
    # SPECIALIZATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # TARGET ROLES
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # LOCATIONS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SUBMIT
    # --------------------------------------------------------

    save_profile = (
        st.form_submit_button(
            "Save Career Profile",
            use_container_width=True,
            type="primary",
        )
    )


# ============================================================
# SAVE PROFILE
# ============================================================

if save_profile:

    target_roles = [
        value.strip()
        for value in
        target_roles_text.split(",")
        if value.strip()
    ]


    skills = [
        value.strip()
        for value in
        skills_text.split(",")
        if value.strip()
    ]


    preferred_locations = [
        value.strip()
        for value in
        preferred_locations_text.split(",")
        if value.strip()
    ]


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
                        specialization_value
                        or "Not specified"
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
                        experience_value
                        or "Not specified"
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
            " • ".join(
                target_roles_value
            )
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
            " • ".join(
                skills_value
            )
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
            " • ".join(
                locations_value
            )
        )

    else:

        st.caption(
            "No preferred locations added yet."
        )


# ============================================================
# CV INTELLIGENCE PREVIEW
# ============================================================

st.divider()

st.markdown(
    "## CV Intelligence"
)

info_box(
    "CV Analysis — Next Step",
    (
        "The next HJMI Career Match feature will allow you "
        "to upload your CV. HJMI will extract career information "
        "and skills from the CV, let you review the extracted "
        "profile, and use the approved information for job matching."
    ),
    "📄",
)


# ============================================================
# MATCHING PREVIEW
# ============================================================

st.markdown(
    "## Personalized Opportunities"
)

info_box(
    "Job Matching — Coming Next",
    (
        "Once your Career Profile is ready, HJMI will identify "
        "jobs that share your skills, target roles, specialization, "
        "experience level or preferred locations. Partial matches "
        "will also be considered instead of requiring every skill "
        "to match."
    ),
    "◎",
)


# ============================================================
# FOOTER
# ============================================================

footer()
