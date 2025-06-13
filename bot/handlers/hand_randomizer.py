from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from InstanceBot import router
from keyboards import randomizer_keyboards
from logger import logger
from states.RandomizerState import RandomizerState
from utils import text
from utils.handlers.messages import editMessageOrAnswer
from utils.handlers.startGeneration import generateImagesInHandler


# Обработка кнопок в меню
async def handle_randomizer_buttons(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split("|")[1]

    # Получаем имена переменных
    stateData = await state.get_data()
    variable_names = stateData.get("variable_names_for_randomizer", [])

    # Если была выбрана кнопка "➕ Добавить переменную"
    if action == "add_variable":
        await editMessageOrAnswer(
        call,text.ADD_VARIABLE_FOR_RANDOMIZER_TEXT)
        await state.set_state(RandomizerState.write_variable_for_randomizer)

    # Если была выбрана кнопка "💬 Одно сообщение"
    elif action == "one_message":
        await editMessageOrAnswer(
        call,text.ONE_MESSAGE_FOR_RANDOMIZER_TEXT)
        await state.set_state(RandomizerState.write_one_message_for_randomizer)

    # Если была выбрана кнопка "⚡️ Начать генерацию"
    elif action == "start_generation":
        stateData = await state.get_data()

        # Если нету переменных для рандомайзера, то отправляем сообщение с ошибкой
        if len(variable_names) == 0:
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
        variable_index = int(action)
        await state.update_data(selected_variable_index=variable_index)
        await editMessageOrAnswer(
        call,text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_names[variable_index]),
        reply_markup=randomizer_keyboards.variableActionKeyboard(variable_index))


# Обработка нажатия кнопок в меню действий с переменной
async def handle_variable_action_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    action = call.data.split("|")[1]
    stateData = await state.get_data()
    variable_names = stateData.get("variable_names_for_randomizer", [])

    # Если была выбрана кнопка "🔙 Назад"
    if action == "back":
        await editMessageOrAnswer(
        call,text.RANDOMIZER_MENU_TEXT,
        reply_markup=randomizer_keyboards.randomizerKeyboard(variable_names))
        return

    variable_index = int(call.data.split("|")[2])

    # Если была выбрана кнопка "➕ Добавить значения"
    if action == "add_val":
        await editMessageOrAnswer(
        call,text.ADD_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_names[variable_index]))
        await state.set_state(RandomizerState.write_value_for_variable_for_randomizer)

    # Если была выбрана кнопка "🗑️ Удалить значение"
    elif action == "delete_val":
        variable_name = variable_names[variable_index]
        variable_name_values = f"randomizer_{variable_name}_values"
        values = stateData.get(variable_name_values, [])

        await editMessageOrAnswer(
        call,text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_names[variable_index]),
        reply_markup=randomizer_keyboards.deleteValuesForVariableKeyboard(values, variable_index))

    # Если была выбрана кнопка "❌ Удалить переменную"
    elif action == "delete_var":
        stateData = await state.get_data()
        variable_names_for_randomizer = stateData.get("variable_names_for_randomizer", [])
        variable_names_for_randomizer.remove(variable_names[variable_index])
        await state.update_data(**stateData)
        await editMessageOrAnswer(
        call,text.RANDOMIZER_MENU_TEXT,
        reply_markup=randomizer_keyboards.randomizerKeyboard(variable_names_for_randomizer))


# Обработка нажатия кнопок для удаления значения из переменной
async def handle_delete_value_for_variable_buttons(call: types.CallbackQuery, state: FSMContext):
    # Если была выбрана кнопка "🔙 Назад"
    stateData = await state.get_data()
    variable_names = stateData.get("variable_names_for_randomizer", [])

    if call.data == "randomizer_delete_value|back":
        selected_variable_index = int(stateData.get("selected_variable_index", 0))
        selected_variable_name = variable_names[selected_variable_index]
        await editMessageOrAnswer(
        call,text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(selected_variable_name),
        reply_markup=randomizer_keyboards.variableActionKeyboard(selected_variable_index))
        return

    # Получаем данные
    variable_index = int(call.data.split("|")[1])
    value_index = int(call.data.split("|")[2])
    variable_name = variable_names[variable_index]
    variable_name_values = f"randomizer_{variable_name}_values"
    values = stateData.get(variable_name_values, [])
    value = values[value_index]

    # Удаляем значение
    values.remove(value)

    # Обновляем стейт
    await state.update_data(**{variable_name_values: values})

    # Отправляем сообщение с обновленной клавиатурой
    await editMessageOrAnswer(
        call,text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name),
        reply_markup=randomizer_keyboards.deleteValuesForVariableKeyboard(values, variable_index))


