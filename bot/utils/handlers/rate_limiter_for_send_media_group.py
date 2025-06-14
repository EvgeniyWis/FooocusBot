import asyncio
import time

from bot.InstanceBot import bot
from bot.logger import logger

_rate_limiter_lock = asyncio.Lock()
_last_send_time = 0.0
_min_delay = 0.15


async def safe_send_media_group(user_id: int, media_group, *args, **kwargs):
    """
    Создает глобальный мьютекс для ограничения частоты отправки медиа-групп.

    :param message: Сообщение, к которому будет привязана медиа-группа.
    :param media_group: Список медиа-объектов для отправки.
    :param args: Дополнительные аргументы для метода `answer_media_group`.
    :param kwargs: Дополнительные ключевые аргументы для метода `answer_media_group`.
    :return: Ответ от метода `answer_media_group`.
    :raises: Исключение, если отправка медиа-группы не удалась.
    """

    global _last_send_time
    async with _rate_limiter_lock:
        logger.info(f"Lock send media group {media_group}")
        now = time.time()
        elapsed = now - _last_send_time
        if elapsed < _min_delay:
            await asyncio.sleep(_min_delay - elapsed)
        _last_send_time = time.time()
        return await bot.send_media_group(
            chat_id=user_id,
            media=media_group,
            *args,
            **kwargs,
        )
