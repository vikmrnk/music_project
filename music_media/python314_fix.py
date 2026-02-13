"""
Monkey patch для виправлення проблеми сумісності Django з Python 3.14.

Проблема: Python 3.14 змінив поведінку super() в __copy__ методах,
що призводить до AttributeError при копіюванні RequestContext.

Цей патч виправляє метод __copy__ в RequestContext для коректної роботи з Python 3.14.
"""
import sys

# Застосовуємо патчі тільки для Python 3.14+
if sys.version_info >= (3, 14):
    import logging
    logger = logging.getLogger(__name__)
    try:
        from django.template.context import RequestContext, BaseContext, RenderContext
        logger.info("Python 3.14 fix: Successfully imported Django context classes")
    except ImportError as e:
        logger.error(f"Python 3.14 fix: Failed to import Django context classes: {e}")
        raise

    def _fixed_requestcontext_copy(self):
        """
        Виправлена версія __copy__ для RequestContext, яка працює з Python 3.14.
        Копіюємо всі атрибути через __dict__, щоб не пропустити жоден.
        """
        # Створюємо новий порожній екземпляр без виклику __init__
        duplicate = object.__new__(self.__class__)
        
        # Копіюємо всі атрибути з оригінального об'єкта
        # Використовуємо __dict__ для отримання всіх атрибутів
        for key, value in self.__dict__.items():
            if key == 'render_context':
                # render_context потребує нового екземпляра
                duplicate.render_context = RenderContext()
                # Копіюємо стан, якщо він існує
                if hasattr(value, '_state'):
                    duplicate.render_context._state = value._state.copy()
            elif key == 'dicts':
                # dicts потрібно скопіювати як список
                duplicate.dicts = value[:]
            else:
                # Всі інші атрибути копіюємо напряму
                setattr(duplicate, key, value)
        
        # Переконаємося, що render_context існує (на випадок, якщо його не було в __dict__)
        if not hasattr(duplicate, 'render_context'):
            duplicate.render_context = RenderContext()
        
        return duplicate

    def _fixed_basecontext_copy(self):
        """
        Виправлена версія __copy__ для BaseContext, яка працює з Python 3.14.
        Копіюємо всі атрибути через __dict__, щоб не пропустити жоден.
        """
        # Створюємо новий порожній екземпляр без виклику __init__
        duplicate = object.__new__(self.__class__)
        
        # Копіюємо всі атрибути з оригінального об'єкта
        for key, value in self.__dict__.items():
            if key == 'render_context':
                # render_context потребує нового екземпляра
                duplicate.render_context = RenderContext()
                # Копіюємо стан, якщо він існує
                if hasattr(value, '_state'):
                    duplicate.render_context._state = value._state.copy()
            elif key == 'dicts':
                # dicts потрібно скопіювати як список
                duplicate.dicts = value[:]
            else:
                # Всі інші атрибути копіюємо напряму
                setattr(duplicate, key, value)
        
        # Переконаємося, що render_context існує (на випадок, якщо його не було в __dict__)
        if not hasattr(duplicate, 'render_context'):
            duplicate.render_context = RenderContext()
        
        return duplicate

    # Застосовуємо патчі
    RequestContext.__copy__ = _fixed_requestcontext_copy
    BaseContext.__copy__ = _fixed_basecontext_copy
    logger.info("Python 3.14 fix: Successfully applied patches to RequestContext and BaseContext")

