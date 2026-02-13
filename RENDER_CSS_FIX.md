# Виправлення проблеми з CSS на Render

## Проблема
CSS файли не підвантажуються на Render.

## Що виправлено:

1. ✅ Додано додаткові налаштування WhiteNoise:
   - `WHITENOISE_USE_FINDERS = True` - дозволяє знаходити файли в STATICFILES_DIRS
   - `WHITENOISE_AUTOREFRESH = True` - автоматично оновлює файли

2. ✅ Оновлено `build.sh`:
   - Додано `--clear` до `collectstatic` для очищення старих файлів

## Перевірка в Render Dashboard:

### 1. Переконайтеся, що Build Command виконується
У налаштуваннях Web Service перевірте, що **Build Command** містить:
```
./build.sh
```
Або:
```
pip install -r requirements.txt && python manage.py collectstatic --noinput --clear
```

### 2. Перевірте логи Build
У Render Dashboard відкрийте **Logs** і перевірте, чи виконується:
```
python manage.py collectstatic --noinput --clear
```

Має бути вивід типу:
```
Copying '/static/css/main.css'
...
X static files copied to '/staticfiles'
```

### 3. Якщо CSS все ще не працює

**Варіант А: Виконайте collectstatic вручну через Shell**
1. Відкрийте **Shell** в Render Dashboard
2. Виконайте:
```bash
python manage.py collectstatic --noinput --clear
ls -la staticfiles/static/css/  # Перевірте, чи файли там
```

**Варіант Б: Перевірте STATIC_ROOT**
У Shell виконайте:
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)
>>> print(settings.STATIC_URL)
```

**Варіант В: Перевірте, чи WhiteNoise працює**
У браузері відкрийте:
```
https://your-app.onrender.com/static/css/main.css
```

Якщо файл не відкривається, WhiteNoise не обслуговує статичні файли.

## Після виправлення:

1. Закомітьте зміни:
```bash
git add .
git commit -m "fix: improve WhiteNoise configuration for static files"
git push origin master
```

2. Render автоматично перезапустить деплой
3. Перевірте логи Build - має бути вивід про копіювання статичних файлів

