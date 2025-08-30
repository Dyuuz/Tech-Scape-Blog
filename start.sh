#!/usr/bin/env bash

echo "=== Boot: validating environment ==="
# Change DB_URL to DATABASE_URL if your settings use that
if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DB_URL is not set"
  exit 1
fi

PORT=${PORT:-8000}
export PYTHONUNBUFFERED=1

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
