"""Операции над статусами обращений (ПР3, объектная модель).

Функции работают со списком объектов :class:`models.Status`.
"""

from models import Status


def add_status(statuses: list, code: str, title: str,
               is_final: bool = False) -> Status:
    """Создать статус, добавить его в список и вернуть объект."""
    code = code.strip().lower()
    title = title.strip()
    if not code or not title:
        raise ValueError("Код и название статуса не могут быть пустыми.")
    if find_status(statuses, code) is not None:
        raise ValueError(f"Статус с кодом «{code}» уже существует.")
    status = Status(code, title, is_final)
    statuses.append(status)
    return status


def find_status(statuses: list, code: str):
    """Найти статус по коду или вернуть ``None``."""
    code = str(code).strip().lower()
    for status in statuses:
        if status.code == code:
            return status
    return None


def is_final_status(statuses: list, code: str) -> bool:
    """Проверить, является ли статус финальным."""
    status = find_status(statuses, code)
    return bool(status and status.is_final)


def list_statuses(statuses: list) -> list:
    """Вернуть статусы в порядке: сначала рабочие, затем финальные."""
    return sorted(statuses, key=lambda status: status.is_final)
