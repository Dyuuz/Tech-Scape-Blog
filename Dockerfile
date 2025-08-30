FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install -vv --no-input --no-cache-dir -r requirements.txt

COPY . .

# Ensure it's executable (will fail if it was excluded by .dockerignore)
RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]
