"""
Сервісний рівень для роботи зі статтями
Чистий код без бізнес-логіки в views
"""
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q, Count
from articles.models import Article, Category, Tag


class ArticleService:
    """Сервіс для роботи зі статтями"""

    @staticmethod
    def get_latest_articles(limit=10, category_slug=None):
        """
        Отримати останні опубліковані статті
        """
        cache_key = f'latest_articles_{category_slug or "all"}_{limit}'
        articles = cache.get(cache_key)
        
        if articles is None:
            queryset = Article.objects.filter(
                status='published'
            ).select_related('author', 'category').prefetch_related('tags')
            
            if category_slug:
                queryset = queryset.filter(category__slug=category_slug)
            
            articles = list(queryset[:limit])
            cache.set(cache_key, articles, 300)  # Кеш на 5 хвилин
        
        return articles

    @staticmethod
    def get_featured_articles(limit=5):
        """
        Отримати рекомендовані статті
        """
        cache_key = f'featured_articles_{limit}'
        articles = cache.get(cache_key)
        
        if articles is None:
            articles = list(
                Article.objects.filter(
                    status='published',
                    is_featured=True
                ).select_related('author', 'category').prefetch_related('tags')[:limit]
            )
            cache.set(cache_key, articles, 600)  # Кеш на 10 хвилин
        
        return articles

    @staticmethod
    def get_articles_by_category(category_slug, page=1, per_page=12):
        """
        Отримати статті за категорією з пагінацією
        """
        try:
            category = Category.objects.get(slug=category_slug, is_active=True)
        except Category.DoesNotExist:
            return None, None
        
        articles = Article.objects.filter(
            category=category,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
        
        paginator = Paginator(articles, per_page)
        page_obj = paginator.get_page(page)
        
        return page_obj, category

    @staticmethod
    def get_articles_by_tag(tag_slug, page=1, per_page=12):
        """
        Отримати статті за тегом з пагінацією
        """
        try:
            tag = Tag.objects.get(slug=tag_slug)
        except Tag.DoesNotExist:
            return None, None
        
        articles = Article.objects.filter(
            tags=tag,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
        
        paginator = Paginator(articles, per_page)
        page_obj = paginator.get_page(page)
        
        return page_obj, tag

    @staticmethod
    def get_popular_articles(limit=10, days=30):
        """
        Отримати популярні статті за кількістю переглядів
        """
        from django.utils import timezone
        from datetime import timedelta
        
        cache_key = f'popular_articles_{days}_{limit}'
        articles = cache.get(cache_key)
        
        if articles is None:
            date_threshold = timezone.now() - timedelta(days=days)
            articles = list(
                Article.objects.filter(
                    status='published',
                    published_at__gte=date_threshold
                ).select_related('author', 'category').prefetch_related('tags')
                .order_by('-views_count')[:limit]
            )
            cache.set(cache_key, articles, 600)  # Кеш на 10 хвилин
        
        return articles

    @staticmethod
    def get_article_by_slug(slug):
        """
        Отримати статтю за slug
        """
        try:
            article = Article.objects.select_related(
                'author', 'category'
            ).prefetch_related('tags').get(slug=slug, status='published')
            return article
        except Article.DoesNotExist:
            return None

    @staticmethod
    def increment_views(article):
        """
        Збільшити кількість переглядів статті
        """
        article.increment_views()
        # Очистити кеш популярних статей
        cache.delete_many([
            'popular_articles_30_10',
            'popular_articles_7_10',
        ])

    @staticmethod
    def search_articles(query, page=1, per_page=12):
        """
        Пошук статей за запитом
        """
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(content__icontains=query),
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').distinct()
        
        paginator = Paginator(articles, per_page)
        page_obj = paginator.get_page(page)
        
        return page_obj

    @staticmethod
    def get_articles_by_author(username, page=1, per_page=12):
        """
        Отримати статті автора з пагінацією
        """
        from django.contrib.auth.models import User
        
        try:
            author = User.objects.get(username=username)
        except User.DoesNotExist:
            return None, None
        
        articles = Article.objects.filter(
            author=author,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
        
        paginator = Paginator(articles, per_page)
        page_obj = paginator.get_page(page)
        
        return page_obj, author

    @staticmethod
    def get_related_articles(article, limit=4):
        """
        Отримати схожі статті (за категорією та тегами)
        """
        related = Article.objects.filter(
            Q(category=article.category) | Q(tags__in=article.tags.all()),
            status='published'
        ).exclude(id=article.id).select_related('author', 'category').prefetch_related('tags').distinct()[:limit]
        
        return list(related)

