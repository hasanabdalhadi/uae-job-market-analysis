# ============================================================
# HJMI — CAREER MATCH ENGINE
# Profile-to-Job Matching Intelligence
# ============================================================

import re

import pandas as pd

from services.data_service import parse_skills


# ============================================================
# MATCHING CONFIGURATION
# ============================================================

MIN_SKILL_MATCHES = 2


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    return re.sub(
        r"\s+",
        " ",
        str(value),
    ).strip()


def normalize_text(value):

    value = clean_text(value).lower()

    value = value.replace(
        "&",
        " and ",
    )

    value = re.sub(
        r"[^a-z0-9+#./ -]",
        " ",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


def normalize_skill(value):

    value = normalize_text(value)

    aliases = {
        "js": "javascript",
        "react.js": "react",
        "reactjs": "react",
        "node.js": "nodejs",
        "node js": "nodejs",
        "vue.js": "vue",
        "vuejs": "vue",
        "postgres": "postgresql",
        "powerbi": "power bi",
        "amazon web services": "aws",
        "google cloud platform": "gcp",
        "object oriented programming": "oop",
        "object-oriented programming": "oop",
        "front end development": "frontend development",
        "back end development": "backend development",
        "full-stack development": "full stack development",
    }

    return aliases.get(
        value,
        value,
    )


def unique_values(values):

    result = []
    seen = set()

    for value in values or []:

        value = clean_text(value)

        if not value:
            continue

        key = normalize_text(value)

        if not key:
            continue

        if key in seen:
            continue

        seen.add(key)
        result.append(value)

    return result


# ============================================================
# PROFILE HELPERS
# ============================================================

def get_profile_skills(profile):

    return unique_values(
        profile.get(
            "skills",
            [],
        )
        or []
    )


def get_profile_roles(profile):

    return unique_values(
        profile.get(
            "target_roles",
            [],
        )
        or []
    )


def get_profile_locations(profile):

    return unique_values(
        profile.get(
            "preferred_locations",
            [],
        )
        or []
    )


# ============================================================
# JOB HELPERS
# ============================================================

def get_job_text(job):

    fields = [
        job.get("job_title", ""),
        job.get("category", ""),
        job.get("description", ""),
        job.get("skills", ""),
    ]

    return normalize_text(
        " ".join(
            clean_text(value)
            for value in fields
        )
    )


def get_job_skills(job):

    raw_skills = job.get(
        "skills",
        "",
    )

    try:
        parsed = parse_skills(
            raw_skills
        )

    except Exception:
        parsed = []

    return unique_values(
        parsed
    )


# ============================================================
# SKILL MATCHING
# ============================================================

def match_skills(
    profile_skills,
    job_skills,
    job_text,
):

    matched = []
    missing = []

    normalized_job_skills = {
        normalize_skill(skill)
        for skill in job_skills
        if normalize_skill(skill)
    }

    for skill in profile_skills:

        normalized = normalize_skill(
            skill
        )

        if not normalized:
            continue

        direct_match = (
            normalized
            in normalized_job_skills
        )

        text_match = False

        if not direct_match:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalized)
                + r"(?![a-z0-9])"
            )

            text_match = bool(
                re.search(
                    pattern,
                    job_text,
                )
            )

        if direct_match or text_match:
            matched.append(skill)

        else:
            missing.append(skill)

    return (
        unique_values(matched),
        unique_values(missing),
    )


# ============================================================
# TARGET ROLE MATCHING
# ============================================================

def match_target_roles(
    profile_roles,
    job_title,
):

    title = normalize_text(
        job_title
    )

    matched_roles = []

    for role in profile_roles:

        normalized_role = normalize_text(
            role
        )

        if not normalized_role:
            continue

        if (
            normalized_role in title
            or title in normalized_role
        ):

            matched_roles.append(
                role
            )

            continue

        role_words = {
            word
            for word in normalized_role.split()
            if len(word) >= 3
        }

        title_words = {
            word
            for word in title.split()
            if len(word) >= 3
        }

        shared_words = (
            role_words
            & title_words
        )

        if (
            role_words
            and len(shared_words)
            >= min(
                2,
                len(role_words),
            )
        ):

            matched_roles.append(
                role
            )

    return unique_values(
        matched_roles
    )


