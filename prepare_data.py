"""
HJMI — Hasan Job Market Intelligence
UAE Technology Job Market Data Preparation Pipeline

This pipeline:
1. Fetches current UAE job listings
2. Cleans and normalizes the data
3. Filters technology-related roles
4. Extracts technical skills
5. Preserves salary information when available
6. Removes duplicates
7. Creates the dashboard-ready dataset

Developer:
Hasan R. H. Abdalhadi
"""

from pathlib import Path
import html
import re

import pandas as pd

from data_source import load_dataset


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data")
CLEAN_FILE = DATA_DIR / "uae_tech_jobs_clean.csv"


# ============================================================
# TECHNOLOGY KEYWORDS
# ============================================================

TECH_KEYWORDS = [
    "software",
    "developer",
    "programmer",
    "computer",
    "information technology",
    "information systems",
    "data",
    "analytics",
    "data scientist",
    "data engineer",
    "data analyst",
    "machine learning",
    "artificial intelligence",
    " ai ",
    "cybersecurity",
    "cyber security",
    "network",
    "networking",
    "cloud",
    "database",
    "web developer",
    "frontend",
    "front-end",
    "backend",
    "back-end",
    "full stack",
    "full-stack",
    "mobile developer",
    "android",
    "ios developer",
    "devops",
    "site reliability",
    "sre",
    "technical support",
    "it support",
    "system administrator",
    "systems administrator",
    "systems engineer",
    "software engineer",
    "cloud engineer",
    "security engineer",
    "network engineer",
    "qa engineer",
    "quality assurance",
    "ui developer",
    "ux designer",
    "solutions architect",
    "cloud architect",
    "database administrator",
    "business intelligence",
    "bi developer",
]


# ============================================================
# SKILLS
# ============================================================

SKILL_PATTERNS = {
    "Python": r"\bpython\b",
    "Java": r"\bjava\b",
    "JavaScript": r"\bjavascript\b|\bjs\b",
    "TypeScript": r"\btypescript\b",
    "C": r"(?<!\+)\bc\b(?!\+)",
    "C++": r"\bc\+\+\b",
    "C#": r"\bc#\b|c sharp",
    "PHP": r"\bphp\b",
    "Ruby": r"\bruby\b",
    "Go": r"\bgolang\b|\bgo language\b",
    "Kotlin": r"\bkotlin\b",
    "Swift": r"\bswift\b",
    "SQL": r"\bsql\b",
    "MySQL": r"\bmysql\b",
    "PostgreSQL": r"\bpostgresql\b|\bpostgres\b",
    "MongoDB": r"\bmongodb\b",
    "Oracle": r"\boracle\b",
    "HTML": r"\bhtml\b",
    "CSS": r"\bcss\b",
    "React": r"\breact(?:\.js|js)?\b",
    "Angular": r"\bangular\b",
    "Vue.js": r"\bvue(?:\.js|js)?\b",
    "Node.js": r"\bnode(?:\.js|js)\b",
    "Django": r"\bdjango\b",
    "Flask": r"\bflask\b",
    "Spring": r"\bspring boot\b|\bspring framework\b",
    "AWS": r"\baws\b|amazon web services",
    "Azure": r"\bazure\b",
    "Google Cloud": r"\bgcp\b|google cloud",
    "Docker": r"\bdocker\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "Git": r"\bgit\b|\bgithub\b|\bgitlab\b",
    "Linux": r"\blinux\b",
    "Power BI": r"\bpower\s*bi\b",
    "Tableau": r"\btableau\b",
    "Excel": r"\bexcel\b",
    "Machine Learning": r"\bmachine learning\b",
    "Artificial Intelligence": (
        r"\bartificial intelligence\b|\bai\b"
    ),
    "Data Analysis": (
        r"\bdata analysis\b|\bdata analytics\b"
    ),
    "Data Science": r"\bdata science\b",
    "Cybersecurity": (
        r"\bcybersecurity\b|\bcyber security\b"
    ),
    "DevOps": r"\bdevops\b",
    "REST API": r"\brest api\b|\brestful\b",
    "GraphQL": r"\bgraphql\b",
    "TensorFlow": r"\btensorflow\b",
    "PyTorch": r"\bpytorch\b",
    "Spark": r"\bapache spark\b|\bspark\b",
    "Hadoop": r"\bhadoop\b",
}


# ============================================================
# UAE LOCATIONS
# ============================================================

