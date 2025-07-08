import re
import traceback

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getAllDataArrays,
    getDataByModelName,
    getModelNameIndex,
    getModelNameByIndex
)
from bot.helpers.generateImages.generateImageBlock import generateImageBlock
from bot.helpers.handlers.messages import deleteMessageFromState
from bot.helpers.handlers.startGeneration import (
    generateImagesInHandler,
    process_image,
    regenerateImage,
)
from bot.InstanceBot import bot, router
from bot.keyboards import (
    randomizer_keyboards,
    start_generation_keyboards,
)
from bot.logger import logger
from bot.states.StartGenerationState import StartGenerationState
from bot.utils.handlers import (
    appendDataToStateArray,
)
from bot.utils.handlers.messages import (
    editMessageOrAnswer,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)

PROMPT_BY_INDEX_PATTERN = re.compile(
    r"(?s)(\d+)\s*[:\-–—]\s*(.*?)(?=(?:\n\d+\s*[:\-–—])|\Z)",
)


# Обработка выбора количества генераций
async def choose_generations_type(
    call: types.CallbackQuery,
    state: FSMContext,
):
    generations_type = call.data.split("|")[1]
    await state.update_data(generations_type=generations_type)

    if generations_type == "work":
        await editMessageOrAnswer(
            call,
            "Выберите режим генерации:\n\n"
            "🖼 Мультивыбор - можно выбрать несколько фотографий одновременно, присылается 10 на выбор\n"
            "✅ Одиночный - можно выбрать только одну генерацию, присылается 4 на выбор",
            reply_markup=start_generation_keyboards.generationModeKeyboard(),
        )
        return

    try:
        prompt_exist = bool(call.data.split("|")[2])
    except:
        prompt_exist = False

    await state.update_data(prompt_exist=prompt_exist)

    await editMessageOrAnswer(
        call,
        text.GET_GENERATIONS_SUCCESS_TEXT,
        reply_markup=start_generation_keyboards.selectSettingKeyboard(
            is_test_generation=generations_type == "test",
        ),
    )


# Обработка выбора режима генерации
async def choose_generation_mode(call: types.CallbackQuery, state: FSMContext):
    mode = call.data.split("|")[1]
    if mode == "multi_select":
        await state.update_data(multi_select_mode=True)
    else:
        await state.update_data(multi_select_mode=False)
    await editMessageOrAnswer(
        call,
        "✅ Тип генерации успешно выбран! Теперь выбери какую настройку будешь использовать:",
        reply_markup=start_generation_keyboards.selectSettingKeyboard(
            is_test_generation=False,
        ),
    )


