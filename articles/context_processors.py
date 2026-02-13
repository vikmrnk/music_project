"""
Context processors для глобального доступу до даних
"""
from articles.models import Category
from django.db import OperationalError


def categories(request):
    """Додати всі активні категорії до контексту"""
    try:
        return {
            'categories': Category.objects.filter(is_active=True).order_by('order', 'name')
        }
    except OperationalError:
        # Якщо таблиці ще не створені (під час першого деплою або міграції не застосовані)
        return {'categories': []}

