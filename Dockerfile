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
RUN python -m pip install --upgrade pip && \
    python -m pip install -vv --no-input --no-cache-dir -r requirements.txt

# Copy all source files (including start.sh if it exists)
COPY . .

# Make sure start.sh is executable
RUN chmod +x start.sh

# Set entrypoint
ENTRYPOINT ["./start.sh"]
