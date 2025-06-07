from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from InstanceBot import router
from keyboards import randomizer_keyboards
from logger import logger
from states.UserState import RandomizerState
from utils import text
from utils.handlers import editMessageOrAnswer
from utils.handlers.startGeneration import generateImagesInHandler


# Обработка кнопок в меню
async def handle_randomizer_buttons(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split("|")[1]

    # Если была выбрана кнопка "➕ Добавить переменную"
    if action == "add_variable":
        await editMessageOrAnswer(
        call,text.ADD_VARIABLE_FOR_RANDOMIZER_TEXT)
        await state.set_state(RandomizerState.write_variable_for_randomizer)

    # Если была выбрана кнопка "⚡️ Начать генерацию"
    elif action == "start_generation":
        stateData = await state.get_data()

        # Если нету переменных для рандомайзера, то отправляем сообщение с ошибкой
        variable_names_for_randomizer = stateData.get("variable_names_for_randomizer", [])
        if len(variable_names_for_randomizer) == 0:
            await call.answer(text.VARIABLES_FOR_RANDOMIZER_NOT_WRITTEN_TEXT, show_alert=True)
            return

        else:
            # Удаляем текущее сообщение
            await call.message.delete()

            # Отправляем сообщение о генерации
            user_id = call.from_user.id
            setting_number = stateData.get("setting_number", 1)
            is_test_generation = setting_number == "test"
            await generateImagesInHandler("", call.message, state, user_id, is_test_generation, setting_number, True)

    else:
        variable_name = action
        await state.update_data(selected_variable_name=variable_name)
        await editMessageOrAnswer(
        call,text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name),
        reply_markup=randomizer_keyboards.variableActionKeyboard(variable_name))


# Обработка нажатия кнопок в меню действий с переменной
async def handle_variable_action_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    action = call.data.split("|")[1]
    stateData = await state.get_data()

    # Если была выбрана кнопка "🔙 Назад"
    if action == "back":
        await editMessageOrAnswer(
        call,text.RANDOMIZER_MENU_TEXT,
        reply_markup=randomizer_keyboards.randomizerKeyboard(stateData.get("variable_names_for_randomizer", [])))
        return

    variable_name = call.data.split("|")[2]
    # Если была выбрана кнопка "➕ Добавить значения"
    if action == "add_val":
        await editMessageOrAnswer(
        call,text.ADD_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name))
        await state.set_state(RandomizerState.write_value_for_variable_for_randomizer)

    # Если была выбрана кнопка "🗑️ Удалить значение"
    elif action == "delete_val":
        variable_name_values = f"randomizer_{variable_name}_values"
        values = stateData.get(variable_name_values, [])

        await editMessageOrAnswer(
        call,text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name),
        reply_markup=randomizer_keyboards.deleteValuesForVariableKeyboard(values, variable_name))

    # Если была выбрана кнопка "❌ Удалить переменную"
    elif action == "delete_var":
        stateData = await state.get_data()
        variable_names_for_randomizer = stateData.get("variable_names_for_randomizer", [])
        variable_names_for_randomizer.remove(variable_name)
        await state.update_data(**stateData)
        await editMessageOrAnswer(
        call,text.RANDOMIZER_MENU_TEXT,
        reply_markup=randomizer_keyboards.randomizerKeyboard(variable_names_for_randomizer))


# Обработка нажатия кнопок для удаления значения из переменной
async def handle_delete_value_for_variable_buttons(call: types.CallbackQuery, state: FSMContext):
    # Если была выбрана кнопка "🔙 Назад"
    stateData = await state.get_data()
    if call.data == "randomizer_delete_value|back":
        selected_variable_name = stateData.get("selected_variable_name", "")
        await editMessageOrAnswer(
        call,text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(selected_variable_name),
        reply_markup=randomizer_keyboards.variableActionKeyboard(selected_variable_name))
        return

    # Получаем данные
    variable_name = call.data.split("|")[1]
    value = call.data.split("|")[2]
    variable_name_values = f"randomizer_{variable_name}_values"
    values = stateData.get(variable_name_values, [])
    values.remove(value)

    # Обновляем стейт
    await state.update_data(**{variable_name_values: values})

    # Отправляем сообщение с обновленной клавиатурой
    await editMessageOrAnswer(
        call,text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name),
        reply_markup=randomizer_keyboards.deleteValuesForVariableKeyboard(values, variable_name))


# Обработка ввода переменных
async def write_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    stateData = await state.get_data()
    variable_name = message.text

    # Если переменная ещё не добавлена в стейт, то добавляем её
    if "variable_names_for_randomizer" not in stateData:
        await state.update_data(variable_names_for_randomizer=[variable_name])
    else:
        variable_names_for_randomizer = stateData.get("variable_names_for_randomizer", [])
        if variable_name not in variable_names_for_randomizer:
            variable_names_for_randomizer.append(variable_name)
            await state.update_data(variable_names_for_randomizer=variable_names_for_randomizer)
        else:
            await message.answer(text.VARIABLE_ALREADY_EXISTS_TEXT)
            return

    await state.set_state(None)
    await message.answer(text.WRITE_VARIABLE_FOR_RANDOMIZER_TEXT,
        reply_markup=randomizer_keyboards.stopInputValuesForVariableKeyboard())
    await state.set_state(RandomizerState.write_value_for_variable_for_randomizer)


# Обработка ввода значения для переменной
async def write_value_for_variable_for_randomizer(message: types.Message, state: FSMContext):
    try:
        # Получаем данные
        stateData = await state.get_data()
        all_variable_names = stateData.get("variable_names_for_randomizer", [])
        variable_name = all_variable_names[-1]
        variable_name_values = f"randomizer_{variable_name}_values"

        # Если пользователь нажал на кнопку "🚫 Остановить ввод значений", то прекращаем ввод значений для переменной
        if message.text == "🚫 Остановить ввод значений":
            selected_variable_name = stateData.get("selected_variable_name", "")
            if selected_variable_name:
                await message.answer(text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(selected_variable_name),
                reply_markup=randomizer_keyboards.variableActionKeyboard(selected_variable_name))
            else:
                await message.answer(text.RANDOMIZER_MENU_TEXT,
                reply_markup=randomizer_keyboards.randomizerKeyboard(all_variable_names))
            return

        # Получаем значение в ином случае
        value = message.text

        # Если переменной ещё нет в стейте, то создаём её
        if variable_name_values not in stateData:
            await state.update_data(**{variable_name_values: [value]})
        else: # Если переменная уже есть в стейте, то добавляем значение в список
            values = stateData.get(variable_name_values, [])
            values.append(value)
            await state.update_data(**{variable_name_values: values})

        await state.set_state(None)
        await message.answer(text.WRITE_VALUE_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(value, variable_name))
        await state.set_state(RandomizerState.write_value_for_variable_for_randomizer)

    except Exception as e:
        logger.error(f"Ошибка при отправке значения для рандомайзера: {e}")


# Добавление обработчиков
def hand_add():
    router.callback_query.register(handle_variable_action_buttons, lambda call: call.data.startswith("var"))

    router.callback_query.register(handle_delete_value_for_variable_buttons, lambda call: call.data.startswith("randomizer_delete_value"))

    router.callback_query.register(handle_randomizer_buttons, lambda call: call.data.startswith("randomizer"))

    router.message.register(write_variable_for_randomizer, StateFilter(RandomizerState.write_variable_for_randomizer))

    router.message.register(write_value_for_variable_for_randomizer, StateFilter(RandomizerState.write_value_for_variable_for_randomizer))
