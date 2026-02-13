"""
Команда для створення тестових даних
python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from articles.models import Category, Tag, Article, AuthorProfile
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Створює тестові дані для сайту'

    def handle(self, *args, **options):
        self.stdout.write('Створення тестових даних...')
        
        # Створити категорії
        categories_data = [
            {'name': 'Новини', 'slug': 'news', 'order': 1},
            {'name': 'Інтервʼю', 'slug': 'interviews', 'order': 2},
            {'name': 'Рецензії', 'slug': 'reviews', 'order': 3},
            {'name': 'Аналітика', 'slug': 'analytics', 'order': 4},
            {'name': 'Добірки', 'slug': 'playlists', 'order': 5},
            {'name': 'Авторські колонки', 'slug': 'columns', 'order': 6},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'  ✓ Створено категорію: {category.name}')
        
        # Створити теги
        tags_data = ['рок', 'поп', 'джаз', 'електронна', 'класична', 'українська', 'альбом', 'концерт']
        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            tags[tag_name] = tag
            if created:
                self.stdout.write(f'  ✓ Створено тег: {tag.name}')
        
        # Створити користувача та профіль автора
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Адмін',
                'last_name': 'Сайту',
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('  ✓ Створено користувача: admin')
        
        author_profile, created = AuthorProfile.objects.get_or_create(
            user=user,
            defaults={
                'bio': 'Головний редактор Music Media',
                'role': 'editor',
            }
        )
        
        # Створити тестові статті
        sample_articles = [
            {
                'title': 'Новий альбом від українського виконавця',
                'category': categories['news'],
                'tags': [tags['українська'], tags['альбом']],
                'is_featured': True,
            },
            {
                'title': 'Ексклюзивне інтервʼю з відомим музикантом',
                'category': categories['interviews'],
                'tags': [tags['рок']],
                'is_featured': False,
            },
            {
                'title': 'Рецензія на останній альбом',
                'category': categories['reviews'],
                'tags': [tags['альбом'], tags['поп']],
                'is_featured': False,
            },
        ]
        
        for i, article_data in enumerate(sample_articles):
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'slug': f'sample-article-{i+1}',
                    'short_description': f'Короткий опис статті "{article_data["title"]}"',
                    'content': f'Повний текст статті "{article_data["title"]}". ' * 50,
                    'author': user,
                    'category': article_data['category'],
                    'status': 'published',
                    'is_featured': article_data['is_featured'],
                    'published_at': timezone.now() - timedelta(days=i),
                }
            )
            
            if created:
                article.tags.set(article_data['tags'])
                self.stdout.write(f'  ✓ Створено статтю: {article.title}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Тестові дані успішно створені!'))
        self.stdout.write('\nДля входу в адмін-панель використайте:')
        self.stdout.write('  Логін: admin')
        self.stdout.write('  Пароль: admin123')

