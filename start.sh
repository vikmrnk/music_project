#!/usr/bin/env bash
# Start script that runs migrations before starting the server
set -o errexit

# Run migrations
python manage.py migrate --noinput

# Start gunicorn
exec gunicorn music_media.wsgi:application

