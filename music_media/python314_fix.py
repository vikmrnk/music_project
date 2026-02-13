"""
Monkey patch для виправлення проблеми сумісності Django з Python 3.14.

Проблема: Python 3.14 змінив поведінку super() в __copy__ методах,
що призводить до AttributeError при копіюванні RequestContext.

Цей патч виправляє метод __copy__ в RequestContext для коректної роботи з Python 3.14.
"""
import sys
from django.template.context import RequestContext, BaseContext


def _fixed_requestcontext_copy(self):
    """
    Виправлена версія __copy__ для RequestContext, яка працює з Python 3.14.
    Використовуємо простий підхід - створюємо порожній екземпляр і копіюємо атрибути.
    """
    # Створюємо новий порожній екземпляр без виклику __init__
    # Це уникає повторного виклику context processors
    duplicate = object.__new__(self.__class__)
    
    # Копіюємо dicts напряму (це найважливіший атрибут)
    duplicate.dicts = self.dicts[:]
    
    # Копіюємо request (обов'язковий атрибут для RequestContext)
    duplicate.request = self.request
    
    # Копіюємо current_app, якщо він існує (опціональний атрибут)
    if hasattr(self, 'current_app'):
        duplicate.current_app = self.current_app
    
    return duplicate


def _fixed_basecontext_copy(self):
    """
    Виправлена версія __copy__ для BaseContext, яка працює з Python 3.14.
    """
    # Створюємо новий екземпляр класу
    duplicate = self.__class__()
    # Копіюємо dicts напряму, без використання super()
    duplicate.dicts = self.dicts[:]
    return duplicate


# Застосовуємо патчі тільки для Python 3.14+
if sys.version_info >= (3, 14):
    RequestContext.__copy__ = _fixed_requestcontext_copy
    BaseContext.__copy__ = _fixed_basecontext_copy

