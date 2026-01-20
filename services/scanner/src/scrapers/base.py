from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class FilterOption:
    value: str
    label: str

@dataclass
class Filter:
    id: str
    label: str
    type: str  # 'text', 'select', 'range'
    options: Optional[List[FilterOption]] = None

@dataclass
class SalaryInfo:
    min: Optional[float] = None
    max: Optional[float] = None
    currency: str = "EUR"
    period: str = "monthly"

@dataclass
class JobSummary:
    id: str
    title: str
    company: str
    location: str
    url: str
    source: str
    salary: Optional[str] = None
    salary_structured: Optional[SalaryInfo] = None
    date_posted: Optional[str] = None
    languages: Optional[List[str]] = None
    extra_data: Optional[Dict[str, Any]] = None

@dataclass
class JobDetail(JobSummary):
    description: str = ""
    raw_html: str = ""

class BaseScraper(ABC):
    @abstractmethod
    def get_filters(self) -> List[Filter]:
        """Returns a list of available search filters for this site."""
        pass

    @abstractmethod
    def get_jobs(self, filters: Dict[str, Any], page: int = 1) -> List[JobSummary]:
        """Returns a list of job summaries based on filters and page number."""
        pass

    @abstractmethod
    def get_job_details(self, job_id: str) -> JobDetail:
        """Returns detailed information for a specific job."""
        pass
