from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .buttons import getGenerationsAmountButtons

# Инлайн-клавиатура для выбора количества генераций
def generationsAmountKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[getGenerationsAmountButtons("generations_amount")])

    return kb


# Инлайн-клавиатура для выбора одного из изображений
def selectImageKeyboard(model_name: str, folder_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data=f'select_image|{model_name}|{folder_id}|1'),
            InlineKeyboardButton(text='2', callback_data=f'select_image|{model_name}|{folder_id}|2')
        ],
        [
            InlineKeyboardButton(text='3', callback_data=f'select_image|{model_name}|{folder_id}|3'),
            InlineKeyboardButton(text='4', callback_data=f'select_image|{model_name}|{folder_id}|4')
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


# Инлайн-клавиатура для генерации видео
def generateVideoKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📹 Сгенерировать видео', callback_data='generate_video')]])

    return kb


# Инлайн-клавиатура при отправки примера видео с промптом с выбором типа генерации и возможности написания кастомного промпта
def videoExampleKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    getGenerationsAmountButtons("generate_video"),
    [InlineKeyboardButton(text='✒️ Написать свой промпт', callback_data='generate_video|write_prompt')]])

    return kb