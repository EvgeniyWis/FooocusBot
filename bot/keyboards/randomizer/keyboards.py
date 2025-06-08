from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


# Клавиатура для выбора переменных в рандомайзере
def randomizerKeyboard(current_variables: list[str]):
    inline_keyboard = []

    for variable_index, variable_name in enumerate(current_variables):
        inline_keyboard.append([InlineKeyboardButton(text=variable_name,
        callback_data=f"randomizer|{variable_index}")])

    inline_keyboard.append(
        [InlineKeyboardButton(text="➕ Добавить переменную", callback_data="randomizer|add_variable")],
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="⚡️ Начать генерацию", callback_data="randomizer|start_generation")],
    )

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Репли-клавиатура для остановки ввода значений для переменных в рандомайзере
def stopInputValuesForVariableKeyboard():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🚫 Остановить ввод значений")],
    ], one_time_keyboard=True)

    return kb


# Клавиатура для выбора действия с переменной в рандомайзере
def variableActionKeyboard(variable_index: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить значения", callback_data=f"var|add_val|{variable_index}")],
        [InlineKeyboardButton(text="🗑️ Удалить значение", callback_data=f"var|delete_val|{variable_index}")],
        [InlineKeyboardButton(text="❌ Удалить переменную", callback_data=f"var|delete_var|{variable_index}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="var|back")],
    ])

    return kb


# Клавиатура со всеми значениями переменной в рандомайзере для их удаления
def deleteValuesForVariableKeyboard(values: list[str], variable_index: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    for value_index, value in enumerate(values):
        kb.inline_keyboard.append([InlineKeyboardButton(text=value, 
                                            callback_data=f"randomizer_delete_value|{variable_index}|{value_index}")])

    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="randomizer_delete_value|back")])
    return kb
