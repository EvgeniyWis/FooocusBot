import asyncio
import time
from collections import defaultdict

from aiogram import types
from aiogram.exceptions import TelegramRetryAfter

from logger import logger

_rate_locks = defaultdict(asyncio.Lock)
_last_edit_times = defaultdict(lambda: 0.0)
_min_delay = 0.5
_last_texts = defaultdict(str)


async def safe_edit_message(
    call: types.CallbackQuery,
    safe_text: str,
    reply_markup: types.InlineKeyboardMarkup | None = None,
    parse_mode: str | None = "HTML",
):
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    key = f"{chat_id}:{message_id}"

    async with _rate_locks[key]:
        if _last_texts[key] == safe_text:
            return call.message

        now = time.time()
        elapsed = now - _last_edit_times[key]
        if elapsed < _min_delay:
            await asyncio.sleep(_min_delay - elapsed)
            logger.info(
                f"Ожидаем {_min_delay} секунд перед повторной попыткой редактирования сообщения {message_id}...",
            )

        _last_edit_times[key] = time.time()

        try:
            msg = await call.message.edit_text(
                safe_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            _last_texts[key] = safe_text
            return msg
        except TelegramRetryAfter as e:
            logger.warning(
                f"Флуд-контроль, ожидаем {e.retry_after} секунд перед повторной попыткой редактирования сообщения {message_id}",
            )
            await asyncio.sleep(e.retry_after)
            msg = await call.message.edit_text(
                safe_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            _last_texts[key] = safe_text
            return msg
        except Exception as e:
            logger.warning(
                f"Ошибка при редактировании сообщения {message_id}: {e}",
            )
            return None
