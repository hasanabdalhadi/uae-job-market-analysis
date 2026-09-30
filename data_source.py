"""
HJMI — Hasan Job Market Intelligence
Automated UAE Technology Jobs Data Source

Collects UAE technology job listings from the Jooble UAE REST API,
normalizes the results, removes duplicates, and preserves historical data.
"""

from pathlib import Path
from datetime import datetime, timezone
import os

import pandas as pd
import requests


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data")
RAW_FILE = DATA_DIR / "uae_jobs_live_raw.csv"

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

# UAE-specific Jooble API endpoint.
API_BASE_URL = "https://ae.jooble.org/api"

# Keep API usage low:
# 3 searches = 3 API requests per pipeline run.
#
# These broad searches cover a useful range of technology roles
# while avoiding excessive use of the 500-request lifetime quota.
SEARCHES = [
    "software engineer developer",
    "data analyst data scientist data engineer",
    "IT cybersecurity cloud AI computer science",
]

SEARCH_LOCATION = "United Arab Emirates"

RESULTS_PER_REQUEST = 50

REQUEST_TIMEOUT = 30


# ============================================================
# HELPERS
# ============================================================

def clean_value(value):
    """
    Safely convert API values into clean strings.
    """

    if value is None:
        return ""

    return str(value).strip()


def build_source_id(job):
    """
    Use Jooble's job ID when available.

    If an ID is missing, create a deterministic fallback
    identifier from stable job fields.
    """

    source_id = clean_value(job.get("id"))

    if source_id:
        return source_id

    title = clean_value(job.get("title"))
    company = clean_value(job.get("company"))
    location = clean_value(job.get("location"))
    link = clean_value(job.get("link"))

    return f"{title}|{company}|{location}|{link}"


# ============================================================
# FETCH DATA FROM JOOBLE
# ============================================================

def fetch_jobs(keywords):
    """
    Fetch one page of UAE job listings from Jooble.
    """

    if not JOOBLE_API_KEY:
        raise RuntimeError(
            "JOOBLE_API_KEY is missing. "
            "Add it to GitHub repository Actions secrets."
        )

    api_url = f"{API_BASE_URL}/{JOOBLE_API_KEY}"

    payload = {
        "keywords": keywords,
        "location": SEARCH_LOCATION,
        "page": 1,
        "ResultOnPage": RESULTS_PER_REQUEST,
        "companysearch": False,
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "HJMI-UAE-Job-Market-Intelligence/1.0",
    }

    print()
    print("--------------------------------------")
    print(f"Search: {keywords}")
    print(f"Location: {SEARCH_LOCATION}")

    try:
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.RequestException as error:
        print(f"Network request failed: {error}")
        return []

    if response.status_code == 403:
        raise RuntimeError(
            "Jooble returned HTTP 403. "
            "Check that JOOBLE_API_KEY is valid and belongs "
            "to the UAE Jooble domain."
        )

    if response.status_code == 404:
        raise RuntimeError(
            "Jooble returned HTTP 404. "
            "The UAE API endpoint could not be reached."
        )

    try:
        response.raise_for_status()

    except requests.RequestException as error:
        print(
            f"Jooble request failed with HTTP "
            f"{response.status_code}: {error}"
        )
        return []

    try:
        data = response.json()

    except ValueError as error:
        print(
            f"Jooble returned an invalid JSON response: {error}"
        )
        return []

    jobs = data.get("jobs", [])

    if not isinstance(jobs, list):
        print("Unexpected Jooble response: 'jobs' is not a list.")
        return []

    total_count = data.get("totalCount", "Unknown")

    print(f"Available matches reported by Jooble: {total_count}")
    print(f"Jobs received in this request: {len(jobs):,}")

    return jobs


# ============================================================
# NORMALIZE JOOBLE RECORDS
# ============================================================

