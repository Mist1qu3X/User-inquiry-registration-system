"""Тесты операций над обращениями (ПР1 и ПР3, объектная модель)."""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inquiries as inquiries_module  # noqa: E402
from models import Category, Inquiry, Status, User  # noqa: E402


def make_refs():
    tech = Category(1, "Ошибка", True)
    billing = Category(2, "Оплата", True)
    new = Status("new", "Новое", False)
    closed = Status("closed", "Закрыто", True)
    user = User(1, "Иван", "ivan@example.com")
    return tech, billing, new, closed, user


def make_inquiries():
    tech, billing, new, closed, user = make_refs()
    return [
        Inquiry(1, "Ошибка входа", "", tech, new, user, "2026-09-20"),
        Inquiry(2, "Возврат средств", "", billing, new, user, "2026-09-22"),
    ], (tech, billing, new, closed, user)


# --- функции ПР1 ---------------------------------------------------------

def test_can_register_inquiry():
    assert inquiries_module.can_register_inquiry("Тема", True) is True
    assert inquiries_module.can_register_inquiry("   ", True) is False
    assert inquiries_module.can_register_inquiry("Тема", False) is False


def test_get_inquiry_state():
    assert inquiries_module.get_inquiry_state(True, 5) == "Закрыто"
    assert inquiries_module.get_inquiry_state(False, 2) == "В работе"
    assert inquiries_module.get_inquiry_state(False, 0) == "Новое"


def test_format_inquiry_card():
    card = inquiries_module.format_inquiry_card(
        "Тема", "Иван", "Новое", date(2026, 9, 25),
    )
    assert card == "[25.09.2026] Тема — Иван (Новое)"


# --- функции ПР3 ---------------------------------------------------------

def test_add_inquiry_returns_object():
    inquiries, (tech, _, new, _, user) = make_inquiries()
    created = inquiries_module.add_inquiry(
        inquiries, "Новая тема", "текст", tech, new, user,
    )
    assert isinstance(created, Inquiry)
    assert created.id == 3
    assert created.status is new


def test_filter_inquiries_by_category():
    inquiries, _ = make_inquiries()
    selected = inquiries_module.filter_inquiries_by_category(inquiries, 1)
    assert [item.id for item in selected] == [1]


def test_change_and_close_status():
    inquiries, (_, _, new, closed, _) = make_inquiries()
    in_progress = Status("in_progress", "В работе", False)
    assert inquiries_module.change_status(inquiries, 1, in_progress) is True
    assert inquiries[0].status is in_progress
    assert inquiries_module.close_inquiry(inquiries, 1, closed) is True
    assert inquiries[0].is_closed() is True
    assert inquiries_module.change_status(inquiries, 99, closed) is False


def test_sort_inquiries_by_date_newest_first():
    inquiries, _ = make_inquiries()
    ordered = inquiries_module.sort_inquiries_by_date(inquiries)
    assert [item.id for item in ordered] == [2, 1]
