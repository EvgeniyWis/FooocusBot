from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.handlers.startGeneration import generateImagesInHandler
from bot.InstanceBot import router
from bot.keyboards import randomizer_keyboards
from bot.states.RandomizerState import RandomizerState
from bot.utils.handlers.messages import editMessageOrAnswer
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_edit_message,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Обработка кнопок в меню
async def handle_randomizer_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    action = call.data.split("|")[1]

    # Получаем имена переменных
    state_data = await state.get_data()
    variable_names = state_data.get("variable_names_for_randomizer", [])

    # Если была выбрана кнопка "➕ Добавить переменную"
    if action == "add_variable":
        await editMessageOrAnswer(call, text.ADD_VARIABLE_FOR_RANDOMIZER_TEXT)
        await state.set_state(RandomizerState.write_variable_for_randomizer)

    # Если была выбрана кнопка "💬 Одно сообщение"
    elif action == "one_message":
        await safe_edit_message(
            call.message,
            text.ONE_MESSAGE_FOR_RANDOMIZER_TEXT,
            parse_mode="HTML",
        )
        await state.set_state(RandomizerState.write_one_message_for_randomizer)

    # Если была выбрана кнопка "⚡️ Начать генерацию"
    elif action == "start_generation":
        state_data = await state.get_data()

        # Если нету переменных для рандомайзера, то отправляем сообщение с ошибкой
        if len(variable_names) == 0:
            await call.answer(
                text.VARIABLES_FOR_RANDOMIZER_NOT_WRITTEN_TEXT,
                show_alert=True,
            )
            return

        else:
            # Удаляем текущее сообщение
            await call.message.delete()

            # Отправляем сообщение о генерации
            user_id = call.from_user.id
            setting_number = state_data.get("setting_number", 1)
            is_test_generation = setting_number == "test"
            await generateImagesInHandler(
                "",
                call.message,
                state,
                user_id,
                is_test_generation,
                setting_number,
                True,
            )

    else:
        variable_index = int(action)
        await state.update_data(selected_variable_index=variable_index)
        await editMessageOrAnswer(
            call,
            text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(
                variable_names[variable_index],
            ),
            reply_markup=randomizer_keyboards.variableActionKeyboard(
                variable_index,
            ),
        )


# Обработка нажатия кнопок в меню действий с переменной
async def handle_variable_action_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем данные
    action = call.data.split("|")[1]
    state_data = await state.get_data()
    variable_names = state_data.get("variable_names_for_randomizer", [])

    # Если была выбрана кнопка "🔙 Назад"
    if action == "back":
        await editMessageOrAnswer(
            call,
            text.RANDOMIZER_MENU_TEXT,
            reply_markup=randomizer_keyboards.randomizerKeyboard(
                variable_names,
            ),
        )
        return

    variable_index = int(call.data.split("|")[2])

    # Если была выбрана кнопка "➕ Добавить значения"
    if action == "add_val":
        await editMessageOrAnswer(
            call,
            text.ADD_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(
                variable_names[variable_index],
            ),
        )
        await state.set_state(
            RandomizerState.write_value_for_variable_for_randomizer,
        )

    # Если была выбрана кнопка "🗑️ Удалить значение"
    elif action == "delete_val":
        variable_name = variable_names[variable_index]
        variable_name_values = f"randomizer_{variable_name}_values"
        values = state_data.get(variable_name_values, [])

        await editMessageOrAnswer(
            call,
            text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(
                variable_names[variable_index],
            ),
            reply_markup=randomizer_keyboards.deleteValuesForVariableKeyboard(
                values,
                variable_index,
            ),
        )

    # Если была выбрана кнопка "❌ Удалить переменную"
    elif action == "delete_var":
        state_data = await state.get_data()
        variable_names_for_randomizer = state_data.get(
            "variable_names_for_randomizer",
            [],
        )
        variable_names_for_randomizer.remove(variable_names[variable_index])
        await state.update_data(**state_data)
        await editMessageOrAnswer(
            call,
            text.RANDOMIZER_MENU_TEXT,
            reply_markup=randomizer_keyboards.randomizerKeyboard(
                variable_names_for_randomizer,
            ),
        )


