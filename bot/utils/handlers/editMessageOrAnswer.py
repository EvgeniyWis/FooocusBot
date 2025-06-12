from aiogram import types
from logger import logger
from aiogram.utils.text_decorations import html_decoration
import re


def preserve_code_tags(text: str) -> str:
    # Сохраняем содержимое тегов code
    code_blocks = re.findall(r'<code>(.*?)</code>', text)
    # Временно заменяем теги code на маркер
    text = re.sub(r'<code>.*?</code>', '###CODE_BLOCK###', text)
    # Экранируем оставшийся текст
    text = html_decoration.quote(text)
    # Возвращаем теги code на место
    for block in code_blocks:
        text = text.replace('###CODE_BLOCK###', f'<code>{block}</code>', 1)
    return text


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

