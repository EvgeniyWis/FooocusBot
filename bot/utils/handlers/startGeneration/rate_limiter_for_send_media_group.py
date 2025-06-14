import asyncio
import time
from collections import defaultdict

from aiogram.exceptions import RetryAfter, TelegramAPIError
from aiogram.types import InputMedia

from bot.InstanceBot import bot
from bot.logger import logger

_chat_locks = defaultdict(asyncio.Lock)
_last_send_time_per_chat = defaultdict(lambda: 0.0)
_min_delay = 0.15


async def safe_send_media_group(
    user_id: int, media_group: list[InputMedia], *args, **kwargs
):
    """
    Безопасно отправляет медиа-группу в чат с учётом rate-limit Telegram.
    Поддерживает отправку в разные чаты параллельно, но ограничивает частоту отправки в пределах одного чата.

    :param user_id: ID чата (пользователя/группы), куда отправлять.
    :param media_group: Список InputMedia (фото/видео и т.п.)
    :return: Результат вызова send_media_group или None в случае ошибки.
    """
    lock = _chat_locks[user_id]
    async with lock:
        now = time.time()
        elapsed = now - _last_send_time_per_chat[user_id]
        if elapsed < _min_delay:
            await asyncio.sleep(_min_delay - elapsed)
            logger.warning(
                f"Ожидаем {_min_delay} секунд перед повторной отправкой медиа-группы юзеру {user_id}..."
            )
        _last_send_time_per_chat[user_id] = time.time()

        try:
            result = await bot.send_media_group(
                chat_id=user_id,
                media=media_group,
                *args,
                **kwargs,
            )
            return result

        except RetryAfter as e:
            logger.warning(
                f"Telegram просит подождать {e.timeout} секунд перед повторной отправкой"
            )
            await asyncio.sleep(e.timeout)
            try:
                return await bot.send_media_group(
                    chat_id=user_id,
                    media=media_group,
                    *args,
                    **kwargs,
                )
            except Exception as retry_exception:
                logger.error(
                    f"Ошибка при повторной попытке отправки медиа-группы: {retry_exception}"
                )
                return None

        except TelegramAPIError as e:
            logger.error(f"Telegram API error при отправке медиа-группы: {e}")
            return None

        except Exception as e:
            logger.exception(
                f"Неизвестная ошибка при отправке медиа-группы: {e}"
            )
            return None
