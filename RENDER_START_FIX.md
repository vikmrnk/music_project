# Виправлення помилки запуску на Render

## Проблема
Render намагається запустити `gunicorn app:app` замість правильної команди з Procfile.

## Рішення

### Варіант 1: Перевірте Start Command в Render Dashboard

1. Зайдіть в налаштування вашого Web Service на Render
2. Знайдіть поле **Start Command**
3. Переконайтеся, що там вказано:
   ```
   gunicorn music_media.wsgi:application
   ```
4. Або залиште поле порожнім - Render автоматично використає команду з Procfile

### Варіант 2: Перевірте Procfile

Procfile має містити:
```
web: gunicorn music_media.wsgi:application
```

## Якщо проблема залишається:

1. Переконайтеся, що Procfile знаходиться в корені проєкту
2. Перевірте, що файл називається саме `Procfile` (без розширення)
3. У налаштуваннях Render встановіть:
   - **Start Command**: `gunicorn music_media.wsgi:application`
   - Або залиште порожнім для використання Procfile

## Після виправлення:

1. Закомітьте зміни (якщо змінювали Procfile):
```bash
git add Procfile
git commit -m "fix: correct Procfile for Render"
git push origin master
```

2. Render автоматично перезапустить деплой

