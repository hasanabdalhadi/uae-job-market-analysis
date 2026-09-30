"""
HJMI — Hasan Job Market Intelligence
UAE Job Market Data Preparation Pipeline

This script:
1. Downloads/loads the ArabJobs dataset
2. Normalizes column names
3. Filters United Arab Emirates records
4. Identifies technology-related jobs
5. Cleans text fields
6. Extracts selected technology skills
7. Creates a dashboard-ready CSV file

Developer:
Hasan R. H. Abdalhadi
"""

from pathlib import Path
import re
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

DATA_URL = (
    "https://huggingface.co/datasets/drelhaj/"
    "ArabJobs/resolve/main/ArabJobs.csv"
)

DATA_DIR = Path("data")

RAW_FILE = DATA_DIR / "arab_jobs_raw.csv"
CLEAN_FILE = DATA_DIR / "uae_tech_jobs_clean.csv"


# ============================================================
# TECHNOLOGY KEYWORDS
# ============================================================

TECH_KEYWORDS = [
    "software",
    "developer",
    "programmer",
    "engineer",
    "data",
    "analyst",
    "analytics",
    "information technology",
    "information systems",
    "computer",
    "network",
    "cyber",
    "security",
    "cloud",
    "database",
    "web",
    "frontend",
    "front-end",
    "backend",
    "back-end",
    "full stack",
    "full-stack",
    "mobile",
    "android",
    "ios",
    "machine learning",
    "artificial intelligence",
    "ai ",
    "it ",
    "technical support",
    "system administrator",
    "systems administrator",
    "devops",
    "qa ",
    "quality assurance",
    "ui",
    "ux",
]


# ============================================================
# SKILLS TO IDENTIFY
# ============================================================

