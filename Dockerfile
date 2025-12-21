FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc libpq-dev bash \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install -vv --no-input --no-cache-dir -r requirements.txt

COPY . .

# TEMP DEBUG
RUN echo "CWD: $(pwd)" && \
    echo "Top-level:" && ls -lah && \
    echo "Find start.sh:" && find . -maxdepth 3 -name start.sh -print


# if start.sh is in /app after the COPY, this will work
RUN chmod +x start.sh

# ENTRYPOINT ["./start.sh"]
ENTRYPOINT ["bash", "start.sh"]
