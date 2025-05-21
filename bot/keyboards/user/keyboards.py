from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from .buttons import getGenerationsTypeButtons

# Инлайн-клавиатура для выбора количества генераций
def generationsTypeKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=getGenerationsTypeButtons("generations_type"))

    return kb


# Инлайн-клавиатура для выбора одного из изображений
def selectImageKeyboard(model_name: str, setting_number: str):
    inline_keyboard = []

    for i in range(1, 5, 2):
        inline_keyboard.append([
            InlineKeyboardButton(text=f'{i}', callback_data=f'select_image|{model_name}|{setting_number}|{i}'),
            InlineKeyboardButton(text=f'{i+1}', callback_data=f'select_image|{model_name}|{setting_number}|{i+1}')
        ])

    inline_keyboard.append([InlineKeyboardButton(text='🔄 Перегенерировать', callback_data=f'select_image|{model_name}|{setting_number}|regenerate')])
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для выбора настройки
def selectSettingKeyboard():
    inline_keyboard = []

    for i in range(1, 5):
        inline_keyboard.append([InlineKeyboardButton(text=f'Настройка {i}', callback_data=f'select_setting|{i}')])
    
    inline_keyboard.append([InlineKeyboardButton(text='Все настройки', callback_data='select_setting|all')])

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Клавиатура для выбора режима написания промпта
def writePromptTypeKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='1️⃣ Один промпт для всех моделей', callback_data='write_prompt_type|one')],
        [InlineKeyboardButton(text='✨ Уникальный промпт для каждой модели', callback_data='write_prompt_type|unique')]
    ])

    return kb


# Клавиатура для подтверждения написания уникального промпта для следующей модели
def confirmWriteUniquePromptForNextModelKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✍️ Написать промпт', callback_data='confirm_write_unique_prompt_for_next_model')]
    ])

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
        InlineKeyboardButton(text='❌ Перегенерировать видео', callback_data=f'start_generate_video|{model_name}')]
    ])

    return kb


# Клавиатура для тестирования с другими настройками
def testGenerationImagesKeyboard(setting_number: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔄 Сгенерировать с другими настройками', callback_data='generations_type|test|prompt_exist')],
        [InlineKeyboardButton(text='✍️ Изменить промпт', callback_data=f'select_setting|{setting_number}')],
        [InlineKeyboardButton(text='◀️ Назад', callback_data='generations_type|test')]
    ])

    return kb


# Клавиатура для выбора режима при генерации с одним промптом
def onePromptGenerationChooseTypeKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⚖️ Статичный промпт', callback_data='one_prompt_generation_type|static')],
        [InlineKeyboardButton(text='🎲 Использовать рандомайзер', callback_data='one_prompt_generation_type|random')]
    ])

    return kb


# Клавиатура для выбора переменных в рандомайзере
def randomizerKeyboard(current_variables: list[str]):
    inline_keyboard = []

    for variable in current_variables:
        inline_keyboard.append([InlineKeyboardButton(text=variable, callback_data=f'randomizer|{variable}')])

    inline_keyboard.append([InlineKeyboardButton(text='➕ Добавить переменную', callback_data='randomizer|add_variable')])

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Репли-клавиатура для остановки ввода значений для переменных в рандомайзере
def stopInputValuesForVariableKeyboard():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🚫 Остановить ввод значений')]
    ], resize_keyboard=True, one_time_keyboard=True)

    return kb


# Клавиатура для выбора действия с переменной в рандомайзере
def variableActionKeyboard(variable_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ Добавить значения', callback_data=f'randomizer|variable|add_values|{variable_name}')],
        [InlineKeyboardButton(text='🗑️ Удалить значение', callback_data=f'randomizer|variable|delete_values|{variable_name}')],
        [InlineKeyboardButton(text='❌ Удалить переменную', callback_data=f'randomizer|variable|delete_variable|{variable_name}')]
    ])

    return kb
