import re
import traceback
from collections import defaultdict

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from helpers.handlers.startGeneration.regenerateImage import get_normal_model
from keyboards.startGeneration.keyboards import done_typing_keyboard
from pydantic import ValidationError
from utils.handlers.messages import safe_edit_message

from bot.constants import MULTI_IMAGE_NUMBER
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getAllDataArrays,
    getDataByModelName,
    getModelNameByIndex,
    getModelNameIndex,
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
from bot.states.StartGenerationState import (
    MultiPromptInputState,
    StartGenerationState,
)
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
            f"🖼 Мультивыбор - можно выбрать несколько фотографий одновременно, присылается {MULTI_IMAGE_NUMBER} на выбор\n"
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
        text.GET_GENERATIONS_SUCCESS_TEXT,
        reply_markup=start_generation_keyboards.selectSettingKeyboard(
            is_test_generation=False,
        ),
    )


# Обработка выбора настройки
async def choose_setting(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные из стейта
    state_data = await state.get_data()

    # Очищаем стейт
    await state.clear()

    # Обновляем только важные значения в стейте после очистки
    initial_state = {
        "multi_select_mode": state_data.get("multi_select_mode", False),
        "prompt_exist": state_data.get("prompt_exist", False),
        "generations_type": state_data.get("generations_type", ""),
    }
    await state.update_data(**initial_state)

    # Если выбрана конкретная модель, то просим ввести название модели
    if call.data == "select_setting|specific_model":
        await safe_edit_message(
            call.message,
            "🖼 Выберите тип генерации:",
            reply_markup=start_generation_keyboards.select_type_specific_generation(),
        )
        await state.update_data(specific_model=True)

        return

    # Если выбрана другая настройка, то продолжаем генерацию
    setting_number = call.data.split("|")[1]
    await state.update_data(setting_number=setting_number)
    prompt_exist = state_data.get("prompt_exist", False)
    generations_type = state_data.get("generations_type", "")
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

    await start_write_prompts_for_models_multiline_input(call, state)


async def start_write_prompts_for_models_multiline_input(
    callback: types.CallbackQuery,
    state: FSMContext,
):
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
        setting_index = int(setting_number) - 1

        # Считаем смещение как сумму длин всех предыдущих сетов
        offset = sum(len(arr) for arr in all_data_arrays[:setting_index])

        # Длина текущего сета
        setting_length = len(all_data_arrays[setting_index])

        start_index = offset + 1
        end_index = offset + setting_length

    # Сохраняем диапазон индексов в стейт
    await state.update_data(
        valid_model_indexes_range=(start_index, end_index),
    )
    await state.update_data(
        prompt_chunks=[],
    )

    await safe_send_message(
        text.WRITE_PROMPTS_FOR_MODELS_TEXT.format(start_index, end_index),
        message=callback.message,
        reply_markup=done_typing_keyboard(),
    )
    await state.set_state(
        MultiPromptInputState.collecting_model_prompts_for_settings,
    )


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
    prompt_counter = defaultdict(int)
    unique_model_indexes: set[int] = set()

    for index_str, prompt in matches:
        index_base = int(index_str.split("+")[0])

        if not (start_index <= index_base <= end_index):
            await safe_send_message(
                text.MODEL_NOT_FOUND_TEXT.format(index_base),
                message,
            )
            return

        unique_model_indexes.add(index_base)

        count = prompt_counter[str(index_base)]
        full_key = str(index_base) if count == 0 else f"{index_base}+{count}"
        model_prompts[full_key] = prompt.strip()
        prompt_counter[str(index_base)] += 1

    if len(unique_model_indexes) != expected_count:
        await safe_send_message(
            f"⚠️ Нужно указать <b>ровно {expected_count}</b> моделей с промптами (а не {len(unique_model_indexes)}).",
            message,
        )
        return

    data_for_update = {
        f"{getModelNameByIndex(key)}_{key}": prompt
        for key, prompt in model_prompts.items()
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


async def get_model_name_with_generation_id(
    state: FSMContext,
    generation_id: str,
) -> str:
    state_data = await state.get_data()
    mapping: dict = state_data.get(
        "generation_id_to_full_model_key",
        {},
    )
    logger.info(
        f"Ищем model_name по generation_id: generation_id={generation_id}",
    )
    logger.info(f"generation_id_to_full_model_key: {mapping}")

    model_name: str | None = None
    for full_job_id, model_key in mapping.items():
        if full_job_id.startswith(generation_id):
            model_name = model_key
            break

    return model_name


# Обработка выбора изображения
async def select_image(call: types.CallbackQuery, state: FSMContext):
    # Отправляем сообщение о выборе изображения
    await editMessageOrAnswer(
        call,
        text.SELECT_IMAGE_PROGRESS_TEXT,
    )

    model_name, setting_number, image_index, generation_id_prefix = (
        call.data.split("|")[1:]
    )

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Удаляем медиагруппу
    logger.info(f"Удаляем медиагруппу для модели {model_name}")
    await deleteMessageFromState(
        state,
        "imageGeneration_mediagroup_messages_ids",
        model_name,
        call.message.chat.id,
        generation_id=generation_id_prefix,
    )
    try:
        if image_index == "regenerate":
            model_name_for_regenerate = (
                await get_model_name_with_generation_id(
                    state,
                    generation_id_prefix,
                )
            )

            if not model_name_for_regenerate:
                logger.warning(
                    f"[regenerate] Не найден model_name_for_regenerate для generation_id_prefix={generation_id_prefix}",
                )
                return await editMessageOrAnswer(
                    call,
                    "❌ Не удалось определить модель для перегенерации.",
                )

            return await regenerateImage(
                model_name_for_regenerate,
                call,
                state,
                setting_number,
            )

        # Если индекс изображения равен "regenerate_with_new_prompt", то перегенерируем изображение с новым промптом
        elif image_index == "regenerate_with_new_prompt":
            model_name_for_regenerate = (
                await get_model_name_with_generation_id(
                    state,
                    generation_id_prefix,
                )
            )

            if not model_name_for_regenerate:
                logger.warning(
                    f"[regenerate_with_new_prompt] Не найден model_name_for_regenerate для generation_id_prefix={generation_id_prefix}",
                )
                return await editMessageOrAnswer(
                    call,
                    "❌ Не удалось определить модель для перегенерации по новому промпту.",
                )

            await state.update_data(
                model_name_for_regenerate_image=model_name_for_regenerate,
                setting_number_for_regenerate_image=setting_number,
                generation_id_for_regenerate=generation_id_prefix,
            )

            await state.set_state(
                StartGenerationState.write_new_prompt_for_regenerate_image,
            )

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

        if not call.message:
            return await editMessageOrAnswer(
                call,
                "Не получилось обнаружить сообщение!",
            )

        try:
            logger.info("Обрабатываем изображение")
            await process_image(
                call,
                state,
                model_name,
                image_index,
            )
        except Exception as e:
            traceback.print_exc()
            logger.exception(f"Ошибка в process_image: {e}")
            await editMessageOrAnswer(
                call,
                f"❌ Ошибка при обработке изображения: {e}",
            )
            raise e

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


async def start_multi_prompt_input_mode(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await state.set_state(MultiPromptInputState.collecting_prompt_parts)
    await state.update_data(
        prompt_chunks=[],
    )

    await safe_edit_message(
        callback.message,
        text.WRITE_MULTI_PROMPTS_FOR_SPECIFIC_GENERATION,
        reply_markup=done_typing_keyboard(),
    )


async def handle_chunk_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chunks = data.get("prompt_chunks", [])
    msg = message.text.strip()

    if not msg:
        await safe_send_message(
            text.EMPTY_PROMPT_TEXT,
            message,
        )
        return

    chunks.append(msg)
    await state.update_data(
        prompt_chunks=chunks,
        last_user_id=message.from_user.id,
        last_chat_id=message.chat.id,
        last_message_id=message.message_id,
    )
    await safe_send_message(
        text.MESSAGE_IS_SUCCESFULLY_DONE,
        message,
        reply_markup=done_typing_keyboard(),
    )


async def finish_prompt_input(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    data = await state.get_data()
    full_text = "\n".join(data.get("prompt_chunks", []))
    prompt_chunks = data.get("prompt_chunks", [])
    if not prompt_chunks:
        await safe_edit_message(
            callback.message,
            "❗️Вы не ввели ни одного промпта.",
        )
        return

    user_id = data.get("last_user_id") or callback.from_user.id
    chat_id = data.get("last_chat_id") or callback.message.chat.id

    await safe_edit_message(
        callback.message,
        "🧠 Обрабатываю длинный промпт...",
    )
    try:
        fake_message = types.Message(
            message_id=callback.message.message_id,
            date=callback.message.date,
            chat=types.Chat(id=chat_id, type="private"),
            from_user=callback.from_user,
            text=full_text,
        )
    except ValidationError:
        logger.exception(
            f"Не удалось собрать сообщение finish_prompt_input для user_id={user_id}, chat_id={chat_id}",
        )
        await safe_edit_message(
            callback.message,
            "❗️Произошла ошибка при обработке промпта.",
        )
        return

    current_state = await state.get_state()

    if (
        current_state
        == MultiPromptInputState.collecting_model_prompts_for_settings.state
    ):
        await write_prompts_for_models(
            message=fake_message,
            state=state,
        )
    else:
        await write_model_for_generation(
            message=fake_message,
            state=state,
            text_input=full_text,
        )


async def send_message_with_info_for_write_prompts_for_models(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await safe_edit_message(
        callback.message,
        text.WRITE_MODELS_NAME_TEXT,
    )
    await state.set_state(
        StartGenerationState.write_models_for_specific_generation,
    )


async def write_models_for_specific_generation(
    message: types.Message,
    state: FSMContext,
):
    message_text = message.text.strip()

    if not all(x.strip().isdigit() for x in message_text.split(",")):
        await safe_send_message(
            text=text.NOT_NUMBER_TEXT,
            message=message,
        )
        return

    raw_model_indexes = [x.strip() for x in message_text.split(",")]
    model_indexes = make_unique_model_keys(raw_model_indexes)

    all_data_arrays = getAllDataArrays()
    all_data_arrays_length = sum(len(arr) for arr in all_data_arrays)

    for model_index in model_indexes:
        if int(model_index) > all_data_arrays_length or int(model_index) < 1:
            await safe_send_message(
                text=text.MODEL_NOT_FOUND_TEXT.format(model_index),
                message=message,
            )
            return

    await state.update_data(model_indexes_for_generation=model_indexes)

    if len(model_indexes) == 1:
        await safe_send_message(
            text=text.GET_MODEL_INDEX_SUCCESS_TEXT,
            message=message,
        )

        await state.set_state(StartGenerationState.write_prompt_for_images)

    else:
        await safe_send_message(
            text=text.GET_MODELS_INDEXES_AND_WRITE_PROMPT_TYPE_SUCCESS_TEXT,
            message=message,
            reply_markup=start_generation_keyboards.onePromptGenerationChooseTypeKeyboard(),
        )


def make_unique_model_keys(model_indexes: list[str]) -> list[str]:
    counter = defaultdict(int)
    result = []
    for index in model_indexes:
        count = counter[index]
        result.append(index if count == 0 else f"{index}+{count}")
        counter[index] += 1
    return result


async def write_model_for_generation(
    message: types.Message,
    state: FSMContext,
    text_input: str | None = None,
):
    text_input = text_input or message.text.strip()
    matches = PROMPT_BY_INDEX_PATTERN.findall(text_input)

    if not matches:
        await safe_send_message(text=text.WRONG_FORMAT_TEXT, message=message)
        return

    prompt_counter = defaultdict(int)
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

        count = prompt_counter[index]
        key = index if count == 0 else f"{index}+{count}"
        model_prompts[key] = prompt.strip()
        prompt_counter[index] += 1

    data_for_update = {
        f"{getModelNameByIndex(key)}_{key}": prompt
        for key, prompt in model_prompts.items()
    }

    logger.info(f"Обновляем промпты в состоянии: {data_for_update}")
    await state.update_data(model_prompts_for_generation=data_for_update)

    message_to_del = await safe_send_message(
        text="✅ Промпты по моделям получены, начинаю генерацию...",
        message=message,
    )
    await state.update_data(message_to_del=message_to_del.message_id)
    await generateImagesInHandler(
        prompt=model_prompts,
        message=message,
        state=state,
        user_id=message.from_user.id,
        is_test_generation=False,
        setting_number="individual",
    )


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

    model_name = state_data.get("model_name_for_regenerate_image", "")
    generation_id = state_data.get("generation_id_for_regenerate", "")

    if not generation_id:
        logger.warning("Нет generation_id_for_regenerate в state!")
        return

    data_for_update = {f"{model_name}": prompt}
    await appendDataToStateArray(
        state,
        "prompts_for_regenerated_models",
        data_for_update,
        unique_keys=("model_name"),
    )

    normal_model_name = await get_normal_model(model_name)

    # Получаем индекс модели
    model_name_index = getModelNameIndex(normal_model_name)

    # Отправляем сообщение о перегенерации изображения
    modified_prompt = prompt[:30] + "..." if len(prompt) > 30 else prompt
    regenerate_progress_message = await safe_send_message(
        text=text.REGENERATE_IMAGE_WITH_NEW_PROMPT_TEXT.format(
            normal_model_name,
            model_name_index,
            modified_prompt,
        ),
        message=message,
    )

    await state.set_state(None)

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(normal_model_name)

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
        write_new_prompt_for_regenerate_image,
        StateFilter(
            StartGenerationState.write_new_prompt_for_regenerate_image,
        ),
    )
    router.message.register(
        write_prompts_for_models,
        StateFilter(
            StartGenerationState.write_multi_prompts_for_models,
        ),
    )
    router.callback_query.register(
        send_message_with_info_for_write_prompts_for_models,
        lambda call: call.data.startswith("specific_generation|one_prompt"),
    )

    router.callback_query.register(
        start_multi_prompt_input_mode,
        lambda call: call.data.startswith("specific_generation|more_prompts"),
    )

    router.message.register(
        handle_chunk_input,
        StateFilter(
            MultiPromptInputState.collecting_model_prompts_for_settings,
            MultiPromptInputState.collecting_prompt_parts,
        ),
    )

    router.callback_query.register(
        finish_prompt_input,
        lambda call: call.data == "done_typing",
    )

    router.message.register(
        write_models_for_specific_generation,
        StateFilter(StartGenerationState.write_models_for_specific_generation),
    )