# Обработка нажатия кнопок для удаления значения из переменной
async def handle_delete_value_for_variable_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Если была выбрана кнопка "🔙 Назад"
    state_data = await state.get_data()
    variable_names = state_data.get("variable_names_for_randomizer", [])

    if call.data == "randomizer_delete_value|back":
        selected_variable_index = int(
            state_data.get("selected_variable_index", 0),
        )
        selected_variable_name = variable_names[selected_variable_index]
        await editMessageOrAnswer(
            call,
            text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(
                selected_variable_name,
            ),
            reply_markup=randomizer_keyboards.variableActionKeyboard(
                selected_variable_index,
            ),
        )
        return

    # Получаем данные
    variable_index = int(call.data.split("|")[1])
    value_index = int(call.data.split("|")[2])
    variable_name = variable_names[variable_index]
    variable_name_values = f"randomizer_{variable_name}_values"
    values = state_data.get(variable_name_values, [])
    value = values[value_index]

    # Удаляем значение
    values.remove(value)

    # Обновляем стейт
    await state.update_data(**{variable_name_values: values})

    # Отправляем сообщение с обновленной клавиатурой
    await editMessageOrAnswer(
        call,
        text.DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(
            variable_name,
        ),
        reply_markup=randomizer_keyboards.deleteValuesForVariableKeyboard(
            values,
            variable_index,
        ),
    )


# Обработка ввода переменных
async def write_variable_for_randomizer(
    message: types.Message,
    state: FSMContext,
):
    # Получаем данные
    state_data = await state.get_data()
    variable_name = message.text

    # Если переменная ещё не добавлена в стейт, то добавляем её
    if "variable_names_for_randomizer" not in state_data:
        variable_names_for_randomizer = [variable_name]
        await state.update_data(
            variable_names_for_randomizer=variable_names_for_randomizer,
        )
    else:
        variable_names_for_randomizer = state_data.get(
            "variable_names_for_randomizer",
            [],
        )
        if variable_name not in variable_names_for_randomizer:
            variable_names_for_randomizer.append(variable_name)
            await state.update_data(
                variable_names_for_randomizer=variable_names_for_randomizer,
            )
        else:
            await safe_send_message(text.VARIABLE_ALREADY_EXISTS_TEXT, message)
            return

    # Устанавливаем значение для стейта, что выбрана переменная с данным индексом
    await state.update_data(
        selected_variable_index=len(variable_names_for_randomizer) - 1,
    )

    # Отправляем сообщение
    await state.set_state(None)
    await safe_send_message(
        text.WRITE_VARIABLE_FOR_RANDOMIZER_TEXT,
        message,
        reply_markup=randomizer_keyboards.stopInputValuesForVariableKeyboard(),
    )
    await state.set_state(
        RandomizerState.write_value_for_variable_for_randomizer,
    )


# Обработка ввода значения для переменной
async def write_value_for_variable_for_randomizer(
    message: types.Message,
    state: FSMContext,
):
    # Получаем данные
    state_data = await state.get_data()
    all_variable_names = state_data.get("variable_names_for_randomizer", [])
    variable_index = int(state_data.get("selected_variable_index", 0))
    variable_name = all_variable_names[variable_index]
    variable_name_values = f"randomizer_{variable_name}_values"

    # Если пользователь нажал на кнопку "🚫 Остановить ввод значений", то прекращаем ввод значений для переменной
    if message.text == "🚫 Остановить ввод значений":
        if variable_name:
            await safe_send_message(
                text.SELECT_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name),
                message,
                reply_markup=randomizer_keyboards.variableActionKeyboard(
                    variable_index,
                ),
            )
        else:
            await safe_send_message(
                text.RANDOMIZER_MENU_TEXT,
                message,
                reply_markup=randomizer_keyboards.randomizerKeyboard(
                    all_variable_names,
                ),
            )
        return

    # Получаем значение в ином случае
    value = message.text

    # Если переменной ещё нет в стейте, то создаём её
    if variable_name_values not in state_data:
        await state.update_data(**{variable_name_values: [value]})
    else:  # Если переменная уже есть в стейте, то добавляем значение в список
        values = state_data.get(variable_name_values, [])
        values.append(value)
        await state.update_data(**{variable_name_values: values})

    await state.set_state(None)
    value = value[:10] + "..."
    await safe_send_message(
        text.WRITE_VALUE_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(
            value,
            variable_name,
        ),
        message,
        reply_markup=randomizer_keyboards.stopInputValuesForVariableKeyboard(),
    )
    await state.set_state(
        RandomizerState.write_value_for_variable_for_randomizer,
    )


