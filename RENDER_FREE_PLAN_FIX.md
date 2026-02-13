# Рішення для безкоштовного плану Render (без Pre-Deploy Command)

## Проблема
Pre-Deploy Command доступний тільки для платних планів. На безкоштовному плані потрібні інші рішення.

## ✅ Рішення 1: Використати start.sh (Вже налаштовано)

Створено файл `start.sh`, який:
1. Виконує міграції перед запуском
2. Запускає gunicorn

**Procfile** вже оновлено для використання `start.sh`.

**Start Command в Render Dashboard:**
```
./start.sh
```

Або залиште порожнім - Render автоматично використає Procfile.

## ✅ Рішення 2: Виконати міграції вручну через Shell

1. Відкрийте **Shell** в Render Dashboard
2. Виконайте:
```bash
python manage.py migrate
python manage.py createsuperuser  # Якщо потрібно
python manage.py import_articles  # Якщо потрібно імпортувати статті
```

**Після цього міграції будуть застосовані**, і сайт працюватиме.

## ✅ Рішення 3: Оновити Start Command напряму

У налаштуваннях Render встановіть **Start Command**:
```bash
python manage.py migrate --noinput && gunicorn music_media.wsgi:application
```

## Рекомендація

**Найкраще рішення:** Використати `start.sh` (вже налаштовано). Просто переконайтеся, що в Render Dashboard:
- **Start Command**: `./start.sh` або залиште порожнім (використається Procfile)

## Після налаштування:

1. Закомітьте зміни:
```bash
git add .
git commit -m "fix: add start.sh for migrations on free plan"
git push origin master
```

2. Render автоматично перезапустить деплой
3. Міграції виконуватимуться автоматично при кожному запуску