# ============================================================
# SPECIALIZATION MATCHING
# ============================================================

def match_specialization(
    specialization,
    job_text,
):

    specialization = normalize_text(
        specialization
    )

    if not specialization:
        return False

    if specialization in job_text:
        return True

    specialization_terms = {
        word
        for word in specialization.split()
        if len(word) >= 4
    }

    if not specialization_terms:
        return False

    matches = sum(
        1
        for term in specialization_terms
        if re.search(
            r"(?<![a-z0-9])"
            + re.escape(term)
            + r"(?![a-z0-9])",
            job_text,
        )
    )

    return (
        matches
        >= min(
            2,
            len(specialization_terms),
        )
    )


# ============================================================
# LOCATION MATCHING
# ============================================================

def match_locations(
    preferred_locations,
    job_location,
):

    job_location_normalized = normalize_text(
        job_location
    )

    matched = []

    for location in preferred_locations:

        normalized_location = normalize_text(
            location
        )

        if not normalized_location:
            continue

        if normalized_location == "remote":

            if "remote" in job_location_normalized:
                matched.append(
                    location
                )

            continue

        if (
            normalized_location
            in job_location_normalized
            or job_location_normalized
            in normalized_location
        ):

            matched.append(
                location
            )

    return unique_values(
        matched
    )


# ============================================================
# EXPERIENCE MATCHING
# ============================================================

EXPERIENCE_ORDER = {
    "Fresh Graduate / Entry Level": 0,
    "0–1 Year": 1,
    "1–2 Years": 2,
    "2–3 Years": 3,
    "3–5 Years": 4,
    "5+ Years": 5,
}


def match_experience(
    profile_experience,
    job_experience,
):

    profile_experience = clean_text(
        profile_experience
    )

    job_experience = clean_text(
        job_experience
    )

    if (
        not profile_experience
        or profile_experience
        == "Not Specified"
    ):

        return {
            "match": False,
            "known": False,
            "label": (
                "Profile experience not specified"
            ),
        }

    if (
        not job_experience
        or job_experience
        == "Not Specified"
    ):

        return {
            "match": False,
            "known": False,
            "label": (
                "Job experience not specified"
            ),
        }

    if profile_experience == job_experience:

        return {
            "match": True,
            "known": True,
            "label": (
                "Experience level aligned"
            ),
        }

    profile_rank = EXPERIENCE_ORDER.get(
        profile_experience
    )

    job_rank = EXPERIENCE_ORDER.get(
        job_experience
    )

    if (
        profile_rank is None
        or job_rank is None
    ):

        return {
            "match": False,
            "known": False,
            "label": (
                "Experience comparison unavailable"
            ),
        }

    if profile_rank >= job_rank:

        return {
            "match": True,
            "known": True,
            "label": (
                "Profile experience is at or above "
                "the listed experience signal"
            ),
        }

    return {
        "match": False,
        "known": True,
        "label": (
            "Listed experience is above profile level"
        ),
    }


# ============================================================
# MATCH SCORE
# ============================================================

def calculate_match_score(
    matched_skills_count,
    profile_skills_count,
    role_match,
    specialization_match,
    experience_match,
    location_match,
):

    score = 0.0

    # Skills — maximum 55 points
    if profile_skills_count > 0:

        skill_ratio = min(
            matched_skills_count
            / profile_skills_count,
            1.0,
        )

        score += (
            skill_ratio
            * 55
        )

    # Target role — 20 points
    if role_match:
        score += 20

    # Specialization — 10 points
    if specialization_match:
        score += 10

    # Experience — 10 points
    if experience_match:
        score += 10

    # Location — 5 points
    if location_match:
        score += 5

    return round(
        min(
            score,
            100,
        ),
        1,
    )


