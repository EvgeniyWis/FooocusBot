from aiogram import types
from logger import logger
from utils.handlers.messages.preserve_code_tags import preserve_code_tags


# Функция для редактирования сообщения и при случаи ошибки отправки сообщения
async def editMessageOrAnswer(
        call: types.CallbackQuery, text: str, reply_markup = None):
    try:
        # Экранируем специальные символы в тексте, сохраняя теги code
        safe_text = preserve_code_tags(text)
    except Exception as e:
        logger.warning(f"Ошибка при экранировании текста: {e}")
        safe_text = text
    
    try:
        message = await call.message.edit_text(safe_text, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Ошибка при редактировании сообщения: {e}")
        message = await call.message.answer(safe_text, reply_markup=reply_markup, parse_mode='HTML')

    return message

