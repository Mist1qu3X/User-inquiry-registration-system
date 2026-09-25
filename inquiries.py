"""Операции над обращениями пользователей (ПР3, объектная модель).

Функции работают со списком объектов :class:`models.Inquiry`. Три функции
``can_register_inquiry``, ``get_inquiry_state`` и ``format_inquiry_card``
перенесены без изменений из ПР1 и продолжают использоваться в проекте.
"""

from datetime import date

from models import Inquiry

# Максимально допустимая длина темы обращения (в символах).
MAX_SUBJECT_LENGTH = 100


# --- Базовые функции, перенесённые из ПР1 -------------------------------

def can_register_inquiry(subject: str, category_active: bool) -> bool:
    """Проверить, можно ли зарегистрировать обращение."""
    subject = subject.strip()
    if not subject:
        return False
    if len(subject) > MAX_SUBJECT_LENGTH:
        return False
    return bool(category_active)


def get_inquiry_state(is_closed: bool, replies_count: int) -> str:
    """Определить текстовое состояние обращения по его признакам."""
    if is_closed:
        return "Закрыто"
    if replies_count > 0:
        return "В работе"
    return "Новое"


def format_inquiry_card(subject: str, author: str, state: str,
                        created: date) -> str:
    """Сформировать краткую карточку обращения одной строкой."""
    subject = subject.strip()
    return f"[{created:%d.%m.%Y}] {subject} — {author} ({state})"


# --- Операции над коллекцией обращений -----------------------------------

def next_inquiry_id(inquiries: list) -> int:
    """Вернуть следующий свободный идентификатор обращения."""
    if not inquiries:
        return 1
    return max(inquiry.id for inquiry in inquiries) + 1


def add_inquiry(inquiries: list, subject: str, text: str, category, status,
                author, created: str = None) -> Inquiry:
    """Создать обращение, добавить его в список и вернуть объект."""
    subject = subject.strip()
    if not subject:
        raise ValueError("Тема обращения не может быть пустой.")
    if len(subject) > MAX_SUBJECT_LENGTH:
        raise ValueError("Тема обращения слишком длинная.")
    inquiry = Inquiry(
        next_inquiry_id(inquiries), subject, text.strip(),
        category, status, author, created,
    )
    inquiries.append(inquiry)
    return inquiry


def find_inquiry(inquiries: list, inquiry_id: int):
    """Найти обращение по идентификатору или вернуть ``None``."""
    for inquiry in inquiries:
        if inquiry.id == inquiry_id:
            return inquiry
    return None


def find_inquiries(inquiries: list, query: str) -> list:
    """Найти обращения, в теме которых встречается ``query``."""
    query = query.strip().lower()
    return [item for item in inquiries if query in item.subject.lower()]


def filter_inquiries_by_category(inquiries: list, category_id: int) -> list:
    """Отобрать обращения указанной категории (по её идентификатору)."""
    return [
        item for item in inquiries
        if item.category is not None and item.category.id == category_id
    ]


def filter_inquiries_by_status(inquiries: list, status_code: str) -> list:
    """Отобрать обращения с указанным статусом (по его коду)."""
    return [
        item for item in inquiries
        if item.status is not None and item.status.code == status_code
    ]


def change_status(inquiries: list, inquiry_id: int, status) -> bool:
    """Изменить статус обращения. Вернуть ``True``, если обращение найдено."""
    inquiry = find_inquiry(inquiries, inquiry_id)
    if inquiry is None:
        return False
    inquiry.change_status(status)
    return True


def close_inquiry(inquiries: list, inquiry_id: int, closed_status) -> bool:
    """Закрыть обращение, присвоив ему финальный статус."""
    inquiry = find_inquiry(inquiries, inquiry_id)
    if inquiry is None:
        return False
    inquiry.close(closed_status)
    return True


def sort_inquiries_by_date(inquiries: list, newest_first: bool = True) -> list:
    """Вернуть обращения, отсортированные по дате создания."""
    return sorted(
        inquiries,
        key=lambda item: item.created,
        reverse=newest_first,
    )
