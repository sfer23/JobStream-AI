import uuid
from typing import List, Dict, Any
from src.scrapers.base import BaseScraper, Filter, JobSummary, JobDetail

class MockScraper(BaseScraper):
    def __init__(self, debug_dir=None):
        self.debug_dir = debug_dir

    def get_filters(self) -> List[Filter]:
        return [
            Filter(id="keywords", label="Keywords", type="text"),
            Filter(id="location", label="Location", type="text")
        ]

    def get_jobs(self, filters: Dict[str, Any], page: int = 1) -> List[JobSummary]:
        keywords = filters.get("keywords", "Generic")
        location = filters.get("location", "Remote")
        
        print(f"[MockScraper] Searching for '{keywords}' in '{location}' (Page {page})...")
        
        jobs = []
        # Generate 5 mock jobs
        for i in range(5):
            job_id = str(uuid.uuid4())[:8]
            jobs.append(JobSummary(
                id=job_id,
                title=f"{keywords} Developer {i+1}",
                company=f"Mock Company {i+1}",
                location=location,
                url=f"https://example.com/jobs/{job_id}",
                source="mock",
                extra_data={"meta": "mock data"}
            ))
        
        print(f"[MockScraper] Found {len(jobs)} jobs.")
        return jobs

    def get_job_details(self, job_id: str) -> JobDetail:
        return JobDetail(
            id=job_id,
            title="Mock Job Title",
            company="Mock Company",
            location="Mock Location",
            url=f"https://example.com/jobs/{job_id}",
            source="mock",
            description=f"This is a detailed description for mock job {job_id}.",
            raw_html=f"<div><h1>Job {job_id}</h1><p>Description...</p></div>"
        )
