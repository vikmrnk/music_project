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
    """
    # Створюємо новий екземпляр RequestContext з тими ж параметрами
    # Використовуємо перший dict як базовий контекст
    base_dict = self.dicts[0] if self.dicts else {}
    duplicate = self.__class__(
        self.request,
        base_dict,
        current_app=self.current_app
    )
    # Копіюємо всі dicts (включаючи ті, що додані через context processors)
    # Це важливо, бо context processors додають додаткові dicts
    duplicate.dicts = self.dicts[:]
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

