#!/usr/bin/env bash
# Build script for Render
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run migrations first (before collectstatic)
python manage.py migrate --noinput

# Collect static files (важливо для WhiteNoise)
# Використовуємо --clear для очищення старих файлів
python manage.py collectstatic --noinput --clear

# Перевірка, чи файли зібрані
echo "Перевірка статичних файлів..."
ls -la staticfiles/static/css/ 2>/dev/null || echo "Попередження: staticfiles/static/css/ не знайдено"

