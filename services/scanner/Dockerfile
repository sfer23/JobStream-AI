FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright/Selenium if needed later
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Command to run the scanner (placeholder)
CMD ["python", "-u", "src/main.py"]
