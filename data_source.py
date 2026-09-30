"""
HJMI — Hasan Job Market Intelligence
Automated UAE Technology Jobs Data Source

Fetches current UAE job listings from The Muse public jobs API.
"""

from pathlib import Path
from datetime import datetime, timezone
import requests
import pandas as pd


DATA_DIR = Path("data")
RAW_FILE = DATA_DIR / "uae_jobs_live_raw.csv"

API_URL = "https://www.themuse.com/api/public/jobs"

UAE_LOCATIONS = [
    "Dubai, United Arab Emirates",
    "Abu Dhabi, United Arab Emirates",
    "United Arab Emirates",
]

TECH_CATEGORIES = [
    "Computer and IT",
    "Data and Analytics",
    "Software",
    "Data Science",
    "Engineering",
]


def fetch_jobs(location, category, max_pages=10):
    """Fetch jobs from The Muse API for one location/category."""

    jobs = []

    for page in range(max_pages):
        params = {
            "page": page,
            "location": location,
            "category": category,
            "descending": "true",
        }

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=30,
            )

            response.raise_for_status()

            payload = response.json()
            results = payload.get("results", [])

            if not results:
                break

            for job in results:
                company = job.get("company") or {}
                locations = job.get("locations") or []
                categories = job.get("categories") or []

                location_names = [
                    item.get("name", "")
                    for item in locations
                    if isinstance(item, dict)
                ]

                category_names = [
                    item.get("name", "")
                    for item in categories
                    if isinstance(item, dict)
                ]

                jobs.append(
                    {
                        "source_id": job.get("id", ""),
                        "job_title": job.get("name", ""),
                        "company": company.get("name", ""),
                        "location": ", ".join(location_names),
                        "category": ", ".join(category_names),
                        "description": job.get("contents", ""),
                        "publication_date": job.get(
                            "publication_date", ""
                        ),
                        "job_url": (
                            (job.get("refs") or {}).get(
                                "landing_page", ""
                            )
                        ),
                        "source": "The Muse",
                        "fetched_at": datetime.now(
                            timezone.utc
                        ).isoformat(),
                    }
                )

        except requests.RequestException as error:
            print(
                f"Request failed for {location} / "
                f"{category}: {error}"
            )
            break

    return jobs


def download_dataset():
    """Fetch current UAE technology jobs."""

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("======================================")
    print(" HJMI LIVE UAE JOB DATA COLLECTION")
    print("======================================")

    all_jobs = []

    for location in UAE_LOCATIONS:
        for category in TECH_CATEGORIES:

            print(
                f"Fetching: {category} | {location}"
            )

            jobs = fetch_jobs(
                location=location,
                category=category,
            )

            all_jobs.extend(jobs)

            print(
                f"Collected {len(jobs):,} records."
            )

    if not all_jobs:
        raise RuntimeError(
            "No jobs were returned by the live data source."
        )

    new_df = pd.DataFrame(all_jobs)

    # Remove duplicates returned from overlapping searches
    if "source_id" in new_df.columns:
        new_df = new_df.drop_duplicates(
            subset=["source_id"]
        )
    else:
        new_df = new_df.drop_duplicates(
            subset=[
                "job_title",
                "company",
                "location",
            ]
        )

    # Keep historical records from previous runs
    if RAW_FILE.exists():

        try:
            old_df = pd.read_csv(
                RAW_FILE,
                low_memory=False,
            )

            combined = pd.concat(
                [old_df, new_df],
                ignore_index=True,
            )

            if "source_id" in combined.columns:
                combined = combined.drop_duplicates(
                    subset=["source_id"],
                    keep="last",
                )
            else:
                combined = combined.drop_duplicates(
                    subset=[
                        "job_title",
                        "company",
                        "location",
                    ],
                    keep="last",
                )

            new_df = combined

        except Exception as error:
            print(
                "Could not merge previous data:",
                error,
            )

    new_df = new_df.reset_index(drop=True)

    new_df.to_csv(
        RAW_FILE,
        index=False,
    )

    print()
    print("Live UAE job dataset updated.")
    print(f"Total stored jobs: {len(new_df):,}")
    print(f"Saved to: {RAW_FILE}")

    return new_df


def load_dataset():
    """
    Always refresh the dataset when the pipeline runs.
    """

    return download_dataset()


if __name__ == "__main__":

    data = download_dataset()

    print("\nColumns:")

    for column in data.columns:
        print(f"- {column}")

    print("\nPreview:")
    print(data.head())
