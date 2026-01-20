# Communication & Data Structures

## Communication Protocols

### 1. Inter-Module Communication (Async)
We use **Redis** as a message broker.

*   **Format**: JSON
*   **Queues**:
    *   `jobs:scan`: Triggers a new search.
    *   `jobs:analyze`: Triggers AI analysis for a specific job.
    *   `jobs:apply`: Triggers the application process (email generation, form filling).

### 2. Database (Shared State)
All modules connect to a shared **PostgreSQL** database.
*   **Why Shared DB?** For a single-user/small-team application, a shared database significantly reduces complexity compared to maintaining separate microservice databases and API layers.

## Data Structures (JSON Schemas)

### 1. Scan Request (Queue: `jobs:scan`)
Payload sent from Dashboard to Scanner.

```json
{
  "request_id": "uuid-v4",
  "user_id": 1,
  "criteria": {
    "keywords": ["PHP", "Architect"],
    "location": "Remote",
    "sources": ["linkedin", "indeed", "glassdoor"]
  }
}
```

### 2. Job Vacancy (DB Table: `vacancies`)
Data collected by Scanner.

```json
{
  "id": "uuid-v4",
  "external_id": "site-specific-id",
  "title": "Senior PHP Developer",
  "company": "Tech Corp",
  "url": "https://...",
  "description_raw": "HTML content...",
  "source": "indeed",
  "status": "new", // new, analyzed, rejected, applied, interview
  "created_at": "2023-10-27T10:00:00Z"
}
```

### 3. Analysis Request (Queue: `jobs:analyze`)
Payload sent from Scanner to AI Processor.

```json
{
  "job_id": "uuid-v4",
  "resume_id": 1 // ID of the user's base resume to match against
}
```

### 4. AI Analysis Result (DB Table: `vacancy_analyses`)
Output from AI Processor.

```json
{
  "job_id": "uuid-v4",
  "match_score": 85, // 0-100
  "summary": "Good match, requires more Python experience.",
  "missing_skills": ["FastAPI"],
  "optimized_resume_text": "Markdown content of tailored resume...",
  "cover_letter_text": "Dear Hiring Manager...",
  "suggested_action": "apply" // apply, ignore
}
```

### 5. Application Context (DB Table: `applications`)
Tracks the funnel.

```json
{
  "id": "uuid-v4",
  "job_id": "uuid-v4",
  "status": "applied",
  "history": [
    {
      "stage": "applied",
      "timestamp": "2023-10-27T12:00:00Z",
      "note": "Sent via Email"
    }
  ]
}
```
