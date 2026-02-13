"""
Context processors для глобального доступу до даних
"""
from articles.models import Category


def categories(request):
    """Додати всі активні категорії до контексту"""
    return {
        'categories': Category.objects.filter(is_active=True).order_by('order', 'name')
    }

