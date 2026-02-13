"""
Monkey patch для виправлення проблеми сумісності Django з Python 3.14.

Проблема: Python 3.14 змінив поведінку super() в __copy__ методах,
що призводить до AttributeError при копіюванні RequestContext.

Цей патч виправляє метод __copy__ в RequestContext для коректної роботи з Python 3.14.
"""
import sys

# Застосовуємо патчі тільки для Python 3.14+
if sys.version_info >= (3, 14):
    from django.template.context import RequestContext, BaseContext, RenderContext

    def _fixed_requestcontext_copy(self):
        """
        Виправлена версія __copy__ для RequestContext, яка працює з Python 3.14.
        Копіюємо всі атрибути, включаючи render_context з BaseContext.
        """
        # Створюємо новий порожній екземпляр без виклику __init__
        duplicate = object.__new__(self.__class__)
        
        # Ініціалізуємо render_context (це робиться в BaseContext.__init__)
        duplicate.render_context = RenderContext()
        
        # Копіюємо dicts напряму (це найважливіший атрибут)
        duplicate.dicts = self.dicts[:]
        
        # Копіюємо request (обов'язковий атрибут для RequestContext)
        duplicate.request = self.request
        
        # Копіюємо current_app, якщо він існує (опціональний атрибут)
        if hasattr(self, 'current_app'):
            duplicate.current_app = self.current_app
        
        # Копіюємо render_context стан, якщо він існує та має _state
        if hasattr(self, 'render_context') and hasattr(self.render_context, '_state'):
            duplicate.render_context._state = self.render_context._state.copy()
        
        return duplicate

    def _fixed_basecontext_copy(self):
        """
        Виправлена версія __copy__ для BaseContext, яка працює з Python 3.14.
        """
        # Створюємо новий порожній екземпляр без виклику __init__
        duplicate = object.__new__(self.__class__)
        
        # Ініціалізуємо render_context (це робиться в BaseContext.__init__)
        duplicate.render_context = RenderContext()
        
        # Копіюємо dicts напряму, без використання super()
        duplicate.dicts = self.dicts[:]
        
        # Копіюємо render_context стан, якщо він існує
        if hasattr(self, 'render_context') and hasattr(self.render_context, '_state'):
            duplicate.render_context._state = self.render_context._state.copy()
        
        return duplicate

    # Застосовуємо патчі
    RequestContext.__copy__ = _fixed_requestcontext_copy
    BaseContext.__copy__ = _fixed_basecontext_copy

