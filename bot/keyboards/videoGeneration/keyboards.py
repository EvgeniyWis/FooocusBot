from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.startGeneration.buttons import getGenerationsTypeButtons


# Инлайн-клавиатура для генерации видео
def generateVideoKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📹 Начать генерацию видео", callback_data="start_generate_video")]])

    return kb


# Инлайн-клавиатура при отправки примера видео с промптом с выбором типа генерации и возможности написания кастомного промпта
def videoWritePromptKeyboard(model_name: str):
    prefix = f"generate_video|{model_name}"

    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(text="✒️ Написать свой промпт", callback_data=f"{prefix}|write_prompt")])

def generatedVideoKeyboard(prefix: str, with_test_generation: bool = True):

    inline_keyboard = getGenerationsTypeButtons(prefix, with_test_generation)

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для выбора типа генерации видео
def videoGenerationTypeKeyboard(model_name: str, with_test_generation: bool = False):
    prefix = f"generate_video|{model_name}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *getGenerationsTypeButtons(prefix, with_test_generation),
    ])

    return kb

# Инлайн-клавиатура для выбора корректности генерации видео
def videoCorrectnessKeyboard(model_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сохранить видео", callback_data=f"video_correctness|correct|{model_name}")],
        [InlineKeyboardButton(text="❌ Перегенерировать видео", callback_data=f"start_generate_video|{model_name}")],
    ])

    return kb


# Инлайн-клавиатура для выбора режима генерации видео
def videoGenerationModeKeyboard(model_name: str):
    prefix = f"generate_video_mode|{model_name}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✒️ Написать свой промпт", callback_data=f"{prefix}|write_prompt")],
        # TODO: режим генерации видео с видео-примерами временно отключен
        # [InlineKeyboardButton(text='⚙️ Использовать заготовленные примеры', callback_data=f'{prefix}|use_examples')]
    ])

    return kb


# Инлайн-клавиатура для сохранения видео
def saveVideoKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📹 Начать сохранение видео", callback_data="start_save_video")]])

    return kb

# TODO:
# Инлайн-клавиатура для сгенерируемого видео из изображения
def generatedVideoKeyboard(file_id_index: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text='🔄 Перегенерировать видео', callback_data=f'regenerate_video_from_image|{file_id_index}')],
        [InlineKeyboardButton(text="💾 Сохранить видео", callback_data=f"save_video|{file_id_index}")],
    ])

    return kb

# TODO:
# Инлайн-клавиатура для сгенерируемого видео из изображения
def generatedVideoKeyboard(file_id_index: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text='🔄 Перегенерировать видео', callback_data=f'regenerate_video_from_image|{file_id_index}')],
        [InlineKeyboardButton(text='💾 Сохранить видео', callback_data=f'save_video|{file_id_index}')]
    ])

    return kb
