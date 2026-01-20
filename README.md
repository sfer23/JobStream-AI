# 🚀 JobStream-AI

Welcome to **JobStream-AI** — your ultimate toolkit for modern job hunting, built with the spirit of **Vibecoding**! 🌊

This project is a collection of tools designed to automate the most tedious parts of the job search process, allowing you to focus on what matters: finding the right role and growing your career.

## ✨ Features

- **🔍 Smart Scanning**: Automated parsers for job boards (Indeed and more) to find vacancies that match your criteria.
- **🧠 AI Analysis**: Intelligent job-to-resume matching using LLMs (via OpenRouter) to give you a realistic "Match Score."
- **✍️ CV Optimization**: AI-powered rewriting of your CV to highlight relevant experience for specific roles—without hallucinating!
- **📄 Pro PDF Generation**: Generate high-quality, professional PDFs with custom styles, clickable links, and emoji support.
- **✉️ Cover Letter Magic**: Automated generation of targeted cover letters that bridge the gap between your skills and the job needs.

## 🏗️ Architecture

The project follows a **strictly modular architecture**:
- [Job Scanner](services/scanner): Data extraction and discovery.
- [AI Processor](services/ai_processor): Intelligence, optimization, and PDF generation.
- [Application Manager](services/app_manager): Core business logic orchestration.
- [Dashboard](services/dashboard): Web interface for easy management.

For more details, see the [Architecture Documentation](docs/architecture/ARCHITECTURE.md).

## 🛠️ Getting Started

1. **Clone the repo**
2. **Configure environment variables**: Copy `.env.example` to `.env` and fill in your `OPENROUTER_API_KEY`.
3. **Explore the modules**: Each service has its own `README.md` with specific setup instructions.

> [!NOTE]  
> This project is currently in **Active Development** as part of a journey to practice **Vibecoding** and build awesome tools. Feel free to explore!

## 📜 License

This project is licensed under the [MIT License](LICENSE) — see the file for details.

---
*Built with ❤️ and AI for the developer community.*
