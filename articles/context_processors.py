"""
Context processors для глобального доступу до даних
"""
from articles.models import Category
from django.db import OperationalError, DatabaseError


def categories(request):
    """Додати всі активні категорії до контексту"""
    # Не додаємо категорії для адмінки, щоб уникнути помилок
    if request.path.startswith('/admin/'):
        return {'categories': []}
    
    try:
        return {
            'categories': Category.objects.filter(is_active=True).order_by('order', 'name')
        }
    except (OperationalError, DatabaseError):
        # Якщо таблиці ще не створені (під час першого деплою або міграції не застосовані)
        return {'categories': []}
    except Exception:
        # Будь-яка інша помилка - повертаємо порожній список
        return {'categories': []}

