from aiogram import types
from InstanceBot import bot

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

    message = await safe_edit_message(
        call,
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
        message = await bot.send_message(
            call.message.chat.id,
            safe_text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    return message
