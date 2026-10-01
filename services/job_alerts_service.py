# ============================================================
# HJMI — JOB ALERTS SERVICE
# Personalized In-App Job Alerts
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
# NORMALIZATION
# ============================================================

def normalize_list(values):
    """
    Convert list-like alert values into clean strings.
    """

    if not values:
        return []

    if not isinstance(values, (list, tuple, set)):
        values = [values]

    cleaned = []

    for value in values:
        value = str(value or "").strip()

        if value and value not in cleaned:
            cleaned.append(value)

    return cleaned


# ============================================================
# CREATE ALERT
# ============================================================

def create_job_alert(
    job_id,
    job_title="",
    company="",
    location="",
    job_url="",
    match_score=0,
    match_label="",
    matched_skills=None,
    match_reasons=None,
):
    """
    Create one in-app alert for the current user.

    The unique (user_id, job_id) database constraint prevents
    the same job from creating duplicate alerts.
    """

    if not is_authenticated():
        return {
            "success": False,
            "created": False,
            "message": "Please sign in to use job alerts.",
        }

    user = get_current_user()

    if user is None:
        return {
            "success": False,
            "created": False,
            "message": "HJMI could not identify the current user.",
        }

    job_id = str(job_id or "").strip()

    if not job_id:
        return {
            "success": False,
            "created": False,
            "message": "This opportunity does not have a valid job identifier.",
        }

    supabase = get_authenticated_client()

    if supabase is None:
        return {
            "success": False,
            "created": False,
            "message": "HJMI could not connect to your account.",
        }

    try:
        existing = (
            supabase.table("job_alerts")
            .select("id")
            .eq("user_id", user.id)
            .eq("job_id", job_id)
            .execute()
        )

        if existing.data:
            return {
                "success": True,
                "created": False,
                "message": "Alert already exists for this opportunity.",
            }

        try:
            score = int(round(float(match_score or 0)))
        except (TypeError, ValueError):
            score = 0

        score = max(0, min(100, score))

        (
            supabase.table("job_alerts")
            .insert(
                {
                    "user_id": user.id,
                    "job_id": job_id,
                    "job_title": str(job_title or ""),
                    "company": str(company or ""),
                    "location": str(location or ""),
                    "job_url": str(job_url or ""),
                    "match_score": score,
                    "match_label": str(match_label or ""),
                    "matched_skills": normalize_list(matched_skills),
                    "match_reasons": normalize_list(match_reasons),
                    "is_read": False,
                }
            )
            .execute()
        )

        return {
            "success": True,
            "created": True,
            "message": "New HJMI job alert created.",
        }

    except Exception as error:
        return {
            "success": False,
            "created": False,
            "message": f"Job alert error: {str(error)}",
        }


# ============================================================
# GET ALERTS
# ============================================================

def get_job_alerts(
    unread_only=False,
    limit=None,
):
    """
    Return alerts belonging to the current authenticated user.
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
        query = (
            supabase.table("job_alerts")
            .select("*")
            .eq("user_id", user.id)
        )

        if unread_only:
            query = query.eq("is_read", False)

        query = query.order(
            "created_at",
            desc=True,
        )

        if limit is not None:
            try:
                safe_limit = max(1, int(limit))
                query = query.limit(safe_limit)
            except (TypeError, ValueError):
                pass

        response = query.execute()

        return response.data or []

    except Exception:
        return []


# ============================================================
# COUNTS
# ============================================================

def get_job_alerts_count():
    """
    Return total alerts for the current user.
    """

    return len(
        get_job_alerts()
    )


def get_unread_job_alerts_count():
    """
    Return unread alert count for the current user.
    """

    return len(
        get_job_alerts(
            unread_only=True
        )
    )


# ============================================================
# CHECK ALERT
# ============================================================

def job_alert_exists(
    job_id,
):
    """
    Check whether the current user already has an alert
    for the supplied job identifier.
    """

    job_id = str(job_id or "").strip()

    if not job_id:
        return False

    alerts = get_job_alerts()

    for alert in alerts:
        if str(
            alert.get(
                "job_id",
                "",
            )
        ) == job_id:
            return True

    return False


# ============================================================
# MARK ONE ALERT READ
# ============================================================

def mark_job_alert_read(
    alert_id,
):
    """
    Mark one alert as read.
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
            supabase.table("job_alerts")
            .update(
                {
                    "is_read": True,
                }
            )
            .eq("id", alert_id)
            .eq("user_id", user.id)
            .execute()
        )

        return True

    except Exception:
        return False


# ============================================================
# MARK ALL ALERTS READ
# ============================================================

def mark_all_job_alerts_read():
    """
    Mark all unread alerts belonging to the current user as read.
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
            supabase.table("job_alerts")
            .update(
                {
                    "is_read": True,
                }
            )
            .eq("user_id", user.id)
            .eq("is_read", False)
            .execute()
        )

        return True

    except Exception:
        return False


# ============================================================
# REMOVE ALERT
# ============================================================

def remove_job_alert(
    alert_id,
):
    """
    Remove one alert belonging to the current user.
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
            supabase.table("job_alerts")
            .delete()
            .eq("id", alert_id)
            .eq("user_id", user.id)
            .execute()
        )

        return True

    except Exception:
        return False


# ============================================================
# CLEAR ALL ALERTS
# ============================================================

def clear_job_alerts():
    """
    Remove all alerts belonging to the current user.
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
            supabase.table("job_alerts")
            .delete()
            .eq("user_id", user.id)
            .execute()
        )

        return True

    except Exception:
        return False
