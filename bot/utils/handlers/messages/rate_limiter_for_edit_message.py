import asyncio
import time

from aiogram import types
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter

from bot.logger import logger

_edit_lock = asyncio.Lock()
_last_edit_time = 0.0

MIN_DELAY = 1.5


async def safe_edit_message(
    call: types.CallbackQuery,
    safe_text: str,
    reply_markup: types.InlineKeyboardMarkup
    | types.ReplyKeyboardMarkup
    | None = None,
    parse_mode: str | None = "HTML",
) -> types.Message | None:
    global _last_edit_time

    async with _edit_lock:
        now = time.monotonic()
        elapsed = now - _last_edit_time
        if elapsed < MIN_DELAY:
            await asyncio.sleep(MIN_DELAY - elapsed)
            logger.warning(
                f"Ожидаем {MIN_DELAY} секунд перед редактированием сообщения {call.message.message_id}...",
            )

        try:
            msg = await call.message.edit_text(
                safe_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            _last_edit_time = time.monotonic()
            return msg
        except TelegramRetryAfter as e:
            logger.warning(f"Telegram RetryAfter: {e.retry_after}s")
            await asyncio.sleep(e.retry_after)
            try:
                msg = await call.message.edit_text(
                    safe_text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode,
                )
                _last_edit_time = time.monotonic()
                return msg
            except Exception:
                logger.exception("RetryAfter second attempt failed")
        except TelegramAPIError as e:
            logger.warning(f"Telegram API error: {e}")
        except Exception:
            logger.exception("Unexpected error in safe_edit_message")

    return None
