from aiogram import types
from logger import logger

# Функция для редактирования сообщения и при случаи ошибки отправки сообщения
async def editMessageOrAnswer(
        call: types.CallbackQuery, text: str, reply_markup = None):
    try:
        await call.message.edit_text(text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при редактировании сообщения: {e}")
        await editMessageOrAnswer(
        call,text, reply_markup=reply_markup)

