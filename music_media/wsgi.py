"""
WSGI config for music_media project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

# Виправлення для Python 3.14 сумісності з Django
# Має бути імпортовано ПЕРЕД get_wsgi_application()
try:
    from music_media.python314_fix import *  # noqa: F403, F401
except ImportError:
    pass  # Якщо файл не знайдено, продовжуємо без патчу

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_media.settings')

application = get_wsgi_application()

