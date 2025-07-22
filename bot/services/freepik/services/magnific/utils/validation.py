class ValidationMixin:
    """
    Миксин для валидации task_id и base64-изображения.
    """
    @staticmethod
    def validate_task_id(task_id: str) -> None:
        """
        Проверяет корректность task_id.
        """
        if not task_id or not isinstance(task_id, str):
            raise ValueError("Некорректный task_id")

    @staticmethod
    def validate_base64_image(image: str) -> None:
        """
        Проверяет, что изображение передано в виде base64-строки.
        """
        if not image or not isinstance(image, str):
            raise ValueError("Некорректный формат изображения (ожидается base64-строка)")

# Для обратной совместимости:
def validate_task_id(task_id: str) -> None:
    ValidationMixin.validate_task_id(task_id)

def validate_base64_image(image: str) -> None:
    ValidationMixin.validate_base64_image(image)
