"""
Кастомний storage для Cloudinary
"""
from cloudinary_storage.storage import MediaCloudinaryStorage
import mimetypes


class VideoCloudinaryStorage(MediaCloudinaryStorage):
    """
    Storage для файлів на Cloudinary.
    Автоматично визначає відео файли за шляхом або типом і встановлює resource_type='video'
    """
    def _save(self, name, content):
        """
        Зберігає файл на Cloudinary, автоматично визначаючи тип
        """
        # Перевіряємо, чи файл у папці videos/ - це відео
        is_video = 'videos/' in name
        
        # Якщо не в папці videos/, перевіряємо тип файлу
        if not is_video:
            content_type = getattr(content, 'content_type', None)
            if not content_type:
                # Спробуємо визначити за розширенням
                content_type, _ = mimetypes.guess_type(name)
            
            # Перевіряємо, чи це відео файл
            if content_type:
                is_video = content_type.startswith('video/')
            else:
                # Перевіряємо за розширенням
                video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v']
                is_video = any(name.lower().endswith(ext) for ext in video_extensions)
        
        # Якщо це відео, використовуємо Cloudinary API напряму з resource_type='video'
        if is_video:
            # Імпортуємо cloudinary тільки коли потрібно
            import cloudinary.uploader
            
            # Використовуємо Cloudinary API напряму для завантаження відео
            options = {
                'resource_type': 'video',
                'folder': 'articles/videos/',
            }
            # Перевіряємо, чи content має метод read
            if hasattr(content, 'read'):
                # Якщо це файловий об'єкт, читаємо його
                content.seek(0)  # Повертаємося на початок файлу
                file_data = content.read()
                response = cloudinary.uploader.upload(file_data, **options)
            else:
                # Якщо це вже дані, використовуємо напряму
                response = cloudinary.uploader.upload(content, **options)
            
            # Повертаємо public_id як ім'я файлу
            # Cloudinary повертає public_id у форматі: folder/public_id або просто public_id
            public_id = response.get('public_id', name)
            # Видаляємо розширення файлу з public_id, якщо воно є
            if '.' in public_id:
                public_id = public_id.rsplit('.', 1)[0]
            return public_id
        else:
            # Для інших файлів (зображення тощо) використовуємо стандартний метод
            return super()._save(name, content)
    
    def url(self, name):
        """
        Генерує правильний URL для файлу з Cloudinary
        Для відео використовуємо resource_type='video'
        """
        # Перевіряємо, чи це відео файл
        is_video = 'videos/' in name or any(name.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v'])
        
        if is_video:
            # Для відео використовуємо Cloudinary API для генерації правильного URL
            try:
                import cloudinary.utils
                # Генеруємо URL для відео з resource_type='video'
                video_url = cloudinary.utils.cloudinary_url(name, resource_type='video')[0]
                return video_url
            except Exception:
                # Якщо не вдалося, використовуємо стандартний метод
                # Але замінюємо /image/upload/ на /video/upload/ якщо потрібно
                url = super().url(name)
                if '/image/upload/' in url:
                    url = url.replace('/image/upload/', '/video/upload/')
                return url
        else:
            # Для інших файлів використовуємо стандартний метод
            return super().url(name)

