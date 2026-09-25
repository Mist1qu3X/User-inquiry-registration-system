"""Класс пользователя — автора обращения (ПР3)."""


class User:
    """Пользователь, регистрирующий обращения.

    Электронная почта необязательна: пользователь может быть создан только
    по имени, которое человек указывает при регистрации обращения.
    """

    def __init__(self, user_id: int, name: str, email: str = ""):
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        if self.email:
            return f"{self.name} <{self.email}>"
        return self.name

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать объект пользователя из словаря (JSON)."""
        return cls(data["id"], data["name"], data.get("email", ""))

    def to_data(self) -> dict:
        """Представить пользователя словарём для сохранения в JSON."""
        return {"id": self.id, "name": self.name, "email": self.email}
