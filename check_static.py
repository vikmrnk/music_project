#!/usr/bin/env python
"""
Скрипт для перевірки статичних файлів
"""
import os
import sys
import django

# Налаштування Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_media.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command

print("=" * 50)
print("Перевірка налаштувань статичних файлів")
print("=" * 50)
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
print()

print("Перевірка директорій:")
for static_dir in settings.STATICFILES_DIRS:
    print(f"  {static_dir}: {'існує' if os.path.exists(static_dir) else 'НЕ існує'}")
    if os.path.exists(static_dir):
        css_path = os.path.join(static_dir, 'css', 'main.css')
        print(f"    main.css: {'існує' if os.path.exists(css_path) else 'НЕ існує'}")

print()
print(f"STATIC_ROOT: {'існує' if os.path.exists(settings.STATIC_ROOT) else 'НЕ існує'}")
if os.path.exists(settings.STATIC_ROOT):
    print(f"  Вміст STATIC_ROOT:")
    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        level = root.replace(settings.STATIC_ROOT, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Перші 5 файлів
            print(f"{subindent}{file}")

print()
print("Виконання collectstatic...")
try:
    call_command('collectstatic', '--noinput', '--clear', verbosity=2)
    print("✓ collectstatic виконано успішно")
except Exception as e:
    print(f"✗ Помилка: {e}")

