from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инлайн-клавиатура для выбора количества генераций
def generationsAmountKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙️ Тестовая генерация', callback_data='generations_amount|test')],
    [InlineKeyboardButton(text=f'⚡️ Рабочая генерация', callback_data='generations_amount|all')]])

    return kb


# Инлайн-клавиатура для выбора одного из изображений
def selectImageKeyboard(job_id: int, model_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data=f'select_image|{job_id}|{model_name}|1'),
            InlineKeyboardButton(text='2', callback_data=f'select_image|{job_id}|{model_name}|2')
        ],
        [
            InlineKeyboardButton(text='3', callback_data=f'select_image|{job_id}|{model_name}|3'),
            InlineKeyboardButton(text='4', callback_data=f'select_image|{job_id}|{model_name}|4')
        ]
    ])

    return kb


# Инлайн-клавиатура для выбора настройки
def selectSettingKeyboard(is_test_generation: bool):
    inline_keyboard = []

    for i in range(1, 4):
        inline_keyboard.append([InlineKeyboardButton(text=f'Настройка {i}', callback_data=f'select_setting|{i}')])
    
    # Если тестовая генерация, то добавляем кнопку "Все настройки"
    if is_test_generation:
        inline_keyboard.append([InlineKeyboardButton(text='Все настройки', callback_data='select_setting|all')])

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb
