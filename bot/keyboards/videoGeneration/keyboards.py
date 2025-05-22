from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.startGeneration.buttons import getGenerationsTypeButtons

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
        InlineKeyboardButton(text='❌ Перегенерировать видео', callback_data=f'start_generate_video|{model_name}')]
    ])

    return kb
