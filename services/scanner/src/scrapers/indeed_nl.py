from typing import List, Dict, Any, Optional
from src.scrapers.base import Filter, FilterOption, JobSummary, JobDetail, SalaryInfo
from src.scrapers.playwright_base import PlaywrightScraper
import time
import re

class IndeedNLScraper(PlaywrightScraper):
    BASE_URL = "https://nl.indeed.com"

    def _parse_salary(self, salary_str: str) -> Optional[SalaryInfo]:
        if not salary_str:
            return None
        
        # Example formats: 
        # "€ 3.500 - € 4.500 per maand"
        # "€ 3.500 per maand"
        # "€ 40.000 - € 50.000 per jaar"
        
        try:
            # Normalize: remove dots (Dutch thousands separator), currency symbol
            clean_str = salary_str.replace(".", "").replace("€", "").strip()
            
            # Detect period
            period = "monthly"
            if "jaar" in clean_str.lower():
                period = "yearly"
            elif "uur" in clean_str.lower():
                period = "hourly"
            elif "week" in clean_str.lower():
                period = "weekly"
            
            # Extract numbers
            numbers = re.findall(r"(\d+)", clean_str)
            if not numbers:
                return None
            
            nums = [float(n) for n in numbers]
            s_min = nums[0]
            s_max = nums[1] if len(nums) > 1 else s_min
            
            # Convert to monthly if needed
            if period == "yearly":
                s_min = s_min / 12
                s_max = s_max / 12
            elif period == "hourly":
                # Assume 160 hours per month
                s_min = s_min * 160
                s_max = s_max * 160
            elif period == "weekly":
                s_min = s_min * 4.33
                s_max = s_max * 4.33
                
            return SalaryInfo(
                min=round(s_min),
                max=round(s_max),
                currency="EUR",
                period="monthly"
            )
        except Exception as e:
            print(f"Error parsing salary '{salary_str}': {e}")
            return None

    def get_filters(self) -> List[Filter]:
        return [
            Filter(id="q", label="Wat (Trefwoorden)", type="text"),
            Filter(id="l", label="Waar (Locatie)", type="text"),
        ]

    def get_jobs(self, filters: Dict[str, Any], page: int = 1) -> List[JobSummary]:
        self.connect()
        
        q = filters.get("q", "")
        l = filters.get("l", "")
        start = (page - 1) * 10
        
        url = f"{self.BASE_URL}/jobs?q={q}&l={l}&start={start}"
        self.navigate(url)
        
        # Save HTML for debugging
        self.save_page_html(f"listing_{q}_{l}_{page}")
        
        # Wait for job cards
        try:
            self.page.wait_for_selector(".job_seen_beacon", timeout=5000)
        except:
            print("No jobs found or timeout.")
            return []

        job_cards = self.page.query_selector_all(".job_seen_beacon")
        jobs = []

        for card in job_cards:
            try:
                title_el = card.query_selector("h2.jobTitle span")
                title = title_el.inner_text() if title_el else "Unknown"
                
                company_el = card.query_selector("[data-testid='company-name']")
                company = company_el.inner_text() if company_el else "Unknown"
                
                location_el = card.query_selector("[data-testid='text-location']")
                location = location_el.inner_text() if location_el else "Unknown"
                
                link_el = card.query_selector("a.jcs-JobTitle")
                url_suffix = link_el.get_attribute("href") if link_el else ""
                url = f"{self.BASE_URL}{url_suffix}" if url_suffix else ""
                
                # Extract ID from JK parameter or data attribute
                job_id = card.query_selector("h2.jobTitle a").get_attribute("data-jk") or "unknown"

                # New: salary and date from listing
                salary_el = card.query_selector("[data-testid='attribute_snippet_testid salary-snippet-container']")
                salary_raw = salary_el.inner_text() if salary_el else None
                
                date_el = card.query_selector("[data-testid='myJobsState']") # Often contains relative date
                if not date_el:
                    date_el = card.query_selector(".date")
                date_posted = date_el.inner_text() if date_el else None

                jobs.append(JobSummary(
                    id=job_id,
                    title=title,
                    company=company,
                    location=location,
                    url=url,
                    source="indeed_nl",
                    salary=salary_raw,
                    salary_structured=self._parse_salary(salary_raw),
                    date_posted=date_posted
                ))
            except Exception as e:
                print(f"Error parsing card: {e}")
                continue
                
        return jobs

    def get_job_details(self, job_id: str) -> JobDetail:
        self.connect()
        # Indeed specific viewjob URL
        url = f"{self.BASE_URL}/viewjob?jk={job_id}"
        self.navigate(url)
        
        # Save HTML for debugging
        self.save_page_html(f"detail_{job_id}")
        
        self.page.wait_for_selector("#jobDescriptionText", timeout=5000)
        
        title = self.page.inner_text("h1.jobsearch-JobInfoHeader-title")
        company = self.page.inner_text("[data-testid='inlineHeader-companyName']")
        
        # Improved location extraction
        location_el = self.page.query_selector("[data-testid='inlineHeader-companyLocation']")
        location = location_el.inner_text() if location_el else "Unknown"
        
        # Salary from detail page
        salary_el = self.page.query_selector("#salaryInfoAndJobType")
        salary_raw = salary_el.inner_text() if salary_el else None
        
        # Date posted from detail page
        date_el = self.page.query_selector(".jobsearch-JobMetadataFooter")
        date_posted = date_el.inner_text() if date_el else None
        
        # Languages extraction
        description_html = self.page.inner_html("#jobDescriptionText")
        languages = []
        if "Nederlands" in description_html:
            languages.append("Dutch")
        if "Engels" in description_html or "English" in description_html:
            languages.append("English")
            
        return JobDetail(
            id=job_id,
            title=title,
            company=company,
            location=location,
            url=url,
            source="indeed_nl",
            salary=salary_raw,
            salary_structured=self._parse_salary(salary_raw),
            date_posted=date_posted,
            languages=languages,
            description=description_html,
            raw_html=description_html
        )
