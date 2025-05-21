from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.user import keyboards
from utils import text
from states import UserState
from InstanceBot import router
import re


# Обработка кнопок в меню 
async def handle_randomizer_buttons(call: types.CallbackQuery, state: FSMContext):
    variable_name = call.data.split("|")[1]
    
    # Если была выбрана кнопка "➕ Добавить переменную"
    if variable_name == "add_variable":
        await call.message.edit_text(text.ADD_VARIABLE_FOR_RANDOMIZER_TEXT)
        await state.set_state(UserState.write_variable_for_randomizer)

    else:
        await state.update_data(selected_variable_name=variable_name)
        await call.message.edit_text(text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name), 
        reply_markup=keyboards.variableActionKeyboard(variable_name))


# Обработка нажатия кнопок в меню действий с переменной
async def handle_variable_action_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    action = call.data.split("|")[2]
    variable_name = call.data.split("|")[3]

    # Если была выбрана кнопка "➕ Добавить значения"
    if action == "add_values":
        await call.message.answer(text.ADD_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name))
        await state.set_state(UserState.write_value_for_variable_for_randomizer)

    # Если была выбрана кнопка "🗑️ Удалить значение"
    elif action == "delete_values":
        data = await state.get_data()
        variable_name_values = f"randomizer_{variable_name}_values"
        values = data[variable_name_values]

        await call.message.answer(text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name), 
        reply_markup=keyboards.deleteValuesForVariableKeyboard(values, variable_name))

    # Если была выбрана кнопка "❌ Удалить переменную"
    elif action == "delete_variable":
        data = await state.get_data()
        data["variable_names_for_randomizer"].remove(variable_name)
        await state.update_data(**data)
        await call.message.edit_text(text.RANDOMIZER_MENU_TEXT, 
        reply_markup=keyboards.randomizerKeyboard(data["variable_names_for_randomizer"]))
        

# Обработка нажатия кнопок для удаления значения из переменной
async def handle_delete_value_for_variable_buttons(call: types.CallbackQuery, state: FSMContext):
    # Если была выбрана кнопка "🔙 Назад"
    data = await state.get_data()
    if call.data == "randomizer|delete_value|back":
        await call.message.edit_text(text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(data["selected_variable_name"]), 
        reply_markup=keyboards.variableActionKeyboard(data["selected_variable_name"]))
        return
    
    # Получаем данные
    variable_name = call.data.split("|")[2]
    value = call.data.split("|")[3]
    variable_name_values = f"randomizer_{variable_name}_values"
    values = data[variable_name_values]
    values.remove(value)

    # Обновляем стейт
    await state.update_data(**{variable_name_values: values})

    # Отправляем сообщение с обновленной клавиатурой
    await call.message.edit_text(text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name), 
        reply_markup=keyboards.deleteValuesForVariableKeyboard(values, variable_name))
    

# Обработка ввода переменных
async def write_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    variable_name = message.text

    # Если переменная ещё не добавлена в стейт, то добавляем её
    if "variable_names_for_randomizer" not in data:
        await state.update_data(variable_names_for_randomizer=[variable_name])
    else:
        data["variable_names_for_randomizer"].append(variable_name)
        await state.update_data(variable_names_for_randomizer=data["variable_names_for_randomizer"])

    await message.answer(text.WRITE_VARIABLE_FOR_RANDOMIZER_TEXT, 
    reply_markup=keyboards.stopInputValuesForVariableKeyboard())
    await state.set_state(UserState.write_value_for_variable_for_randomizer)


# Обработка ввода значения для переменной
async def write_value_for_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    all_variable_names = data["variable_names_for_randomizer"]
    variable_name = all_variable_names[-1]
    variable_name_values = f"randomizer_{variable_name}_values"

    # Если пользователь нажал на кнопку "🚫 Остановить ввод значений", то прекращаем ввод значений для переменной
    if message.text == "🚫 Остановить ввод значений":
        if "selected_variable_name" in data:
            await message.answer(text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(data["selected_variable_name"]), 
            reply_markup=keyboards.variableActionKeyboard(data["selected_variable_name"]))
        else:
            await message.answer(text.RANDOMIZER_MENU_TEXT, 
            reply_markup=keyboards.randomizerKeyboard(all_variable_names))
        return
    
    # Получаем значение в ином случае
    value = message.text
    
    # Если переменной ещё нет в стейте, то создаём её
    if variable_name_values not in data:
        await state.update_data(**{variable_name_values: [value]})
    else: # Если переменная уже есть в стейте, то добавляем значение в список
        data[variable_name_values].append(value)
        await state.update_data(**{variable_name_values: data[variable_name_values]})

    await message.answer(text.WRITE_VALUE_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name))
    await state.set_state(UserState.write_value_for_variable_for_randomizer)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(handle_variable_action_buttons, lambda call: call.data.startswith("randomizer|variable"))
    
    router.callback_query.register(handle_delete_value_for_variable_buttons, lambda call: call.data.startswith("randomizer|delete_value"))
    
    router.callback_query.register(handle_randomizer_buttons, lambda call: call.data.startswith("randomizer"))

    router.message.register(write_variable_for_randomizer, StateFilter(UserState.write_variable_for_randomizer))

    router.message.register(write_value_for_variable_for_randomizer, StateFilter(UserState.write_value_for_variable_for_randomizer))