# Обработка выбора настройки
async def choose_setting(call: types.CallbackQuery, state: FSMContext):
    # Получаем текущие данные стейта для извлечения переменных рандомайзера
    current_state_data = await state.get_data()
    variable_names_for_randomizer = current_state_data.get(
        "variable_names_for_randomizer",
        [],
    )

    # Создаем базовый initial_state
    initial_state = {
        "generation_step": 1,
        "prompts_for_regenerated_models": [],
        "regenerated_models": [],
        "model_indexes_for_generation": [],
        "saved_images_urls": [],
        "faceswap_generated_models": [],
        "imageGeneration_mediagroup_messages_ids": [],
        "videoGeneration_messages_ids": [],
        "process_images_steps": [],
        "upscale_progress_messages": [],
        "variable_names_for_randomizer": [],
        "generated_video_paths": [],
        "model_prompts_for_generation": [],
    }

    # Добавляем все ключи с формой "randomizer_{variable_name}_values" со значением [] (для очистки данных рандомайзера)
    for variable_name in variable_names_for_randomizer:
        key = f"randomizer_{variable_name}_values"
        initial_state[key] = []

    await state.update_data(**initial_state)

    # Если выбрана конкретная модель, то просим ввести название модели
    if call.data == "select_setting|specific_model":
        await editMessageOrAnswer(
            call,
            text.WRITE_MODELS_NAME_TEXT,
        )
        await state.update_data(specific_model=True)
        # Очищаем стейт
        await state.set_state(
            StartGenerationState.write_model_name_for_generation,
        )
        return

    # Если выбрана другая настройка, то продолжаем генерацию
    setting_number = call.data.split("|")[1]
    await state.update_data(setting_number=setting_number)
    state_data = await state.get_data()
    generations_type = state_data.get("generations_type", "")
    prompt_exist = state_data.get("prompt_exist", False)
    await state.update_data(specific_model=False)

    # Если выбрана настройка для теста, то продолжаем генерацию в тестовом режиме
    if generations_type == "test":
        if prompt_exist:
            prompt = state_data.get("prompt_for_images", "")
            user_id = call.from_user.id
            is_test_generation = generations_type == "test"
            setting_number = setting_number

            # Удаляем сообщение с выбором настройки
            await bot.delete_message(user_id, call.message.message_id)

            await generateImagesInHandler(
                prompt,
                call.message,
                state,
                user_id,
                is_test_generation,
                setting_number,
            )

            await state.update_data(prompt_exist=False)
        else:
            await editMessageOrAnswer(
                call,
                text.GET_SETTINGS_SUCCESS_TEXT,
            )
            await state.set_state(StartGenerationState.write_prompt_for_images)

    # Если выбрана настройка для работы, то продолжаем генерацию в рабочем режиме
    elif generations_type == "work":
        await editMessageOrAnswer(
            call,
            text.CHOOSE_WRITE_PROMPT_TYPE_SUCCESS_TEXT,
            reply_markup=start_generation_keyboards.writePromptTypeKeyboard(),
        )


