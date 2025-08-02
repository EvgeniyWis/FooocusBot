import asyncio
import time

from aiogram import types
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramRetryAfter,
)
from InstanceBot import bot

from bot.logger import logger
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)

_edit_lock = asyncio.Lock()
_last_edit_time = 0.0

MIN_DELAY = 1.5


async def safe_edit_message(
    message: types.Message,
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
                f"Ожидаем {MIN_DELAY} секунд перед редактированием сообщения {message.message_id}...",
            )

        try:
            method = message.edit_text(
                safe_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            method = method.as_(bot)
            result = await method
            _last_edit_time = time.monotonic()
            return result
        except TelegramRetryAfter as e:
            logger.warning(f"Telegram RetryAfter: {e.retry_after}s")
            await asyncio.sleep(e.retry_after)
            try:
                method = message.edit_text(
                    safe_text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode,
                )
                method = method.as_(bot)
                result = await method
                _last_edit_time = time.monotonic()
                return result
            except Exception:
                logger.exception("RetryAfter second attempt failed")
        except TelegramAPIError as e:
            # Игнорируем ошибку "message is not modified"
            if "message is not modified" in str(e):
                logger.debug(f"Ignoring 'message is not modified' error for message {message.message_id}")
                return message
            
            logger.warning(f"Telegram API error: {e}")

            # При ошибке, связанной с тем, что сообщение не найдено, то отправляем новое сообщение
            if "message to edit not found" in e.message.lower():
                return await safe_send_message(
                    safe_text,
                    message,
                )
        except Exception:
            logger.exception("Unexpected error in safe_edit_message")

    return None
