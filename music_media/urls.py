"""
URL configuration for music_media project.
"""
import os
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

# Обслуговування медіа-файлів
# Якщо використовується Cloudinary, медіа-файли обслуговуються через Cloudinary
# Якщо ні - обслуговуємо локально (для розробки та production без Cloudinary)
cloudinary_url = os.environ.get('CLOUDINARY_URL', '')
# Завжди обслуговуємо медіа-файли локально, якщо Cloudinary не використовується
if not cloudinary_url:
    if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
        # Використовуємо serve для обслуговування медіа-файлів в production
        from django.views.static import serve
        from django.urls import re_path
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        ]

# Обробка помилок
handler404 = 'articles.views.handler404'
handler500 = 'articles.views.handler500'
