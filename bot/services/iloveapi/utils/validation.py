from functools import wraps

from bot.logger import logger
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


def log_task_step(step_name: str):
    """
    Декоратор для логирования этапов работы с задачей.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"[ILoveAPI] Начало этапа: {step_name}")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"[ILoveAPI] Этап '{step_name}' завершён успешно")
                return result
            except Exception as e:
                logger.error(f"[ILoveAPI] Ошибка на этапе '{step_name}': {e}")
                raise
        return wrapper
    return decorator
