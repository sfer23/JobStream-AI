# Module: User Dashboard

## Technology Stack
*   **Language**: PHP 8.2+
*   **Framework**: Laravel (Recommended for rapid development, queues, and robust ORM) or Symfony.
*   **Frontend**: Blade Templates + TailwindCSS (or Vue.js/React if preferred, but server-side rendering is simpler for this).
*   **Container**: `php:8.2-fpm` + Nginx.

## Responsibilities
1.  **Profile Management**: Upload base resumes (PDF/DOCX -> Text conversion), define skills, set search preferences.
2.  **Job Board**: View found vacancies, filter by AI score, status.
3.  **Funnel View**: Kanban board (New -> Applied -> Interview -> Offer).
4.  **Manual Override**: Edit generated cover letters/resumes before sending.
5.  **System Control**: Trigger manual scans, view system logs.

## Database Schema (Key Tables)

### `users`
*   `id`, `email`, `password`, `name`

### `resumes`
*   `id`, `user_id`, `title` (e.g., "Backend Dev"), `content_text` (parsed), `file_path`

### `search_configs`
*   `id`, `user_id`, `keywords`, `locations`, `frequency`

### `vacancies`
*   `id`, `title`, `company`, `description`, `url`, `source`, `status`

### `vacancy_analyses`
*   `vacancy_id`, `match_score`, `reasoning`, `tailored_resume`, `cover_letter`

## API / Interaction
*   **GET /jobs**: List jobs with pagination and filters.
*   **POST /jobs/{id}/apply**: Manually trigger application process (pushes to `jobs:apply` queue).
*   **POST /scan**: Trigger immediate scan (pushes to `jobs:scan` queue).

## File Structure (Laravel Style)
```text
app/
  Models/
    Job.php
    Resume.php
  Http/
    Controllers/
      JobController.php
      DashboardController.php
  Jobs/ (Queues)
    ProcessScanResult.php
```
