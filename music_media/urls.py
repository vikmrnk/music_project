"""
URL configuration for music_media project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from articles.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap

sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

# Обслуговування статичних файлів
# WhiteNoise обслуговує статичні файли в production через middleware
# Додаємо fallback для надійності
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обробка помилок
handler404 = 'articles.views.handler404'
handler500 = 'articles.views.handler500'
