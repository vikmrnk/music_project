# Generated manually to remove video_url field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_featured_video_article_video_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='video_url',
        ),
    ]

