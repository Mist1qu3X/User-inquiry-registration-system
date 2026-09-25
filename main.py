"""Консольное меню системы регистрации обращений InquiryDesk (ПР2).

Приложение загружает данные из JSON-файлов каталога ``data/``, предоставляет
пользователю меню сценариев и сохраняет изменения обратно в JSON.
"""

import categories as categories_module
import inquiries as inquiries_module
import statuses as statuses_module
import storage
import users as users_module
from utils import input_int, input_text


def print_inquiry(inquiry, users, categories, statuses) -> None:
    """Вывести одно обращение в виде карточки."""
    author = users_module.get_user_name(users, inquiry["user_id"])
    category = categories_module.find_category(categories, inquiry["category_id"])
    category_name = category["name"] if category else "—"
    status = statuses_module.status_title(statuses, inquiry["status_code"])
    print(f"  #{inquiry['id']} [{inquiry['created']}] {inquiry['subject']}")
    print(f"      автор: {author} | категория: {category_name} | статус: {status}")


def show_inquiries(inquiries, users, categories, statuses) -> None:
    """Показать все обращения, отсортированные по дате (сначала новые)."""
    if not inquiries:
        print("Обращений пока нет.")
        return
    print("Список обращений:")
    for inquiry in inquiries_module.sort_inquiries_by_date(inquiries):
        print_inquiry(inquiry, users, categories, statuses)


def show_categories(categories) -> None:
    """Показать доступные категории."""
    print("Категории:")
    for category in categories_module.sort_categories(categories):
        mark = "активна" if category["is_active"] else "скрыта"
        print(f"  {category['id']}. {category['name']} ({mark})")


def register_inquiry(inquiries, users, categories, statuses) -> None:
    """Сценарий регистрации нового обращения."""
    show_categories(categories)
    category_id = input_int("Идентификатор категории: ")
    if not categories_module.is_category_active(categories, category_id):
        print("Выбранная категория недоступна для новых обращений.")
        return

    subject = input_text("Тема обращения: ")
    if not inquiries_module.can_register_inquiry(subject, True):
        print("Тема обращения некорректна.")
        return

    text = input_text("Текст обращения: ", allow_empty=True)

    print("Пользователи:")
    for user in users:
        print(f"  {user['id']}. {user['name']}")
    user_id = input_int("Идентификатор пользователя: ")
    if users_module.find_user(users, user_id) is None:
        print("Пользователь не найден.")
        return

    try:
        inquiry = inquiries_module.add_inquiry(
            inquiries, subject, text, category_id, user_id,
        )
    except ValueError as error:
        print(f"Не удалось зарегистрировать обращение: {error}")
        return
    print(f"Обращение #{inquiry['id']} зарегистрировано.")


def change_inquiry_status(inquiries, statuses) -> None:
    """Сценарий изменения статуса обращения."""
    inquiry_id = input_int("Идентификатор обращения: ")
    if inquiries_module.find_inquiry(inquiries, inquiry_id) is None:
        print("Обращение не найдено.")
        return
    print("Доступные статусы:")
    for status in statuses_module.list_statuses(statuses):
        print(f"  {status['code']} — {status['title']}")
    code = input_text("Код нового статуса: ").lower()
    if statuses_module.find_status(statuses, code) is None:
        print("Такого статуса нет.")
        return
    inquiries_module.change_status(inquiries, inquiry_id, code)
    print("Статус обновлён.")


def filter_by_category(inquiries, users, categories, statuses) -> None:
    """Сценарий отбора обращений по категории."""
    show_categories(categories)
    category_id = input_int("Идентификатор категории: ")
    selected = inquiries_module.filter_inquiries_by_category(
        inquiries, category_id,
    )
    if not selected:
        print("В этой категории обращений нет.")
        return
    for inquiry in selected:
        print_inquiry(inquiry, users, categories, statuses)


def save_all(users, categories, statuses, inquiries) -> None:
    """Сохранить все коллекции в JSON."""
    storage.save_users(users)
    storage.save_categories(categories)
    storage.save_statuses(statuses)
    storage.save_inquiries(inquiries)


MENU = """
=== InquiryDesk — система регистрации обращений ===
1. Показать обращения
2. Зарегистрировать обращение
3. Изменить статус обращения
4. Обращения по категории
5. Показать категории
0. Выход (с сохранением)
"""


def main() -> None:
    users = storage.load_users()
    categories = storage.load_categories()
    statuses = storage.load_statuses()
    inquiries = storage.load_inquiries()

    while True:
        print(MENU)
        choice = input_text("Выберите пункт меню: ")

        if choice == "1":
            show_inquiries(inquiries, users, categories, statuses)
        elif choice == "2":
            register_inquiry(inquiries, users, categories, statuses)
        elif choice == "3":
            change_inquiry_status(inquiries, statuses)
        elif choice == "4":
            filter_by_category(inquiries, users, categories, statuses)
        elif choice == "5":
            show_categories(categories)
        elif choice == "0":
            save_all(users, categories, statuses, inquiries)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестный пункт меню. Повторите выбор.")


if __name__ == "__main__":
    main()
