from functools import wraps

from bot.logger import logger


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
