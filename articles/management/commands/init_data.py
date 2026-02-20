"""
Команда для ініціалізації даних (міграції + імпорт статей, якщо база порожня)
python manage.py init_data
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from articles.models import Article, Category
import os


class Command(BaseCommand):
    help = 'Ініціалізує дані: міграції + імпорт статей, якщо база порожня'

    def handle(self, *args, **options):
        # Виконати міграції
        self.stdout.write('Виконання міграцій...')
        call_command('migrate', '--noinput')
        
        # Перевірити, чи є дані в базі
        has_categories = Category.objects.exists()
        has_articles = Article.objects.exists()
        
        # Перевірити, чи використовується SQLite (тимчасова база на Render)
        # Якщо використовується SQLite, не виконуємо автоматичний імпорт
        # щоб уникнути втрати даних, створених через адмінку при spin down
        database_url = os.environ.get('DATABASE_URL', '')
        is_sqlite = False
        
        if database_url:
            is_sqlite = 'sqlite' in database_url.lower()
        else:
            # Якщо DATABASE_URL не встановлено, перевіряємо налаштування Django
            from django.conf import settings
            db_engine = settings.DATABASES['default'].get('ENGINE', '')
            is_sqlite = 'sqlite' in db_engine.lower()
        
        # Імпортуємо статті тільки якщо:
        # 1. База даних порожня (немає категорій або статей)
        # 2. І НЕ використовується SQLite (щоб уникнути втрати даних при spin down)
        # На Render з SQLite база скидається при spin down, тому не імпортуємо автоматично
        if not has_categories or not has_articles:
            if is_sqlite:
                self.stdout.write(
                    self.style.WARNING(
                        '⚠ Використовується SQLite. Автоматичний імпорт пропущено, '
                        'щоб уникнути втрати даних, створених через адмінку.\n'
                        'SQLite на Render скидається при spin down, тому статті, створені через адмінку, '
                        'будуть втрачені.\n\n'
                        'Для постійного зберігання даних налаштуйте PostgreSQL на Render:\n'
                        '1. Створіть PostgreSQL базу даних на Render (Dashboard → New → PostgreSQL)\n'
                        '2. Додайте DATABASE_URL до Environment Variables вашого Web Service\n'
                        '3. Перезапустіть сервіс\n\n'
                        'Або виконайте імпорт вручну: python manage.py import_articles --append'
                    )
                )
            else:
                self.stdout.write('База даних порожня. Імпорт статей...')
                # Використовуємо --append, щоб не видаляти існуючі дані (якщо вони є)
                call_command('import_articles', '--append')
                self.stdout.write(self.style.SUCCESS('✓ Дані успішно імпортовано!'))
        else:
            self.stdout.write('Дані вже присутні в базі. Пропущено імпорт.')

