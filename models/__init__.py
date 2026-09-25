"""Пакет объектной модели предметной области InquiryDesk (ПР3).

Содержит классы основных сущностей: :class:`Category`, :class:`Status`,
:class:`User`, :class:`Inquiry`.
"""

from models.category import Category
from models.inquiry import Inquiry
from models.status import Status
from models.user import User

__all__ = ["Category", "Status", "User", "Inquiry"]
