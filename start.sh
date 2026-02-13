#!/usr/bin/env bash
# Start script that runs migrations and imports data before starting the server
set -o errexit

# Run migrations
python manage.py migrate --noinput

# Collect static files (fallback, якщо не виконано в build.sh)
if [ ! -d "staticfiles" ] || [ -z "$(ls -A staticfiles 2>/dev/null)" ]; then
    echo "Збір статичних файлів (fallback)..."
    python manage.py collectstatic --noinput || true
fi

# Create superuser if doesn't exist
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='адмін').exists():
    User.objects.create_superuser('адмін', '', 'адмін123')
    print('✓ Суперкористувач створено: адмін / адмін123')
else:
    print('✓ Суперкористувач вже існує')
EOF

# Initialize data (import articles if database is empty)
python manage.py init_data || true  # || true щоб не зупинити сервер при помилці

# Start gunicorn
exec gunicorn music_media.wsgi:application

