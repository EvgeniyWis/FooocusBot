import re
from aiogram.utils.text_decorations import html_decoration

# Функция для сохранения тегов code в тексте
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
