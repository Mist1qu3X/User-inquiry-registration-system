"""Загрузка и сохранение данных проекта в формате JSON (ПР3).

При загрузке словари из JSON преобразуются в объекты предметной модели, при
сохранении объекты сериализуются обратно в словари. Чтение и запись
выполняются через контекстные менеджеры ``with``.
"""

import json
import os

from models import Category, Inquiry, Status, User

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
STATUSES_FILE = os.path.join(DATA_DIR, "statuses.json")
INQUIRIES_FILE = os.path.join(DATA_DIR, "inquiries.json")


def _load_raw(path: str) -> list:
    """Прочитать список словарей из JSON-файла."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def _save_raw(path: str, items: list) -> None:
    """Записать список словарей в JSON-файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)


def load_users() -> list:
    return [User.from_data(item) for item in _load_raw(USERS_FILE)]


def save_users(users: list) -> None:
    _save_raw(USERS_FILE, [user.to_data() for user in users])


def load_categories() -> list:
    return [Category.from_data(item) for item in _load_raw(CATEGORIES_FILE)]


def save_categories(categories: list) -> None:
    _save_raw(CATEGORIES_FILE, [c.to_data() for c in categories])


def load_statuses() -> list:
    return [Status.from_data(item) for item in _load_raw(STATUSES_FILE)]


def save_statuses(statuses: list) -> None:
    _save_raw(STATUSES_FILE, [status.to_data() for status in statuses])


def load_inquiries(categories: list, statuses: list, users: list) -> list:
    """Загрузить обращения, разрешив ссылки на категории, статусы и авторов."""
    categories_by_id = {category.id: category for category in categories}
    statuses_by_code = {status.code: status for status in statuses}
    users_by_id = {user.id: user for user in users}
    return [
        Inquiry.from_data(
            item, categories_by_id, statuses_by_code, users_by_id,
        )
        for item in _load_raw(INQUIRIES_FILE)
    ]


def save_inquiries(inquiries: list) -> None:
    _save_raw(INQUIRIES_FILE, [inquiry.to_data() for inquiry in inquiries])
