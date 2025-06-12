from aiogram import types
from logger import logger
from aiogram.utils.text_decorations import html_decoration


# Функция для редактирования сообщения и при случаи ошибки отправки сообщения
async def editMessageOrAnswer(
        call: types.CallbackQuery, text: str, reply_markup = None):
    try:
        # Экранируем специальные символы в тексте
        safe_text = html_decoration.quote(text)
    except Exception as e:
        logger.warning(f"Ошибка при экранировании текста: {e}")
        safe_text = text
    
    try:
        message = await call.message.edit_text(safe_text, reply_markup=reply_markup, parse_mode=None)
    except Exception as e:
        logger.warning(f"Ошибка при редактировании сообщения: {e}")
        message = await call.message.answer(safe_text, reply_markup=reply_markup, parse_mode=None)

    return message