# Обработка выбора режима написания промпта
async def choose_writePrompt_type(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем тип: one или multi
    prompt_type = call.data.split("|")[1]
    await state.update_data(writePrompt_type=prompt_type)

    if prompt_type == "one":
        # Один промпт на все модели
        await editMessageOrAnswer(
            call,
            text.GET_ONE_PROMPT_GENERATION_SUCCESS_TEXT,
            reply_markup=start_generation_keyboards.onePromptGenerationChooseTypeKeyboard(),
        )
        return

    state_data = await state.get_data()
    setting_number = state_data.get("setting_number", 1)

    # Получаем допустимые индексы моделей
    if setting_number == "all":
        # Если выбрано all — берём все модели
        all_data_arrays = getAllDataArrays()
        start_index = 1
        end_index = sum(len(setting) for setting in all_data_arrays)
    else:
        # Берём только модели из выбранной настройки
        all_data_arrays = getAllDataArrays()
        logger.info([len(arr) for arr in all_data_arrays])
        setting_index = int(setting_number) - 1

        # Считаем смещение как сумму длин всех предыдущих сетов
        offset = sum(len(arr) for arr in all_data_arrays[:setting_index])

        # Длина текущего сета
        setting_length = len(all_data_arrays[setting_index])

        start_index = offset + 1
        end_index = offset + setting_length

    # Сохраняем диапазон индексов в стейт
    await state.update_data(valid_model_indexes_range=(start_index, end_index))

    await editMessageOrAnswer(
        call,
        text.WRITE_PROMPTS_FOR_MODELS_TEXT.format(start_index, end_index),
    )
    await state.set_state(StartGenerationState.write_multi_prompts_for_models)


# Обработка списка "индекс: промпт" для текущей настройки
async def write_prompts_for_models(message: types.Message, state: FSMContext):
    text_input = message.text.strip()
    matches = PROMPT_BY_INDEX_PATTERN.findall(text_input)

    if not matches:
        await safe_send_message(
            text.EMPTY_MATCHES_WRITE_PROMPTS_TEXT,
            message,
        )
        return

    state_data = await state.get_data()
    valid_range = state_data.get("valid_model_indexes_range", (1, 100))
    start_index, end_index = valid_range
    user_id = message.from_user.id
    expected_count = end_index - start_index + 1
    setting_number = state_data.get("setting_number", "1")

    model_prompts = {}
    for index_str, prompt in matches:
        if not index_str.isdigit():
            continue
        index = int(index_str)
        if not (start_index <= index <= end_index):
            await safe_send_message(
                text.MODEL_NOT_FOUND_TEXT.format(index),
                message,
            )
            return
        model_prompts[str(index)] = prompt.strip()

    if len(model_prompts) != expected_count:
        await safe_send_message(
            f"⚠️ Нужно указать <b>ровно {expected_count}</b> промптов (а не {len(model_prompts)}).",
            message,
        )
        return

    data_for_update = {
        f"{getModelNameByIndex(str(index))}": prompt
        for index, prompt in model_prompts.items()
    }
    await appendDataToStateArray(
        state,
        "model_prompts_for_generation",
        data_for_update,
        unique_keys=("model_name"),
    )

    await safe_send_message(
        "✅ Промпты получены. Начинаю генерацию...",
        message,
    )

    try:
        await generateImagesInHandler(
            prompt=model_prompts,
            message=message,
            state=state,
            user_id=user_id,
            is_test_generation=False,
            setting_number=setting_number,
            with_randomizer=False,
        )
    except Exception:
        await safe_send_message("❌ Произошла ошибка при генерации", message)
        return

    await safe_send_message("✅ Генерация завершена", message)


# Обработка выбора режима при генерации с одним промптом
async def chooseOnePromptGenerationType(
    call: types.CallbackQuery,
    state: FSMContext,
):
    one_prompt_generation_type = call.data.split("|")[1]

    if one_prompt_generation_type == "static":
        await editMessageOrAnswer(
            call,
            text.GET_STATIC_PROMPT_TYPE_SUCCESS_TEXT,
        )
        await state.set_state(StartGenerationState.write_prompt_for_images)

    elif one_prompt_generation_type == "random":
        # Очищаем все данные, которые используются в рандомайзере
        await state.update_data(variable_names_for_randomizer=[])
        await state.update_data(variable_name_values=[])
        await editMessageOrAnswer(
            call,
            text.GET_RANDOM_PROMPT_TYPE_SUCCESS_TEXT,
            reply_markup=randomizer_keyboards.randomizerKeyboard([]),
        )


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    user_id = message.from_user.id
    state_data = await state.get_data()
    is_test_generation = state_data.get("generations_type", "") == "test"
    await state.update_data(prompt_for_images=prompt)

    await state.set_state(None)

    # Если в стейте есть номер настройки, то используем его, иначе получаем номер настройки по названию модели
    if "setting_number" in state_data:
        setting_number = state_data.get("setting_number", 1)

        # Генерируем изображения
        await generateImagesInHandler(
            prompt,
            message,
            state,
            user_id,
            is_test_generation,
            setting_number,
        )
    else:
        model_indexes = state_data.get("model_indexes_for_generation", [])
        logger.info(f"Список моделей для генерации: {model_indexes}")

        # Генерируем изображения
        await generateImagesInHandler(
            prompt,
            message,
            state,
            user_id,
            is_test_generation,
            "individual",
        )


# Обработка выбора изображения
async def select_image(call: types.CallbackQuery, state: FSMContext):
    # Отправляем сообщение о выборе изображения
    await editMessageOrAnswer(
        call,
        text.SELECT_IMAGE_PROGRESS_TEXT,
    )

    # Получаем индекс работы и индекс изображения
    model_name = call.data.split("|")[1]
    setting_number = call.data.split("|")[2]
    image_index = call.data.split("|")[3]

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Удаляем медиагруппу
    await deleteMessageFromState(
        state,
        "imageGeneration_mediagroup_messages_ids",
        model_name,
        call.message.chat.id,
    )

    try:
        # Если индекс изображения равен "regenerate", то перегенерируем изображение
        if image_index == "regenerate":
            return await regenerateImage(
                model_name,
                call,
                state,
                setting_number,
            )

        # Если индекс изображения равен "regenerate_with_new_prompt", то перегенерируем изображение с новым промптом
        elif image_index == "regenerate_with_new_prompt":
            # Устанавливаем стейт для ввода нового промпта
            await state.update_data(model_name_for_regenerate_image=model_name)
            await state.update_data(
                setting_number_for_regenerate_image=setting_number,
            )

            await state.set_state(
                StartGenerationState.write_new_prompt_for_regenerate_image,
            )

            # Просим ввести новый промпт
            write_new_prompt_for_regenerate_message = (
                await editMessageOrAnswer(call, text.WRITE_NEW_PROMPT_TEXT)
            )
            await state.update_data(
                write_new_prompt_message_id=write_new_prompt_for_regenerate_message.message_id,
            )
            return

        image_index = int(image_index)

        # Если данные не найдены, ищем во всех доступных массивах
        if data is None:
            all_data_arrays = getAllDataArrays()
            for arr in all_data_arrays:
                data = next(
                    (d for d in arr if d["model_name"] == model_name),
                    None,
                )
                if data is not None:
                    break

        # Сохраняем название модели и id папки для видео
        await state.update_data(model_name=model_name)

        try:
            logger.info("Обрабатываем изображение")
            await process_image(
                call,
                state,
                model_name,
                image_index,
            )
        except Exception as e:
            logger.exception("Ошибка в process_image")
            await editMessageOrAnswer(
                call,
                f"❌ Ошибка при обработке изображения: {e}",
            )

    except Exception as e:
        traceback.print_exc()
        model_name_index = getModelNameIndex(model_name)

        await editMessageOrAnswer(
            call,
            text.GENERATE_IMAGE_ERROR_TEXT.format(
                model_name,
                model_name_index,
                e,
            ),
        )
        raise e


async def write_model_name_for_generation(
    message: types.Message,
    state: FSMContext,
):
    text_input = message.text.strip()

    # 1. Новый формат: 1 - текст
    matches = PROMPT_BY_INDEX_PATTERN.findall(text_input)

    if matches:
        model_prompts = {}
        for index, prompt in matches:
            if not index.isdigit():
                continue
            if not (1 <= int(index) <= 100):
                await safe_send_message(
                    text=text.MODEL_NOT_FOUND_TEXT.format(index),
                    message=message,
                )
                return
            model_prompts[str(index)] = prompt.strip()

        data_for_update = {
            f"{getModelNameByIndex(str(index))}": prompt
            for index, prompt in model_prompts.items()
        }
        await appendDataToStateArray(
            state,
            "model_prompts_for_generation",
            data_for_update,
        )

        await safe_send_message(
            text="✅ Промпты по моделям получены, начинаю генерацию...",
            message=message,
        )

        await generateImagesInHandler(
            prompt=model_prompts,
            message=message,
            state=state,
            user_id=message.from_user.id,
            is_test_generation=False,
            setting_number="individual",
        )
        return

    # 2. Старый формат: одна модель или через запятую

    # Проверяем, что введённое значение является числом
    if not message.text.isdigit():
        await safe_send_message(
            text=text.NOT_NUMBER_TEXT,
            message=message,
        )
        return

    model_indexes = message.text.split(",")
    if len(model_indexes) == 1:
        model_indexes = [message.text]

    # Получаем данные всех моделей
    all_data_arrays = getAllDataArrays()
    all_data_arrays_length = sum(len(arr) for arr in all_data_arrays)

    # Проверяем, существует ли такие модели
    for model_index in model_indexes:
        # Если индекс больше числа моделей или меньше 1, то просим ввести другой индекс
        if int(model_index) > all_data_arrays_length or int(model_index) < 1:
            await safe_send_message(
                text=text.MODEL_NOT_FOUND_TEXT.format(model_index),
                message=message,
            )
            return

    await state.update_data(model_indexes_for_generation=model_indexes)
    # Всё валидно — идём по старой логике
    await state.update_data(
        model_indexes_for_generation=model_indexes,
    )

    await state.set_state(None)
    await safe_send_message(
        text=text.GET_MODEL_INDEX_SUCCESS_TEXT
        if len(model_indexes) == 1
        else text.GET_MODEL_INDEXES_SUCCESS_TEXT,
        message=message,
    )

    await state.set_state(StartGenerationState.write_prompt_for_images)


# Обработка ввода нового промпта для перегенерации изображения
async def write_new_prompt_for_regenerate_image(
    message: types.Message,
    state: FSMContext,
):
    # Получаем данные
    prompt = message.text
    if not prompt:
        await safe_send_message(
            text=text.EMPTY_PROMPT_TEXT,
            message=message,
        )
        return

    state_data = await state.get_data()
    is_test_generation = state_data.get("generations_type", "") == "test"
    model_name = state_data.get("model_name_for_regenerate_image", "")
    setting_number = state_data.get("setting_number_for_regenerate_image", 1)
    user_id = message.from_user.id

    # Удаляем сообщение пользователя
    await message.delete()

    # Удаляем сообщение бота
    write_new_prompt_message_id = state_data.get(
        "write_new_prompt_message_id",
        None,
    )
    if write_new_prompt_message_id:
        try:
            await bot.delete_message(user_id, write_new_prompt_message_id)
        except Exception as e:
            logger.error(
                f"Не удалось удалить сообщение для перегенерации изображения по"
                f"новому промпту {write_new_prompt_message_id} - {e}",
            )

    # Записываем новый промпт в стейт для этой модели
    data_for_update = {f"{model_name}": prompt}
    await appendDataToStateArray(
        state,
        "prompts_for_regenerated_models",
        data_for_update,
    )

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о перегенерации изображения
    modified_prompt = prompt[:30] + "..." if len(prompt) > 30 else prompt
    regenerate_progress_message = await safe_send_message(
        text=text.REGENERATE_IMAGE_WITH_NEW_PROMPT_TEXT.format(
            model_name,
            model_name_index,
            modified_prompt,
        ),
        message=message,
    )

    await state.set_state(None)

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    await generateImageBlock(
        data,
        regenerate_progress_message.message_id,
        state,
        user_id,
        setting_number,
        prompt,
        is_test_generation,
        False,
        chat_id=message.chat.id,
    )
    await regenerate_progress_message.delete()


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        choose_generations_type,
        lambda call: call.data.startswith("generations_type"),
    )

    router.callback_query.register(
        choose_generation_mode,
        lambda call: call.data.startswith("generation_mode"),
    )

    router.callback_query.register(
        choose_setting,
        lambda call: call.data.startswith("select_setting"),
    )

    router.callback_query.register(
        choose_writePrompt_type,
        lambda call: call.data.startswith("write_prompt_type"),
    )

    router.callback_query.register(
        chooseOnePromptGenerationType,
        lambda call: call.data.startswith("one_prompt_generation_type"),
    )

    router.message.register(
        write_prompt,
        StateFilter(StartGenerationState.write_prompt_for_images),
    )

    router.callback_query.register(
        select_image,
        lambda call: call.data.startswith("select_image"),
    )

    router.message.register(
        write_model_name_for_generation,
        StateFilter(StartGenerationState.write_model_name_for_generation),
    )

    router.message.register(
        write_new_prompt_for_regenerate_image,
        StateFilter(
            StartGenerationState.write_new_prompt_for_regenerate_image,
        ),
    )
    router.message.register(
        write_prompts_for_models,
        StartGenerationState.write_multi_prompts_for_models,
    )
