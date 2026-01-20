# Project Architecture

## Overview
This project is built using a strictly modular architecture designed for maximum isolation, maintainability, and focused development. The system is decomposed into independent services that interact through a common communication interface (message bus).

## Core Modules

| Module Name | Directory | Description |
| ----------- | --------- | ----------- |
| **Job Scanner** | `services/scanner` | Responsible for interacting with job sources, parsing platforms, and discovering new vacancies. |
| **AI Processor** | `services/ai_processor` | Handles intelligent processing, including vacancy analysis and automated resume adaptation. |
| **Application Manager** | `services/app_manager` | Orchestrates the core business logic and manages the application workflow across all modules. |
| **User Dashboard** | `services/dashboard` | Provides a client-side web interface for users to monitor system results and manage operations. |
| **PDF Generator** | `services/pdf_generator` | Handles generation of PDF documents and asset management (e.g., emojis). |

## Development Principles

### 1. Focused Development
Development is strictly module-centric. When interacting with the AI during development, the specific module being worked on must be explicitly specified. Context and changes should remain confined to that module's scope.

### 2. Service Isolation
- **No Direct Dependencies**: Modules are prohibited from having direct dependencies on one another. All cross-module interaction is handled via the communication bus.
- **Isolated Roots**: Each module's source code is located in its respective directory under `services/`. This directory is treated as the root for that specific module.
- **Entry Point**: Every module contains its own `main.py` entry point within its folder.
- **Relative Imports**: All code within a module must use imports relative to the module's root (e.g., `from src.utils import ...` inside `services/scanner`).

## Documentation Structure
Each module has its own dedicated documentation folder within the `docs/` directory. These files define:
- The module's internal logic and features.
- The communication protocols and interfaces used for inter-module integration.

Specific module documentation can be found in `docs/architecture/`:
- [Job Scanner](03_module_job_scanner.md)
- [AI Processor](04_module_ai_processor.md)
- [Application Manager](05_module_application_manager.md)
- [User Dashboard](02_module_user_dashboard.md)
