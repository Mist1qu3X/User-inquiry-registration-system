"""Класс статуса обращения (ПР3)."""


class Status:
    """Состояние обработки обращения.

    Финальные статусы (``is_final``) завершают жизненный цикл обращения.
    """

    def __init__(self, code: str, title: str, is_final: bool = False):
        self.code = code
        self.title = title
        self.is_final = bool(is_final)

    def __str__(self) -> str:
        return self.title

    def is_closing(self) -> bool:
        """Является ли статус завершающим обработку."""
        return self.is_final

    @classmethod
    def from_data(cls, data: dict) -> "Status":
        """Создать объект статуса из словаря (JSON)."""
        return cls(data["code"], data["title"], data.get("is_final", False))

    def to_data(self) -> dict:
        """Представить статус словарём для сохранения в JSON."""
        return {
            "code": self.code,
            "title": self.title,
            "is_final": self.is_final,
        }
