import asyncio
import os
import traceback

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.constants import TEMP_FOLDER_PATH
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getAllDataArrays,
    getDataArrayBySettingNumber,
    getDataByModelName,
    getModelNameIndex,
    getNextModel,
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
    # Очищаем стейт
    initial_state = {
        "generation_step": 1,
        "prompts_for_regenerated_models": [],
        "regenerated_models": [],
        "model_indexes_for_generation": [],
        "saved_images_urls": [],
        "faceswap_generated_models": [],
        "imageGeneration_mediagroup_messages_ids": [],
        "videoGeneration_messages_ids": [],
    }

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
    # Получаем данные
    writePrompt_type = call.data.split("|")[1]
    await state.update_data(writePrompt_type=writePrompt_type)

    if writePrompt_type == "one":
        await editMessageOrAnswer(
            call,
            text.GET_ONE_PROMPT_GENERATION_SUCCESS_TEXT,
            reply_markup=start_generation_keyboards.onePromptGenerationChooseTypeKeyboard(),
        )

    else:
        # Получаем данные
        state_data = await state.get_data()
        setting_number = state_data.get("setting_number", 1)

        if setting_number == "all":
            # Получаем все настройки
            dataArrays = getAllDataArrays()

            # Инициализируем начальные данные
            model_name = dataArrays[0][0]["model_name"]
            await state.update_data(current_setting_number_for_unique_prompt=1)
            await state.set_state(StartGenerationState.write_prompt_for_model)
        else:
            # Получаем данные по настройке
            dataArray = getDataArrayBySettingNumber(int(setting_number))
            model_name = dataArray[0]["model_name"]
            await state.update_data(
                current_setting_number_for_unique_prompt=int(setting_number),
            )

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        await editMessageOrAnswer(
            call,
            text.WRITE_PROMPT_FOR_MODEL_START_TEXT.format(
                model_name,
                model_name_index,
            ),
        )
        await state.update_data(current_model_for_unique_prompt=model_name)
        await state.set_state(StartGenerationState.write_prompt_for_model)


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


# Обработка ввода промпта для конкретной модели
async def write_prompt_for_model(message: types.Message, state: FSMContext):
    # Получаем данные
    state_data = await state.get_data()
    prompt = message.text
    model_name = state_data.get("current_model_for_unique_prompt", "")
    setting_number = state_data.get("setting_number", 1)
    user_id = message.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале генерации
    message_for_edit = await safe_send_message(
        text=text.GENERATE_IMAGE_PROGRESS_TEXT.format(
            model_name,
            model_name_index,
        ),
        message=message,
    )

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Генерируем изображения
    await generateImageBlock(
        data,
        message_for_edit,
        state,
        user_id,
        setting_number,
        prompt,
        False,
        False,
    )

    # Получаем следующую модель
    next_model = await getNextModel(model_name, setting_number, state)

    # Если следующая модель не найдена, то завершаем генерацию
    if not next_model:
        await safe_send_message(
            text=text.GENERATION_SUCCESS_TEXT,
            message=message,
        )
        return

    await message.answer()

    # Выводим в лог следующую модель
    logger.info(f"Следующая модель: {next_model}")

    # Получаем индекс следующей модели
    next_model_index = getModelNameIndex(next_model)

    await state.set_state(None)
    # Просим пользователя отправить промпт для следующей модели
    await safe_send_message(
        text=text.WRITE_PROMPT_FOR_MODEL_TEXT.format(
            next_model,
            next_model_index,
        ),
        message=message,
        reply_markup=start_generation_keyboards.confirmWriteUniquePromptForNextModelKeyboard(),
    )
    await state.update_data(current_model_for_unique_prompt=next_model)


