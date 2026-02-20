#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# FORCE MIGRATIONS (This is what's missing)
python manage.py makemigrations accounts
python manage.py makemigrations
python manage.py migrate --no-input