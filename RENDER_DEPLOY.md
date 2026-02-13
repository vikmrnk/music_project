# Інструкція для деплою на Render

## ✅ Що вже зроблено:

1. ✅ Додано необхідні пакети в `requirements.txt`:
   - gunicorn
   - dj-database-url
   - psycopg2-binary
   - whitenoise

2. ✅ Оновлено `settings.py`:
   - Додано імпорти `dj_database_url`
   - `ALLOWED_HOSTS = ["*"]` (тимчасово)
   - `DEBUG` змінено на змінну середовища
   - `DATABASES` налаштовано для PostgreSQL через `dj_database_url`
   - Додано `WhiteNoise` middleware
   - Додано `STATIC_ROOT` та `STATICFILES_STORAGE`

3. ✅ Створено `Procfile` з командою для запуску
4. ✅ Створено `runtime.txt` з версією Python
5. ✅ Створено `build.sh` для автоматичної збірки

## 🚀 Кроки для деплою на Render:

### 1. Підготуйте репозиторій

```bash
git add .
git commit -m "deploy ready: Render configuration"
git push origin main
```

### 2. Створіть Web Service на Render

1. Зайдіть на [render.com](https://render.com)
2. Натисніть "New +" → "Web Service"
3. Підключіть ваш GitHub репозиторій `vikmrnk/music_project`
4. Налаштуйте:
   - **Name**: `music-media` (або будь-яка назва)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh` (або залиште порожнім, Render використає автоматично)
   - **Start Command**: `gunicorn music_media.wsgi:application`
   - **Plan**: `Free`

### 3. Додайте PostgreSQL Database

1. Натисніть "New +" → "PostgreSQL"
2. Налаштуйте:
   - **Name**: `music-media-db`
   - **Plan**: `Free`
3. Після створення скопіюйте **Internal Database URL**

### 4. Налаштуйте Environment Variables

У налаштуваннях Web Service додайте:

- **DATABASE_URL**: Вставте Internal Database URL з PostgreSQL
- **SECRET_KEY**: Згенеруйте новий ключ (можна через `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- **DEBUG**: `False` (для production)

### 5. Запустіть міграції та створіть суперкористувача

Після успішного деплою:

1. Відкрийте **Shell** в Render Dashboard
2. Виконайте:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py import_articles  # Якщо потрібно імпортувати статті
```

### 6. Оновіть ALLOWED_HOSTS (опціонально)

Після отримання домену від Render, оновіть в `settings.py`:
```python
ALLOWED_HOSTS = ["your-app-name.onrender.com"]
```

## 📝 Додаткові поради:

- **Static files**: WhiteNoise автоматично обслуговує статичні файли
- **Media files**: Для production рекомендовано використовувати S3 або інший cloud storage
- **Logs**: Переглядайте логи в Render Dashboard для діагностики
- **Auto-deploy**: Render автоматично деплоїть при push в main гілку

## 🔒 Безпека:

- Не комітьте `.env` файли
- Використовуйте Environment Variables в Render
- Встановіть `DEBUG=False` для production
- Оновіть `SECRET_KEY` на унікальний

