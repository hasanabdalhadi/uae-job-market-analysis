# ============================================================
# HJMI — CV INTELLIGENCE SERVICE
# PDF Reading • Career Information • Skill Extraction
# ============================================================

import io
import re

from pypdf import PdfReader


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(value):

    return re.sub(
        r"\s+",
        " ",
        str(value or ""),
    ).strip()


def normalize_value(value):

    return clean_text(value).lower()


def unique_values(values):

    result = []
    seen = set()

    for value in values:

        value = clean_text(value)

        if not value:
            continue

        key = value.lower()

        if key in seen:
            continue

        seen.add(key)
        result.append(value)

    return result


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    if uploaded_file is None:

        return {
            "success": False,
            "message": "No CV file was provided.",
            "text": "",
            "pages": 0,
        }

    try:

        file_bytes = uploaded_file.getvalue()

        reader = PdfReader(
            io.BytesIO(file_bytes)
        )

        pages = []

        for page in reader.pages:

            try:

                page_text = (
                    page.extract_text()
                    or ""
                )

            except Exception:

                page_text = ""

            if page_text.strip():

                pages.append(
                    page_text.strip()
                )

        text = "\n\n".join(
            pages
        ).strip()

        if not text:

            return {
                "success": False,
                "message": (
                    "HJMI could not detect readable text in this PDF. "
                    "The CV may be scanned or image-based."
                ),
                "text": "",
                "pages": len(
                    reader.pages
                ),
            }

        return {
            "success": True,
            "message": (
                "CV text extracted successfully."
            ),
            "text": text,
            "pages": len(
                reader.pages
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                f"HJMI could not read this CV: {str(error)}"
            ),
            "text": "",
            "pages": 0,
        }


# ============================================================
# SKILL CATALOG
# ============================================================

SKILL_CATALOG = [

    # Programming
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C",
    "C++",
    "C#",
    "PHP",
    "Ruby",
    "Go",
    "Rust",
    "Swift",
    "Kotlin",
    "Dart",
    "R",
    "MATLAB",
    "Scala",
    "Shell",
    "Bash",
    "PowerShell",

    # Web
    "HTML",
    "CSS",
    "React",
    "React.js",
    "Next.js",
    "Vue",
    "Vue.js",
    "Angular",
    "Node.js",
    "Express",
    "Django",
    "Flask",
    "FastAPI",
    "Laravel",
    "Spring",
    "Spring Boot",
    "ASP.NET",
    ".NET",
    "Bootstrap",
    "Tailwind CSS",
    "REST API",
    "REST APIs",
    "GraphQL",

    # Databases
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Oracle",
    "Microsoft SQL Server",
    "Redis",
    "Firebase",
    "Supabase",
    "NoSQL",

    # Data
    "Data Analysis",
    "Data Analytics",
    "Data Science",
    "Data Engineering",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "AI",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Plotly",
    "Power BI",
    "Tableau",
    "Excel",
    "Google Sheets",
    "ETL",
    "Data Visualization",
    "Statistics",

    # Cloud / DevOps
    "AWS",
    "Azure",
    "Google Cloud",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "GitLab",
    "CI/CD",
    "Jenkins",
    "Terraform",
    "Linux",
    "Unix",

    # Cybersecurity / Networks
    "Cybersecurity",
    "Network Security",
    "Information Security",
    "Penetration Testing",
    "Ethical Hacking",
    "Firewall",
    "VPN",
    "TCP/IP",
    "DNS",
    "Networking",
    "Cisco",

    # Software / CS
    "Data Structures",
    "Algorithms",
    "Object-Oriented Programming",
    "OOP",
    "DBMS",
    "Software Engineering",
    "Software Development",
    "System Design",
    "Operating Systems",
    "Computer Networks",
    "API Development",
    "Microservices",
    "Agile",
    "Scrum",

    # Design / Product
    "UI/UX",
    "UI Design",
    "UX Design",
    "Figma",
    "Adobe XD",
    "Canva",
    "Photoshop",

    # Business / Systems
    "Information Systems",
    "Business Analysis",
    "Project Management",
    "CRM",
    "ERP",
    "Zoho",
    "Salesforce",
    "SAP",
    "Microsoft Office",
    "Word",
    "PowerPoint",

    # General technical
    "Troubleshooting",
    "Technical Support",
    "IT Support",
    "Data Management",
    "Database Management",
    "Web Development",
    "Front-End Development",
    "Frontend Development",
    "Back-End Development",
    "Backend Development",
    "Full Stack Development",
]


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "js": "JavaScript",
    "javascript": "JavaScript",

    "ts": "TypeScript",
    "typescript": "TypeScript",

    "reactjs": "React",
    "react.js": "React",

    "nodejs": "Node.js",
    "node.js": "Node.js",

    "vuejs": "Vue.js",

    "postgres": "PostgreSQL",

    "powerbi": "Power BI",

    "amazon web services": "AWS",

    "microsoft azure": "Azure",

    "google cloud platform": "GCP",

    "machine learning": "Machine Learning",

    "artificial intelligence": "Artificial Intelligence",

    "object oriented programming": (
        "Object-Oriented Programming"
    ),

    "object-oriented programming": (
        "Object-Oriented Programming"
    ),

    "user interface": "UI Design",

    "user experience": "UX Design",

    "front end": "Front-End Development",

    "frontend": "Frontend Development",

    "back end": "Back-End Development",

    "backend": "Backend Development",

    "full stack": "Full Stack Development",

    "full-stack": "Full Stack Development",
}


