from bot.services.iloveapi.types.task_file_format import TaskFileFormat


def validate_file_format(data: TaskFileFormat) -> None:
    """
    Валидация структуры данных TaskFileFormat.
    """
    required_keys = ["server_filename", "filename"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Отсутствует обязательное поле '{key}' в TaskFileFormat: {data}")
    # Можно добавить дополнительные проверки типов и значений

