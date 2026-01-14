import json
from pathlib import Path


def load_clean_jobs(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_jobs(cleaned_jobs):
    total_jobs = len(cleaned_jobs)

    missing_company = 0
    missing_category = 0
    missing_level = 0

    for job in cleaned_jobs:
        if not job.get("company_name"):
            missing_company += 1

        if not job.get("job_category"):
            missing_category += 1

        if not job.get("job_level"):
            missing_level += 1

    print("📊 SILVER DATA VALIDATION REPORT")
    print("--------------------------------")
    print(f"Total jobs            : {total_jobs}")
    print(f"Missing company name  : {missing_company}")
    print(f"Missing job category  : {missing_category}")
    print(f"Missing job level     : {missing_level}")


def main():
    silver_file = Path("silver/jobs/clean_jobs.json")
    cleaned_jobs = load_clean_jobs(silver_file)
    validate_jobs(cleaned_jobs)


if __name__ == "__main__":
    main()