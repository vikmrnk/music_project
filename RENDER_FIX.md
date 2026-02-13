# Виправлення помилки деплою на Render

## Проблема
Render використовує Python 3.14.3 замість вказаного в `runtime.txt` Python 3.11.9, і Pillow 10.2.0 не сумісний з Python 3.14.

## Що виправлено:

1. ✅ Оновлено `Pillow` з 10.2.0 до 11.0.0 (підтримує Python 3.14)
2. ✅ Додано оновлення pip в `build.sh`

## Додаткові кроки в Render Dashboard:

### Варіант 1: Вказати версію Python вручну
1. Зайдіть в налаштування Web Service на Render
2. Знайдіть поле **Environment** або **Python Version**
3. Встановіть: `python-3.11.9` або `python-3.12`

### Варіант 2: Використати Python 3.14 (рекомендовано)
Оскільки Render використовує Python 3.14, краще оновити `runtime.txt`:

```txt
python-3.14.3
```

Або видаліть `runtime.txt` взагалі - Render автоматично вибере сумісну версію.

## Після виправлення:

1. Закомітьте зміни:
```bash
git add .
git commit -m "fix: update Pillow to 11.0.0 for Python 3.14 compatibility"
git push origin master
```

2. Render автоматично перезапустить деплой

## Альтернативне рішення (якщо все ще не працює):

Оновіть всі залежності до останніх версій:
```bash
pip install --upgrade Django Pillow django-ckeditor django-crispy-forms crispy-bootstrap5 python-decouple unidecode gunicorn dj-database-url psycopg2-binary whitenoise
pip freeze > requirements.txt
```

