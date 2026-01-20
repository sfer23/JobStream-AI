# Module: AI Processor

## Technology Stack
*   **Language**: Python 3.11+
*   **AI Integration**: [OpenRouter API](https://openrouter.ai/) (replacing local Ollama for better performance/flexibility).
*   **Libraries**:
    *   `openai`: For OpenRouter API communication.
    *   `fpdf`: High-quality PDF generation.
    *   `Pillow (PIL)`: Emoji rendering and image processing.
    *   `python-dotenv`: Environment variable management.

## Responsibilities
1.  **Analyze Match**: Compares Job Description (JSON), Candidate's CV (Markdown), and Preferences (Markdown) to provide a match score and detailed reasoning.
2.  **Optimize CV**: Rewrites the CV to highlight relevant experience for a specific job while maintaining factual accuracy.
3.  **Create Cover Letter**: Generates a professional, targeted cover letter based on the job requirements and candidate's background.
4.  **PDF Generation**: Converts the optimized Markdown CV into a professional PDF format.
5.  **Emoji Support**: Handles emoji rendering in PDF headers by pre-extracting them as images.

## Core Components
- `processor.py`: Implementation of `CVProcessor` class for AI analysis and text generation.
- `client.py`: Wrapper for OpenRouter API with optional request/response logging.
- `pdf_gen.py`: Advanced PDF generator using `fpdf` with support for styles, links, and icons.
- `extract_emojis.py`: Utility to render emojis as PNG icons using system fonts.
- `debug_processor.py`: Comprehensive CLI tool for manual testing and debugging.

## Prompt Engineering Strategy
The module uses structured prompts to ensure consistent output from LLMs (e.g., DeepSeek, Gemma).

### 1. Analysis Prompt
Tasks the model to evaluate fit based on three inputs and return a clean JSON with `score` and `reasoning`.

### 2. Optimization Prompt
Instructs the model to rewrite the CV in Markdown, emphasizing relevant skills without "hallucinating" experience.

### 3. Cover Letter Prompt
Focuses on bridging the gap between candidate experience and job needs in a professional tone.

## Debugging & Manual Use
The module includes a `debug_processor.py` script that allows running any part of the pipeline manually:
- `analyze`: Get match score/reasoning.
- `optimize`: Generate optimized Markdown CV.
- `pdf`: Convert Markdown to PDF.
- `cover_letter`: Generate cover letter Markdown.

## Current Limitations
- **Non-Production Ready**: Currently optimized for development and debugging workflows.
- **Dependency on Local Fonts**: PDF generation and emoji extraction rely on Windows system fonts.
- **API Latency**: Processing multiple jobs depends on OpenRouter response times.
