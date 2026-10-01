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


# ============================================================
# ALERT PREFERENCES
# ============================================================

def get_alert_preferences():
    """
    Return the current user's Smart Job Alert preferences.
    """

    if not is_authenticated():
        return None

    user = get_current_user()

    if user is None:
        return None

    supabase = get_authenticated_client()

    if supabase is None:
        return None

    try:
        response = (
            supabase.table("job_alert_preferences")
            .select("*")
            .eq("user_id", user.id)
            .limit(1)
            .execute()
        )

        if response.data:
            return response.data[0]

        return None

    except Exception:
        return None


def initialize_alert_preferences():
    """
    Create the user's alert baseline.

    On first initialization, last_checked_at is set by the database
    to the current time. This prevents existing recommendations from
    being treated as brand-new alerts.
    """

    if not is_authenticated():
        return {
            "success": False,
            "created": False,
            "message": "Please sign in to use Smart Job Alerts.",
        }

    user = get_current_user()

    if user is None:
        return {
            "success": False,
            "created": False,
            "message": "HJMI could not identify the current user.",
        }

    existing = get_alert_preferences()

    if existing:
        return {
            "success": True,
            "created": False,
            "preferences": existing,
            "message": "Smart Job Alerts are already initialized.",
        }

    supabase = get_authenticated_client()

    if supabase is None:
        return {
            "success": False,
            "created": False,
            "message": "HJMI could not connect to your account.",
        }

    try:
        response = (
            supabase.table("job_alert_preferences")
            .insert(
                {
                    "user_id": user.id,
                    "alerts_enabled": True,
                }
            )
            .execute()
        )

        preferences = (
            response.data[0]
            if response.data
            else get_alert_preferences()
        )

        return {
            "success": True,
            "created": True,
            "preferences": preferences,
            "message": "Smart Job Alerts initialized.",
        }

    except Exception as error:
        return {
            "success": False,
            "created": False,
            "message": f"Alert initialization error: {str(error)}",
        }


def set_alerts_enabled(enabled):
    """
    Enable or disable Smart Job Alerts for the current user.
    """

    if not is_authenticated():
        return False

    user = get_current_user()

    if user is None:
        return False

    preferences = get_alert_preferences()

    if preferences is None:
        result = initialize_alert_preferences()

        if not result.get("success"):
            return False

    supabase = get_authenticated_client()

    if supabase is None:
        return False

    try:
        (
            supabase.table("job_alert_preferences")
            .update(
                {
                    "alerts_enabled": bool(enabled),
                }
            )
            .eq("user_id", user.id)
            .execute()
        )

        return True

    except Exception:
        return False


