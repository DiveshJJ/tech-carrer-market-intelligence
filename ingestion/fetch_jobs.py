import requests
import json
from datetime import datetime
from pathlib import Path


def fetch_jobs(max_pages=5):
    """
    Fetch multiple pages of job postings from The Muse API
    """
    url = "https://www.themuse.com/api/public/jobs"
    all_jobs = []

    for page in range(1, max_pages + 1):
        print(f"📄 Fetching page {page}")

        params = {"page": page}
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        jobs = data.get("results", [])

        if not jobs:
            print("⚠️ No more jobs found, stopping.")
            break

        all_jobs.extend(jobs)

    print(f"✅ Total jobs fetched: {len(all_jobs)}")
    return all_jobs


def save_raw_jobs(data):
    """
    Save raw job data into bronze layer
    """
    today = datetime.today().strftime("%Y-%m-%d")

    bronze_path = Path("bronze") / "jobs" / f"date={today}"
    bronze_path.mkdir(parents=True, exist_ok=True)

    file_path = bronze_path / "jobs_raw.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Raw job data saved to {file_path}")


def main():
    print("🚀 Ingestion started")

    jobs_data = fetch_jobs()
    save_raw_jobs(jobs_data)

    print("🎯 Ingestion completed successfully")


if __name__ == "__main__":
    main()