"""Операции над категориями обращений (ПР2).

Категория представлена словарём::

    {"id": int, "name": str, "is_active": bool}
"""


def next_category_id(categories: list) -> int:
    """Вернуть следующий свободный идентификатор категории."""
    if not categories:
        return 1
    return max(category["id"] for category in categories) + 1


def add_category(categories: list, name: str, is_active: bool = True) -> dict:
    """Добавить категорию в список и вернуть созданный объект."""
    name = name.strip()
    if not name:
        raise ValueError("Название категории не может быть пустым.")
    category = {
        "id": next_category_id(categories),
        "name": name,
        "is_active": bool(is_active),
    }
    categories.append(category)
    return category


def find_category(categories: list, category_id: int):
    """Найти категорию по идентификатору или вернуть ``None``."""
    for category in categories:
        if category["id"] == category_id:
            return category
    return None


def is_category_active(categories: list, category_id: int) -> bool:
    """Проверить, активна ли категория с указанным идентификатором."""
    category = find_category(categories, category_id)
    return bool(category and category["is_active"])


def filter_active_categories(categories: list) -> list:
    """Вернуть только активные категории."""
    return [category for category in categories if category["is_active"]]


def sort_categories(categories: list) -> list:
    """Вернуть категории, отсортированные по названию."""
    return sorted(categories, key=lambda category: category["name"].lower())