def update_last_checked_at(timestamp_value=None):
    """
    Advance the alert baseline after a successful Smart Alert check.
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
        payload = {}

        if timestamp_value is not None:
            payload["last_checked_at"] = str(timestamp_value)

        else:
            # Generate an explicit UTC timestamp client-side.
            from datetime import datetime, timezone

            payload["last_checked_at"] = (
                datetime.now(timezone.utc).isoformat()
            )

        (
            supabase.table("job_alert_preferences")
            .update(payload)
            .eq("user_id", user.id)
            .execute()
        )

        return True

    except Exception:
        return False


# ============================================================
# SMART ALERT SYNC
# ============================================================

def sync_smart_job_alerts(recommendations):
    """
    Create in-app alerts only for newly discovered HJMI jobs that
    match the user's Career Profile.

    `first_seen` is the HJMI discovery timestamp/date. It is not
    necessarily the employer's original posting time.

    The first sync creates a baseline and intentionally generates
    no alerts for recommendations that already existed.
    """

    result = {
        "success": False,
        "initialized": False,
        "checked": 0,
        "created": 0,
        "message": "",
    }

    if not is_authenticated():
        result["message"] = "Please sign in to use Smart Job Alerts."
        return result

    preferences = get_alert_preferences()

    # First run: create baseline only. Do not flood the user with
    # all recommendations that existed before alerts were enabled.
    if preferences is None:
        init_result = initialize_alert_preferences()

        if not init_result.get("success"):
            result["message"] = init_result.get(
                "message",
                "HJMI could not initialize Smart Job Alerts.",
            )
            return result

        result["success"] = True
        result["initialized"] = True
        result["message"] = (
            "Smart Job Alerts initialized. Future new matching "
            "opportunities can now generate alerts."
        )
        return result

    if not preferences.get("alerts_enabled", True):
        result["success"] = True
        result["message"] = "Smart Job Alerts are disabled."
        return result

    last_checked_at = preferences.get("last_checked_at")

    if not last_checked_at:
        if update_last_checked_at():
            result["success"] = True
            result["initialized"] = True
            result["message"] = "Smart Job Alerts baseline created."
        else:
            result["message"] = "HJMI could not create the alert baseline."

        return result

    if recommendations is None:
        result["message"] = "No recommendation data was available to check."
        return result

    try:
        import pandas as pd

        if not isinstance(recommendations, pd.DataFrame):
            recommendations = pd.DataFrame(recommendations)

        if recommendations.empty:
            # The check itself succeeded even though there are no matches.
            update_last_checked_at()
            result["success"] = True
            result["message"] = "No matching opportunities were available."
            return result

        if "first_seen" not in recommendations.columns:
            result["message"] = (
                "HJMI could not determine which opportunities are new."
            )
            return result

        baseline = pd.to_datetime(
            last_checked_at,
            utc=True,
            errors="coerce",
        )

        if pd.isna(baseline):
            if update_last_checked_at():
                result["success"] = True
                result["initialized"] = True
                result["message"] = "Smart Job Alerts baseline refreshed."
            else:
                result["message"] = (
                    "HJMI could not refresh the alert baseline."
                )

            return result

        working = recommendations.copy()

        working["_alert_first_seen"] = pd.to_datetime(
            working["first_seen"],
            utc=True,
            errors="coerce",
        )

        new_matches = working[
            working["_alert_first_seen"].notna()
            & (working["_alert_first_seen"] > baseline)
        ].copy()

        result["checked"] = int(len(new_matches))

        for _, job in new_matches.iterrows():
            job_title = (
                job.get("job_title_display", "")
                or job.get("job_title", "")
                or "Untitled Opportunity"
            )

            company = (
                job.get("company_display", "")
                or job.get("company", "")
                or "Company not specified"
            )

            location = (
                job.get("location_display", "")
                or job.get("location", "")
                or "Location not specified"
            )

            job_url = str(
                job.get("job_url", "")
                or ""
            ).strip()

            job_identifier = (
                job_url
                or (
                    f"{job_title}|"
                    f"{company}|"
                    f"{location}"
                )
            )

            alert_result = create_job_alert(
                job_id=job_identifier,
                job_title=job_title,
                company=company,
                location=location,
                job_url=job_url,
                match_score=job.get(
                    "hjmi_match_score",
                    0,
                ),
                match_label=job.get(
                    "hjmi_match_label",
                    "",
                ),
                matched_skills=job.get(
                    "hjmi_matched_skills",
                    [],
                ),
                match_reasons=job.get(
                    "hjmi_match_reasons",
                    [],
                ),
            )

            if (
                alert_result.get("success")
                and alert_result.get("created")
            ):
                result["created"] += 1

        # Advance the baseline only after the recommendation set has
        # been processed, preventing repeated alerts on later reruns.
        if not update_last_checked_at():
            result["message"] = (
                "Alerts were checked, but HJMI could not update "
                "the last-check time."
            )
            return result

        result["success"] = True

        if result["created"] > 0:
            result["message"] = (
                f"{result['created']} new matching "
                f"opportunit{'y' if result['created'] == 1 else 'ies'} "
                "added to Smart Job Alerts."
            )
        else:
            result["message"] = "No new matching opportunities since the last check."

        return result

    except Exception as error:
        result["message"] = f"Smart Alert sync error: {str(error)}"
        return result
