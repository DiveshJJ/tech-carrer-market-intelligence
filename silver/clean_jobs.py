import json
from pathlib import Path


def load_raw_jobs(bronze_file_path):
    """
    Load raw jobs JSON from Bronze layer
    """
    with open(bronze_file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_jobs(raw_jobs):
    """
    Extract and clean required fields from raw job data
    """
    cleaned_jobs = []

    for job in raw_jobs:
        levels = job.get("levels", [])
        categories = job.get("categories", [])
        locations = job.get("locations", [])

        cleaned_job = {
            "job_id": job.get("id"),
            "job_title": job.get("name"),
            "company_name": job.get("company", {}).get("name"),
            "locations": [loc.get("name") for loc in locations],
            "publication_date": job.get("publication_date"),
            "job_description": job.get("contents"),
            "job_level": levels[0].get("name") if levels else None,
            "job_category": categories[0].get("name") if categories else None,
        }

        cleaned_jobs.append(cleaned_job)

    return cleaned_jobs


def save_clean_jobs(cleaned_jobs, silver_file_path):
    """
    Save cleaned jobs into Silver layer
    """
    silver_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(silver_file_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_jobs, f, indent=2)

    print(f"✅ Cleaned data saved to {silver_file_path}")


def main():
    bronze_file = Path("bronze/jobs").glob("date=*/jobs_raw.json")
    bronze_file = sorted(bronze_file)[-1]  # latest date

    print(f"📥 Loading raw data from {bronze_file}")

    raw_jobs = load_raw_jobs(bronze_file)
    cleaned_jobs = clean_jobs(raw_jobs)

    silver_file = Path("silver/jobs/clean_jobs.json")
    save_clean_jobs(cleaned_jobs, silver_file)

    print("🎯 Silver layer completed successfully")


if __name__ == "__main__":
    main()