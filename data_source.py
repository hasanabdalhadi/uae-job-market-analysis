"""
HJMI — Hasan Job Market Intelligence
Automated UAE Technology Jobs Data Source

Collects UAE technology job listings from the Jooble UAE REST API,
normalizes the results, removes duplicates, and preserves historical data.

The pipeline also tracks:
- First time a job was seen
- Last time a job was seen
- Whether a job is currently active
- Whether a job is new in the latest collection
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
    """Safely convert API values into clean strings."""

    if value is None:
        return ""

    return str(value).strip()


def utc_now():
    """Return the current UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


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
    """Fetch one page of UAE job listings from Jooble."""

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

def normalize_job(job, collection_time):
    """Convert one Jooble record into the standard HJMI schema."""

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
        "fetched_at": collection_time,
    }


# ============================================================
# CURRENT DATA COLLECTION
# ============================================================

def collect_current_jobs():
    """Run the configured searches and return current jobs."""

    collected_jobs = []

    collection_time = utc_now()

    for keywords in SEARCHES:

        jobs = fetch_jobs(keywords)

        for job in jobs:

            if not isinstance(job, dict):
                continue

            normalized = normalize_job(
                job,
                collection_time,
            )

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

    current_df = current_df.drop_duplicates(
        subset=["source_id"],
        keep="last",
    )

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
# HISTORICAL DATA + JOB STATUS TRACKING
# ============================================================

def merge_historical_data(current_df):
    """
    Merge current jobs with historical HJMI records.

    Jobs found in the latest collection:
        is_active = True

    Historical jobs not found in the latest collection:
        is_active = False

    Existing records are preserved for long-term market analysis.
    """

    now = utc_now()

    current_df = current_df.copy()

    current_df["first_seen"] = now
    current_df["last_seen"] = now
    current_df["is_active"] = True
    current_df["status"] = "Active"
    current_df["is_new"] = True

    if not RAW_FILE.exists():

        print()
        print("No historical dataset found.")
        print("All current jobs will be marked as new.")

        return current_df.reset_index(drop=True)

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

        return current_df.reset_index(drop=True)

    if old_df.empty:
        return current_df.reset_index(drop=True)

    print()
    print(
        f"Previously stored records: {len(old_df):,}"
    )

    # --------------------------------------------------------
    # Support datasets created before status tracking existed
    # --------------------------------------------------------

    if "first_seen" not in old_df.columns:

        if "fetched_at" in old_df.columns:
            old_df["first_seen"] = old_df["fetched_at"]
        else:
            old_df["first_seen"] = ""

    if "last_seen" not in old_df.columns:

        if "fetched_at" in old_df.columns:
            old_df["last_seen"] = old_df["fetched_at"]
        else:
            old_df["last_seen"] = ""

    if "is_active" not in old_df.columns:
        old_df["is_active"] = False

    if "status" not in old_df.columns:
        old_df["status"] = "Inactive"

    if "is_new" not in old_df.columns:
        old_df["is_new"] = False

    # --------------------------------------------------------
    # Create lookup using source IDs
    # --------------------------------------------------------

    old_df["source_id"] = (
        old_df["source_id"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    current_df["source_id"] = (
        current_df["source_id"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    old_lookup = (
        old_df
        .drop_duplicates(
            subset=["source_id"],
            keep="last",
        )
        .set_index("source_id")
    )

    current_ids = set(
        current_df["source_id"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    current_ids.discard("")

    old_ids = set(
        old_df["source_id"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    old_ids.discard("")

    # --------------------------------------------------------
    # Preserve original first_seen for known jobs
    # --------------------------------------------------------

    for index, row in current_df.iterrows():

        source_id = row["source_id"]

        if source_id and source_id in old_lookup.index:

            old_record = old_lookup.loc[source_id]

            previous_first_seen = clean_value(
                old_record.get("first_seen", "")
            )

            if previous_first_seen:
                current_df.at[
                    index,
                    "first_seen"
                ] = previous_first_seen

            current_df.at[
                index,
                "is_new"
            ] = False

    # --------------------------------------------------------
    # Mark old jobs inactive before merging
    # --------------------------------------------------------

    old_df["is_active"] = False
    old_df["status"] = "Inactive"
    old_df["is_new"] = False

    # --------------------------------------------------------
    # Remove old versions of jobs that appeared again
    # --------------------------------------------------------

    historical_only = old_df[
        ~old_df["source_id"].isin(current_ids)
    ].copy()

    # --------------------------------------------------------
    # Merge historical and current records
    # --------------------------------------------------------

    combined_df = pd.concat(
        [
            historical_only,
            current_df,
        ],
        ignore_index=True,
        sort=False,
    )

    # --------------------------------------------------------
    # Final duplicate protection
    # --------------------------------------------------------

    if "source_id" in combined_df.columns:

        with_id = combined_df[
            combined_df["source_id"]
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
        ].drop_duplicates(
            subset=["source_id"],
            keep="last",
        )

        without_id = combined_df[
            combined_df["source_id"]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
        ].drop_duplicates(
            subset=[
                "job_title",
                "company",
                "location",
            ],
            keep="last",
        )

        combined_df = pd.concat(
            [
                with_id,
                without_id,
            ],
            ignore_index=True,
        )

    else:

        combined_df = combined_df.drop_duplicates(
            subset=[
                "job_title",
                "company",
                "location",
            ],
            keep="last",
        )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    active_count = int(
        combined_df["is_active"]
        .fillna(False)
        .astype(bool)
        .sum()
    )

    new_count = int(
        combined_df["is_new"]
        .fillna(False)
        .astype(bool)
        .sum()
    )

    historical_count = len(combined_df)

    inactive_count = (
        historical_count - active_count
    )

    print()
    print("======================================")
    print(" JOB STATUS TRACKING")
    print("======================================")

    print(
        f"Active jobs: {active_count:,}"
    )

    print(
        f"New jobs this collection: {new_count:,}"
    )

    print(
        f"Inactive historical jobs: "
        f"{inactive_count:,}"
    )

    print(
        f"Total jobs collected historically: "
        f"{historical_count:,}"
    )

    return combined_df.reset_index(drop=True)


# ============================================================
# SAVE DATASET
# ============================================================

def save_dataset(dataframe):
    """Save the raw historical HJMI dataset."""

    if dataframe.empty:
        raise RuntimeError(
            "HJMI refused to save an empty dataset."
        )

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
    """Fetch, normalize, track, merge and save UAE tech jobs."""

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

    active_count = int(
        final_df["is_active"]
        .fillna(False)
        .astype(bool)
        .sum()
    )

    new_count = int(
        final_df["is_new"]
        .fillna(False)
        .astype(bool)
        .sum()
    )

    print()
    print("======================================")
    print(" HJMI DATA COLLECTION COMPLETE")
    print("======================================")

    print(
        f"Current unique jobs received: "
        f"{len(current_df):,}"
    )

    print(
        f"Active jobs: "
        f"{active_count:,}"
    )

    print(
        f"New jobs: "
        f"{new_count:,}"
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
        "first_seen",
        "last_seen",
        "status",
        "is_new",
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
