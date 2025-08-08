import asyncio
import time

from aiogram import types
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter

from bot.InstanceBot import bot
from bot.logger import logger
from bot.utils.handlers.messages.spinner_registry import pop_spinner

_send_lock = asyncio.Lock()
_last_send_time = 0.0

MIN_DELAY = 1.5


async def safe_send_message(
    text: str,
    message: types.Message | types.CallbackQuery | None = None,
    reply_markup: types.InlineKeyboardMarkup
    | types.ReplyKeyboardMarkup
    | types.ReplyKeyboardRemove
    | None = None,
    chat_id: int | None = None,
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
                f"Ожидаем {MIN_DELAY} сек перед отправкой сообщения"
                + (f" (ответ на {message.message_id})" if message else ""),
            )

        try:
            if message:
                method = message.answer(text, reply_markup=reply_markup)
                msg = await bot(method)
                target_chat_id = message.chat.id
            elif chat_id:
                msg = await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=reply_markup,
                )
                target_chat_id = chat_id
            else:
                raise ValueError(
                    "safe_send_message: ни message, ни chat_id не передан!"
                )

            _last_send_time = time.monotonic()

            # После успешной отправки удаляем спиннер в этом чате (если был)
            try:
                if target_chat_id:
                    spinner_id = pop_spinner(target_chat_id)
                    if spinner_id:
                        try:
                            await bot.delete_message(
                                chat_id=target_chat_id,
                                message_id=spinner_id,
                            )
                        except Exception as e:
                            logger.debug(
                                f"Не удалось удалить спиннер {spinner_id} в чате {target_chat_id}: {e}",
                            )
            except Exception:
                logger.debug(
                    "Ошибка при попытке удалить спиннер после отправки сообщения",
                )

            return msg

        except TelegramRetryAfter as e:
            logger.warning(f"Telegram RetryAfter: {e.retry_after}s")
            await asyncio.sleep(e.retry_after)
            try:
                if message:
                    msg = await message.answer(text, reply_markup=reply_markup)
                    target_chat_id = message.chat.id
                elif chat_id:
                    msg = await bot.send_message(
                        chat_id=chat_id,
                        text=text,
                        reply_markup=reply_markup,
                    )
                    target_chat_id = chat_id
                else:
                    raise ValueError(
                        "safe_send_message: ни message, ни chat_id не передан!"
                    )

                _last_send_time = time.monotonic()

                try:
                    if target_chat_id:
                        spinner_id = pop_spinner(target_chat_id)
                        if spinner_id:
                            try:
                                await bot.delete_message(
                                    chat_id=target_chat_id,
                                    message_id=spinner_id,
                                )
                            except Exception as e:
                                logger.debug(
                                    f"Не удалось удалить спиннер {spinner_id} в чате {target_chat_id}: {e}",
                                )
                except Exception:
                    logger.debug(
                        "Ошибка при попытке удалить спиннер после отправки сообщения (повтор)",
                    )

                return msg
            except Exception:
                logger.exception("RetryAfter повторная попытка не удалась")
        except TelegramAPIError as e:
            logger.warning(f"Telegram API ошибка: {e}")
        except Exception:
            logger.exception("Неожиданная ошибка в safe_send_message")

    return None
