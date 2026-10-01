# ============================================================
# HJMI — CAREER PROFILE SERVICE
# Career Profile • Skills • Preferences • CV Information
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
# NORMALIZE LIST
# ============================================================

def normalize_list(values):

    if values is None:
        return []

    if isinstance(values, str):

        values = values.split(",")

    cleaned = []

    seen = set()

    for value in values:

        value = str(
            value or ""
        ).strip()

        if not value:
            continue

        normalized = value.lower()

        if normalized in seen:
            continue

        seen.add(normalized)

        cleaned.append(value)

    return cleaned


# ============================================================
# GET CAREER PROFILE
# ============================================================

def get_career_profile():

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
            supabase
            .table("career_profiles")
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


# ============================================================
# SAVE / UPDATE CAREER PROFILE
# ============================================================

def save_career_profile(
    specialization="",
    target_roles=None,
    skills=None,
    experience_level="",
    preferred_locations=None,
):

    if not is_authenticated():

        return {
            "success": False,
            "message": (
                "Please sign in to create your Career Profile."
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

    specialization = str(
        specialization or ""
    ).strip()

    experience_level = str(
        experience_level or ""
    ).strip()

    target_roles = normalize_list(
        target_roles
    )

    skills = normalize_list(
        skills
    )

    preferred_locations = normalize_list(
        preferred_locations
    )

    profile_data = {
        "user_id": user.id,
        "specialization": specialization,
        "target_roles": target_roles,
        "skills": skills,
        "experience_level": experience_level,
        "preferred_locations": preferred_locations,
    }

    try:

        existing = (
            supabase
            .table("career_profiles")
            .select("id")
            .eq("user_id", user.id)
            .limit(1)
            .execute()
        )

        if existing.data:

            (
                supabase
                .table("career_profiles")
                .update(profile_data)
                .eq("user_id", user.id)
                .execute()
            )

            return {
                "success": True,
                "message": (
                    "Career Profile updated successfully."
                ),
            }

        (
            supabase
            .table("career_profiles")
            .insert(profile_data)
            .execute()
        )

        return {
            "success": True,
            "message": (
                "Career Profile created successfully."
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                f"Career Profile error: {str(error)}"
            ),
        }


# ============================================================
# SAVE CV INFORMATION
# ============================================================

def save_cv_information(
    file_path="",
    file_name="",
):

    if not is_authenticated():

        return {
            "success": False,
            "message": "Please sign in first.",
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

        existing = (
            supabase
            .table("career_profiles")
            .select("id")
            .eq("user_id", user.id)
            .limit(1)
            .execute()
        )

        cv_data = {
            "cv_file_path": str(
                file_path or ""
            ),
            "cv_file_name": str(
                file_name or ""
            ),
        }

        if existing.data:

            (
                supabase
                .table("career_profiles")
                .update(cv_data)
                .eq("user_id", user.id)
                .execute()
            )

        else:

            cv_data["user_id"] = user.id

            (
                supabase
                .table("career_profiles")
                .insert(cv_data)
                .execute()
            )

        return {
            "success": True,
            "message": (
                "CV information saved successfully."
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                f"CV information error: {str(error)}"
            ),
        }


# ============================================================
# DELETE CAREER PROFILE
# ============================================================

def delete_career_profile():

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
            supabase
            .table("career_profiles")
            .delete()
            .eq("user_id", user.id)
            .execute()
        )

        return True

    except Exception:

        return False


# ============================================================
# PROFILE COMPLETION
# ============================================================

def get_profile_completion(profile=None):

    if profile is None:

        profile = get_career_profile()

    if not profile:
        return 0

    fields = [
        bool(
            str(
                profile.get(
                    "specialization",
                    "",
                )
                or ""
            ).strip()
        ),
        bool(
            profile.get(
                "target_roles",
                []
            )
        ),
        bool(
            profile.get(
                "skills",
                []
            )
        ),
        bool(
            str(
                profile.get(
                    "experience_level",
                    "",
                )
                or ""
            ).strip()
        ),
        bool(
            profile.get(
                "preferred_locations",
                []
            )
        ),
    ]

    completed = sum(fields)

    return round(
        (completed / len(fields)) * 100
    )


# ============================================================
# PROFILE READY FOR MATCHING
# ============================================================

def profile_ready_for_matching(
    profile=None,
):

    if profile is None:

        profile = get_career_profile()

    if not profile:
        return False

    skills = profile.get(
        "skills",
        []
    ) or []

    specialization = str(
        profile.get(
            "specialization",
            "",
        )
        or ""
    ).strip()

    target_roles = profile.get(
        "target_roles",
        []
    ) or []

    return bool(
        skills
        or specialization
        or target_roles
    )
