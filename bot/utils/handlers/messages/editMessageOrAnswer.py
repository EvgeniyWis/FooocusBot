from aiogram import types

from bot.logger import logger
from bot.utils.handlers.messages.preserve_code_tags import preserve_code_tags
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_edit_message,
)


# Функция для редактирования сообщения и при случаи ошибки отправки сообщения
async def editMessageOrAnswer(
    call: types.CallbackQuery,
    text: str,
    reply_markup=None,
):
    try:
        # Экранируем специальные символы в тексте, сохраняя теги code
        safe_text = preserve_code_tags(text)
    except Exception as e:
        logger.warning(f"Ошибка при экранировании текста: {e}")
        safe_text = text

    try:
        message = await safe_edit_message(
            call,
            safe_text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Ошибка при редактировании сообщения: {e}")
        message = await call.message.answer(
            safe_text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    return message
