FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .

# after
RUN python -m pip install --upgrade pip && \
    python -m pip install -vv --no-input --no-cache-dir -r requirements.txt

# Copy files
COPY . .

COPY start.sh .
RUN chmod +x start.sh

# Set entrypoint
ENTRYPOINT ["./start.sh"]
