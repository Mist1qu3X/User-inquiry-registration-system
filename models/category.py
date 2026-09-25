"""Класс категории обращения (ПР3)."""


class Category:
    """Тематическая категория, к которой относится обращение."""

    def __init__(self, category_id: int, name: str, is_active: bool = True):
        self.id = category_id
        self.name = name
        self.is_active = bool(is_active)

    def __str__(self) -> str:
        state = "активна" if self.is_active else "скрыта"
        return f"{self.id}. {self.name} ({state})"

    def is_available(self) -> bool:
        """Доступна ли категория для регистрации новых обращений."""
        return self.is_active

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать объект категории из словаря (JSON)."""
        return cls(data["id"], data["name"], data.get("is_active", True))

    def to_data(self) -> dict:
        """Представить категорию словарём для сохранения в JSON."""
        return {"id": self.id, "name": self.name, "is_active": self.is_active}
