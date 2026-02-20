#!/usr/bin/env bash
# Start script that runs migrations and imports data before starting the server
set -o errexit

# Діагностика CLOUDINARY_URL
echo "=========================================="
echo "Перевірка CLOUDINARY_URL:"
if [ -z "$CLOUDINARY_URL" ]; then
    echo "✗ CLOUDINARY_URL не встановлено!"
    echo "Встановіть змінну середовища CLOUDINARY_URL на Render"
else
    echo "✓ CLOUDINARY_URL встановлено"
    # Показуємо тільки перші символи для безпеки
    echo "CLOUDINARY_URL: ${CLOUDINARY_URL:0:30}..."
fi
echo "=========================================="

# Run migrations
python manage.py migrate --noinput

# Collect static files (fallback, якщо не виконано в build.sh)
if [ ! -d "staticfiles" ] || [ -z "$(ls -A staticfiles 2>/dev/null)" ]; then
    echo "Збір статичних файлів (fallback)..."
    python manage.py collectstatic --noinput || true
fi

# Create superuser if doesn't exist
python manage.py create_superuser || true

# Initialize data (import articles if database is empty)
python manage.py init_data || true  # || true щоб не зупинити сервер при помилці

# Start gunicorn
exec gunicorn music_media.wsgi:application

