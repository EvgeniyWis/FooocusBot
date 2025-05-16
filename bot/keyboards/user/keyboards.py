from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .buttons import getGenerationsTypeButtons

# Инлайн-клавиатура для выбора количества генераций
def generationsTypeKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=getGenerationsTypeButtons("generations_type"))

    return kb


# Инлайн-клавиатура для выбора одного из изображений
def selectImageKeyboard(model_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data=f'select_image|{model_name}|1'),
            InlineKeyboardButton(text='2', callback_data=f'select_image|{model_name}|2')
        ],
        [
            InlineKeyboardButton(text='3', callback_data=f'select_image|{model_name}|3'),
            InlineKeyboardButton(text='4', callback_data=f'select_image|{model_name}|4')
        ]
    ])

    return kb


# Инлайн-клавиатура для выбора настройки
def selectSettingKeyboard():
    inline_keyboard = []

    for i in range(1, 5):
        inline_keyboard.append([InlineKeyboardButton(text=f'Настройка {i}', callback_data=f'select_setting|{i}')])
    
    inline_keyboard.append([InlineKeyboardButton(text='Все настройки', callback_data='select_setting|all')])

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для генерации видео
def generateVideoKeyboard(model_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📹 Сгенерировать видео', callback_data=f'start_generate_video|{model_name}')]])

    return kb


# Инлайн-клавиатура при отправки примера видео с промптом с выбором типа генерации и возможности написания кастомного промпта
def videoExampleKeyboard(index: str, model_name: str, with_test_generation: bool = True, with_write_prompt: bool = True):
    prefix = f"generate_video|{index}|{model_name}"

    inline_keyboard = getGenerationsTypeButtons(prefix, with_test_generation)

    if with_write_prompt:
        inline_keyboard.append([InlineKeyboardButton(text='✒️ Написать свой промпт', callback_data=f'{prefix}|write_prompt')])
    
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для выбора корректности генерации видео
def videoCorrectnessKeyboard(model_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Сохранить видео', callback_data=f'video_correctness|correct|{model_name}'),
        InlineKeyboardButton(text='❌ Перегенерировать видео', callback_data=f'generate_video|{model_name}')]
    ])

    return kb
