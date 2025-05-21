from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.user import keyboards
from utils import text
from states import UserState
from InstanceBot import router

# Обработка кнопок в меню рандомайзера
async def handle_randomizer_buttons(call: types.CallbackQuery, state: FSMContext):
    variable_name = call.data.split("|")[1]
    
    # Если была выбрана кнопка "➕ Добавить переменную"
    if variable_name == "add_variable":
        await call.message.edit_text(text.ADD_VARIABLE_FOR_RANDOMIZER_TEXT)
        await state.set_state(UserState.write_variable_for_randomizer)

    else:
        await call.message.edit_text(text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name))


# Обработка нажатия кнопок в меню действий с переменной в рандомайзере
async def handle_variable_action_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    action = call.data.split("|")[2]
    variable_name = call.data.split("|")[3]

    # Если была выбрана кнопка "➕ Добавить значения"
    if action == "add_values":
        await call.message.answer(text.ADD_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name))
        await state.set_state(UserState.write_value_for_variable_for_randomizer)



# Обработка ввода переменных для рандомайзера
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


# Обработка ввода значения для переменной для рандомайзера
async def write_value_for_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    all_variable_names = data["variable_names_for_randomizer"]
    variable_name = all_variable_names[-1]
    variable_name_values = f"randomizer_{variable_name}_values"

    # Если пользователь нажал на кнопку "🚫 Остановить ввод значений", то прекращаем ввод значений для переменной
    if message.text == "🚫 Остановить ввод значений":
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

    router.callback_query.register(handle_randomizer_buttons, lambda call: call.data.startswith("randomizer"))

    router.message.register(write_variable_for_randomizer, StateFilter(UserState.write_variable_for_randomizer))

    router.message.register(write_value_for_variable_for_randomizer, StateFilter(UserState.write_value_for_variable_for_randomizer))
