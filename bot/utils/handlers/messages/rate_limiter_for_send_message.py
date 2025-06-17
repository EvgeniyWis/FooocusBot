import asyncio
import time
from collections import defaultdict
from typing import Optional

from aiogram import types
from aiogram.exceptions import TelegramRetryAfter

from bot.logger import logger

_rate_locks = defaultdict(asyncio.Lock)
_last_message_times = defaultdict(lambda: 0.0)
_min_delay = 1.0

_last_messages = defaultdict(str)


async def safe_send_message(
    message: types.Message,
    text: str,
    reply_markup: types.InlineKeyboardMarkup | None = None,
    parse_mode: str | None = "HTML",
    disable_web_page_preview: bool = True,
    disable_notification: bool = False,
) -> Optional[types.Message]:
    """
    Безопасная отправка сообщения с защитой от флуда.

    Args:
        message: Объект сообщения
        text: Текст сообщения
        reply_markup: Клавиатура (опционально)
        parse_mode: Режим парсинга (по умолчанию HTML)
        disable_web_page_preview: Отключить предпросмотр веб-страниц
        disable_notification: Отключить уведомление

    Returns:
        Объект сообщения или None в случае ошибки
    """
    chat_id = str(message.chat.id)

    async with _rate_locks[chat_id]:
        if _last_messages[chat_id] == text:
            return None

        now = time.time()
        elapsed = now - _last_message_times[chat_id]

        if elapsed < _min_delay:
            wait_time = _min_delay - elapsed
            logger.debug(
                f"Ожидаем {wait_time:.2f} секунд перед отправкой сообщения в чат {chat_id}",
            )
            await asyncio.sleep(wait_time)

        _last_message_times[chat_id] = time.time()

        try:
            msg = await message.answer(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
            )
            _last_messages[chat_id] = text
            return msg

        except TelegramRetryAfter as e:
            retry_after = e.retry_after
            logger.warning(
                f"Флуд-контроль от Telegram. Ожидаем {retry_after} секунд перед повторной попыткой отправки сообщения в чат {chat_id}",
            )
            await asyncio.sleep(retry_after)

            try:
                msg = await message.answer(
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                )
                _last_messages[chat_id] = text
                return msg
            except Exception as e:
                logger.error(
                    f"Ошибка при повторной отправке сообщения в чат {chat_id}: {e}",
                )
                return None

        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")
            return None
