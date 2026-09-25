"""Тесты операций над обращениями (ПР1 и ПР2)."""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inquiries as inquiries_module  # noqa: E402


def make_inquiries():
    return [
        {
            "id": 1, "subject": "Ошибка входа", "text": "",
            "category_id": 1, "status_code": "new", "user_id": 1,
            "created": "2026-09-20",
        },
        {
            "id": 2, "subject": "Возврат средств", "text": "",
            "category_id": 2, "status_code": "new", "user_id": 2,
            "created": "2026-09-22",
        },
    ]


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


# --- функции ПР2 ---------------------------------------------------------

def test_add_inquiry_assigns_id_and_status():
    inquiries = make_inquiries()
    created = inquiries_module.add_inquiry(
        inquiries, "Новая тема", "текст", 1, 1,
    )
    assert created["id"] == 3
    assert created["status_code"] == "new"


def test_filter_inquiries_by_category():
    inquiries = make_inquiries()
    selected = inquiries_module.filter_inquiries_by_category(inquiries, 1)
    assert [item["id"] for item in selected] == [1]


def test_change_and_close_status():
    inquiries = make_inquiries()
    assert inquiries_module.change_status(inquiries, 1, "in_progress") is True
    assert inquiries[0]["status_code"] == "in_progress"
    assert inquiries_module.close_inquiry(inquiries, 1) is True
    assert inquiries[0]["status_code"] == "closed"
    assert inquiries_module.change_status(inquiries, 99, "closed") is False


def test_sort_inquiries_by_date_newest_first():
    inquiries = make_inquiries()
    ordered = inquiries_module.sort_inquiries_by_date(inquiries)
    assert [item["id"] for item in ordered] == [2, 1]