# Обработка нажатия кнопки "✅ Написать промпт" для подтверждения написания уникального промпта для следующей модели
async def confirm_write_unique_prompt_for_next_model(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем данные
    state_data = await state.get_data()
    next_model = state_data.get("current_model_for_unique_prompt", "")

    # Получаем индекс следующей модели
    next_model_index = getModelNameIndex(next_model)

    # Отправляем сообщение для ввода промпта
    await editMessageOrAnswer(
        call,
        text.WRITE_UNIQUE_PROMPT_FOR_MODEL_TEXT.format(
            next_model,
            next_model_index,
        ),
    )
    await state.set_state(StartGenerationState.write_prompt_for_model)


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
    image_index = int(call.data.split("|")[3]) - 1

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
        await editMessageOrAnswer(
            call,
            text.GENERATE_IMAGE_ERROR_TEXT.format(model_name, e),
        )
        raise e


# Обработка ввода названия модели для генерации
async def write_model_name_for_generation(
    message: types.Message,
    state: FSMContext,
):
    # Если в сообщении есть запятые, то записываем массив моделей в стейт
    model_indexes = message.text.split(",")

    # Если запятых нет, то записываем одну модель в стейт
    if len(model_indexes) == 1:
        model_indexes = [message.text]

    # Удаляем пробелы из названий моделей
    model_indexes = [model_index.strip() for model_index in model_indexes]

    # Проверяем, что это число
    for model_index in model_indexes:
        if not model_index.isdigit():
            await safe_send_message(
                text=text.MODEL_NOT_FOUND_TEXT.format(model_index),
                message=message,
            )
            return

    # Проверяем, существует ли такие модели
    for model_index in model_indexes:
        # Если индекс больше 100 или меньше 1, то просим ввести другой индекс
        if int(model_index) > 100 or int(model_index) < 1:
            await safe_send_message(
                text=text.MODEL_NOT_FOUND_TEXT.format(model_index),
                message=message,
            )
            return

    await state.update_data(model_indexes_for_generation=model_indexes)

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
    state_data = await state.get_data()
    is_test_generation = state_data.get("generations_type", "") == "test"
    model_name = state_data.get("model_name_for_regenerate_image", "")
    setting_number = state_data.get("setting_number_for_regenerate_image", 1)
    prompt = message.text
    user_id = message.from_user.id

    # Удаляем сообщение пользователя
    await message.delete()

    # Удаляем сообщение бота
    write_new_prompt_message_id = state_data.get(
        "write_new_prompt_message_id",
        None,
    )
    if write_new_prompt_message_id:
        await bot.delete_message(user_id, write_new_prompt_message_id)

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
    regenerate_progress_message = await safe_send_message(
        text=text.REGENERATE_IMAGE_WITH_NEW_PROMPT_TEXT.format(
            model_name,
            model_name_index,
            prompt,
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


async def select_multi_image(call: types.CallbackQuery, state: FSMContext):
    _, model_name, setting_number, image_index = call.data.split("|")
    image_index = int(image_index)
    state_data = await state.get_data()
    selected_indexes_raw = state_data.get("selected_indexes", {})
    if isinstance(selected_indexes_raw, list):
        selected_indexes_dict = {model_name: selected_indexes_raw}
    else:
        selected_indexes_dict = selected_indexes_raw
    selected_indexes = selected_indexes_dict.get(model_name, [])
    if image_index in selected_indexes:
        selected_indexes.remove(image_index)
    else:
        if len(selected_indexes) < 10:
            selected_indexes.append(image_index)
    selected_indexes_dict[model_name] = selected_indexes
    await state.update_data(selected_indexes=selected_indexes_dict)
    from bot.keyboards.startGeneration.keyboards import (
        selectMultiImageKeyboard,
    )

    kb = selectMultiImageKeyboard(
        model_name,
        setting_number,
        10,
        selected_indexes,
    )
    await call.message.edit_reply_markup(reply_markup=kb)
    await call.answer()


async def multi_image_done(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    model_name = call.data.split("|")[1]
    selected_indexes_raw = state_data.get("selected_indexes", {})
    if isinstance(selected_indexes_raw, list):
        selected_indexes_dict = {model_name: selected_indexes_raw}
    else:
        selected_indexes_dict = selected_indexes_raw
    selected_indexes = selected_indexes_dict.get(model_name, [])
    if not selected_indexes:
        await call.answer(
            "Выберите хотя бы одно изображение!",
            show_alert=True,
        )
        return

    temp_dir = TEMP_FOLDER_PATH / f"{model_name}_{call.from_user.id}"
    if os.path.exists(temp_dir):
        files_in_dir = sorted(os.listdir(temp_dir))
        logger.info(
            f"[multi_image_done] Существующие файлы в {temp_dir}: {files_in_dir}",
        )
        # Фильтруем selected_indexes по реально существующим файлам
        existing_indexes = set()
        for fname in files_in_dir:
            if fname.endswith(".jpg") and fname[:-4].isdigit():
                existing_indexes.add(int(fname[:-4]))
        filtered_selected_indexes = [
            i for i in selected_indexes if i in existing_indexes
        ]
        skipped_indexes = [
            i for i in selected_indexes if i not in existing_indexes
        ]
        if skipped_indexes:
            logger.warning(
                f"[multi_image_done] Эти индексы выбраны пользователем, но файлов нет: {skipped_indexes}",
            )
        selected_indexes = filtered_selected_indexes
    else:
        logger.warning(f"[multi_image_done] Директория {temp_dir} не найдена!")
    logger.info(
        f"[multi_image_done] RAW selected_indexes: {selected_indexes}",
    )
    selected_indexes_sorted = sorted(selected_indexes)
    logger.info(
        f"[multi_image_done] SORTED selected_indexes: {selected_indexes_sorted}",
    )

    await call.message.answer(
        f"Вы выбрали изображения с номерами: {', '.join(str(i + 1) for i in selected_indexes_sorted)}.\nОбрабатываю выбор изображений...",
    )

    await deleteMessageFromState(
        state,
        "imageGeneration_mediagroup_messages_ids",
        model_name,
        call.message.chat.id,
        delete_keyboard_message=True,
    )

    selected_indexes_copy = list(selected_indexes_sorted)

    # Последовательная обработка изображений
    for idx, image_index in enumerate(selected_indexes_copy, 1):
        logger.info(
            f"[multi_image_done] Обрабатываю image_index={image_index}",
        )
        status_message = await call.message.answer(
            f"🔄 Работаю с изображением для модели {model_name} под номером {image_index}... (обработано {idx}/{len(selected_indexes_copy)})",
        )

        fake_call = types.CallbackQuery(
            id=call.id,
            from_user=call.from_user,
            chat_instance=call.chat_instance,
            message=status_message,
            data=call.data,
            inline_message_id=call.inline_message_id,
        )

        try:
            await process_image(fake_call, state, model_name, image_index)
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(
                f"Ошибка при обработке изображения {image_index}: {e}",
            )
            await status_message.edit_text(
                f"❌ Ошибка при обработке изображения {image_index}: {str(e)}",
            )
            continue

    await call.message.answer(
        f"✅ Все выбранные изображения для модели {model_name} успешно обработаны!",
    )


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

    router.message.register(
        write_prompt_for_model,
        StateFilter(StartGenerationState.write_prompt_for_model),
    )

    router.callback_query.register(
        confirm_write_unique_prompt_for_next_model,
        lambda call: call.data.startswith(
            "confirm_write_unique_prompt_for_next_model",
        ),
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

    router.callback_query.register(
        select_multi_image,
        lambda call: call.data.startswith("select_multi_image"),
    )

    router.callback_query.register(
        multi_image_done,
        lambda call: call.data.startswith("multi_image_done"),
    )
