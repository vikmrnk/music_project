"""
Команда для оновлення slugs з transliteration
python manage.py update_slugs
"""
from django.core.management.base import BaseCommand
from articles.models import Tag, Category, Article
from django.utils.text import slugify

try:
    from unidecode import unidecode
    HAS_UNIDECODE = True
except ImportError:
    HAS_UNIDECODE = False
    # Простий transliteration для української
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
    
    def simple_transliterate(text):
        result = ''
        for char in text:
            result += UKR_TO_LAT.get(char, char)
        return result


class Command(BaseCommand):
    help = 'Оновлює slugs для всіх моделей з transliteration'

    def handle(self, *args, **options):
        if HAS_UNIDECODE:
            translit_func = unidecode
        else:
            translit_func = simple_transliterate
        
        # Оновити теги
        updated_tags = 0
        for tag in Tag.objects.all():
            old_slug = tag.slug
            new_slug = slugify(translit_func(tag.name))
            if old_slug != new_slug:
                tag.slug = new_slug
                tag.save(update_fields=['slug'])
                updated_tags += 1
                self.stdout.write(f'  ✓ Оновлено тег: {tag.name} ({old_slug} → {new_slug})')
        
        # Оновити категорії
        updated_categories = 0
        for category in Category.objects.all():
            old_slug = category.slug
            new_slug = slugify(translit_func(category.name))
            if old_slug != new_slug:
                category.slug = new_slug
                category.save(update_fields=['slug'])
                updated_categories += 1
                self.stdout.write(f'  ✓ Оновлено категорію: {category.name} ({old_slug} → {new_slug})')
        
        # Оновити статті
        updated_articles = 0
        for article in Article.objects.all():
            old_slug = article.slug
            new_slug = slugify(translit_func(article.title))
            if old_slug != new_slug:
                article.slug = new_slug
                article.save(update_fields=['slug'])
                updated_articles += 1
                self.stdout.write(f'  ✓ Оновлено статтю: {article.title} ({old_slug} → {new_slug})')
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Оновлено: {updated_tags} тегів, {updated_categories} категорій, {updated_articles} статей'
        ))