# Обработка ввода одного сообщения для рандомайзера
async def write_one_message_for_randomizer(
    message: types.Message,
    state: FSMContext,
):
    """
    Переменная 1: значение 1/значение 2/значение 3;
    Переменная 2: значение 1/значение 2/значение 3;
    Переменная 3: значение 1/значение 2/значение 3;
    """
    # Разбиваем сообщение на строки и удаляем пустые строки
    lines = [line.strip() for line in message.text.split("\n") if line.strip()]

    # Проверяем, что есть хотя бы одна строка
    if not lines:
        await safe_send_message(
            "Сообщение пустое. Пожалуйста, введите данные в правильном формате.",
            message,
        )
        return

    # Очищаем предыдущие данные
    await state.update_data(variable_names_for_randomizer=[])

    variable_names = []

    # Обрабатываем каждую строку
    for line in lines:
        # Проверяем формат строки (должна содержать ":")
        if ":" not in line:
            await safe_send_message(
                f"Неправильный формат строки: {line}\nКаждая строка должна содержать название переменной, двоеточие и значения.",
                message,
            )
            return

        # Разделяем на название переменной и значения
        variable_name, values_str = line.split(":", 1)
        variable_name = variable_name.strip()

        # Проверяем, что строка заканчивается на точку с запятой
        if not values_str.strip().endswith(";"):
            await safe_send_message(
                f"Строка должна заканчиваться точкой с запятой (;): {line}",
                message,
            )
            return

        # Убираем точку с запятой и разбиваем значения по слешу
        values = [val.strip() for val in values_str.rstrip(";").split("/")]
        values = [val for val in values if val]  # Удаляем пустые значения

        # Проверяем, что есть хотя бы одно значение
        if not values:
            await safe_send_message(
                f"Не указаны значения для переменной: {variable_name}",
                message,
            )
            return

        # Добавляем переменную и её значения в state
        variable_names.append(variable_name)
        await state.update_data(
            **{f"randomizer_{variable_name}_values": values},
        )

    # Сохраняем список имен переменных
    await state.update_data(variable_names_for_randomizer=variable_names)

    # Отправляем сообщение об успешном добавлении
    await safe_send_message(
        text.ONE_MESSAGE_FOR_RANDOMIZER_SUCCESS_TEXT,
        message,
    )

    await safe_send_message(
        text.RANDOMIZER_MENU_TEXT,
        message,
        reply_markup=randomizer_keyboards.randomizerKeyboard(variable_names),
    )
    await state.set_state(None)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        handle_variable_action_buttons,
        lambda call: call.data.startswith("var"),
    )

    router.callback_query.register(
        handle_delete_value_for_variable_buttons,
        lambda call: call.data.startswith("randomizer_delete_value"),
    )

    router.callback_query.register(
        handle_randomizer_buttons,
        lambda call: call.data.startswith("randomizer"),
    )

    router.message.register(
        write_variable_for_randomizer,
        StateFilter(RandomizerState.write_variable_for_randomizer),
    )

    router.message.register(
        write_value_for_variable_for_randomizer,
        StateFilter(RandomizerState.write_value_for_variable_for_randomizer),
    )

    router.message.register(
        write_one_message_for_randomizer,
        StateFilter(RandomizerState.write_one_message_for_randomizer),
    )
