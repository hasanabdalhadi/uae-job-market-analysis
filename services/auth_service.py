# ============================================================
# HJMI — AUTHENTICATION SERVICE
# Supabase Authentication
# ============================================================

import streamlit as st
from supabase import create_client, Client


# ============================================================
# SUPABASE CLIENT
# ============================================================

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Create and cache the Supabase client using
    credentials stored securely in Streamlit Secrets.
    """

    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]

        return create_client(
            supabase_url,
            supabase_key,
        )

    except Exception as error:
        raise RuntimeError(
            "Supabase configuration is missing or invalid."
        ) from error


# ============================================================
# CREATE ACCOUNT
# ============================================================

def sign_up(
    email: str,
    password: str,
    full_name: str = "",
):
    """
    Register a new HJMI user with Supabase Authentication.
    """

    supabase = get_supabase_client()

    email = email.strip().lower()
    full_name = full_name.strip()

    if not email:
        return {
            "success": False,
            "message": "Please enter your email address.",
        }

    if len(password) < 8:
        return {
            "success": False,
            "message": (
                "Password must contain at least 8 characters."
            ),
        }

    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name,
                        "account_type": "job_seeker",
                    }
                },
            }
        )

        if response.user is None:
            return {
                "success": False,
                "message": (
                    "HJMI could not create the account."
                ),
            }

        return {
            "success": True,
            "message": (
                "Account created. Please check your email "
                "and confirm your account before signing in."
            ),
            "user": response.user,
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error),
        }


# ============================================================
# SIGN IN
# ============================================================

def sign_in(
    email: str,
    password: str,
):
    """
    Sign an existing HJMI user in.
    """

    supabase = get_supabase_client()

    email = email.strip().lower()

    if not email or not password:
        return {
            "success": False,
            "message": (
                "Please enter your email and password."
            ),
        }

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        if response.user is None or response.session is None:
            return {
                "success": False,
                "message": (
                    "HJMI could not sign you in."
                ),
            }

        st.session_state["hjmi_authenticated"] = True
        st.session_state["hjmi_user"] = response.user
        st.session_state["hjmi_access_token"] = (
            response.session.access_token
        )
        st.session_state["hjmi_refresh_token"] = (
            response.session.refresh_token
        )

        return {
            "success": True,
            "message": "Signed in successfully.",
            "user": response.user,
        }

    except Exception:
        return {
            "success": False,
            "message": (
                "Invalid email or password, or the account "
                "has not been confirmed yet."
            ),
        }


# ============================================================
# SIGN OUT
# ============================================================

def sign_out():
    """
    Sign the current HJMI user out and clear
    authentication data from the Streamlit session.
    """

    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()

    except Exception:
        pass

    for key in [
        "hjmi_authenticated",
        "hjmi_user",
        "hjmi_access_token",
        "hjmi_refresh_token",
    ]:
        st.session_state.pop(key, None)

    return {
        "success": True,
        "message": "Signed out successfully.",
    }


# ============================================================
# AUTHENTICATION STATE
# ============================================================

def is_authenticated() -> bool:
    """
    Return True when the current Streamlit session
    contains an authenticated HJMI user.
    """

    return bool(
        st.session_state.get(
            "hjmi_authenticated",
            False,
        )
        and st.session_state.get(
            "hjmi_user"
        ) is not None
    )


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user():
    """
    Return the currently authenticated HJMI user.
    """

    if not is_authenticated():
        return None

    return st.session_state.get(
        "hjmi_user"
    )


# ============================================================
# USER DISPLAY NAME
# ============================================================

def get_user_display_name() -> str:
    """
    Return the user's name when available,
    otherwise return the account email.
    """

    user = get_current_user()

    if user is None:
        return "HJMI User"

    metadata = getattr(
        user,
        "user_metadata",
        {},
    ) or {}

    full_name = metadata.get(
        "full_name",
        "",
    )

    if full_name:
        return full_name

    email = getattr(
        user,
        "email",
        None,
    )

    return email or "HJMI User"
