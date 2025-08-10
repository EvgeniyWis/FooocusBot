from aiogram import types

from bot.app.core.logging import logger
from bot.utils.handlers.messages.preserve_code_tags import preserve_code_tags
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_edit_message,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
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

    message = await safe_edit_message(
        call.message,
        safe_text,
        reply_markup=reply_markup,
        parse_mode="HTML",
    )
    if message is None:
        logger.warning(
            f"Не удалось редактировать сообщение {call.message.message_id}, отправляем новое",
        )
        logger.debug(
            f"Отправляем новое сообщение с reply_markup: {reply_markup}",
        )
        message = await safe_send_message(
            safe_text,
            call,
            reply_markup=reply_markup,
        )

    return message
