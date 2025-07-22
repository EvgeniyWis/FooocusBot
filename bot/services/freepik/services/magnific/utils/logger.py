from bot.logger import logger


def log_magnific_step(step_name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger.info(f"[Magnific] Начало этапа: {step_name}")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"[Magnific] Этап '{step_name}' завершён успешно")
                return result
            except Exception as e:
                logger.error(f"[Magnific] Ошибка на этапе '{step_name}': {e}")
                raise
        return wrapper
    return decorator
