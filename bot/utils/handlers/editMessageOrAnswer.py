from aiogram import types

from bot.logger import logger
from bot.utils.handlers.rate_limiter_for_edit_message import (
    safe_edit_message,
)


# Функция для редактирования сообщения и при случаи ошибки отправки сообщения
async def editMessageOrAnswer(
    call: types.CallbackQuery,
    text: str,
    reply_markup=None,
):
    try:
        message = await safe_edit_message(
            call,
            text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Ошибка при редактировании сообщения: {e}")
        message = await call.message.answer(
            text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    return message

