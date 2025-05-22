from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для выбора переменных в рандомайзере
def randomizerKeyboard(current_variables: list[str]):
    inline_keyboard = []

    for variable in current_variables:
        inline_keyboard.append([InlineKeyboardButton(text=variable, callback_data=f'randomizer|{variable}')])

    inline_keyboard.append(
        [InlineKeyboardButton(text='➕ Добавить переменную', callback_data='randomizer|add_variable')]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text='✒️ Основной промпт', callback_data='randomizer|prompt')]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text='⚡️ Начать генерацию', callback_data='randomizer|start_generation')]
    )   

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Репли-клавиатура для остановки ввода значений для переменных в рандомайзере
def stopInputValuesForVariableKeyboard():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🚫 Остановить ввод значений')]
    ], one_time_keyboard=True)

    return kb


# Клавиатура для выбора действия с переменной в рандомайзере
def variableActionKeyboard(variable_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ Добавить значения', callback_data=f'randomizer_variable|add_values|{variable_name}')],
        [InlineKeyboardButton(text='🗑️ Удалить значение', callback_data=f'randomizer_variable|delete_values|{variable_name}')],
        [InlineKeyboardButton(text='❌ Удалить переменную', callback_data=f'randomizer_variable|delete_variable|{variable_name}')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data=f'randomizer_variable|back')]
    ])

    return kb


# Клавиатура со всеми значениями переменной в рандомайзере для их удаления
def deleteValuesForVariableKeyboard(values: list[str], variable_name: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    for value in values:
        kb.inline_keyboard.append([InlineKeyboardButton(text=value, callback_data=f'randomizer_delete_value|{variable_name}|{value}')])

    kb.inline_keyboard.append([InlineKeyboardButton(text='🔙 Назад', callback_data=f'randomizer_delete_value|back')])
    return kb


# Клавиатура для основного промпта для рандомайзера
def mainPromptForRandomizerKeyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✍️ Изменить промпт', callback_data='randomizer_prompt|change')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='randomizer_prompt|back')]
    ])

    return kb