# ============================================================
# MATCH LABEL
# ============================================================

def get_match_label(
    score,
    matched_skills_count,
):

    if (
        score >= 70
        and matched_skills_count >= 2
    ):
        return "Strong Profile Match"

    if (
        score >= 45
        or matched_skills_count >= 3
    ):
        return "Good Profile Match"

    if matched_skills_count >= 2:
        return "Skill Match"

    return "Possible Match"


# ============================================================
# MATCH REASONS
# ============================================================

def build_match_reasons(
    matched_skills,
    matched_roles,
    specialization_match,
    experience_result,
    matched_locations,
):

    reasons = []

    if matched_skills:

        reasons.append(
            f"{len(matched_skills)} shared skill"
            + (
                "s"
                if len(matched_skills) != 1
                else ""
            )
        )

    if matched_roles:
        reasons.append(
            "target role overlap"
        )

    if specialization_match:
        reasons.append(
            "specialization overlap"
        )

    if experience_result.get(
        "match"
    ):
        reasons.append(
            "experience-level alignment"
        )

    if matched_locations:
        reasons.append(
            "preferred-location overlap"
        )

    return reasons


# ============================================================
# SINGLE JOB MATCH
# ============================================================

def match_job(
    profile,
    job,
):

    if isinstance(
        job,
        pd.Series,
    ):
        job = job.to_dict()

    profile_skills = get_profile_skills(
        profile
    )

    profile_roles = get_profile_roles(
        profile
    )

    preferred_locations = (
        get_profile_locations(
            profile
        )
    )

    specialization = (
        profile.get(
            "specialization",
            "",
        )
        or ""
    )

    profile_experience = (
        profile.get(
            "experience_level",
            "",
        )
        or ""
    )

    job_title = clean_text(
        job.get(
            "job_title",
            "",
        )
    )

    job_location = clean_text(
        job.get(
            "location",
            "",
        )
    )

    job_text = get_job_text(
        job
    )

    job_skills = get_job_skills(
        job
    )

    matched_skills, missing_skills = (
        match_skills(
            profile_skills,
            job_skills,
            job_text,
        )
    )

    matched_roles = match_target_roles(
        profile_roles,
        job_title,
    )

    specialization_match = (
        match_specialization(
            specialization,
            job_text,
        )
    )

    matched_locations = (
        match_locations(
            preferred_locations,
            job_location,
        )
    )

    # IMPORTANT:
    # data_service.py creates "experience_level"
    # for every prepared HJMI job.
    job_experience = clean_text(
        job.get(
            "experience_level",
            "",
        )
    )

    experience_result = (
        match_experience(
            profile_experience,
            job_experience,
        )
    )

    score = calculate_match_score(
        matched_skills_count=len(
            matched_skills
        ),
        profile_skills_count=len(
            profile_skills
        ),
        role_match=bool(
            matched_roles
        ),
        specialization_match=(
            specialization_match
        ),
        experience_match=(
            experience_result.get(
                "match",
                False,
            )
        ),
        location_match=bool(
            matched_locations
        ),
    )

    reasons = build_match_reasons(
        matched_skills=matched_skills,
        matched_roles=matched_roles,
        specialization_match=(
            specialization_match
        ),
        experience_result=(
            experience_result
        ),
        matched_locations=(
            matched_locations
        ),
    )

    # A job qualifies when:
    # 1. At least two profile skills match, OR
    # 2. A target role matches, OR
    # 3. Specialization matches + at least one skill matches.
    qualifies = (
        len(matched_skills)
        >= MIN_SKILL_MATCHES
        or bool(matched_roles)
        or (
            specialization_match
            and len(matched_skills) >= 1
        )
    )

    return {
        "qualifies": qualifies,
        "match_score": score,
        "match_label": get_match_label(
            score,
            len(matched_skills),
        ),
        "matched_skills": matched_skills,
        "missing_profile_skills": (
            missing_skills
        ),
        "matched_roles": matched_roles,
        "specialization_match": (
            specialization_match
        ),
        "matched_locations": (
            matched_locations
        ),
        "experience_match": (
            experience_result.get(
                "match",
                False,
            )
        ),
        "experience_known": (
            experience_result.get(
                "known",
                False,
            )
        ),
        "experience_label": (
            experience_result.get(
                "label",
                "",
            )
        ),
        "match_reasons": reasons,
        "match_interpretation": (
            "HJMI profile-to-job data overlap. "
            "This is not an employer assessment, hiring probability, "
            "or prediction of application outcome."
        ),
    }


