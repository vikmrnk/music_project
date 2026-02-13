"""
Команда для створення суперюзера
python manage.py create_superuser
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Створює суперкористувача, якщо він не існує'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'адмін'
        email = 'admin@example.com'
        password = 'адмін123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'✓ Суперкористувач "{username}" вже існує'))
            # Переконаємося, що він має права суперюзера
            user = User.objects.get(username=username)
            if not user.is_superuser or not user.is_staff:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Права суперюзера оновлено для "{username}"'))
        else:
            try:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Суперкористувач створено: {username} / {password}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Помилка створення суперюзера: {e}'))
                # Спробуємо створити вручну
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Суперкористувач створено вручну: {username} / {password}'))
                except Exception as e2:
                    self.stdout.write(self.style.ERROR(f'✗ Помилка створення суперюзера вручну: {e2}'))

