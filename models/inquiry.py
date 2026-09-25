"""Класс обращения пользователя (ПР3).

Обращение хранит ссылки на объекты :class:`Category`, :class:`Status`
и :class:`User`, реализуя связи между сущностями через объектные ссылки.
"""

from datetime import date

MAX_SUBJECT_LENGTH = 100


class Inquiry:
    """Обращение пользователя в систему поддержки."""

    def __init__(self, inquiry_id, subject, text, category, status, author,
                 created=None):
        self.id = inquiry_id
        self.subject = subject
        self.text = text
        self.category = category    # объект Category
        self.status = status        # объект Status
        self.author = author        # объект User
        self.created = created or date.today().isoformat()

    def __str__(self) -> str:
        return (
            f"#{self.id} [{self.created}] {self.subject} — "
            f"{self.author.name} ({self.status.title})"
        )

    def change_status(self, status) -> None:
        """Назначить обращению новый статус."""
        self.status = status

    def close(self, closed_status) -> None:
        """Закрыть обращение, присвоив финальный статус."""
        self.status = closed_status

    def is_closed(self) -> bool:
        """Проверить, завершено ли обращение."""
        return self.status.is_final

    def card(self) -> str:
        """Краткая карточка обращения (аналог ``format_inquiry_card`` ПР1)."""
        return str(self)

    @classmethod
    def from_data(cls, data, categories_by_id, statuses_by_code,
                  users_by_id) -> "Inquiry":
        """Создать обращение из словаря, разрешив ссылки на объекты."""
        return cls(
            inquiry_id=data["id"],
            subject=data["subject"],
            text=data.get("text", ""),
            category=categories_by_id.get(data["category_id"]),
            status=statuses_by_code.get(data["status_code"]),
            author=users_by_id.get(data["user_id"]),
            created=data.get("created"),
        )

    def to_data(self) -> dict:
        """Представить обращение словарём для сохранения в JSON."""
        return {
            "id": self.id,
            "subject": self.subject,
            "text": self.text,
            "category_id": self.category.id if self.category else None,
            "status_code": self.status.code if self.status else None,
            "user_id": self.author.id if self.author else None,
            "created": self.created,
        }
