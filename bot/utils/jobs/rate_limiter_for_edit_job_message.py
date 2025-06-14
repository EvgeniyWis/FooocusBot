import asyncio
import time
from collections import defaultdict

from aiogram import Bot, types
from aiogram.exceptions import TelegramRetryAfter

from bot.logger import logger

_rate_locks = defaultdict(asyncio.Lock)
_last_edit_times = defaultdict(lambda: 0.0)
_last_texts = defaultdict(str)
_min_delay = 0.5


async def safe_bot_edit_job_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    safe_text: str,
    reply_markup: types.InlineKeyboardMarkup | None = None,
    parse_mode: str | None = "HTML",
):
    key = f"{chat_id}:{message_id}"

    async with _rate_locks[key]:
        if _last_texts[key] == safe_text:
            return

        now = time.time()
        elapsed = now - _last_edit_times[key]
        if elapsed < _min_delay:
            await asyncio.sleep(_min_delay - elapsed)
            logger.info(
                f"Ожидаем {_min_delay} секунд перед повторным редактированием сообщения {message_id}...",
            )

        _last_edit_times[key] = time.time()

        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=safe_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            _last_texts[key] = safe_text
        except TelegramRetryAfter as e:
            logger.warning(
                f"Флуд-контроль, ожидаем {e.retry_after} секунд <UNK> <UNK> <UNK> <UNK> {message_id}...",
            )
            await asyncio.sleep(e.retry_after)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=safe_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            _last_texts[key] = safe_text
        except Exception as e:
            logger.warning(
                f"Ошибка при редактировании сообщения {message_id}: {e}",
            )
