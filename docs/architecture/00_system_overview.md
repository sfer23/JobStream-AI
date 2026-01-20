# System Overview

## High-Level Architecture

The system is designed as a distributed, containerized application using a Microservices pattern (orchestrated via Docker Compose in a Monorepo).

### Diagram

```mermaid
graph TD
    subgraph "Client Layer"
        Browser[Web Browser]
    end

    subgraph "Frontend/Backend (User Dashboard)"
        Nginx[Nginx Gateway]
        PHP[PHP App (Laravel/Symfony)]
        Postgres[(PostgreSQL Primary DB)]
        Redis[(Redis Queue & Cache)]
    end

    subgraph "Worker Layer (Python)"
        Scanner[Job Scanner Service]
        AI[AI Processor Service]
        Manager[Application Manager Service]
    end

    subgraph "Infrastructure"
        Ollama[Ollama LLM Service]
        Mail[SMTP / Mail Service]
    end

    Browser -->|HTTP/HTTPS| Nginx
    Nginx -->|FastCGI| PHP
    PHP -->|Read/Write| Postgres
    PHP -->|Push Jobs| Redis

    Redis -->|Pop 'scan_jobs'| Scanner
    Scanner -->|Save Raw Jobs| Postgres
    Scanner -->|Push 'analyze_job'| Redis

    Redis -->|Pop 'analyze_job'| AI
    AI -->|Inference| Ollama
    AI -->|Update Job Data| Postgres
    AI -->|Push 'apply_job'| Redis

    Redis -->|Pop 'apply_job'| Manager
    Manager -->|Send Email| Mail
    Manager -->|Update Status| Postgres
```

## Monorepo Structure

We will use a single repository with the following structure to keep code organized but separated.

```text
/
├── docker-compose.yml      # Orchestration for all services
├── .env.example            # Global environment variables
├── docs/                   # Architecture and design docs
├── services/
│   ├── dashboard/          # PHP User Dashboard
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── ...
│   ├── scanner/            # Python Job Scanner
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── requirements.txt
│   ├── ai_processor/       # Python AI Worker
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── requirements.txt
│   └── app_manager/        # Python Application Manager
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── requirements.txt
└── data/                   # Local data persistence (DB, Redis, Ollama models)
```

## Infrastructure Components

1.  **Docker Compose**: Manages the lifecycle of all containers.
2.  **PostgreSQL**: Central relational database. Shared by all modules.
3.  **Redis**: Message Broker for asynchronous tasks.
4.  **Ollama**: Local LLM inference server.
