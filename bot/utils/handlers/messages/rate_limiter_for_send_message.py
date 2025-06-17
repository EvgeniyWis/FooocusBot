import asyncio
import time

from aiogram import types
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter

from bot.logger import logger

_send_lock = asyncio.Lock()
_last_send_time = 0.0

MIN_DELAY = 1.5


async def safe_send_message(
    text: str,
    message: types.Message | types.CallbackQuery,
    reply_markup: types.InlineKeyboardMarkup
    | types.ReplyKeyboardMarkup
    | types.ReplyKeyboardRemove
    | None = None,
) -> types.Message | None:
    logger.info(
        f"safe_send_message called with text={text!r}, reply_markup={reply_markup!r}",
    )
    global _last_send_time

    if isinstance(message, types.CallbackQuery):
        message = message.message

    async with _send_lock:
        now = time.monotonic()
        elapsed = now - _last_send_time
        if elapsed < MIN_DELAY:
            await asyncio.sleep(MIN_DELAY - elapsed)
            logger.warning(
                f"Ожидаем {MIN_DELAY} сек перед отправкой сообщения (ответ на {message.message_id})",
            )

        try:
            msg = await message.answer(text, reply_markup=reply_markup)
            _last_send_time = time.monotonic()
            return msg
        except TelegramRetryAfter as e:
            logger.warning(f"Telegram RetryAfter: {e.retry_after}s")
            await asyncio.sleep(e.retry_after)
            try:
                msg = await message.answer(text, reply_markup=reply_markup)
                _last_send_time = time.monotonic()
                return msg
            except Exception:
                logger.exception("RetryAfter повторная попытка не удалась")
        except TelegramAPIError as e:
            logger.warning(f"Telegram API ошибка: {e}")
        except Exception:
            logger.exception("Неожиданная ошибка в safe_send_message")

    return None
