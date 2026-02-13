"""
Команда для ініціалізації даних (міграції + імпорт статей, якщо база порожня)
python manage.py init_data
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from articles.models import Article, Category


class Command(BaseCommand):
    help = 'Ініціалізує дані: міграції + імпорт статей, якщо база порожня'

    def handle(self, *args, **options):
        # Виконати міграції
        self.stdout.write('Виконання міграцій...')
        call_command('migrate', '--noinput')
        
        # Перевірити, чи є дані в базі
        has_categories = Category.objects.exists()
        has_articles = Article.objects.exists()
        
        if not has_categories or not has_articles:
            self.stdout.write('База даних порожня. Імпорт статей...')
            # Використовуємо --append, щоб не видаляти існуючі дані (якщо вони є)
            call_command('import_articles', '--append')
            self.stdout.write(self.style.SUCCESS('✓ Дані успішно імпортовано!'))
        else:
            self.stdout.write('Дані вже присутні в базі. Пропущено імпорт.')

