"""Вспомогательные функции ввода данных с клавиатуры (ПР2).

Функции инкапсулируют безопасный ввод: повторяют запрос, пока пользователь
не введёт корректное значение, и позволяют отменить ввод пустой строкой.
"""

import os
import sys


def setup_console() -> None:
    """Настроить консоль на UTF-8, чтобы русский текст читался без «кракозябр».

    В Windows дополнительно переключает кодовую страницу консоли на 65001.
    Все возможные ошибки перенастройки безопасно игнорируются.
    """
    if os.name == "nt":
        os.system("chcp 65001 > nul")
    for stream in (sys.stdout, sys.stdin):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError, OSError):
            pass


def input_text(prompt: str, allow_empty: bool = False) -> str:
    """Прочитать строку. При ``allow_empty=False`` не принимает пустой ввод."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Значение не может быть пустым. Повторите ввод.")


def input_int(prompt: str, allow_empty: bool = False):
    """Прочитать целое число. Возвращает ``None`` при пустом вводе."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            if allow_empty:
                return None
            print("Значение не может быть пустым. Повторите ввод.")
            continue
        try:
            return int(raw)
        except ValueError:
            print("Нужно ввести целое число. Повторите ввод.")


def input_choice(prompt: str, choices) -> str:
    """Прочитать значение, входящее в множество допустимых ``choices``."""
    choices = [str(choice) for choice in choices]
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print(f"Допустимые значения: {', '.join(choices)}. Повторите ввод.")
