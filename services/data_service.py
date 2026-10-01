# ============================================================
# HJMI 2.0 — CENTRAL DATA SERVICE
# Hasan Job Market Intelligence
# ============================================================

from pathlib import Path
import re

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path("data/uae_tech_jobs_clean.csv")

EMPTY_TEXT_VALUES = {
    "",
    "nan",
    "none",
    "null",
    "n/a",
    "na",
    "not available",
}


# ============================================================
# BASIC HELPERS
# ============================================================

def clean_text(value, fallback="Not specified"):
    """Return clean user-facing text."""

    if pd.isna(value):
        return fallback

    text = str(value).strip()

    if text.lower() in EMPTY_TEXT_VALUES:
        return fallback

    return text


def normalize_boolean_series(series):
    """Safely convert CSV values to booleans."""

    return (
        series
        .fillna(False)
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes", "y"])
    )


def normalize_text_series(series):
    """Clean a pandas text column."""

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# EXPERIENCE INTELLIGENCE
# ============================================================

FRESH_GRADUATE_PATTERNS = [
    r"\bfresh graduate(?:s)?\b",
    r"\brecent graduate(?:s)?\b",
    r"\bnew graduate(?:s)?\b",
    r"\bgraduate program(?:me)?\b",
    r"\bgraduate trainee\b",
    r"\bentry[\s-]?level\b",
    r"\bjunior level\b",
    r"\bno experience required\b",
    r"\bno prior experience\b",
    r"\bwithout experience\b",
    r"\b0[\s-]*(?:to|-)[\s-]*1 year",
    r"\b0[\s-]*(?:to|-)[\s-]*2 years",
]


EXPERIENCE_PATTERNS = [
    # 2-3 years / 2 to 3 years
    r"(\d+)\s*(?:-|–|—|to)\s*(\d+)\s*\+?\s*(?:years?|yrs?)",

    # minimum 3 years / at least 3 years
    r"(?:minimum|min\.?|at least)\s*(?:of\s*)?(\d+)\s*\+?\s*(?:years?|yrs?)",

    # 3+ years
    r"(\d+)\s*\+\s*(?:years?|yrs?)",

    # 3 years of experience
    r"(\d+)\s*(?:years?|yrs?)\s+(?:of\s+)?(?:relevant\s+)?experience",

    # experience of 3 years
    r"experience\s+(?:of\s+)?(?:at least\s+)?(\d+)\s*\+?\s*(?:years?|yrs?)",
]


def combined_job_text(row):
    """Combine useful text fields for classification."""

    fields = [
        "job_title",
        "category",
        "description",
    ]

    values = []

    for field in fields:
        if field in row.index:
            value = row.get(field)

            if pd.notna(value):
                values.append(str(value))

    return " ".join(values).lower()


def detect_experience_years(text):
    """
    Extract an experience range when explicitly mentioned.

    Returns:
        (minimum_years, maximum_years)
    """

    if not text:
        return None, None

    text = str(text).lower()

    # Range first
    range_pattern = (
        r"(\d+)\s*(?:-|–|—|to)\s*(\d+)"
        r"\s*\+?\s*(?:years?|yrs?)"
    )

    match = re.search(range_pattern, text)

    if match:
        minimum = int(match.group(1))
        maximum = int(match.group(2))

        if minimum <= maximum and maximum <= 30:
            return minimum, maximum

    # Single minimum values
    single_patterns = [
        r"(?:minimum|min\.?|at least)\s*(?:of\s*)?"
        r"(\d+)\s*\+?\s*(?:years?|yrs?)",

        r"(\d+)\s*\+\s*(?:years?|yrs?)",

        r"(\d+)\s*(?:years?|yrs?)\s+"
        r"(?:of\s+)?(?:relevant\s+)?experience",

        r"experience\s+(?:of\s+)?(?:at least\s+)?"
        r"(\d+)\s*\+?\s*(?:years?|yrs?)",
    ]

    for pattern in single_patterns:
        match = re.search(pattern, text)

        if match:
            minimum = int(match.group(1))

            if minimum <= 30:
                return minimum, None

    return None, None


def detect_fresh_graduate(text, minimum_years=None, maximum_years=None):
    """
    Detect whether a listing explicitly appears suitable
    for fresh graduates or entry-level candidates.
    """

    if not text:
        return False

    text = str(text).lower()

    for pattern in FRESH_GRADUATE_PATTERNS:
        if re.search(pattern, text):
            return True

    # Explicit 0-year requirement
    if minimum_years == 0:
        return True

    return False


