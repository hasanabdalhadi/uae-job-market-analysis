# ============================================================
# HJMI — APPLICATION SERVICE
# Application Tracking
# ============================================================

import streamlit as st

from services.auth_service import (
    get_supabase_client,
    get_current_user,
    is_authenticated,
)


# ============================================================
# AUTHENTICATED SUPABASE CLIENT
# ============================================================

def get_authenticated_client():
    """
    Return a Supabase client authenticated with the
    current HJMI user's session.
    """

    if not is_authenticated():
        return None

    access_token = st.session_state.get(
        "hjmi_access_token"
    )

    refresh_token = st.session_state.get(
        "hjmi_refresh_token"
    )

    if not access_token or not refresh_token:
        return None

    try:

        supabase = get_supabase_client()

        supabase.auth.set_session(
            access_token,
            refresh_token,
        )

        return supabase

    except Exception:

        return None


# ============================================================
# CREATE / TRACK APPLICATION
# ============================================================

def add_application(
    job_id,
    job_title="",
    company="",
    location="",
    job_url="",
    status="Applied",
):
    """
    Add a job to the current user's Application Tracker.
    """

    if not is_authenticated():

        return {
            "success": False,
            "message": (
                "Please sign in to track applications."
            ),
        }

    user = get_current_user()

    if user is None:

        return {
            "success": False,
            "message": (
                "HJMI could not identify the current user."
            ),
        }

    job_id = str(job_id or "").strip()

    if not job_id:

        return {
            "success": False,
            "message": (
                "This opportunity does not have "
                "a valid job identifier."
            ),
        }

    supabase = get_authenticated_client()

    if supabase is None:

        return {
            "success": False,
            "message": (
                "HJMI could not connect to your account."
            ),
        }

    try:

        existing = (
            supabase.table(
                "job_applications"
            )
            .select("id")
            .eq(
                "user_id",
                user.id,
            )
            .eq(
                "job_id",
                job_id,
            )
            .execute()
        )

        if existing.data:

            return {
                "success": True,
                "message": (
                    "This job is already in "
                    "your Application Tracker."
                ),
            }

        (
            supabase.table(
                "job_applications"
            )
            .insert(
                {
                    "user_id": user.id,
                    "job_id": job_id,
                    "job_title": str(
                        job_title or ""
                    ),
                    "company": str(
                        company or ""
                    ),
                    "location": str(
                        location or ""
                    ),
                    "job_url": str(
                        job_url or ""
                    ),
                    "status": status,
                }
            )
            .execute()
        )

        return {
            "success": True,
            "message": (
                "Application added to My HJMI."
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                f"Application error: {str(error)}"
            ),
        }


# ============================================================
# GET APPLICATIONS
# ============================================================

def get_applications():
    """
    Return all applications belonging to the
    currently authenticated user.
    """

    if not is_authenticated():
        return []

    user = get_current_user()

    if user is None:
        return []

    supabase = get_authenticated_client()

    if supabase is None:
        return []

    try:

        response = (
            supabase.table(
                "job_applications"
            )
            .select("*")
            .eq(
                "user_id",
                user.id,
            )
            .order(
                "updated_at",
                desc=True,
            )
            .execute()
        )

        return response.data or []

    except Exception:

        return []


# ============================================================
# APPLICATION COUNT
# ============================================================

def get_applications_count():
    """
    Return the number of applications tracked by
    the current user.
    """

    return len(
        get_applications()
    )


# ============================================================
# APPLICATION STATUS
# ============================================================

def get_application_status(
    job_id,
):
    """
    Return the current tracking status for a job.
    """

    job_id = str(
        job_id or ""
    ).strip()

    if not job_id:
        return None

    applications = get_applications()

    for application in applications:

        if str(
            application.get(
                "job_id",
                "",
            )
        ) == job_id:

            return application.get(
                "status",
                "Applied",
            )

    return None


# ============================================================
# CHECK IF JOB IS TRACKED
# ============================================================

def is_application_tracked(
    job_id,
):
    """
    Check whether a job already exists in the
    user's Application Tracker.
    """

    return (
        get_application_status(
            job_id
        )
        is not None
    )


# ============================================================
# UPDATE APPLICATION STATUS
# ============================================================

def update_application_status(
    application_id,
    status,
):
    """
    Update an application's current status.
    """

    allowed_statuses = [
        "Applied",
        "Interview",
        "Offer",
        "Rejected",
        "Withdrawn",
    ]

    if status not in allowed_statuses:

        return {
            "success": False,
            "message": (
                "Invalid application status."
            ),
        }

    if not is_authenticated():

        return {
            "success": False,
            "message": (
                "Please sign in first."
            ),
        }

    user = get_current_user()

    if user is None:

        return {
            "success": False,
            "message": (
                "HJMI could not identify the current user."
            ),
        }

    supabase = get_authenticated_client()

    if supabase is None:

        return {
            "success": False,
            "message": (
                "HJMI could not connect to your account."
            ),
        }

    try:

        (
            supabase.table(
                "job_applications"
            )
            .update(
                {
                    "status": status,
                }
            )
            .eq(
                "id",
                application_id,
            )
            .eq(
                "user_id",
                user.id,
            )
            .execute()
        )

        return {
            "success": True,
            "message": (
                "Application status updated."
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                f"Application update error: {str(error)}"
            ),
        }


# ============================================================
# UPDATE APPLICATION NOTES
# ============================================================

def update_application_notes(
    application_id,
    notes,
):
    """
    Save personal notes for an application.
    """

    if not is_authenticated():

        return {
            "success": False,
            "message": (
                "Please sign in first."
            ),
        }

    user = get_current_user()

    if user is None:

        return {
            "success": False,
            "message": (
                "HJMI could not identify the current user."
            ),
        }

    supabase = get_authenticated_client()

    if supabase is None:

        return {
            "success": False,
            "message": (
                "HJMI could not connect to your account."
            ),
        }

    try:

        (
            supabase.table(
                "job_applications"
            )
            .update(
                {
                    "notes": str(
                        notes or ""
                    ),
                }
            )
            .eq(
                "id",
                application_id,
            )
            .eq(
                "user_id",
                user.id,
            )
            .execute()
        )

        return {
            "success": True,
            "message": (
                "Application notes saved."
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                f"Notes update error: {str(error)}"
            ),
        }


# ============================================================
# REMOVE APPLICATION
# ============================================================

def remove_application(
    application_id,
):
    """
    Remove an application from the user's tracker.
    """

    if not is_authenticated():
        return False

    user = get_current_user()

    if user is None:
        return False

    supabase = get_authenticated_client()

    if supabase is None:
        return False

    try:

        (
            supabase.table(
                "job_applications"
            )
            .delete()
            .eq(
                "id",
                application_id,
            )
            .eq(
                "user_id",
                user.id,
            )
            .execute()
        )

        return True

    except Exception:

        return False
