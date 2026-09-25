"""Тесты классов объектной модели (ПР3)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Category, Inquiry, Status, User  # noqa: E402


def test_category_roundtrip_and_str():
    category = Category.from_data({"id": 1, "name": "Оплата", "is_active": True})
    assert category.is_available() is True
    assert "Оплата" in str(category)
    assert category.to_data() == {"id": 1, "name": "Оплата", "is_active": True}


def test_status_is_closing_and_str():
    status = Status.from_data({"code": "closed", "title": "Закрыто",
                               "is_final": True})
    assert status.is_closing() is True
    assert str(status) == "Закрыто"


def test_user_str_and_roundtrip():
    user = User(1, "Иван", "ivan@example.com")
    assert str(user) == "Иван <ivan@example.com>"
    assert User.from_data(user.to_data()).name == "Иван"


def test_inquiry_references_and_close():
    category = Category(1, "Оплата", True)
    new = Status("new", "Новое", False)
    closed = Status("closed", "Закрыто", True)
    user = User(1, "Иван", "ivan@example.com")
    inquiry = Inquiry(1, "Двойное списание", "текст", category, new, user,
                      "2026-09-22")

    assert inquiry.author is user
    assert inquiry.category is category
    assert inquiry.is_closed() is False
    inquiry.close(closed)
    assert inquiry.is_closed() is True


def test_inquiry_from_data_resolves_references():
    categories_by_id = {1: Category(1, "Оплата", True)}
    statuses_by_code = {"new": Status("new", "Новое", False)}
    users_by_id = {5: User(5, "Мария", "maria@example.com")}
    data = {
        "id": 7, "subject": "Тема", "text": "т",
        "category_id": 1, "status_code": "new", "user_id": 5,
        "created": "2026-09-25",
    }
    inquiry = Inquiry.from_data(data, categories_by_id, statuses_by_code,
                                users_by_id)
    assert inquiry.category.name == "Оплата"
    assert inquiry.author.name == "Мария"
    assert inquiry.to_data()["category_id"] == 1
