# Module: Job Scanner

## Technology Stack
*   **Language**: Python 3.11+
*   **Libraries**:
    *   `playwright` or `selenium`: For rendering JS-heavy sites (LinkedIn, Glassdoor).
    *   `beautifulsoup4`: For parsing static HTML.
    *   `sqlalchemy`: For DB access.
    *   `redis`: For queue consumption.

## Responsibilities
1.  **Listen**: Consumes `jobs:scan` messages.
2.  **Scrape**: Navigates to target sites based on criteria.
3.  **Parse**: Extracts structured data (Title, Company, Description, Salary).
4.  **Deduplicate**: Checks DB to avoid saving duplicate jobs (by URL or composite key).
5.  **Store**: Saves new jobs to `vacancies` table with status `new`.
6.  **Notify**: Pushes new job IDs to `jobs:analyze` queue.

## Architecture

### Scraper Interface
We will use a Strategy pattern for different sites.

```python
class BaseScraper(ABC):
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> List[JobData]:
        pass

class IndeedScraper(BaseScraper):
    ...

class LinkedInScraper(BaseScraper):
    ...
```

### Anti-Bot Measures
*   **User-Agent Rotation**: Randomize headers.
*   **Delays**: Random sleep between requests.
*   **Headless Mode**: Configurable (sometimes headful is needed for debugging).

## Data Flow
1.  Receive `{"criteria": {...}}` from Redis.
2.  Instantiate Scrapers.
3.  Loop through results.
4.  `if not db.exists(job.url): db.save(job); redis.push("jobs:analyze", job.id)`
