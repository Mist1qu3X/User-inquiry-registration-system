"""Начальный сценарий проекта InquiryDesk (ПР1).

Модуль содержит три базовые функции работы с обращениями пользователей.
Эти функции сохраняются и переиспользуются в последующих версиях проекта.
Используются простые типы данных, операции, преобразование типов,
ветвления, функции и импорт модуля ``datetime.date``.
"""

from datetime import date

# Максимально допустимая длина темы обращения (в символах).
MAX_SUBJECT_LENGTH = 100


def can_register_inquiry(subject: str, category_active: bool) -> bool:
    """Проверить, можно ли зарегистрировать обращение.

    Обращение можно зарегистрировать, если тема не пустая, её длина не
    превышает :data:`MAX_SUBJECT_LENGTH`, а выбранная категория активна.
    """
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
