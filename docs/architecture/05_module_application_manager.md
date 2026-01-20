# Module: Application Manager

## Technology Stack
*   **Language**: Python 3.11+
*   **Libraries**:
    *   `smtplib` / `emails`: For sending emails.
    *   `playwright`: For filling web forms (if applying directly on sites).
    *   `sqlalchemy`: DB access.

## Responsibilities
1.  **Listen**: Consumes `jobs:apply` messages.
2.  **Execute Application**:
    *   **Method A (Email)**: Sends an email to the recruiter/contact found in the job description with the tailored resume and cover letter attached.
    *   **Method B (Web Form)**: *Advanced*. Uses Playwright to fill out the "Easy Apply" forms. (Phase 2 feature).
3.  **Follow-up**:
    *   Schedules follow-up emails (e.g., "Checking in on my application") if no response in X days.
4.  **Status Tracking**: Updates DB status to `applied`.

## Funnel Logic (The "Sales Pipeline")
The module acts as a CRM automation tool.

*   **Stage 1: Applied**. Action: Send Application.
*   **Stage 2: Follow-up 1** (3 days later). Action: Send polite nudge.
*   **Stage 3: Follow-up 2** (7 days later). Action: Final check-in.
*   **Stage 4: Archived**. Action: Mark as closed if no response.

## Configuration
*   **SMTP Settings**: Host, Port, User, Pass.
*   **Templates**: Email body templates for applications and follow-ups.