def normalize_job(job):
    """
    Convert one Jooble record into the standard HJMI schema.
    """

    return {
        "source_id": build_source_id(job),
        "job_title": clean_value(job.get("title")),
        "company": clean_value(job.get("company")),
        "location": clean_value(job.get("location")),
        "category": clean_value(job.get("type")),
        "description": clean_value(job.get("snippet")),
        "salary": clean_value(job.get("salary")),
        "publication_date": clean_value(job.get("updated")),
        "job_url": clean_value(job.get("link")),
        "source": clean_value(job.get("source")) or "Jooble",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# CURRENT DATA COLLECTION
# ============================================================

def collect_current_jobs():
    """
    Run the three configured searches and return one DataFrame.
    """

    collected_jobs = []

    for keywords in SEARCHES:
        jobs = fetch_jobs(keywords)

        for job in jobs:
            if not isinstance(job, dict):
                continue

            normalized = normalize_job(job)

            # A record without a title is not useful for HJMI.
            if not normalized["job_title"]:
                continue

            collected_jobs.append(normalized)

    if not collected_jobs:
        raise RuntimeError(
            "Jooble returned no usable UAE technology job records."
        )

    current_df = pd.DataFrame(collected_jobs)

    print()
    print("======================================")
    print(" CURRENT COLLECTION")
    print("======================================")
    print(
        f"Records before deduplication: "
        f"{len(current_df):,}"
    )

    # First deduplicate using Jooble's ID.
    current_df = current_df.drop_duplicates(
        subset=["source_id"],
        keep="last",
    )

    # Additional protection for overlapping searches.
    current_df = current_df.drop_duplicates(
        subset=[
            "job_title",
            "company",
            "location",
        ],
        keep="last",
    )

    current_df = current_df.reset_index(drop=True)

    print(
        f"Unique current records: "
        f"{len(current_df):,}"
    )

    return current_df


# ============================================================
# HISTORICAL DATA
# ============================================================

def merge_historical_data(current_df):
    """
    Merge newly fetched records with previous HJMI records.

    Existing jobs are retained so the project can build
    historical job-market data over time.
    """

    if not RAW_FILE.exists():
        return current_df

    try:
        old_df = pd.read_csv(
            RAW_FILE,
            low_memory=False,
        )

    except Exception as error:
        print()
        print(
            "Previous dataset could not be loaded. "
            f"Continuing with current data only: {error}"
        )
        return current_df

    if old_df.empty:
        return current_df

    print()
    print(
        f"Previously stored records: {len(old_df):,}"
    )

    combined_df = pd.concat(
        [old_df, current_df],
        ignore_index=True,
        sort=False,
    )

    if "source_id" in combined_df.columns:
        combined_df = combined_df.drop_duplicates(
            subset=["source_id"],
            keep="last",
        )

    required_dedupe_columns = [
        "job_title",
        "company",
        "location",
    ]

    if all(
        column in combined_df.columns
        for column in required_dedupe_columns
    ):
        combined_df = combined_df.drop_duplicates(
            subset=required_dedupe_columns,
            keep="last",
        )

    return combined_df.reset_index(drop=True)


# ============================================================
# SAVE DATASET
# ============================================================

def save_dataset(dataframe):
    """
    Save the raw historical HJMI dataset.
    """

    if dataframe.empty:
        raise RuntimeError(
            "HJMI refused to save an empty dataset."
        )

    # Convert publication dates safely for correct sorting.
    if "publication_date" in dataframe.columns:
        sort_dates = pd.to_datetime(
            dataframe["publication_date"],
            errors="coerce",
            utc=True,
        )

        dataframe = dataframe.assign(
            _sort_date=sort_dates
        )

        dataframe = dataframe.sort_values(
            by="_sort_date",
            ascending=False,
            na_position="last",
        )

        dataframe = dataframe.drop(
            columns=["_sort_date"]
        )

    dataframe = dataframe.reset_index(drop=True)

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        RAW_FILE,
        index=False,
    )

    return dataframe


# ============================================================
# MAIN DATA PIPELINE
# ============================================================

def download_dataset():
    """
    Fetch, normalize, merge, and save UAE technology jobs.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("======================================")
    print(" HJMI — UAE JOB MARKET INTELLIGENCE")
    print(" Automated Data Collection")
    print(" Source: Jooble UAE")
    print("======================================")

    if not JOOBLE_API_KEY:
        raise RuntimeError(
            "JOOBLE_API_KEY environment variable was not found."
        )

    current_df = collect_current_jobs()

    final_df = merge_historical_data(
        current_df
    )

    final_df = save_dataset(
        final_df
    )

    print()
    print("======================================")
    print(" HJMI DATA COLLECTION COMPLETE")
    print("======================================")
    print(
        f"Current unique jobs collected: "
        f"{len(current_df):,}"
    )
    print(
        f"Total historical records stored: "
        f"{len(final_df):,}"
    )
    print(
        f"API requests used this run: "
        f"{len(SEARCHES)}"
    )
    print(
        f"Saved to: {RAW_FILE}"
    )

    return final_df


# ============================================================
# PUBLIC LOADER
# ============================================================

def load_dataset():
    """
    Called by prepare_data.py.

    Each pipeline execution refreshes the Jooble data first.
    """

    return download_dataset()


# ============================================================
# MANUAL EXECUTION
# ============================================================

if __name__ == "__main__":
    data = download_dataset()

    print()
    print("Dataset columns:")

    for column in data.columns:
        print(f"- {column}")

    print()
    print("Preview:")

    preview_columns = [
        "job_title",
        "company",
        "location",
        "salary",
        "publication_date",
        "source",
    ]

    available_columns = [
        column
        for column in preview_columns
        if column in data.columns
    ]

    print(
        data[available_columns]
        .head(10)
        .to_string(index=False)
    )
