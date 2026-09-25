"""Тесты операций над пользователями и статусами (ПР2)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import statuses as statuses_module  # noqa: E402
import users as users_module  # noqa: E402


def make_users():
    return [
        {"id": 1, "name": "Иван Петров", "email": "ivan@example.com"},
        {"id": 2, "name": "Мария Сидорова", "email": "maria@example.com"},
    ]


def make_statuses():
    return [
        {"code": "new", "title": "Новое", "is_final": False},
        {"code": "closed", "title": "Закрыто", "is_final": True},
    ]


def test_add_user_and_get_name():
    users = make_users()
    created = users_module.add_user(users, "Пётр Иванов", "P.Ivanov@Example.com")
    assert created["id"] == 3
    assert created["email"] == "p.ivanov@example.com"
    assert users_module.get_user_name(users, 3) == "Пётр Иванов"


def test_add_user_rejects_bad_email():
    users = make_users()
    try:
        users_module.add_user(users, "Тест", "не-почта")
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалось исключение ValueError")


def test_find_users_by_substring():
    users = make_users()
    found = users_module.find_users(users, "мария")
    assert [user["id"] for user in found] == [2]


def test_is_final_status():
    statuses = make_statuses()
    assert statuses_module.is_final_status(statuses, "closed") is True
    assert statuses_module.is_final_status(statuses, "new") is False


def test_add_status_rejects_duplicate():
    statuses = make_statuses()
    try:
        statuses_module.add_status(statuses, "new", "Повтор")
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалось исключение ValueError")
