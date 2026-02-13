"""
ASGI config for music_media project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

# Виправлення для Python 3.14 сумісності з Django
# Має бути імпортовано ПЕРЕД get_asgi_application()
try:
    from music_media.python314_fix import *  # noqa: F403, F401
except ImportError:
    pass  # Якщо файл не знайдено, продовжуємо без патчу

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_media.settings')

application = get_asgi_application()

