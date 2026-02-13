# Виправлення проблеми з CSS на Render

## Можливі причини:

1. **collectstatic не виконується** - перевірте логи Build
2. **WhiteNoise не обслуговує файли** - перевірте налаштування
3. **Неправильний STATIC_ROOT** - перевірте шлях
4. **Файли не копіюються** - перевірте структуру

## Що виправлено:

1. ✅ Додано `WHITENOISE_MANIFEST_STRICT = False` - не вимагає всіх файлів
2. ✅ Оновлено `build.sh` з перевіркою файлів
3. ✅ Додано створення директорії staticfiles

## Перевірка в Render Dashboard:

### 1. Перевірте логи Build
У **Logs** шукайте:
```
Copying '/static/css/main.css'
...
X static files copied to '/staticfiles'
```

### 2. Перевірте Build Command
У налаштуваннях Web Service поле **Build Command** має містити:
```
./build.sh
```
Або повну команду з `collectstatic`.

### 3. Якщо CSS все ще не працює - спробуйте альтернативу

**Варіант А: Використати простіший storage**
У `settings.py` замініть:
```python
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```
І додайте в `urls.py`:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**Варіант Б: Перевірити через браузер**
Відкрийте в браузері:
```
https://your-app.onrender.com/static/css/main.css
```
Якщо файл не відкривається - проблема з collectstatic або WhiteNoise.

## Після виправлення:

1. Закомітьте зміни:
```bash
git add .
git commit -m "fix: improve static files configuration for Render"
git push origin master
```

2. Перевірте логи Build - має бути вивід про копіювання CSS файлів

