import asyncio
from logger import logger
from aiogram.exceptions import TelegramRetryAfter


# Функция для повторных попыток с задержкой во избежание блокировки бота flood control
async def retry_with_delay(func, *args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func(*args)
        except TelegramRetryAfter as e:
            if attempt == max_retries - 1:
                raise
            retry_after = int(e.retry_after)
            logger.warning(f"Флуд контроль обнаружен. Ожидание {retry_after} секунд перед повторной попыткой. Попытка {attempt + 1}/{max_retries}")
            await asyncio.sleep(retry_after)
        except Exception as e:
            raise e