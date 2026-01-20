# AI Processor Service

> [!WARNING]
> This module is currently in **Active Development** and is intended for debugging and evaluation purposes. It is **NOT** yet ready for production use.

## Overview
The AI Processor is responsible for all "intelligent" tasks in the JobStream-AI ecosystem, including job match analysis, CV optimization, and PDF generation.

## Prerequisites
- Python 3.11+
- [OpenRouter API Key](https://openrouter.ai/keys)
- Windows system fonts (Segoe UI, Segoe UI Emoji) are required for high-quality PDF rendering.

## Setup
1. Ensure your `.env` file in the project root contains:
   ```env
   OPENROUTER_API_KEY=your_key_here
   OPENROUTER_MODEL=tngtech/deepseek-r1t2-chimera:free # or your preferred model
   ```
2. **[CRITICAL] Icon Generation**: Before generating PDFs, you must extract the necessary emoji icons:
   ```powershell
   python src/extract_emojis.py
   ```
   This will create a `assets/icons/` directory with PNG versions of common emojis.

## Usage (CLI Debug Tool)
Use `src/debug_processor.py` to test the module components:

### Analyze Job Match
```powershell
python src/debug_processor.py --action analyze --job path/to/job.json --cv path/to/cv.md --prefs path/to/prefs.md
```

### Optimize CV & Generate PDF
```powershell
python src/debug_processor.py --action pdf --job path/to/job.json --cv path/to/cv.md --prefs path/to/prefs.md --photo path/to/photo.jpg
```

### Generate Cover Letter
```powershell
python src/debug_processor.py --action cover_letter --job path/to/job.json --cv path/to/cv.md --prefs path/to/prefs.md
```

## Key Files
- `src/processor.py`: Main logic for AI interactions.
- `src/pdf_gen.py`: Markdown to PDF conversion engine.
- `src/client.py`: OpenRouter API client with logging support.
- `src/debug_processor.py`: CLI interface for the module.
- `src/extract_emojis.py`: Emoji extraction utility.

## Notes
- **Logs**: If a `--debug-dir` is provided to the CLI tool, it will save all LLM requests and responses for inspection.
- **Output**: Default output directory for generated files is `debug/output/`.
