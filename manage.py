#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Виправлення для Python 3.14 сумісності з Django
# Має бути імпортовано ПЕРЕД будь-якими імпортами Django
try:
    from music_media.python314_fix import *  # noqa: F403, F401
except ImportError:
    pass  # Якщо файл не знайдено, продовжуємо без патчу


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_media.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

