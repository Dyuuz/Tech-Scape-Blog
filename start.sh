#!/usr/bin/env bash

set -e

echo "=== Boot: validating environment ==="

if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL is not set"
  exit 1
fi

if [ -z "$PORT" ]; then
  echo "ERROR: PORT not set by Render"
  exit 1
fi

export PYTHONUNBUFFERED=1

echo "Starting TechScape on port $PORT..."

echo "=== Step 1/3: applying migrations ==="
python manage.py migrate --noinput
echo "=== Migrations: done ==="

echo "=== Step 2/3: collecting static files ==="
python manage.py collectstatic --noinput -v 2
echo "=== Collectstatic: done ==="

echo "=== Step 3/3: starting Gunicorn on 0.0.0.0:${PORT} ==="
exec gunicorn Blog.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --access-logfile - \
  --error-logfile - \
  --log-level info
