"""
Django settings for music_media project.
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-!@#$%^&*()')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]  # Тимчасово для Render, потім можна поставити домен


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Має бути перед 'django.contrib.staticfiles'
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'cloudinary',  # Cloudinary для зберігання медіа
    'articles',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music_media.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Вимикаємо categories для адмінки, щоб уникнути проблем з Python 3.14
                # Категорії додаються вручну в views
                # 'articles.context_processors.categories',
            ],
        },
    },
]

# Логування для діагностики
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'articles': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

WSGI_APPLICATION = 'music_media.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
# Перевірка, чи існує директорія static (для локальної розробки)
static_dir = BASE_DIR / 'static'
if static_dir.exists():
    STATICFILES_DIRS = [static_dir]
else:
    # Якщо static не існує, використовуємо порожній список (файли вже в staticfiles)
    STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Переконайтеся, що staticfiles існує
os.makedirs(STATIC_ROOT, exist_ok=True)

# Cloudinary налаштування для медіа-файлів
# ВСЕГДА використовуємо Cloudinary для зберігання медіа-файлів
import logging
logger = logging.getLogger(__name__)

# Читаємо CLOUDINARY_URL з .env файлу або змінних середовища
# django-cloudinary-storage читає CLOUDINARY_URL з os.environ
CLOUDINARY_URL = config('CLOUDINARY_URL', default='')

# Встановлюємо в os.environ для django-cloudinary-storage
if CLOUDINARY_URL:
    os.environ['CLOUDINARY_URL'] = CLOUDINARY_URL
else:
    logger.error("✗ CLOUDINARY_URL не встановлено! Встановіть змінну середовища CLOUDINARY_URL")
    print("✗ CLOUDINARY_URL не встановлено! Встановіть змінну середовища CLOUDINARY_URL")
    raise ValueError("CLOUDINARY_URL must be set. Please set the CLOUDINARY_URL environment variable.")

# Використовуємо Cloudinary для зберігання медіа ВСЮДИ (локально і на Render)
# Важливо: cloudinary_storage має бути перед django.contrib.staticfiles в INSTALLED_APPS
# Використовуємо стандартний storage для всіх файлів
# VideoCloudinaryStorage перевизначає url() для правильного формату URL для відео
DEFAULT_FILE_STORAGE = 'articles.storage.VideoCloudinaryStorage'
# Для ImageField використовуємо стандартний storage
DEFAULT_IMAGE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
# MEDIA_ROOT не потрібен при використанні Cloudinary

# Налаштування папок для Cloudinary
# django-cloudinary-storage автоматично використовує CLOUDINARY_URL з os.environ
# Не потрібно встановлювати CLOUD_NAME, API_KEY, API_SECRET окремо
CLOUDINARY_STORAGE = {
    'PREFIX': 'media/',  # Префікс для всіх файлів
}

# Перевіряємо, чи правильно імпортується storage
try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
    logger.info("✓ MediaCloudinaryStorage imported successfully")
    print("✓ MediaCloudinaryStorage imported successfully")
except ImportError as e:
    logger.error(f"✗ Failed to import MediaCloudinaryStorage: {e}")
    print(f"✗ Failed to import MediaCloudinaryStorage: {e}")
    raise

# Налаштування Cloudinary через CLOUDINARY_URL
# django-cloudinary-storage автоматично використовує CLOUDINARY_URL з os.environ
# Перевіряємо, чи правильно встановлено CLOUDINARY_URL
try:
    # Перевіряємо формат URL
    if not CLOUDINARY_URL.startswith('cloudinary://'):
        raise ValueError("CLOUDINARY_URL must start with 'cloudinary://'")
    
    # Парсимо для перевірки та логування
    url_parts = CLOUDINARY_URL.replace('cloudinary://', '').split('@')
    if len(url_parts) == 2:
        auth_parts = url_parts[0].split(':')
        if len(auth_parts) == 2:
            api_key = auth_parts[0]
            cloud_name = url_parts[1]
            
            logger.info(f"✓ Cloudinary URL format is correct: cloud_name={cloud_name}, api_key={api_key[:5]}...")
            print(f"✓ Cloudinary URL format is correct: cloud_name={cloud_name}")
            print(f"✓ All media files will be stored on Cloudinary (both locally and on Render)")
            print(f"✓ django-cloudinary-storage will use CLOUDINARY_URL from environment")
        else:
            logger.error("✗ Could not parse CLOUDINARY_URL: invalid auth format")
            print("✗ Could not parse CLOUDINARY_URL: invalid auth format")
            raise ValueError("Invalid CLOUDINARY_URL format: auth parts")
    else:
        logger.error(f"✗ Could not parse CLOUDINARY_URL: invalid format. URL parts: {len(url_parts)}")
        print(f"✗ Could not parse CLOUDINARY_URL: invalid format")
        raise ValueError("Invalid CLOUDINARY_URL format: URL parts")
except Exception as e:
    logger.error(f"✗ Could not validate CLOUDINARY_URL: {e}")
    print(f"✗ Could not validate CLOUDINARY_URL: {e}")
    import traceback
    traceback.print_exc()
    raise

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB (для відео)
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Session settings
SESSION_COOKIE_AGE = 86400  # 1 day
SESSION_COOKIE_SECURE = True  # Для HTTPS на Render
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF settings для Render
# Отримуємо домен з environment або використовуємо за замовчуванням
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'music-project-dqkr.onrender.com')
CSRF_TRUSTED_ORIGINS = [
    f'https://{RENDER_EXTERNAL_HOSTNAME}',
    'https://music-project-dqkr.onrender.com',  # Явно вказаний домен
]
CSRF_COOKIE_SECURE = True  # Для HTTPS на Render
CSRF_COOKIE_HTTPONLY = False  # Адмінка потребує доступу до CSRF токена через JS
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False  # Використовуємо cookies для CSRF

# WhiteNoise settings for static files
# Використовуємо стандартний storage (WhiteNoise обслуговує файли через middleware)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# WhiteNoise configuration
WHITENOISE_USE_FINDERS = True  # Дозволяє WhiteNoise знаходити файли в STATICFILES_DIRS
WHITENOISE_AUTOREFRESH = False  # В production не потрібно
WHITENOISE_INDEX_FILE = False  # Не використовуємо index файли
WHITENOISE_ROOT = STATIC_ROOT  # Вказуємо корінь для статичних файлів

