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
echo "Збір статичних файлів..."
python manage.py collectstatic --noinput --clear --verbosity=2

# Перевірка, чи файли зібрані
echo ""
echo "=== Перевірка статичних файлів ==="
if [ -d "staticfiles" ]; then
    echo "✓ Директорія staticfiles існує"
    echo "Вміст staticfiles:"
    find staticfiles -type f -name "*.css" | head -5
    if [ -f "staticfiles/css/main.css" ]; then
        echo "✓ Знайдено: staticfiles/css/main.css"
    elif [ -f "staticfiles/static/css/main.css" ]; then
        echo "✓ Знайдено: staticfiles/static/css/main.css"
    else
        echo "⚠ main.css не знайдено в очікуваних місцях"
        echo "Пошук main.css:"
        find staticfiles -name "main.css" 2>/dev/null || echo "  main.css не знайдено"
    fi
else
    echo "✗ Директорія staticfiles не існує!"
fi