# ============================================================
# SKILL DETECTION
# ============================================================

def contains_skill(
    text,
    skill,
):

    normalized_text = (
        normalize_value(text)
    )

    normalized_skill = (
        normalize_value(skill)
    )

    if not normalized_skill:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(
            normalized_skill
        )
        + r"(?![a-z0-9])"
    )

    return bool(
        re.search(
            pattern,
            normalized_text,
        )
    )


def extract_skills(text):

    if not text:
        return []

    detected = []

    for skill in SKILL_CATALOG:

        if contains_skill(
            text,
            skill,
        ):

            detected.append(
                skill
            )

    normalized_text = (
        normalize_value(text)
    )

    for alias, canonical in (
        SKILL_ALIASES.items()
    ):

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(alias)
            + r"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            normalized_text,
        ):

            detected.append(
                canonical
            )

    return unique_values(
        detected
    )


# ============================================================
# EMAIL DETECTION
# ============================================================

def extract_email(text):

    if not text:
        return ""

    match = re.search(
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}\b",
        text,
    )

    if match:
        return match.group(0)

    return ""


# ============================================================
# PHONE DETECTION
# ============================================================

def extract_phone(text):

    if not text:
        return ""

    candidates = re.findall(
        r"(?:\+?\d[\d\s().-]{7,}\d)",
        text,
    )

    for candidate in candidates:

        digits = re.sub(
            r"\D",
            "",
            candidate,
        )

        if 8 <= len(digits) <= 15:

            return clean_text(
                candidate
            )

    return ""


# ============================================================
# LINKEDIN DETECTION
# ============================================================

def extract_linkedin(text):

    if not text:
        return ""

    match = re.search(
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"linkedin\.com/"
        r"[A-Za-z0-9_?=/.-]+",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(0)

    return ""


# ============================================================
# GITHUB DETECTION
# ============================================================

def extract_github(text):

    if not text:
        return ""

    match = re.search(
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"github\.com/"
        r"[A-Za-z0-9_.-]+",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(0)

    return ""


# ============================================================
# EDUCATION KEYWORDS
# ============================================================

EDUCATION_KEYWORDS = [
    "computer science",
    "software engineering",
    "information technology",
    "information systems",
    "data science",
    "cybersecurity",
    "computer engineering",
    "artificial intelligence",
    "business information systems",
]


def detect_specialization(text):

    normalized_text = (
        normalize_value(text)
    )

    for field in (
        EDUCATION_KEYWORDS
    ):

        if field in normalized_text:

            return field.title()

    return ""


# ============================================================
# EXPERIENCE SIGNALS
# ============================================================

def detect_experience_level(text):

    if not text:
        return "Not Specified"

    normalized_text = (
        normalize_value(text)
    )

    patterns = [
        (
            r"\b(?:5|6|7|8|9|10)\+?\s*years?\b",
            "5+ Years",
        ),
        (
            r"\b(?:3|4)\+?\s*years?\b",
            "3–5 Years",
        ),
        (
            r"\b2\+?\s*years?\b",
            "2–3 Years",
        ),
        (
            r"\b1\+?\s*years?\b",
            "1–2 Years",
        ),
    ]

    for pattern, level in patterns:

        if re.search(
            pattern,
            normalized_text,
        ):

            return level

    graduate_terms = [
        "fresh graduate",
        "recent graduate",
        "student",
        "internship",
        "intern",
    ]

    if any(
        term in normalized_text
        for term in graduate_terms
    ):

        return (
            "Fresh Graduate / Entry Level"
        )

    return "Not Specified"


# ============================================================
# TARGET ROLE SIGNALS
# ============================================================

ROLE_KEYWORDS = [
    "Software Engineer",
    "Software Developer",
    "Web Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Analyst",
    "Data Scientist",
    "Data Engineer",
    "Business Analyst",
    "Cybersecurity Analyst",
    "Security Analyst",
    "Network Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
    "IT Support",
    "Technical Support",
    "Database Administrator",
    "Systems Analyst",
    "Machine Learning Engineer",
    "AI Engineer",
    "Project Coordinator",
]


def extract_role_signals(text):

    if not text:
        return []

    roles = []

    for role in ROLE_KEYWORDS:

        if contains_skill(
            text,
            role,
        ):

            roles.append(
                role
            )

    return unique_values(
        roles
    )


# ============================================================
# CV ANALYSIS
# ============================================================

def analyze_cv(uploaded_file):

    extraction = extract_pdf_text(
        uploaded_file
    )

    if not extraction["success"]:

        return {
            "success": False,
            "message": extraction[
                "message"
            ],
            "pages": extraction[
                "pages"
            ],
            "text": "",
            "skills": [],
            "specialization": "",
            "experience_level": (
                "Not Specified"
            ),
            "target_roles": [],
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": "",
        }

    text = extraction["text"]

    skills = extract_skills(
        text
    )

    specialization = (
        detect_specialization(
            text
        )
    )

    experience_level = (
        detect_experience_level(
            text
        )
    )

    target_roles = (
        extract_role_signals(
            text
        )
    )

    return {
        "success": True,
        "message": (
            "HJMI successfully analyzed the CV."
        ),
        "pages": extraction[
            "pages"
        ],
        "text": text,
        "skills": skills,
        "specialization": specialization,
        "experience_level": (
            experience_level
        ),
        "target_roles": (
            target_roles
        ),
        "email": extract_email(
            text
        ),
        "phone": extract_phone(
            text
        ),
        "linkedin": extract_linkedin(
            text
        ),
        "github": extract_github(
            text
        ),
    }