UAE_KEYWORDS = [
    "united arab emirates",
    "uae",
    "dubai",
    "abu dhabi",
    "sharjah",
    "ajman",
    "fujairah",
    "ras al khaimah",
    "ras al-khaimah",
    "umm al quwain",
    "umm al-quwain",
    "al ain",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value):
    """Clean HTML, line breaks and unnecessary spaces."""

    if pd.isna(value):
        return ""

    value = str(value)

    value = html.unescape(value)

    value = re.sub(
        r"<[^>]+>",
        " ",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


def is_uae_job(location):
    """Check whether a location represents the UAE."""

    text = clean_text(location).lower()

    return any(
        keyword in text
        for keyword in UAE_KEYWORDS
    )


def contains_tech_keyword(text):
    """Check whether job information is technology related."""

    text = clean_text(text).lower()

    return any(
        keyword in text
        for keyword in TECH_KEYWORDS
    )


def extract_skills(text):
    """Extract known technology skills from job information."""

    text = clean_text(text)

    detected = []

    for skill, pattern in SKILL_PATTERNS.items():

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            detected.append(skill)

    return detected


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data():

    print()
    print("======================================")
    print(" HJMI DATA PREPARATION")
    print("======================================")
    print()

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Fetch live/current source data
    # --------------------------------------------------------

    df = load_dataset()

    if df.empty:
        raise RuntimeError(
            "The job data source returned no records."
        )

    print(
        f"Source records available: {len(df):,}"
    )

    # --------------------------------------------------------
    # Make sure required columns exist
    # --------------------------------------------------------

    required_columns = [
        "job_title",
        "company",
        "location",
        "category",
        "description",
    ]

    for column in required_columns:

        if column not in df.columns:
            df[column] = ""

    optional_columns = [
        "source_id",
        "salary",
        "publication_date",
        "job_url",
        "source",
        "fetched_at",
    ]

    for column in optional_columns:

        if column not in df.columns:
            df[column] = ""

    # --------------------------------------------------------
    # Clean text
    # --------------------------------------------------------

    text_columns = [
        "job_title",
        "company",
        "location",
        "category",
        "description",
        "salary",
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .fillna("")
            .apply(clean_text)
        )

    # --------------------------------------------------------
    # UAE validation
    # --------------------------------------------------------

    uae_mask = df["location"].apply(
        is_uae_job
    )

    uae_df = df[uae_mask].copy()

    print(
        f"UAE records identified: {len(uae_df):,}"
    )

    if uae_df.empty:
        raise RuntimeError(
            "No UAE job records were identified."
        )

    # --------------------------------------------------------
    # Searchable job information
    # --------------------------------------------------------

    uae_df["_search_text"] = (
        uae_df[
            [
                "job_title",
                "category",
                "description",
            ]
        ]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    # --------------------------------------------------------
    # Technology filtering
    # --------------------------------------------------------

    tech_mask = uae_df["_search_text"].apply(
        contains_tech_keyword
    )

    tech_df = uae_df[tech_mask].copy()

    print(
        "Technology-related UAE records: "
        f"{len(tech_df):,}"
    )

    if tech_df.empty:
        raise RuntimeError(
            "No UAE technology jobs were identified."
        )

    # --------------------------------------------------------
    # Skill extraction
    # --------------------------------------------------------

    tech_df["detected_skills"] = (
        tech_df["_search_text"]
        .apply(extract_skills)
    )

    tech_df["skills"] = (
        tech_df["detected_skills"]
        .apply(
            lambda skills:
            ", ".join(skills)
        )
    )

    tech_df["skill_count"] = (
        tech_df["detected_skills"]
        .apply(len)
    )

    # --------------------------------------------------------
    # Build clean dashboard dataset
    # --------------------------------------------------------

    output_columns = [
        "source_id",
        "job_title",
        "company",
        "location",
        "category",
        "description",
        "skills",
        "skill_count",
        "salary",
        "publication_date",
        "job_url",
        "source",
        "fetched_at",
    ]

    output = tech_df[
        output_columns
    ].copy()

    # --------------------------------------------------------
    # Remove empty job titles
    # --------------------------------------------------------

    output["job_title"] = (
        output["job_title"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    output = output[
        output["job_title"] != ""
    ]

    if output.empty:
        raise RuntimeError(
            "No usable technology job records remained "
            "after data preparation."
        )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    has_source_ids = (
        "source_id" in output.columns
        and output["source_id"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        .any()
    )

    if has_source_ids:

        with_id = output[
            output["source_id"]
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
        ].drop_duplicates(
            subset=["source_id"],
            keep="last",
        )

        without_id = output[
            output["source_id"]
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

        output = pd.concat(
            [with_id, without_id],
            ignore_index=True,
        )

    else:

        output = output.drop_duplicates(
            subset=[
                "job_title",
                "company",
                "location",
            ],
            keep="last",
        )

    # --------------------------------------------------------
    # Sort newest jobs first
    # --------------------------------------------------------

    if "publication_date" in output.columns:

        output["_sort_date"] = pd.to_datetime(
            output["publication_date"],
            errors="coerce",
            utc=True,
        )

        output = output.sort_values(
            "_sort_date",
            ascending=False,
            na_position="last",
        )

        output = output.drop(
            columns=["_sort_date"]
        )

    output = output.reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Save dashboard dataset
    # --------------------------------------------------------

    output.to_csv(
        CLEAN_FILE,
        index=False,
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    unique_titles = (
        output["job_title"]
        .nunique()
    )

    unique_locations = (
        output["location"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )

    skills_found = set()

    for skills in output["skills"].fillna(""):

        for skill in str(skills).split(","):

            skill = skill.strip()

            if skill:
                skills_found.add(skill)

    salary_records = (
        output["salary"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )

    print()
    print("======================================")
    print(" HJMI DATA PREPARATION COMPLETE")
    print("======================================")
    print()

    print(
        f"UAE technology jobs: {len(output):,}"
    )

    print(
        f"Unique job titles: {unique_titles:,}"
    )

    print(
        f"Locations represented: "
        f"{unique_locations:,}"
    )

    print(
        f"Technology skills identified: "
        f"{len(skills_found):,}"
    )

    print(
        f"Jobs with salary information: "
        f"{salary_records:,}"
    )

    print()
    print(
        f"Dashboard dataset saved to: "
        f"{CLEAN_FILE}"
    )

    print()
    print("Preview:")
    print()

    preview_columns = [
        "job_title",
        "company",
        "location",
        "skills",
        "salary",
    ]

    print(
        output[
            preview_columns
        ]
        .head(10)
        .to_string(index=False)
    )

    return output


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    prepare_data()
