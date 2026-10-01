# ============================================================
# HJMI — AUTHENTICATION SERVICE
# Supabase Authentication + Persistent Login
# ============================================================

from datetime import datetime, timedelta

import streamlit as st
import extra_streamlit_components as stx
from supabase import create_client, Client


# ============================================================
# COOKIE CONFIGURATION
# ============================================================

AUTH_COOKIE_NAME = "hjmi_refresh_token"
COOKIE_EXPIRY_DAYS = 30


# ============================================================
# COOKIE MANAGER
# ============================================================

# Create one CookieManager component only.
# Creating it repeatedly with the same key causes Streamlit's
# duplicate-element-key error.

_COOKIE_MANAGER = stx.CookieManager(
    key="hjmi_auth_cookie_manager"
)


def get_cookie_manager():
    """
    Return the single HJMI CookieManager instance.
    """

    return _COOKIE_MANAGER


# ============================================================
# SUPABASE CLIENT
# ============================================================

def get_supabase_client() -> Client:
    """
    Create a fresh Supabase client.

    Authentication clients are intentionally not cached
    globally because Supabase auth state is mutable and
    must not be shared between Streamlit users.
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
# SESSION HELPERS
# ============================================================

def store_session(
    user,
    session,
):
    """
    Store the authenticated Supabase session inside the
    current Streamlit session.
    """

    if user is None or session is None:
        return False

    st.session_state[
        "hjmi_authenticated"
    ] = True

    st.session_state[
        "hjmi_user"
    ] = user

    st.session_state[
        "hjmi_access_token"
    ] = session.access_token

    st.session_state[
        "hjmi_refresh_token"
    ] = session.refresh_token

    return True


def clear_session():
    """
    Remove HJMI authentication information from the
    current Streamlit session.
    """

    for key in [
        "hjmi_authenticated",
        "hjmi_user",
        "hjmi_access_token",
        "hjmi_refresh_token",
    ]:

        st.session_state.pop(
            key,
            None,
        )


# ============================================================
# PERSISTENT LOGIN COOKIE
# ============================================================

def save_auth_cookie(
    refresh_token: str,
):
    """
    Save the Supabase refresh token in the browser cookie.
    """

    if not refresh_token:
        return False

    try:

        cookie_manager = get_cookie_manager()

        cookie_manager.set(
            AUTH_COOKIE_NAME,
            refresh_token,
            expires_at=(
                datetime.now()
                + timedelta(
                    days=COOKIE_EXPIRY_DAYS
                )
            ),
        )

        return True

    except Exception as error:

        # Temporary diagnostic message.
        # Remove after persistent login is verified.
        st.error(
            f"HJMI cookie error: {error}"
        )

        return False


def get_auth_cookie():
    """
    Return the stored HJMI refresh token when available.
    """

    try:

        cookie_manager = get_cookie_manager()

        return cookie_manager.get(
            AUTH_COOKIE_NAME
        )

    except Exception:

        return None


def delete_auth_cookie():
    """
    Remove the persistent HJMI authentication cookie.
    """

    try:

        cookie_manager = get_cookie_manager()

        cookie_manager.delete(
            AUTH_COOKIE_NAME
        )

        return True

    except Exception as error:

        # Temporary diagnostic message.
        st.error(
            f"HJMI cookie delete error: {error}"
        )

        return False


# ============================================================
# RESTORE AUTHENTICATION
# ============================================================

def restore_session():
    """
    Restore the user's Supabase authentication session
    from the persistent refresh-token cookie.
    """

    # If the current Streamlit session is already
    # authenticated, no restoration is required.

    if (
        st.session_state.get(
            "hjmi_authenticated",
            False,
        )
        and st.session_state.get(
            "hjmi_user"
        ) is not None
        and st.session_state.get(
            "hjmi_access_token"
        )
        and st.session_state.get(
            "hjmi_refresh_token"
        )
    ):

        return True

    refresh_token = get_auth_cookie()

    if not refresh_token:
        return False

    try:

        supabase = get_supabase_client()

        response = (
            supabase.auth.refresh_session(
                refresh_token
            )
        )

        if (
            response.user is None
            or response.session is None
        ):

            clear_session()
            return False

        store_session(
            response.user,
            response.session,
        )

        # Supabase may rotate the refresh token.
        # Save the newest refresh token.

        save_auth_cookie(
            response.session.refresh_token
        )

        return True

    except Exception:

        clear_session()
        return False


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
            "message": (
                "Please enter your email address."
            ),
        }

    if len(password) < 8:

        return {
            "success": False,
            "message": (
                "Password must contain at least "
                "8 characters."
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
                    "HJMI could not create "
                    "the account."
                ),
            }

        return {
            "success": True,
            "message": (
                "Account created. Please check "
                "your email and confirm your "
                "account before signing in."
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
    Sign an existing HJMI user in and persist the
    authentication session.
    """

    supabase = get_supabase_client()

    email = email.strip().lower()

    if not email or not password:

        return {
            "success": False,
            "message": (
                "Please enter your email "
                "and password."
            ),
        }

    try:

        response = (
            supabase.auth
            .sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
        )

        if (
            response.user is None
            or response.session is None
        ):

            return {
                "success": False,
                "message": (
                    "HJMI could not sign you in."
                ),
            }

        store_session(
            response.user,
            response.session,
        )

        cookie_saved = save_auth_cookie(
            response.session.refresh_token
        )

        if not cookie_saved:

            return {
                "success": False,
                "message": (
                    "Signed in, but HJMI could not "
                    "save the persistent session."
                ),
            }

        return {
            "success": True,
            "message": (
                "Signed in successfully."
            ),
            "user": response.user,
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                "Invalid email or password, "
                "or the account has not been "
                "confirmed yet."
            ),
        }


# ============================================================
# SIGN OUT
# ============================================================

def sign_out():
    """
    Sign the current HJMI user out, clear the Streamlit
    session and remove the persistent login cookie.
    """

    access_token = st.session_state.get(
        "hjmi_access_token"
    )

    refresh_token = st.session_state.get(
        "hjmi_refresh_token"
    )

    try:

        if access_token and refresh_token:

            supabase = get_supabase_client()

            supabase.auth.set_session(
                access_token,
                refresh_token,
            )

            supabase.auth.sign_out()

    except Exception:

        pass

    clear_session()

    delete_auth_cookie()

    return {
        "success": True,
        "message": (
            "Signed out successfully."
        ),
    }


# ============================================================
# AUTHENTICATION STATE
# ============================================================

def is_authenticated() -> bool:
    """
    Return True when the user is authenticated.

    If the Streamlit session is lost, HJMI attempts
    to restore authentication from the browser cookie.
    """

    authenticated = bool(
        st.session_state.get(
            "hjmi_authenticated",
            False,
        )
        and st.session_state.get(
            "hjmi_user"
        ) is not None
        and st.session_state.get(
            "hjmi_access_token"
        )
        and st.session_state.get(
            "hjmi_refresh_token"
        )
    )

    if authenticated:
        return True

    return restore_session()


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
