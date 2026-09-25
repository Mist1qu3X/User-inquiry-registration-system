"""Демонстрационный запуск начального сценария InquiryDesk (ПР1)."""

from datetime import date

from inquiries import (
    can_register_inquiry,
    format_inquiry_card,
    get_inquiry_state,
)


def main() -> None:
    subject = "Не приходит письмо для сброса пароля"
    category_active = True

    if can_register_inquiry(subject, category_active):
        state = get_inquiry_state(is_closed=False, replies_count=0)
        card = format_inquiry_card(subject, "Иван Петров", state, date.today())
        print("Обращение зарегистрировано:")
        print(card)
    else:
        print("Обращение не может быть зарегистрировано.")


if __name__ == "__main__":
    main()
