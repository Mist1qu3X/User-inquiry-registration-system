"""Операции над пользователями (ПР2).

Пользователь представлен словарём::

    {"id": int, "name": str, "email": str}
"""


def next_user_id(users: list) -> int:
    """Вернуть следующий свободный идентификатор пользователя."""
    if not users:
        return 1
    return max(user["id"] for user in users) + 1


def add_user(users: list, name: str, email: str) -> dict:
    """Добавить пользователя в список и вернуть созданный объект."""
    name = name.strip()
    email = email.strip().lower()
    if not name:
        raise ValueError("Имя пользователя не может быть пустым.")
    if "@" not in email:
        raise ValueError("Некорректный адрес электронной почты.")
    user = {"id": next_user_id(users), "name": name, "email": email}
    users.append(user)
    return user


def find_user(users: list, user_id: int):
    """Найти пользователя по идентификатору или вернуть ``None``."""
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def find_users(users: list, query: str) -> list:
    """Найти пользователей, в имени которых встречается ``query``."""
    query = query.strip().lower()
    return [user for user in users if query in user["name"].lower()]


def get_user_name(users: list, user_id: int) -> str:
    """Вернуть имя пользователя по идентификатору (или прочерк)."""
    user = find_user(users, user_id)
    return user["name"] if user else "—"
