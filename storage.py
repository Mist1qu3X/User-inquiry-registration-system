"""Загрузка и сохранение данных проекта в формате JSON (ПР2).

Все коллекции хранятся в каталоге ``data/`` в виде JSON-файлов. Чтение и
запись выполняются через контекстные менеджеры ``with``; отсутствующие
файлы трактуются как пустые коллекции.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
STATUSES_FILE = os.path.join(DATA_DIR, "statuses.json")
INQUIRIES_FILE = os.path.join(DATA_DIR, "inquiries.json")


def _load(path: str) -> list:
    """Прочитать список объектов из JSON-файла."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def _save(path: str, items: list) -> None:
    """Записать список объектов в JSON-файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)


def load_users() -> list:
    return _load(USERS_FILE)


def save_users(users: list) -> None:
    _save(USERS_FILE, users)


def load_categories() -> list:
    return _load(CATEGORIES_FILE)


def save_categories(categories: list) -> None:
    _save(CATEGORIES_FILE, categories)


def load_statuses() -> list:
    return _load(STATUSES_FILE)


def save_statuses(statuses: list) -> None:
    _save(STATUSES_FILE, statuses)


def load_inquiries() -> list:
    return _load(INQUIRIES_FILE)


def save_inquiries(inquiries: list) -> None:
    _save(INQUIRIES_FILE, inquiries)
