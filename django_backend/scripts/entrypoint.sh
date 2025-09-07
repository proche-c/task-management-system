#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Seeding database (if empty)..."
python manage.py seed || true

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Replace the current shell with the command passed as arguments (from CMD or docker-compose)
exec "$@"