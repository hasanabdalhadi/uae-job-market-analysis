# ============================================================
# HJMI — SAVED JOBS SERVICE
# Supabase Saved Jobs Management
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

    supabase = get_supabase_client()

    try:
        supabase.auth.set_session(
            access_token,
            refresh_token,
        )

        return supabase

    except Exception:
        return None


# ============================================================
# SAVE JOB
# ============================================================

def save_job(
    job_id,
    job_title="",
    company="",
    location="",
    job_url="",
):
    """
    Save a job to the current user's HJMI account.
    """

    user = get_current_user()
    supabase = get_authenticated_client()

    if user is None or supabase is None:
        return {
            "success": False,
            "message": "Please sign in to save jobs.",
        }

    try:
        supabase.table(
            "saved_jobs"
        ).insert(
            {
                "user_id": str(user.id),
                "job_id": str(job_id),
                "job_title": str(job_title or ""),
                "company": str(company or ""),
                "location": str(location or ""),
                "job_url": str(job_url or ""),
            }
        ).execute()

        return {
            "success": True,
            "message": "Job saved to My HJMI.",
        }

    except Exception as error:

        error_text = str(error).lower()

        if (
            "duplicate" in error_text
            or "unique" in error_text
            or "23505" in error_text
        ):
            return {
                "success": True,
                "message": "This job is already saved.",
            }

        return {
            "success": False,
            "message": "HJMI could not save this job.",
        }


# ============================================================
# GET SAVED JOBS
# ============================================================

def get_saved_jobs():
    """
    Return saved jobs belonging to the current user.
    """

    user = get_current_user()
    supabase = get_authenticated_client()

    if user is None or supabase is None:
        return []

    try:
        response = (
            supabase.table("saved_jobs")
            .select("*")
            .eq("user_id", str(user.id))
            .order("saved_at", desc=True)
            .execute()
        )

        return response.data or []

    except Exception:
        return []


# ============================================================
# CHECK IF JOB IS SAVED
# ============================================================

def is_job_saved(job_id):
    """
    Check whether a job is already saved by
    the current authenticated user.
    """

    user = get_current_user()
    supabase = get_authenticated_client()

    if user is None or supabase is None:
        return False

    try:
        response = (
            supabase.table("saved_jobs")
            .select("id")
            .eq("user_id", str(user.id))
            .eq("job_id", str(job_id))
            .limit(1)
            .execute()
        )

        return bool(response.data)

    except Exception:
        return False


# ============================================================
# REMOVE SAVED JOB
# ============================================================

def remove_saved_job(job_id):
    """
    Remove a saved job from the current user's account.
    """

    user = get_current_user()
    supabase = get_authenticated_client()

    if user is None or supabase is None:
        return {
            "success": False,
            "message": "Please sign in first.",
        }

    try:
        (
            supabase.table("saved_jobs")
            .delete()
            .eq("user_id", str(user.id))
            .eq("job_id", str(job_id))
            .execute()
        )

        return {
            "success": True,
            "message": "Job removed from Saved Jobs.",
        }

    except Exception:
        return {
            "success": False,
            "message": "HJMI could not remove this job.",
        }


# ============================================================
# SAVED JOB COUNT
# ============================================================

def get_saved_jobs_count():
    """
    Return the number of jobs saved by the current user.
    """

    return len(
        get_saved_jobs()
    )
