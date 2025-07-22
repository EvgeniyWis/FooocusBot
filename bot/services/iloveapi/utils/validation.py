from bot.services.iloveapi.client.types import FileFormat


def validate_file_format(data: FileFormat) -> None:
    """
    Валидация структуры данных FileFormat.
    """
    required_keys = ["server_filename", "filename"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Отсутствует обязательное поле '{key}' в FileFormat: {data}")
    # Можно добавить дополнительные проверки типов и значений

