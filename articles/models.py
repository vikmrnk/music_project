from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
import math

try:
    from unidecode import unidecode
except ImportError:
    # Простий transliteration для української, якщо unidecode не встановлено
    UKR_TO_LAT = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
        'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'IE',
        'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ю': 'Iu', 'Я': 'Ia'
    }
    
    def unidecode(text):
        return ''.join(UKR_TO_LAT.get(char, char) for char in text)


class Category(models.Model):
    """Категорія контенту (новини, інтервʼю, рецензії тощо)"""
    name = models.CharField(max_length=100, verbose_name="Назва")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Опис")
    order = models.IntegerField(default=0, verbose_name="Порядок сортування")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Теги для гнучкої фільтрації та SEO"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Назва")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:tag_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)


class AuthorProfile(models.Model):
    """Профіль автора"""
    ROLE_CHOICES = [
        ('editor', 'Редактор'),
        ('author', 'Автор'),
        ('admin', 'Адміністратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile', verbose_name="Користувач")
    bio = models.TextField(blank=True, verbose_name="Біографія")
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name="Аватар")
    social_links = models.JSONField(default=dict, blank=True, verbose_name="Соціальні мережі")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='author', verbose_name="Роль")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профіль автора"
        verbose_name_plural = "Профілі авторів"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def get_absolute_url(self):
        return reverse('articles:author_detail', kwargs={'username': self.user.username})


class Article(models.Model):
    """Стаття/публікація"""
    STATUS_CHOICES = [
        ('draft', 'Чернетка'),
        ('published', 'Опубліковано'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    short_description = models.TextField(max_length=300, verbose_name="Короткий опис")
    content = models.TextField(verbose_name="Контент")
    
    # Зв'язки
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name="Категорія")
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name="Теги")
    
    # Медіа
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Головне зображення")
    featured_video = models.FileField(upload_to='articles/videos/', blank=True, null=True, verbose_name="Відео (файл)")
    video_url = models.URLField(blank=True, max_length=500, verbose_name="Відео URL (YouTube/Vimeo)")
    
    # Метадані
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta заголовок")
    meta_description = models.TextField(max_length=300, blank=True, verbose_name="Meta опис")
    
    # Статистика
    reading_time = models.IntegerField(default=0, verbose_name="Час читання (хв)")
    views_count = models.IntegerField(default=0, verbose_name="Переглядів")
    
    # Статус
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендована")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    
    # Дати
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Опубліковано")

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        
        # Автоматичний розрахунок часу читання
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, math.ceil(word_count / 200))  # ~200 слів на хвилину
        
        # Встановлення дати публікації
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)

    def increment_views(self):
        """Збільшити кількість переглядів"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_video_embed_url(self):
        """Конвертує YouTube/Vimeo URL в embed формат"""
        if not self.video_url:
            return None
        
        url = self.video_url.strip()
        
        # YouTube
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtube.com/embed/' in url:
            return url  # Вже embed формат
        
        # Vimeo
        elif 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        elif 'player.vimeo.com/video/' in url:
            return url  # Вже embed формат
        
        # Якщо не вдалося розпізнати, повертаємо оригінальний URL
        return url


class NewsletterSubscriber(models.Model):
    """Підписник на розсилку"""
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Підписник"
        verbose_name_plural = "Підписники"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

