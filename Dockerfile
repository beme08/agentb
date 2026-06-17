FROM python:3.11-slim

# System deps for Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright + browsers only when needed by BrowserUseAgent.
# Comment out the next two lines to keep the image small.
# RUN pip install playwright && playwright install --with-deps chromium

COPY . .

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python3", "run_benchmark.py"]
CMD ["--agent", "stub", "--all"]
