from aiogram import types
from logger import logger


# Функция для редактирования сообщения и при случаи ошибки отправки сообщения
async def editMessageOrAnswer(
        call: types.CallbackQuery, text: str, reply_markup = None):
    try:
        message = await call.message.edit_text(text, reply_markup=reply_markup)
    except Exception as e:
        logger.warning(f"Ошибка при редактировании сообщения: {e}")
        message = await call.message.answer(text, reply_markup=reply_markup)

    return message