# ============================================================
# DATAFRAME MATCHING
# ============================================================

def get_recommended_jobs(
    jobs_df,
    profile,
    limit=None,
    only_active=True,
):

    if jobs_df is None:
        return pd.DataFrame()

    if jobs_df.empty:
        return pd.DataFrame()

    if not profile:
        return pd.DataFrame()

    working_df = jobs_df.copy()

    # Only use jobs returned by the latest HJMI collection.
    if (
        only_active
        and "is_active"
        in working_df.columns
    ):

        active_mask = (
            working_df["is_active"]
            .fillna(False)
            .astype(bool)
        )

        working_df = (
            working_df[
                active_mask
            ]
            .copy()
        )

    matched_rows = []

    for _, row in working_df.iterrows():

        job = row.to_dict()

        match = match_job(
            profile,
            job,
        )

        if not match["qualifies"]:
            continue

        result = dict(job)

        result.update(
            {
                "hjmi_match_score": (
                    match["match_score"]
                ),
                "hjmi_match_label": (
                    match["match_label"]
                ),
                "hjmi_matched_skills": (
                    match["matched_skills"]
                ),
                "hjmi_missing_profile_skills": (
                    match[
                        "missing_profile_skills"
                    ]
                ),
                "hjmi_matched_roles": (
                    match["matched_roles"]
                ),
                "hjmi_specialization_match": (
                    match[
                        "specialization_match"
                    ]
                ),
                "hjmi_matched_locations": (
                    match[
                        "matched_locations"
                    ]
                ),
                "hjmi_experience_match": (
                    match[
                        "experience_match"
                    ]
                ),
                "hjmi_experience_known": (
                    match[
                        "experience_known"
                    ]
                ),
                "hjmi_experience_label": (
                    match[
                        "experience_label"
                    ]
                ),
                "hjmi_match_reasons": (
                    match["match_reasons"]
                ),
                "hjmi_match_interpretation": (
                    match["match_interpretation"]
                ),
            }
        )

        matched_rows.append(
            result
        )

    if not matched_rows:
        return pd.DataFrame()

    results = pd.DataFrame(
        matched_rows
    )

    sort_columns = [
        "hjmi_match_score",
    ]

    ascending = [
        False,
    ]

    if (
        "publication_date"
        in results.columns
    ):

        sort_columns.append(
            "publication_date"
        )

        ascending.append(
            False
        )

    results = (
        results.sort_values(
            by=sort_columns,
            ascending=ascending,
            na_position="last",
        )
        .reset_index(
            drop=True
        )
    )

    if (
        limit is not None
        and int(limit) > 0
    ):

        results = results.head(
            int(limit)
        )

    return results


# ============================================================
# MATCH SUMMARY
# ============================================================

def get_match_summary(
    recommendations,
):

    if (
        recommendations is None
        or recommendations.empty
    ):

        return {
            "total_matches": 0,
            "strong_matches": 0,
            "good_matches": 0,
            "skill_matches": 0,
        }

    labels = (
        recommendations[
            "hjmi_match_label"
        ]
        .fillna("")
        .astype(str)
    )

    return {
        "total_matches": len(
            recommendations
        ),
        "strong_matches": int(
            (
                labels
                == "Strong Profile Match"
            ).sum()
        ),
        "good_matches": int(
            (
                labels
                == "Good Profile Match"
            ).sum()
        ),
        "skill_matches": int(
            (
                labels
                == "Skill Match"
            ).sum()
        ),
    }
