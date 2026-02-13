#!/usr/bin/env bash
# Build script for Render
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files (важливо для WhiteNoise)
python manage.py collectstatic --noinput --clear

# Run migrations
python manage.py migrate --noinput

