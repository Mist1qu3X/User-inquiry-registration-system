"""Тесты операций над категориями (ПР2)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import categories as categories_module  # noqa: E402


def make_categories():
    return [
        {"id": 1, "name": "Техническая проблема", "is_active": True},
        {"id": 2, "name": "Прочее", "is_active": False},
    ]


def test_add_category_assigns_next_id():
    categories = make_categories()
    created = categories_module.add_category(categories, "Оплата")
    assert created["id"] == 3
    assert created["is_active"] is True
    assert len(categories) == 3


def test_add_category_rejects_empty_name():
    categories = make_categories()
    try:
        categories_module.add_category(categories, "   ")
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалось исключение ValueError")


def test_is_category_active():
    categories = make_categories()
    assert categories_module.is_category_active(categories, 1) is True
    assert categories_module.is_category_active(categories, 2) is False
    assert categories_module.is_category_active(categories, 99) is False


def test_filter_active_categories():
    categories = make_categories()
    active = categories_module.filter_active_categories(categories)
    assert [category["id"] for category in active] == [1]


def test_sort_categories_by_name():
    categories = make_categories()
    names = [c["name"] for c in categories_module.sort_categories(categories)]
    assert names == ["Прочее", "Техническая проблема"]
