# ============================================================
# HJMI 2.2 — SMART JOB EXPLORER
# Hasan Job Market Intelligence
# ============================================================

import streamlit as st

from components.theme import (
    apply_theme,
    brand,
    page_header,
    footer,
)

from components.ui import (
    info_box,
    job_card,
    empty_state,
    data_status,
    result_count,
)

from services.data_service import (
    load_jobs,
    get_active_jobs,
    get_new_jobs,
    get_historical_jobs,
    get_filter_options,
    search_jobs,
    get_market_metrics,
)

from services.auth_service import (
    is_authenticated,
)

from services.saved_jobs_service import (
    save_job,
    remove_saved_job,
    get_saved_jobs,
)

from services.application_service import (
    add_application,
    get_applications,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Find Jobs | HJMI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN
# ============================================================

apply_theme()


# ============================================================
# SIDEBAR BRAND
# ============================================================

with st.sidebar:

    brand()

    st.markdown(
        """
        <div style="
            color:#d8ad57;
            font-size:9px;
            font-weight:800;
            letter-spacing:2px;
            margin:5px 0 10px 0;
        ">
            SMART JOB EXPLORER
        </div>

        <div style="
            color:#758b9d;
            font-size:11px;
            line-height:1.8;
            margin-bottom:18px;
        ">
            Discover UAE technology opportunities using
            HJMI market intelligence and practical filters.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

df = load_jobs()


if df.empty:

    page_header(
        "HJMI JOB DISCOVERY",
        "Find Jobs",
        "Explore UAE technology opportunities.",
    )

    empty_state(
        title="Job data is unavailable",
        message=(
            "HJMI could not load the current market dataset."
        ),
        icon="⚠",
    )

    footer()

    st.stop()


# ============================================================
# HEADER
# ============================================================

page_header(
    "SMART JOB EXPLORER",
    "Find UAE Technology Opportunities",
    (
        "Search and filter technology opportunities by status, "
        "location, company, skill, experience and graduate suitability."
    ),
)


# ============================================================
# DATA STATUS
# ============================================================

metrics = get_market_metrics(df)

data_status(
    metrics["last_update"]
)


# ============================================================
# STATUS EXPLANATION
# ============================================================

info_box(
    "Opportunity status",
    (
        "Active means the opportunity appeared in HJMI's latest "
        "market collection. New means HJMI discovered it for the "
        "first time during the latest update. Historical means the "
        "record is retained by HJMI but was not returned in the "
        "latest collection."
    ),
    "ⓘ",
)


# ============================================================
# STATUS FILTER
# ============================================================

status_choice = st.segmented_control(
    "Opportunity Status",
    options=[
        "Active",
        "New",
        "Historical",
        "All",
    ],
    default="Active",
)


if status_choice == "New":

    working_df = get_new_jobs(df)

elif status_choice == "Historical":

    working_df = get_historical_jobs(df)

elif status_choice == "All":

    working_df = df.copy()

else:

    working_df = get_active_jobs(df)


# ============================================================
# SEARCH
# ============================================================

st.markdown("### 🔎 Search")

search_text = st.text_input(
    "Search jobs",
    placeholder=(
        "Search job title, company, skill, category or keyword..."
    ),
    label_visibility="collapsed",
)


# ============================================================
# FILTER OPTIONS
# ============================================================

filter_options = get_filter_options(
    working_df
)


# ============================================================
# FILTER PANEL
# ============================================================

st.markdown("### ◇ Refine Results")

filter_row_1 = st.columns(3)


with filter_row_1[0]:

    location = st.selectbox(
        "Location",
        [
            "All Locations",
            *filter_options["locations"],
        ],
    )


with filter_row_1[1]:

    company = st.selectbox(
        "Company",
        [
            "All Companies",
            *filter_options["companies"],
        ],
    )


with filter_row_1[2]:

    skill = st.selectbox(
        "Skill",
        [
            "All Skills",
            *filter_options["skills"],
        ],
    )


filter_row_2 = st.columns(3)


with filter_row_2[0]:

    experience = st.selectbox(
        "Experience Level",
        [
            "All Experience Levels",
            *filter_options[
                "experience_levels"
            ],
        ],
    )


with filter_row_2[1]:

    graduate_only = st.checkbox(
        "🎓 Fresh Graduate Friendly"
    )


with filter_row_2[2]:

    salary_only = st.checkbox(
        "💰 Salary Disclosed"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_jobs = search_jobs(
    working_df,
    search_text=search_text,
    location=location,
    company=company,
    skill=skill,
    experience=experience,
    graduate_only=graduate_only,
)


if salary_only:

    filtered_jobs = filtered_jobs[
        filtered_jobs["salary_disclosed"]
    ].copy()


# ============================================================
# SORTING
# ============================================================

sort_choice = st.selectbox(
    "Sort results",
    [
        "Newest discovered by HJMI",
        "Job title A–Z",
        "Company A–Z",
        "Location A–Z",
    ],
)


if sort_choice == "Job title A–Z":

    filtered_jobs = filtered_jobs.sort_values(
        "job_title",
        key=lambda col:
        col.fillna("").str.lower(),
    )


elif sort_choice == "Company A–Z":

    filtered_jobs = filtered_jobs.sort_values(
        "company",
        key=lambda col:
        col.fillna("").str.lower(),
    )


elif sort_choice == "Location A–Z":

    filtered_jobs = filtered_jobs.sort_values(
        "location",
        key=lambda col:
        col.fillna("").str.lower(),
    )


else:

    if "first_seen" in filtered_jobs.columns:

        filtered_jobs = (
            filtered_jobs
            .assign(
                _first_seen_sort=
                st.session_state.get(
                    "_unused_sort",
                    None,
                )
            )
        )

        filtered_jobs[
            "_first_seen_sort"
        ] = filtered_jobs[
            "first_seen"
        ]

        filtered_jobs = (
            filtered_jobs
            .sort_values(
                "_first_seen_sort",
                ascending=False,
            )
        )


# ============================================================
# RESULTS HEADER
# ============================================================

st.markdown("---")

result_count(
    len(filtered_jobs),
    "matching opportunities",
)


# ============================================================
# ACTIVE FILTER SUMMARY
# ============================================================

active_filters = []


if search_text:
    active_filters.append(
        f'Search: "{search_text}"'
    )

if location != "All Locations":
    active_filters.append(
        f"Location: {location}"
    )

if company != "All Companies":
    active_filters.append(
        f"Company: {company}"
    )

if skill != "All Skills":
    active_filters.append(
        f"Skill: {skill}"
    )

if experience != "All Experience Levels":
    active_filters.append(
        f"Experience: {experience}"
    )

if graduate_only:
    active_filters.append(
        "Fresh Graduate Friendly"
    )

if salary_only:
    active_filters.append(
        "Salary Disclosed"
    )


if active_filters:

    st.caption(
        "Filters: "
        + " • ".join(active_filters)
    )


# ============================================================
# USER STATE
# ============================================================

authenticated = is_authenticated()

saved_job_ids = set()

tracked_job_ids = set()


if authenticated:

    try:

        saved_jobs = get_saved_jobs()

        saved_job_ids = {
            str(saved_job.get("job_id", ""))
            for saved_job in saved_jobs
            if saved_job.get("job_id")
        }

    except Exception:

        saved_job_ids = set()


    try:

        applications = get_applications()

        tracked_job_ids = {
            str(application.get("job_id", ""))
            for application in applications
            if application.get("job_id")
        }

    except Exception:

        tracked_job_ids = set()


# ============================================================
# RESULTS
# ============================================================

if filtered_jobs.empty:

    empty_state(
        title="No matching opportunities found",
        message=(
            "Try removing one or more filters or using "
            "a broader search term."
        ),
        icon="⌕",
    )

else:

    # Prevent extremely long pages.
    # Users can increase the number displayed.

    display_options = [
        10,
        25,
        50,
        100,
    ]

    max_available = len(
        filtered_jobs
    )


    if max_available <= 10:

        display_limit = max_available

    else:

        display_limit = st.selectbox(
            "Jobs displayed",
            [
                option
                for option in display_options
                if option <= max_available
            ]
            + (
                [max_available]
                if (
                    max_available
                    not in display_options
                    and max_available > 10
                )
                else []
            ),
        )


    jobs_to_display = (
        filtered_jobs
        .head(display_limit)
    )


    # ========================================================
    # JOB CARDS
    # ========================================================

    for row_index, job in jobs_to_display.iterrows():

        job_card(
            job,
            show_description=False,
        )


        # ----------------------------------------------------
        # JOB DATA
        # ----------------------------------------------------

        job_url = str(
            job.get(
                "job_url",
                "",
            )
            or ""
        ).strip()


        job_title = str(
            job.get(
                "job_title_display",
                job.get(
                    "job_title",
                    "Job opportunity",
                ),
            )
            or "Job opportunity"
        ).strip()


        company_name = str(
            job.get(
                "company_display",
                job.get(
                    "company",
                    "",
                ),
            )
            or ""
        ).strip()


        job_location = str(
            job.get(
                "location_display",
                job.get(
                    "location",
                    "",
                ),
            )
            or ""
        ).strip()


        # ----------------------------------------------------
        # JOB IDENTIFIER
        # ----------------------------------------------------

        # HJMI currently uses the source job URL as the stable
        # identifier because the central dataset does not
        # expose a separate job_id column.

        job_identifier = job_url


        # ----------------------------------------------------
        # NOT AUTHENTICATED
        # ----------------------------------------------------

        if not authenticated:

            st.caption(
                "🔐 Sign in to My HJMI to save and "
                "track this opportunity."
            )

            st.markdown("---")

            continue


        # ----------------------------------------------------
        # INVALID IDENTIFIER
        # ----------------------------------------------------

        if not job_identifier:

            st.caption(
                "Saving and application tracking are unavailable "
                "for this opportunity because no source URL "
                "is available."
            )

            st.markdown("---")

            continue


        # ----------------------------------------------------
        # ACTION LAYOUT
        # ----------------------------------------------------

        save_column, application_column = st.columns(
            2
        )


        # ====================================================
        # SAVE JOB
        # ====================================================

        with save_column:

            if job_identifier in saved_job_ids:

                saved_col_1, saved_col_2 = st.columns(
                    [3, 1]
                )

                with saved_col_1:

                    st.success(
                        "✓ Saved to My HJMI"
                    )

                with saved_col_2:

                    if st.button(
                        "Remove",
                        key=(
                            f"remove_job_"
                            f"{row_index}"
                        ),
                        use_container_width=True,
                    ):

                        result = remove_saved_job(
                            job_identifier
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

            else:

                if st.button(
                    "♡ Save Job",
                    key=(
                        f"save_job_"
                        f"{row_index}"
                    ),
                    use_container_width=True,
                ):

                    result = save_job(
                        job_id=job_identifier,
                        job_title=job_title,
                        company=company_name,
                        location=job_location,
                        job_url=job_url,
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


        # ====================================================
        # APPLICATION TRACKER
        # ====================================================

        with application_column:

            if job_identifier in tracked_job_ids:

                st.success(
                    "✓ Application Tracked"
                )

            else:

                if st.button(
                    "Track Application",
                    key=(
                        f"track_application_"
                        f"{row_index}"
                    ),
                    use_container_width=True,
                    type="primary",
                ):

                    result = add_application(
                        job_id=job_identifier,
                        job_title=job_title,
                        company=company_name,
                        location=job_location,
                        job_url=job_url,
                        status="Applied",
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


        st.markdown("---")


    # --------------------------------------------------------
    # DISPLAY NOTE
    # --------------------------------------------------------

    if display_limit < max_available:

        st.caption(
            f"Displaying {display_limit:,} of "
            f"{max_available:,} matching opportunities."
        )


# ============================================================
# SALARY TRANSPARENCY
# ============================================================

info_box(
    "Salary information",
    (
        "HJMI shows salary information when it is available "
        "in the source listing. When salary information is not "
        "provided, HJMI displays 'To be discussed after the "
        "interview' instead of inventing or estimating a salary."
    ),
    "💰",
)


# ============================================================
# GRADUATE TRANSPARENCY
# ============================================================

info_box(
    "Fresh Graduate Friendly",
    (
        "This filter uses signals available in the listing text, "
        "such as fresh graduate, entry level, no experience "
        "required or an experience requirement beginning at zero. "
        "A job is not automatically marked graduate-friendly just "
        "because its experience requirement is missing."
    ),
    "🎓",
)


# ============================================================
# APPLICATION TRACKING NOTE
# ============================================================

info_box(
    "Applying and tracking opportunities",
    (
        "The View Opportunity button opens the external source "
        "listing. Signed-in users can save opportunities for later "
        "or add jobs they have applied for to the HJMI Application "
        "Tracker. Tracking a job does not submit an application "
        "to the employer."
    ),
    "↗",
)


# ============================================================
# FOOTER
# ============================================================

footer()
