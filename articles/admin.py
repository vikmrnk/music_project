from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Tag, AuthorProfile, Article, NewsletterSubscriber


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'article_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def article_count(self, obj):
        try:
            if obj and obj.pk:
                return obj.articles.filter(status='published').count()
            return 0
        except (AttributeError, Exception) as e:
            return 0
    article_count.short_description = 'Статей'
    article_count.admin_order_field = None  # Вимкнути сортування


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def article_count(self, obj):
        try:
            if obj and obj.pk:
                return obj.articles.filter(status='published').count()
            return 0
        except (AttributeError, Exception) as e:
            return 0
    article_count.short_description = 'Статей'
    article_count.admin_order_field = None  # Вимкнути сортування


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'article_count', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    fieldsets = (
        ('Основна інформація', {
            'fields': ('user', 'role', 'bio', 'avatar')
        }),
        ('Соціальні мережі', {
            'fields': ('social_links',),
            'description': 'JSON формат: {"twitter": "url", "facebook": "url", "instagram": "url"}'
        }),
    )

    def article_count(self, obj):
        try:
            if obj and obj.user and hasattr(obj.user, 'pk') and obj.user.pk:
                return obj.user.articles.filter(status='published').count()
            return 0
        except (AttributeError, Exception) as e:
            return 0
    article_count.short_description = 'Статей'
    article_count.admin_order_field = None  # Вимкнути сортування


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views_count', 'published_at', 'preview_image']
    list_filter = ['status', 'is_featured', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'reading_time', 'created_at', 'updated_at']
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Контент', {
            'fields': ('short_description', 'content', 'featured_image')
        }),
        ('Відео', {
            'fields': ('video_url', 'featured_video'),
            'description': 'Можна додати відео через URL (YouTube/Vimeo) або завантажити файл. Якщо вказано обидва, пріоритет має URL.',
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Статистика', {
            'fields': ('views_count', 'reading_time', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def preview_image(self, obj):
        try:
            if obj.featured_image and obj.featured_image.url:
                return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.featured_image.url)
            return '-'
        except Exception:
            return '-'
    preview_image.short_description = 'Зображення'

    def save_model(self, request, obj, form, change):
        try:
            if not change and not obj.author:  # Нова стаття без автора
                obj.author = request.user
            super().save_model(request, obj, form, change)
        except Exception as e:
            # Логуємо помилку, але не зупиняємо процес
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Помилка збереження статті: {e}')
            # Пробуємо зберегти без автоматичного призначення автора
            if not change and not obj.author:
                # Якщо не вдалося встановити автора, залишаємо як є
                pass
            super().save_model(request, obj, form, change)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']

