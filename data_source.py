"""
UAE Job Market Data Analysis
Data Source Loader

Source:
ArabJobs Dataset
https://huggingface.co/datasets/drelhaj/ArabJobs

This module downloads the public dataset and makes it available
for the UAE job market analysis project.
"""

from pathlib import Path
import pandas as pd

DATA_URL = (
    "https://huggingface.co/datasets/drelhaj/"
    "ArabJobs/resolve/main/ArabJobs.csv"
)

DATA_DIR = Path("data")
RAW_FILE = DATA_DIR / "arab_jobs_raw.csv"


def download_dataset():
    """Download the ArabJobs dataset and save a local copy."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading ArabJobs dataset...")

    df = pd.read_csv(DATA_URL)

    df.to_csv(RAW_FILE, index=False)

    print("Dataset downloaded successfully.")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Saved to: {RAW_FILE}")

    return df


def load_dataset():
    """Load the dataset from disk or download it if necessary."""

    if RAW_FILE.exists():
        print("Loading local dataset...")
        return pd.read_csv(RAW_FILE)

    return download_dataset()


if __name__ == "__main__":
    data = load_dataset()

    print("\nAvailable columns:")
    for column in data.columns:
        print(f"- {column}")

    print("\nDataset preview:")
    print(data.head())
