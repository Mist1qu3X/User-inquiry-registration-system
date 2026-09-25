"""Консольное меню системы регистрации обращений InquiryDesk (ПР3).

Программа помогает регистрировать обращения пользователей, распределять их
по категориям и отслеживать статус обработки. Данные загружаются из JSON в
объекты предметной модели и сохраняются обратно при выходе.

Интерфейс построен на выборе из нумерованных списков: пользователю не нужно
запоминать внутренние идентификаторы или коды статусов — достаточно ввести
номер нужного пункта.
"""

import categories as categories_module
import inquiries as inquiries_module
import statuses as statuses_module
import storage
from utils import input_text

LINE = "-" * 52


def choose(title: str, items: list, render):
    """Показать нумерованный список и вернуть выбранный объект.

    ``render`` — функция, превращающая элемент в строку для показа.
    Возврат ``None`` означает отмену (пункт «0») или пустой список.
    """
    if not items:
        print("  (список пуст)")
        return None
    print(title)
    for number, item in enumerate(items, start=1):
        print(f"  {number}) {render(item)}")
    print("  0) отмена")
    while True:
        raw = input("Введите номер: ").strip()
        if raw == "0":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(items):
            return items[int(raw) - 1]
        print(f"  Нужно ввести число от 0 до {len(items)}. Повторите ввод.")


def print_inquiry(inquiry, number=None) -> None:
    """Вывести одно обращение в виде читаемой карточки."""
    category_name = inquiry.category.name if inquiry.category else "—"
    author_name = inquiry.author.name if inquiry.author else "—"
    status_title = inquiry.status.title if inquiry.status else "—"
    prefix = f"{number}) " if number is not None else ""
    print(f"  {prefix}«{inquiry.subject}»")
    print(f"       статус: {status_title}  |  категория: {category_name}")
    print(f"       автор: {author_name}  |  дата: {inquiry.created}")


def show_inquiries(inquiries) -> None:
    """Показать все обращения, отсортированные по дате (сначала новые)."""
    if not inquiries:
        print("Обращений пока нет. Добавьте первое через пункт меню «2».")
        return
    ordered = inquiries_module.sort_inquiries_by_date(inquiries)
    print(f"Всего обращений: {len(ordered)} (сначала новые)")
    print(LINE)
    for inquiry in ordered:
        print_inquiry(inquiry)
        print(LINE)


def show_categories(categories) -> None:
    """Показать список категорий и их доступность."""
    print("Категории обращений:")
    for category in categories_module.sort_categories(categories):
        mark = "открыта" if category.is_active else "закрыта"
        print(f"  • {category.name} ({mark})")


def register_inquiry(inquiries, users, categories, statuses) -> None:
    """Сценарий регистрации нового обращения (шаг за шагом)."""
    print("Регистрация нового обращения.")

    active = categories_module.sort_categories(
        categories_module.filter_active_categories(categories)
    )
    category = choose("Шаг 1. Выберите категорию:", active,
                      lambda c: c.name)
    if category is None:
        print("Регистрация отменена.")
        return

    subject = input_text("Шаг 2. Кратко опишите тему обращения: ")
    if not inquiries_module.can_register_inquiry(subject, True):
        print("Тема слишком длинная или некорректна. Регистрация отменена.")
        return

    text = input_text("Шаг 3. Подробное описание (можно пропустить): ",
                      allow_empty=True)

    author = choose("Шаг 4. Кто автор обращения?", users, lambda u: u.name)
    if author is None:
        print("Регистрация отменена.")
        return

    new_status = statuses_module.find_status(statuses, "new")
    try:
        inquiry = inquiries_module.add_inquiry(
            inquiries, subject, text, category, new_status, author,
        )
    except ValueError as error:
        print(f"Не удалось зарегистрировать обращение: {error}")
        return
    print("\nОбращение зарегистрировано:")
    print_inquiry(inquiry)


def change_inquiry_status(inquiries, statuses) -> None:
    """Сценарий изменения статуса обращения."""
    if not inquiries:
        print("Обращений пока нет.")
        return
    ordered = inquiries_module.sort_inquiries_by_date(inquiries)
    inquiry = choose(
        "Выберите обращение, статус которого нужно изменить:",
        ordered,
        lambda i: f"«{i.subject}» (сейчас: "
                  f"{i.status.title if i.status else '—'})",
    )
    if inquiry is None:
        print("Действие отменено.")
        return

    status = choose(
        "Выберите новый статус:",
        statuses_module.list_statuses(statuses),
        lambda s: s.title,
    )
    if status is None:
        print("Действие отменено.")
        return

    inquiry.change_status(status)
    print(f"Готово. Новый статус обращения «{inquiry.subject}»: "
          f"{status.title}.")


def filter_by_category(inquiries, categories) -> None:
    """Сценарий отбора обращений по выбранной категории."""
    category = choose(
        "Выберите категорию для просмотра:",
        categories_module.sort_categories(categories),
        lambda c: c.name,
    )
    if category is None:
        print("Действие отменено.")
        return
    selected = inquiries_module.filter_inquiries_by_category(
        inquiries, category.id,
    )
    if not selected:
        print(f"В категории «{category.name}» обращений нет.")
        return
    print(f"Обращения в категории «{category.name}»:")
    print(LINE)
    for inquiry in inquiries_module.sort_inquiries_by_date(selected):
        print_inquiry(inquiry)
        print(LINE)


def save_all(users, categories, statuses, inquiries) -> None:
    """Сохранить все коллекции в JSON."""
    storage.save_users(users)
    storage.save_categories(categories)
    storage.save_statuses(statuses)
    storage.save_inquiries(inquiries)


MENU = """
╔══════════════════════════════════════════════════╗
║   InquiryDesk — учёт обращений пользователей       ║
╠══════════════════════════════════════════════════╣
║   1  Показать все обращения                        ║
║   2  Зарегистрировать новое обращение              ║
║   3  Изменить статус обращения                     ║
║   4  Показать обращения выбранной категории        ║
║   5  Показать категории                            ║
║   0  Выход (данные сохранятся автоматически)       ║
╚══════════════════════════════════════════════════╝"""


def main() -> None:
    users = storage.load_users()
    categories = storage.load_categories()
    statuses = storage.load_statuses()
    inquiries = storage.load_inquiries(categories, statuses, users)

    print("Добро пожаловать в InquiryDesk!")
    print("Приложение регистрирует обращения пользователей и следит за их "
          "статусом.")

    while True:
        print(MENU)
        choice = input_text("Что сделать? Введите номер пункта: ")
        print()

        if choice == "1":
            show_inquiries(inquiries)
        elif choice == "2":
            register_inquiry(inquiries, users, categories, statuses)
        elif choice == "3":
            change_inquiry_status(inquiries, statuses)
        elif choice == "4":
            filter_by_category(inquiries, categories)
        elif choice == "5":
            show_categories(categories)
        elif choice == "0":
            save_all(users, categories, statuses, inquiries)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Нет такого пункта меню. Введите число от 0 до 5.")


if __name__ == "__main__":
    main()
