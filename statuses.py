"""Операции над статусами обращений (ПР2).

Статус представлен словарём::

    {"code": str, "title": str, "is_final": bool}

Код статуса — короткий строковый идентификатор (например, ``"new"``),
финальные статусы завершают обработку обращения.
"""


def add_status(statuses: list, code: str, title: str,
               is_final: bool = False) -> dict:
    """Добавить статус в список и вернуть созданный объект."""
    code = code.strip().lower()
    title = title.strip()
    if not code or not title:
        raise ValueError("Код и название статуса не могут быть пустыми.")
    if find_status(statuses, code) is not None:
        raise ValueError(f"Статус с кодом «{code}» уже существует.")
    status = {"code": code, "title": title, "is_final": bool(is_final)}
    statuses.append(status)
    return status


def find_status(statuses: list, code: str):
    """Найти статус по коду или вернуть ``None``."""
    code = str(code).strip().lower()
    for status in statuses:
        if status["code"] == code:
            return status
    return None


def is_final_status(statuses: list, code: str) -> bool:
    """Проверить, является ли статус финальным."""
    status = find_status(statuses, code)
    return bool(status and status["is_final"])


def status_title(statuses: list, code: str) -> str:
    """Вернуть название статуса по коду (или сам код, если не найден)."""
    status = find_status(statuses, code)
    return status["title"] if status else str(code)


def list_statuses(statuses: list) -> list:
    """Вернуть статусы в порядке: сначала рабочие, затем финальные."""
    return sorted(statuses, key=lambda status: status["is_final"])