SKILL_PATTERNS = {
    "Python": r"\bpython\b",
    "Java": r"\bjava\b",
    "JavaScript": r"\bjavascript\b|\bjs\b",
    "C++": r"\bc\+\+\b",
    "C#": r"\bc#\b|c sharp",
    "PHP": r"\bphp\b",
    "SQL": r"\bsql\b",
    "MySQL": r"\bmysql\b",
    "HTML": r"\bhtml\b",
    "CSS": r"\bcss\b",
    "React": r"\breact(?:\.js|js)?\b",
    "Angular": r"\bangular\b",
    "Node.js": r"\bnode(?:\.js|js)\b",
    "AWS": r"\baws\b|amazon web services",
    "Azure": r"\bazure\b",
    "Docker": r"\bdocker\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "Git": r"\bgit\b|\bgithub\b",
    "Linux": r"\blinux\b",
    "Power BI": r"\bpower\s*bi\b",
    "Tableau": r"\btableau\b",
    "Excel": r"\bexcel\b",
    "Machine Learning": r"\bmachine learning\b",
    "Artificial Intelligence": (
        r"\bartificial intelligence\b|\bai\b"
    ),
    "Data Analysis": r"\bdata analysis\b|\bdata analytics\b",
    "Cybersecurity": (
        r"\bcybersecurity\b|\bcyber security\b"
    ),
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_column_name(column):
    """Convert a column name to a simple snake_case format."""

    column = str(column).strip().lower()
    column = re.sub(r"[^a-z0-9]+", "_", column)

    return column.strip("_")


def clean_text(value):
    """Clean unnecessary spaces and line breaks."""

    if pd.isna(value):
        return ""

    value = str(value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def find_column(columns, candidates):
    """Find the first matching column from possible names."""

    normalized = list(columns)

    for candidate in candidates:
        if candidate in normalized:
            return candidate

    for column in normalized:
        for candidate in candidates:
            if candidate in column:
                return column

    return None


def contains_tech_keyword(text):
    """Return True if the text appears technology-related."""

    text = str(text).lower()

    return any(keyword in text for keyword in TECH_KEYWORDS)


def extract_skills(text):
    """Extract known technology skills from job text."""

    text = str(text).lower()

    detected = []

    for skill, pattern in SKILL_PATTERNS.items():

        if re.search(pattern, text, flags=re.IGNORECASE):
            detected.append(skill)

    return detected


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_FILE.exists():

        print("Loading existing raw dataset...")

        return pd.read_csv(
            RAW_FILE,
            low_memory=False,
        )

    print("Downloading ArabJobs dataset...")

    df = pd.read_csv(
        DATA_URL,
        low_memory=False,
    )

    df.to_csv(
        RAW_FILE,
        index=False,
    )

    print("Raw dataset saved.")

    return df


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data():

    print("\n======================================")
    print(" HJMI DATA PREPARATION")
    print("======================================\n")

    df = load_data()

    print(f"Original records: {len(df):,}")

    # --------------------------------------------------------
    # Normalize column names
    # --------------------------------------------------------

    df.columns = [
        clean_column_name(column)
        for column in df.columns
    ]

    print("\nAvailable columns:")

    for column in df.columns:
        print(f" - {column}")

    # --------------------------------------------------------
    # Identify important columns
    # --------------------------------------------------------

    country_col = find_column(
        df.columns,
        [
            "country",
            "country_name",
        ],
    )

    title_col = find_column(
        df.columns,
        [
            "job_title",
            "title",
            "position",
        ],
    )

    location_col = find_column(
        df.columns,
        [
            "location",
            "city",
            "job_location",
        ],
    )

    description_col = find_column(
        df.columns,
        [
            "job_description",
            "description",
            "details",
        ],
    )

    company_col = find_column(
        df.columns,
        [
            "company",
            "company_name",
            "employer",
        ],
    )

    salary_col = find_column(
        df.columns,
        [
            "salary",
            "salary_range",
        ],
    )

    category_col = find_column(
        df.columns,
        [
            "category",
            "job_category",
            "classification",
        ],
    )

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    if country_col is None:
        raise ValueError(
            "Country column could not be identified."
        )

    if title_col is None:
        raise ValueError(
            "Job title column could not be identified."
        )

    # --------------------------------------------------------
    # Clean text columns
    # --------------------------------------------------------

    text_columns = [
        title_col,
        location_col,
        description_col,
        company_col,
        salary_col,
        category_col,
    ]

    for column in text_columns:

        if column and column in df.columns:
            df[column] = df[column].apply(clean_text)

    # --------------------------------------------------------
    # Filter UAE
    # --------------------------------------------------------

    country_values = (
        df[country_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    uae_mask = country_values.str.contains(
        r"united arab emirates|\buae\b|الإمارات",
        regex=True,
        na=False,
    )

    uae_df = df[uae_mask].copy()

    print(
        f"\nUAE records identified: "
        f"{len(uae_df):,}"
    )

    # --------------------------------------------------------
    # Build searchable text
    # --------------------------------------------------------

    searchable_columns = [
        column
        for column in [
            title_col,
            description_col,
            category_col,
        ]
        if column and column in uae_df.columns
    ]

    uae_df["_search_text"] = (
        uae_df[searchable_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )

    # --------------------------------------------------------
    # Identify technology jobs
    # --------------------------------------------------------

    tech_mask = uae_df["_search_text"].apply(
        contains_tech_keyword
    )

    tech_df = uae_df[tech_mask].copy()

    print(
        f"Technology-related UAE records: "
        f"{len(tech_df):,}"
    )

    # --------------------------------------------------------
    # Extract technology skills
    # --------------------------------------------------------

    tech_df["detected_skills"] = (
        tech_df["_search_text"]
        .apply(extract_skills)
    )

    tech_df["skills"] = tech_df[
        "detected_skills"
    ].apply(
        lambda skills: ", ".join(skills)
    )

    tech_df["skill_count"] = tech_df[
        "detected_skills"
    ].apply(len)

    # --------------------------------------------------------
    # Create clean standardized output
    # --------------------------------------------------------

    output = pd.DataFrame()

    output["job_title"] = tech_df[
        title_col
    ]

    if company_col:
        output["company"] = tech_df[
            company_col
        ]
    else:
        output["company"] = ""

    if location_col:
        output["location"] = tech_df[
            location_col
        ]
    else:
        output["location"] = ""

    if category_col:
        output["category"] = tech_df[
            category_col
        ]
    else:
        output["category"] = ""

    if salary_col:
        output["salary"] = tech_df[
            salary_col
        ]
    else:
        output["salary"] = ""

    if description_col:
        output["description"] = tech_df[
            description_col
        ]
    else:
        output["description"] = ""

    output["skills"] = tech_df["skills"]
    output["skill_count"] = tech_df[
        "skill_count"
    ]

    # --------------------------------------------------------
    # Remove empty titles and duplicates
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

    duplicate_columns = [
        "job_title",
        "company",
        "location",
    ]

    output = output.drop_duplicates(
        subset=duplicate_columns,
    )

    output = output.reset_index(drop=True)

    # --------------------------------------------------------
    # Save clean dataset
    # --------------------------------------------------------

    output.to_csv(
        CLEAN_FILE,
        index=False,
    )

    print("\n======================================")
    print(" DATA PREPARATION COMPLETE")
    print("======================================")

    print(
        f"\nClean UAE technology jobs: "
        f"{len(output):,}"
    )

    print(
        f"Unique job titles: "
        f"{output['job_title'].nunique():,}"
    )

    print(
        f"Locations represented: "
        f"{output['location'].nunique():,}"
    )

    skills_found = set()

    for skills in output["skills"]:

        if skills:
            skills_found.update(
                skill.strip()
                for skill in skills.split(",")
                if skill.strip()
            )

    print(
        f"Technology skills identified: "
        f"{len(skills_found):,}"
    )

    print(
        f"\nClean dataset saved to:\n"
        f"{CLEAN_FILE}"
    )

    print("\nPreview:\n")

    print(
        output[
            [
                "job_title",
                "company",
                "location",
                "skills",
            ]
        ].head(10)
    )

    return output


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    prepare_data()
