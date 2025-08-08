import asyncio
import time
from collections import defaultdict

from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter
from aiogram.types import InputMedia

from bot.app.instance import bot
from bot.app.core.logging import logger

_chat_locks = defaultdict(asyncio.Lock)
_last_send_time_per_chat = defaultdict(lambda: 0.0)
_min_delay = 1.5


async def safe_send_media_group(
    user_id: int,
    media_group: list[InputMedia],
    *args,
    **kwargs,
):
    lock = _chat_locks[user_id]
    async with lock:
        now = time.time()
        elapsed = now - _last_send_time_per_chat[user_id]
        if elapsed < _min_delay:
            await asyncio.sleep(_min_delay - elapsed)
            logger.warning(
                f"Ожидаем {_min_delay} секунд перед повторной отправкой медиа-группы юзеру {user_id}...",
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

        except TelegramRetryAfter as e:
            logger.warning(
                f"Telegram просит подождать {e.retry_after} секунд перед повторной отправкой",
            )
            await asyncio.sleep(e.retry_after)
            try:
                return await bot.send_media_group(
                    chat_id=user_id,
                    media=media_group,
                    *args,
                    **kwargs,
                )
            except Exception as retry_exception:
                logger.error(
                    f"Ошибка при повторной попытке отправки медиа-группы: {retry_exception}",
                )
                return None

        except TelegramAPIError as e:
            logger.error(f"Telegram API error при отправке медиа-группы: {e}")
            return None

        except Exception as e:
            logger.exception(
                f"Неизвестная ошибка при отправке медиа-группы: {e}",
            )
            return None
