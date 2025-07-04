import asyncio
import time

from aiogram import types
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter
from aiogram.methods import SendPhoto
from InstanceBot import bot

from bot.logger import logger

_send_lock = asyncio.Lock()
_last_send_time = 0.0

MIN_DELAY = 1.5


async def safe_send_photo(
    photo: str | bytes,
    message: types.Message | types.CallbackQuery,
    caption: str | None = None,
    reply_markup: types.InlineKeyboardMarkup
    | types.ReplyKeyboardMarkup
    | types.ReplyKeyboardRemove
    | None = None,
) -> types.Message | None:
    global _last_send_time

    if isinstance(message, types.CallbackQuery):
        message = message.message

    async with _send_lock:
        now = time.monotonic()
        elapsed = now - _last_send_time
        if elapsed < MIN_DELAY:
            await asyncio.sleep(MIN_DELAY - elapsed)
            logger.warning(
                f"Ожидаем {MIN_DELAY} сек перед отправкой фото (ответ на {message.message_id})",
            )

        try:
            method = message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=reply_markup,
            )
            method = await method.as_(bot)
            _last_send_time = time.monotonic()
            return method
        except TelegramRetryAfter as e:
            logger.warning(f"Telegram RetryAfter: {e.retry_after}s (photo)")
            await asyncio.sleep(e.retry_after)
            try:
                method = message.answer_photo(
                    photo=photo,
                    caption=caption,
                    reply_markup=reply_markup,
                )
                method = await method.as_(bot)
                _last_send_time = time.monotonic()
                return method
            except Exception:
                logger.exception(
                    "RetryAfter повторная попытка отправки фото не удалась",
                )
        except TelegramAPIError as e:
            logger.warning(f"Telegram API ошибка (photo): {e}")
        except Exception:
            logger.exception("Неожиданная ошибка в safe_send_photo")

    return None
