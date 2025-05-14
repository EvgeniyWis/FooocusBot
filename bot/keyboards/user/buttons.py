from aiogram.types import InlineKeyboardButton

# Функция для выдавания кнопок с выбором типа генерации
def getGenerationsAmountButtons(prefix: str, with_test_generation: bool = True):
    inline_buttons = [
        [InlineKeyboardButton(text='⚙️ Тестовая генерация', callback_data=f'{prefix}|test')],
        [InlineKeyboardButton(text=f'⚡️ Рабочая генерация', callback_data=f'{prefix}|all')]
    ]

    return inline_buttons

