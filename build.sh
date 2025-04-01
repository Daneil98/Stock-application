#!/usr/bin/env bash
set -o errexit  # Exit on error

echo "=== Installing dependencies ==="
pip install -r Requirement.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput  # Critical for static files

echo "=== Applying database migrations ==="
python manage.py migrate --noinput