def classify_experience(minimum_years, maximum_years, fresh_graduate):
    """Create a clear user-facing experience category."""

    if fresh_graduate:
        return "Fresh Graduate / Entry Level"

    if minimum_years is None:
        return "Not Specified"

    if maximum_years is not None:
        if maximum_years <= 1:
            return "0–1 Year"

        if maximum_years <= 2:
            return "1–2 Years"

        if maximum_years <= 3:
            return "2–3 Years"

        if maximum_years <= 5:
            return "3–5 Years"

        return "5+ Years"

    if minimum_years <= 1:
        return "0–1 Year"

    if minimum_years <= 2:
        return "1–2 Years"

    if minimum_years <= 3:
        return "2–3 Years"

    if minimum_years <= 5:
        return "3–5 Years"

    return "5+ Years"


def enrich_experience_data(df):
    """Add experience intelligence columns."""

    if df.empty:
        return df

    minimum_values = []
    maximum_values = []
    levels = []
    graduate_flags = []

    for _, row in df.iterrows():

        text = combined_job_text(row)

        minimum, maximum = detect_experience_years(text)

        graduate_friendly = detect_fresh_graduate(
            text,
            minimum,
            maximum,
        )

        level = classify_experience(
            minimum,
            maximum,
            graduate_friendly,
        )

        minimum_values.append(minimum)
        maximum_values.append(maximum)
        graduate_flags.append(graduate_friendly)
        levels.append(level)

    df["experience_min"] = minimum_values
    df["experience_max"] = maximum_values
    df["experience_level"] = levels
    df["fresh_graduate_friendly"] = graduate_flags

    return df


# ============================================================
# EXPERIENCE DISPLAY
# ============================================================

def experience_display(row):
    """Return a readable experience requirement."""

    if bool(row.get("fresh_graduate_friendly", False)):
        return "Fresh Graduate / Entry Level"

    minimum = row.get("experience_min")
    maximum = row.get("experience_max")

    if pd.notna(minimum) and pd.notna(maximum):
        minimum = int(minimum)
        maximum = int(maximum)

        if minimum == maximum:
            return f"{minimum} Years"

        return f"{minimum}–{maximum} Years"

    if pd.notna(minimum):
        return f"{int(minimum)}+ Years"

    return "Not specified"


# ============================================================
# SALARY INTELLIGENCE
# ============================================================

def salary_is_missing(value):
    """Check whether salary information is unavailable."""

    if pd.isna(value):
        return True

    text = str(value).strip().lower()

    return text in EMPTY_TEXT_VALUES


def salary_display(value):
    """
    Return salary information for users.

    HJMI never fabricates an employer salary.
    """

    if salary_is_missing(value):
        return "To be discussed after the interview"

    text = str(value).strip()

    lower = text.lower()

    negotiation_terms = [
        "negotiable",
        "to be discussed",
        "discussed during interview",
        "discussed after interview",
        "upon interview",
    ]

    if any(term in lower for term in negotiation_terms):
        return "To be discussed after the interview"

    return text


def enrich_salary_data(df):
    """Add user-facing salary information."""

    if df.empty:
        return df

    if "salary" not in df.columns:
        df["salary"] = pd.NA

    df["salary_display"] = df["salary"].apply(salary_display)

    df["salary_disclosed"] = ~df["salary"].apply(
        salary_is_missing
    )

    return df


# ============================================================
# SKILLS INTELLIGENCE
# ============================================================

def parse_skills(value):
    """Convert stored skill text into a clean list."""

    if pd.isna(value):
        return []

    raw = str(value).strip()

    if raw.lower() in EMPTY_TEXT_VALUES:
        return []

    skills = []

    for item in raw.split(","):
        skill = item.strip()

        if skill and skill.lower() not in EMPTY_TEXT_VALUES:
            skills.append(skill)

    # Preserve order while removing duplicates
    return list(dict.fromkeys(skills))


def all_skills(df):
    """Return unique skills represented in a dataframe."""

    if df.empty or "skills" not in df.columns:
        return []

    values = []

    for item in df["skills"]:
        values.extend(parse_skills(item))

    return sorted(
        set(values),
        key=lambda x: x.lower(),
    )


