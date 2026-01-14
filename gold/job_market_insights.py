import json
from collections import Counter, defaultdict
from pathlib import Path


# ---------- Load Silver Data ----------
def load_clean_jobs(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Q1 & Q3: Job Roles ----------
def job_role_counts(cleaned_jobs):
    roles = [job["job_title"] for job in cleaned_jobs if job["job_title"]]
    return Counter(roles).most_common(10)


# ---------- Q2: Locations ----------
def top_locations(cleaned_jobs):
    locations = []
    for job in cleaned_jobs:
        locations.extend(job.get("locations", []))
    return Counter(locations).most_common(10)


# ---------- Skill extraction helper ----------
def extract_skills(text):
    skill_keywords = [
        "python", "sql", "aws", "azure", "gcp", "spark",
        "hadoop", "docker", "kubernetes", "java",
        "machine learning", "pandas", "numpy"
    ]

    found = []
    text = text.lower()

    for skill in skill_keywords:
        if skill in text:
            found.append(skill)

    return found


# ---------- Q4: Top skills overall ----------
def top_skills_overall(cleaned_jobs):
    skills = []

    for job in cleaned_jobs:
        description = job.get("job_description", "")
        skills.extend(extract_skills(description))

    return Counter(skills).most_common(10)


# ---------- Q5: Skills per role ----------
def skills_per_role(cleaned_jobs):
    role_skills = defaultdict(list)

    for job in cleaned_jobs:
        role = job.get("job_title")
        description = job.get("job_description", "")

        if role and description:
            role_skills[role].extend(extract_skills(description))

    result = {}
    for role, skills in role_skills.items():
        result[role] = Counter(skills).most_common(5)

    return result


# ---------- Save output ----------
def save_output(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------- Main ----------
def main():
    silver_file = Path("silver/jobs/clean_jobs.json")
    jobs = load_clean_jobs(silver_file)

    save_output(job_role_counts(jobs), Path("gold/top_job_roles.json"))
    save_output(top_locations(jobs), Path("gold/top_locations.json"))
    save_output(job_role_counts(jobs), Path("gold/role_availability.json"))
    save_output(top_skills_overall(jobs), Path("gold/top_skills_overall.json"))
    save_output(skills_per_role(jobs), Path("gold/skills_per_role.json"))

    print("🏆 Gold layer insights generated successfully")


if __name__ == "__main__":
    main()