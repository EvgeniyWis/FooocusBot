from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инлайн-клавиатура для выбора количества генераций
def generationsAmountKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙️ Тестовая генерация', callback_data='generations_amount|test')],
    [InlineKeyboardButton(text=f'⚡️ Рабочая генерация', callback_data='generations_amount|all')]])

    return kb


# Инлайн-клавиатура для выбора одного из изображений
def selectImageKeyboard(job_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data=f'select_image|{job_id}|1'),
            InlineKeyboardButton(text='2', callback_data=f'select_image|{job_id}|2')
        ],
        [
            InlineKeyboardButton(text='3', callback_data=f'select_image|{job_id}|3'),
            InlineKeyboardButton(text='4', callback_data=f'select_image|{job_id}|4')
        ]
    ])

    return kb