def skill_counts(df):
    """Count jobs mentioning each identified skill."""

    if df.empty or "skills" not in df.columns:
        return pd.Series(dtype="int64")

    skills = (
        df["skills"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    skills = skills[
        (skills != "")
        & (~skills.str.lower().isin(EMPTY_TEXT_VALUES))
    ]

    return skills.value_counts()


# ============================================================
# STATUS INTELLIGENCE
# ============================================================

def status_display(row):
    """Return a user-friendly job status."""

    is_active = bool(row.get("is_active", False))
    is_new = bool(row.get("is_new", False))

    if is_active and is_new:
        return "New Opportunity"

    if is_active:
        return "Active"

    return "Historical"


def new_display(value):
    """Replace True/False with meaningful UI text."""

    return "New" if bool(value) else "—"


# ============================================================
# DATE HELPERS
# ============================================================

def format_date(value):
    """Return a readable date where possible."""

    if pd.isna(value):
        return "Not available"

    parsed = pd.to_datetime(
        value,
        errors="coerce",
        utc=True,
    )

    if pd.isna(parsed):
        return clean_text(
            value,
            fallback="Not available",
        )

    return parsed.strftime("%d %b %Y")


def get_last_update(df):
    """Find the latest known collection time."""

    if df.empty:
        return "Not available"

    candidate_columns = [
        "last_seen",
        "fetched_at",
        "publication_date",
    ]

    for column in candidate_columns:

        if column not in df.columns:
            continue

        values = pd.to_datetime(
            df[column],
            errors="coerce",
            utc=True,
        ).dropna()

        if not values.empty:
            return values.max().strftime(
                "%d %b %Y • %H:%M UTC"
            )

    return "Not available"


# ============================================================
# DATA PREPARATION
# ============================================================

def prepare_dataframe(df):
    """Prepare raw clean CSV data for HJMI 2.0."""

    if df.empty:
        return df

    df = df.copy()

    # --------------------------------------------------------
    # REQUIRED TEXT COLUMNS
    # --------------------------------------------------------

    text_columns = [
        "job_title",
        "company",
        "location",
        "category",
        "description",
        "skills",
        "salary",
        "publication_date",
        "job_url",
        "source",
        "first_seen",
        "last_seen",
        "fetched_at",
    ]

    for column in text_columns:

        if column not in df.columns:
            df[column] = ""

        df[column] = normalize_text_series(
            df[column]
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if "is_active" in df.columns:
        df["is_active"] = normalize_boolean_series(
            df["is_active"]
        )
    else:
        df["is_active"] = True

    if "is_new" in df.columns:
        df["is_new"] = normalize_boolean_series(
            df["is_new"]
        )
    else:
        df["is_new"] = False

    df["job_status"] = df.apply(
        status_display,
        axis=1,
    )

    df["new_label"] = df["is_new"].apply(
        new_display
    )

    # --------------------------------------------------------
    # USER-FACING FALLBACKS
    # --------------------------------------------------------

    df["job_title_display"] = df["job_title"].apply(
        lambda x: clean_text(
            x,
            "Job title not specified",
        )
    )

    df["company_display"] = df["company"].apply(
        lambda x: clean_text(
            x,
            "Company not specified",
        )
    )

    df["location_display"] = df["location"].apply(
        lambda x: clean_text(
            x,
            "UAE location not specified",
        )
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    df = enrich_experience_data(df)

    df["experience_display"] = df.apply(
        experience_display,
        axis=1,
    )

    # --------------------------------------------------------
    # SALARY
    # --------------------------------------------------------

    df = enrich_salary_data(df)

    # --------------------------------------------------------
    # DISPLAY DATES
    # --------------------------------------------------------

    df["first_seen_display"] = df[
        "first_seen"
    ].apply(format_date)

    df["last_seen_display"] = df[
        "last_seen"
    ].apply(format_date)

    df["publication_date_display"] = df[
        "publication_date"
    ].apply(format_date)

    return df


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=900)
def load_jobs():
    """
    Load the central HJMI dataset.

    Cache refreshes every 15 minutes so the dashboard can
    pick up updated GitHub-generated CSV data.
    """

    if not DATA_FILE.exists():
        return pd.DataFrame()

    try:
        raw_df = pd.read_csv(DATA_FILE)

    except Exception:
        return pd.DataFrame()

    return prepare_dataframe(raw_df)


# ============================================================
# DATA VIEWS
# ============================================================

def get_active_jobs(df):
    """Jobs seen in the latest HJMI collection."""

    if df.empty:
        return df.copy()

    return df[df["is_active"]].copy()


def get_new_jobs(df):
    """Jobs first discovered in the latest update."""

    if df.empty:
        return df.copy()

    return df[
        df["is_active"]
        & df["is_new"]
    ].copy()


def get_historical_jobs(df):
    """Jobs stored historically but not seen in latest check."""

    if df.empty:
        return df.copy()

    return df[
        ~df["is_active"]
    ].copy()


def get_graduate_jobs(df):
    """Jobs identified as fresh-graduate friendly."""

    if df.empty:
        return df.copy()

    return df[
        df["fresh_graduate_friendly"]
    ].copy()


# ============================================================
# MARKET METRICS
# ============================================================

def get_market_metrics(df):
    """Return reusable market metrics."""

    if df.empty:
        return {
            "active_jobs": 0,
            "new_jobs": 0,
            "historical_jobs": 0,
            "jobs_collected": 0,
            "graduate_jobs": 0,
            "companies": 0,
            "locations": 0,
            "skills": 0,
            "salary_disclosed": 0,
            "last_update": "Not available",
        }

    active = get_active_jobs(df)
    new = get_new_jobs(df)
    historical = get_historical_jobs(df)
    graduate = get_graduate_jobs(active)

    company_values = (
        active["company"]
        .replace("", pd.NA)
        .dropna()
    )

    location_values = (
        active["location"]
        .replace("", pd.NA)
        .dropna()
    )

    return {
        "active_jobs": len(active),
        "new_jobs": len(new),
        "historical_jobs": len(historical),
        "jobs_collected": len(df),
        "graduate_jobs": len(graduate),
        "companies": company_values.nunique(),
        "locations": location_values.nunique(),
        "skills": len(all_skills(active)),
        "salary_disclosed": int(
            active["salary_disclosed"].sum()
        ),
        "last_update": get_last_update(df),
    }


# ============================================================
# FILTER OPTIONS
# ============================================================

def get_filter_options(df):
    """Return common filter options used across HJMI pages."""

    if df.empty:
        return {
            "locations": [],
            "companies": [],
            "skills": [],
            "experience_levels": [],
        }

    locations = sorted(
        [
            value
            for value in df["location"].dropna().unique()
            if str(value).strip()
        ],
        key=lambda x: str(x).lower(),
    )

    companies = sorted(
        [
            value
            for value in df["company"].dropna().unique()
            if str(value).strip()
        ],
        key=lambda x: str(x).lower(),
    )

    experience_levels = [
        "Fresh Graduate / Entry Level",
        "0–1 Year",
        "1–2 Years",
        "2–3 Years",
        "3–5 Years",
        "5+ Years",
        "Not Specified",
    ]

    return {
        "locations": locations,
        "companies": companies,
        "skills": all_skills(df),
        "experience_levels": experience_levels,
    }


# ============================================================
# JOB SEARCH
# ============================================================

def search_jobs(
    df,
    search_text="",
    location=None,
    company=None,
    skill=None,
    experience=None,
    graduate_only=False,
    new_only=False,
):
    """Reusable job filtering engine."""

    if df.empty:
        return df.copy()

    result = df.copy()

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if search_text:

        query = str(search_text).strip().lower()

        searchable_columns = [
            "job_title",
            "company",
            "location",
            "category",
            "description",
            "skills",
        ]

        available = [
            column
            for column in searchable_columns
            if column in result.columns
        ]

        if available:

            mask = (
                result[available]
                .fillna("")
                .astype(str)
                .apply(
                    lambda column:
                    column.str.lower().str.contains(
                        query,
                        regex=False,
                    )
                )
                .any(axis=1)
            )

            result = result[mask]

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    if location and location != "All Locations":

        result = result[
            result["location"] == location
        ]

    # --------------------------------------------------------
    # COMPANY
    # --------------------------------------------------------

    if company and company != "All Companies":

        result = result[
            result["company"] == company
        ]

    # --------------------------------------------------------
    # SKILL
    # --------------------------------------------------------

    if skill and skill != "All Skills":

        skill_lower = str(skill).lower()

        result = result[
            result["skills"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(
                skill_lower,
                regex=False,
            )
        ]

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    if (
        experience
        and experience != "All Experience Levels"
    ):

        result = result[
            result["experience_level"]
            == experience
        ]

    # --------------------------------------------------------
    # FRESH GRADUATE
    # --------------------------------------------------------

    if graduate_only:

        result = result[
            result["fresh_graduate_friendly"]
        ]

    # --------------------------------------------------------
    # NEW
    # --------------------------------------------------------

    if new_only:

        result = result[
            result["is_new"]
        ]

    return result.copy()
