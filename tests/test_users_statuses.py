"""Тесты операций над пользователями и статусами (ПР3, объектная модель)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import statuses as statuses_module  # noqa: E402
import users as users_module  # noqa: E402
from models import Status, User  # noqa: E402


def make_users():
    return [
        User(1, "Иван Петров", "ivan@example.com"),
        User(2, "Мария Сидорова", "maria@example.com"),
    ]


def make_statuses():
    return [
        Status("new", "Новое", False),
        Status("closed", "Закрыто", True),
    ]


def test_add_user_and_get_name():
    users = make_users()
    created = users_module.add_user(
        users, "Пётр Иванов", "P.Ivanov@Example.com",
    )
    assert created.id == 3
    assert created.email == "p.ivanov@example.com"
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
    assert [user.id for user in found] == [2]


def test_get_or_create_user_creates_new_by_name():
    users = make_users()
    created = users_module.get_or_create_user(users, "Пётр")
    assert created.id == 3
    assert created.name == "Пётр"
    assert len(users) == 3


def test_get_or_create_user_reuses_existing():
    users = make_users()
    same = users_module.get_or_create_user(users, "  иван петров  ")
    assert same.id == 1
    assert len(users) == 2


def test_get_or_create_user_rejects_empty():
    users = make_users()
    try:
        users_module.get_or_create_user(users, "   ")
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалось исключение ValueError")


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