# Обработка ввода переменных
async def write_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    stateData = await state.get_data()
    variable_name = message.text

    # Если переменная ещё не добавлена в стейт, то добавляем её
    if "variable_names_for_randomizer" not in stateData:
        variable_names_for_randomizer = [variable_name]
        await state.update_data(variable_names_for_randomizer=variable_names_for_randomizer)
    else:
        variable_names_for_randomizer = stateData.get("variable_names_for_randomizer", [])
        if variable_name not in variable_names_for_randomizer:
            variable_names_for_randomizer.append(variable_name)
            await state.update_data(variable_names_for_randomizer=variable_names_for_randomizer)
        else:
            await message.answer(text.VARIABLE_ALREADY_EXISTS_TEXT)
            return
        
    # Устанавливаем значение для стейта, что выбрана переменная с данным индексом
    await state.update_data(selected_variable_index=len(variable_names_for_randomizer) - 1)

    # Отправляем сообщение
    await state.set_state(None)
    await message.answer(text.WRITE_VARIABLE_FOR_RANDOMIZER_TEXT,
        reply_markup=randomizer_keyboards.stopInputValuesForVariableKeyboard())
    await state.set_state(RandomizerState.write_value_for_variable_for_randomizer)


# Обработка ввода значения для переменной
async def write_value_for_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    stateData = await state.get_data()
    all_variable_names = stateData.get("variable_names_for_randomizer", [])
    variable_index = int(stateData.get("selected_variable_index", 0))
    variable_name = all_variable_names[variable_index]
    variable_name_values = f"randomizer_{variable_name}_values"

    # Если пользователь нажал на кнопку "🚫 Остановить ввод значений", то прекращаем ввод значений для переменной
    if message.text == "🚫 Остановить ввод значений":
        if variable_name:
            await message.answer(text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name),
            reply_markup=randomizer_keyboards.variableActionKeyboard(variable_index))
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
    value = value[:10] + "..."
    await message.answer(text.WRITE_VALUE_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(value, variable_name),
                         reply_markup=randomizer_keyboards.stopInputValuesForVariableKeyboard())
    await state.set_state(RandomizerState.write_value_for_variable_for_randomizer)


# Обработка ввода одного сообщения для рандомайзера
async def write_one_message_for_randomizer(message: types.Message, state: FSMContext):
    """
    Переменная 1: значение 1/значение 2/значение 3;
    Переменная 2: значение 1/значение 2/значение 3;
    Переменная 3: значение 1/значение 2/значение 3;
    """
    # Разбиваем сообщение на строки и удаляем пустые строки
    lines = [line.strip() for line in message.text.split('\n') if line.strip()]
    
    # Проверяем, что есть хотя бы одна строка
    if not lines:
        await message.answer("Сообщение пустое. Пожалуйста, введите данные в правильном формате.")
        return

    # Очищаем предыдущие данные
    await state.update_data(variable_names_for_randomizer=[])

    variable_names = []
    
    # Обрабатываем каждую строку
    for line in lines:
        # Проверяем формат строки (должна содержать ":")
        if ":" not in line:
            await message.answer(f"Неправильный формат строки: {line}\nКаждая строка должна содержать название переменной, двоеточие и значения.")
            return
            
        # Разделяем на название переменной и значения
        variable_name, values_str = line.split(":", 1)
        variable_name = variable_name.strip()
        
        # Проверяем, что строка заканчивается на точку с запятой
        if not values_str.strip().endswith(";"):
            await message.answer(f"Строка должна заканчиваться точкой с запятой (;): {line}")
            return
            
        # Убираем точку с запятой и разбиваем значения по слешу
        values = [val.strip() for val in values_str.rstrip(";").split("/")]
        values = [val for val in values if val]  # Удаляем пустые значения
        
        # Проверяем, что есть хотя бы одно значение
        if not values:
            await message.answer(f"Не указаны значения для переменной: {variable_name}")
            return
            
        # Добавляем переменную и её значения в state
        variable_names.append(variable_name)
        await state.update_data(**{f"randomizer_{variable_name}_values": values})
    
    # Сохраняем список имен переменных
    await state.update_data(variable_names_for_randomizer=variable_names)
    
    # Отправляем сообщение об успешном добавлении
    await message.answer(text.ONE_MESSAGE_FOR_RANDOMIZER_SUCCESS_TEXT)
    
    await message.answer(
        text.RANDOMIZER_MENU_TEXT,
        reply_markup=randomizer_keyboards.randomizerKeyboard(variable_names)
    )
    await state.set_state(None)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(handle_variable_action_buttons, lambda call: call.data.startswith("var"))

    router.callback_query.register(handle_delete_value_for_variable_buttons, lambda call: call.data.startswith("randomizer_delete_value"))

    router.callback_query.register(handle_randomizer_buttons, lambda call: call.data.startswith("randomizer"))

    router.message.register(write_variable_for_randomizer, StateFilter(RandomizerState.write_variable_for_randomizer))

    router.message.register(write_value_for_variable_for_randomizer, StateFilter(RandomizerState.write_value_for_variable_for_randomizer))

    router.message.register(write_one_message_for_randomizer, StateFilter(RandomizerState.write_one_message_for_randomizer))