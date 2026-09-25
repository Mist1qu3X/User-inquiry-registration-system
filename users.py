"""Операции над пользователями (ПР3, объектная модель).

Функции работают со списком объектов :class:`models.User`.
"""

from models import User


def next_user_id(users: list) -> int:
    """Вернуть следующий свободный идентификатор пользователя."""
    if not users:
        return 1
    return max(user.id for user in users) + 1


def add_user(users: list, name: str, email: str) -> User:
    """Создать пользователя, добавить его в список и вернуть объект."""
    name = name.strip()
    email = email.strip().lower()
    if not name:
        raise ValueError("Имя пользователя не может быть пустым.")
    if "@" not in email:
        raise ValueError("Некорректный адрес электронной почты.")
    user = User(next_user_id(users), name, email)
    users.append(user)
    return user


def get_or_create_user(users: list, name: str) -> User:
    """Найти пользователя по имени или создать нового (только с именем).

    Сравнение имён выполняется без учёта регистра и лишних пробелов, поэтому
    повторные обращения одного человека привязываются к тому же пользователю.
    """
    name = name.strip()
    if not name:
        raise ValueError("Имя не может быть пустым.")
    for user in users:
        if user.name.strip().lower() == name.lower():
            return user
    user = User(next_user_id(users), name)
    users.append(user)
    return user


def find_user(users: list, user_id: int):
    """Найти пользователя по идентификатору или вернуть ``None``."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_users(users: list, query: str) -> list:
    """Найти пользователей, в имени которых встречается ``query``."""
    query = query.strip().lower()
    return [user for user in users if query in user.name.lower()]


def get_user_name(users: list, user_id: int) -> str:
    """Вернуть имя пользователя по идентификатору (или прочерк)."""
    user = find_user(users, user_id)
    return user.name if user else "—"
