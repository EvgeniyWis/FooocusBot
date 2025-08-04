import asyncio
import re

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import bot.constants as constants
from bot.helpers import text
from bot.helpers.generateImages.dataArray.check_model_index_is_exist import (
    check_model_index_is_exist,
)
from bot.helpers.generateImages.dataArray.get_all_model_indexes import (
    get_all_model_indexes,
)
from bot.helpers.generateImages.dataArray.get_model_name_by_index import (
    get_model_name_by_index,
)
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.helpers.handlers.img2video import process_video
from bot.InstanceBot import bot, img2video_router
from bot.keyboards import video_generation_keyboards
from bot.logger import logger
from bot.states import StartGenerationState
from bot.utils.handlers import appendDataToStateArray
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_edit_message,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)

PROMPT_BY_INDEX_PATTERN = re.compile(
    r"(?s)(\d+)\s*[:\-–—]\s*(.*?)\s*[:\-–—]\s*(\d+)(?=(?:\n\d+\s*[:\-–—].*?\s*[:\-–—]\s*\d+)|\Z)",
)

all_model_indexes = get_all_model_indexes()


# Обработка нажатия на кнопку "📹 Сгенерировать видео из изображения'"
async def start_generateVideoFromImage(
    call: types.CallbackQuery,
    state: FSMContext,
):
    await state.clear()

    await safe_edit_message(
        call.message,
        text.SEND_IMAGES_FOR_VIDEO_GENERATION,
        reply_markup=video_generation_keyboards.img2video_done_send_images_keyboard(),
    )
    await state.set_state(StartGenerationState.send_image_for_video_generation)


# Обработка присылания изображения для генерации видео и запроса на присылания промпта
async def get_images_for_img2video(
    message: types.Message,
    state: FSMContext,
    album: list[types.Message] = [],
):
    # Проверяем, есть ли изображение в сообщении
    if not message.photo and not album:
        await safe_send_message(
            text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT,
            message,
        )
        return

    # Получаем file_id самого большого изображения
    state_data = await state.get_data()
    img2video_images_file_ids = state_data.get("img2video_images_file_ids", [])

    if not album:
        if message.photo:
            photo = message.photo[-1]
            image_file_id = photo.file_id
            img2video_images_file_ids.append(image_file_id)
    else:
        for message in album:
            if message.photo:
                photo = message.photo[-1]
                image_file_id = photo.file_id
                img2video_images_file_ids.append(image_file_id)

    # Сохраняем путь в стейт
    await state.update_data(img2video_images_file_ids=img2video_images_file_ids)

    await safe_send_message(
        text.SUCCESS_GET_IMAGES_FOR_VIDEO_GENERATION_TEXT.format(len(img2video_images_file_ids))
        if len(img2video_images_file_ids) > 1 else text.SUCCESS_GET_IMAGE_FOR_VIDEO_GENERATION_TEXT,
        message,
        reply_markup=video_generation_keyboards.img2video_done_send_images_keyboard(),
    )


# Обработка нажатия на кнопку "✅ Готово" для прекращения сбора изображений для генерации видео
async def done_send_images_for_img2video(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Удаляем сообщение с кнопкой
    try:
        await call.message.delete()
    except Exception as e:
        logger.error(f"Не удалось удалить сообщение: {e}")

    state_data = await state.get_data()
    img2video_images_file_ids = state_data.get("img2video_images_file_ids", [])

    if len(img2video_images_file_ids) == 0:
        await safe_send_message(
            text.NO_IMAGES_FOR_VIDEO_GENERATION_ERROR_TEXT,
            call.message,
        )
        return

    # Скачиваем все изображения и сохраняем в папку
    temp_paths_for_video_generation = []
    for image_file_id in img2video_images_file_ids:
        # Скачиваем изображение (file_id) и получаем путь к файлу
        # Для этого используем bot.download_file и сохраняем во временную папку
        try:
            file = await asyncio.wait_for(
                bot.get_file(image_file_id),
                timeout=30,
            )
        except TimeoutError:
            await safe_send_message(
                "⏰ Время ожидания получения файла Telegram истекло. Попробуйте позже.",
                call.message,
            )
            raise TimeoutError(
                "Время ожидания получения файла Telegram истекло.",
            )

        file_path = file.file_path
        temp_path = f"{constants.TEMP_IMAGE_FILES_DIR}/{image_file_id}.jpg"
        temp_paths_for_video_generation.append(temp_path)

        try:
            await asyncio.wait_for(
                bot.download_file(file_path, temp_path),
                timeout=60,
            )
        except TimeoutError:
            await safe_send_message(
                "⏰ Время ожидания скачивания файла Telegram истекло. Попробуйте позже.",
                call.message,
            )
            raise TimeoutError(
                "Время ожидания скачивания файла Telegram истекло.",
            )

    # Сохраняем путь в стейт
    await state.update_data(temp_paths_for_video_generation=temp_paths_for_video_generation)

    # Если изображение только одно, сразу используем старый функционал
    if len(temp_paths_for_video_generation) == 1:
        await state.set_state(StartGenerationState.write_single_prompt_for_img2video)
        
        await safe_send_message(
            text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT,
            call.message,
        )
    else:
        # Если изображений несколько, предлагаем выбрать тип ввода промпта
        await state.set_state(None)

        await safe_send_message(
            text.CHOOSE_WRITE_PROMPT_TYPE_SUCCESS_TEXT,
            call.message,
            reply_markup=video_generation_keyboards.choose_prompt_type_keyboard(),
        )


# Обработка выбора типа ввода промпта для img2video
async def choose_prompt_type_for_img2video(
    call: types.CallbackQuery,
    state: FSMContext,
):

    prompt_type = call.data.split("|")[2]  # "one" или "multi"
    
    if prompt_type == "one":
        # Один промпт для всех изображений - используем старый функционал
        state_data = await state.get_data()
        temp_paths_for_video_generation = state_data.get("temp_paths_for_video_generation", [])

        message_text = text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT \
            if len(temp_paths_for_video_generation) == 1 \
            else text.WRITE_PROMPT_FOR_MULTI_VIDEO_GENERATION_FROM_IMAGE_TEXT.format(len(temp_paths_for_video_generation))
        
        logger.info(f"Отправляем текст для одного промпта: {message_text}")
        
        await call.message.edit_text(message_text, reply_markup=None)
        await state.set_state(StartGenerationState.write_single_prompt_for_img2video)
    else:
        # Множественные промпты для каждого изображения
        await start_multi_prompt_input_mode_for_img2video(call, state)


# Запуск режима ввода множественных промптов для img2video
async def start_multi_prompt_input_mode_for_img2video(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    # Удаляем сообщение с кнопкой
    try:
        await callback.message.delete()
    except Exception as e:
        logger.error(f"Не удалось удалить сообщение: {e}")

    await state.set_state(StartGenerationState.collecting_prompt_parts_for_img2video)
    await state.update_data(
        prompt_chunks=[],
    )

    await safe_send_message(
        text.WRITE_MULTI_PROMPTS_FOR_IMG2VIDEO,
        callback,
        reply_markup=video_generation_keyboards.img2video_done_typing_keyboard(),
    )


# Обработка ввода частей промпта для img2video
async def handle_chunk_input_for_img2video(message: types.Message, state: FSMContext):
    logger.info("Обрабатываем ввод в handle_chunk_input_for_img2video")
    
    data = await state.get_data()
    chunks = data.get("prompt_chunks", [])
    msg = message.text.strip()

    if not msg:
        await safe_send_message(
            text.EMPTY_PROMPT_TEXT,
            message,
        )
        return

    # Проверяем, содержит ли сообщение формат "№ изображения - промпт - № модели"
    matches = PROMPT_BY_INDEX_PATTERN.findall(msg)
    if matches:
        # Если найден формат "№ изображения - промпт - № модели", проверяем существование моделей
        for image_index_str, prompt, model_index_str in matches:
            model_index = int(model_index_str)
            
            if not check_model_index_is_exist(model_index):
                await safe_send_message(
                    text.MODEL_NOT_FOUND_TEXT.format(model_index, all_model_indexes),
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
        reply_markup=video_generation_keyboards.img2video_done_typing_keyboard(),
    )


# Завершение ввода промптов для img2video
async def finish_prompt_input_for_img2video(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    # Удаляем сообщение с кнопкой
    try:
        await callback.message.delete()
    except Exception as e:
        logger.error(f"Не удалось удалить сообщение: {e}")

    data = await state.get_data()
    full_text = "\n".join(data.get("prompt_chunks", []))
    prompt_chunks = data.get("prompt_chunks", [])
    if not prompt_chunks:
        await safe_send_message(
            "❗️Вы не ввели ни одного промпта.",
            callback.message,
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
    except Exception as e:
        logger.exception(
            f"Не удалось собрать сообщение finish_prompt_input_for_img2video для user_id={user_id}, chat_id={chat_id}",
        )
        await safe_edit_message(
            callback.message,
            "❗️Произошла ошибка при обработке промпта.",
        )
        return

    await process_multi_prompts_for_img2video(
        message=fake_message,
        state=state,
        text_input=full_text,
    )


# Обработка множественных промптов для img2video
async def process_multi_prompts_for_img2video(
    message: types.Message,
    state: FSMContext,
    text_input: str = None,
):
    text_input = text_input or message.text.strip()
    matches = PROMPT_BY_INDEX_PATTERN.findall(text_input)

    if not matches:
        await safe_send_message(
            text=text.WRONG_FORMAT_TEXT,
            message=message,
        )
        return

    state_data = await state.get_data()
    temp_paths_for_video_generation = state_data.get("temp_paths_for_video_generation", [])
    
    # Проверяем, что количество введённых записей равно количеству изображений
    if len(matches) != len(temp_paths_for_video_generation):
        await safe_send_message(
            f"❌ Количество введённых записей ({len(matches)}) не соответствует количеству изображений ({len(temp_paths_for_video_generation)})!",
            message,
    )
        return

    # Проверяем существование моделей и валидность индексов изображений
    for image_index_str, prompt, model_index_str in matches:
        image_index = int(image_index_str)
        model_index = int(model_index_str)
        
        # Проверяем индекс изображения
        if image_index < 1 or image_index > len(temp_paths_for_video_generation):
            await safe_send_message(
                f"❌ Неверный индекс изображения: {image_index}. Допустимые значения: 1-{len(temp_paths_for_video_generation)}",
                message,
            )
            return
        
        # Проверяем существование модели
        if not check_model_index_is_exist(model_index):
            await safe_send_message(
                text.MODEL_NOT_FOUND_TEXT.format(model_index, all_model_indexes),
                message,
            )
            return

    # Сохраняем данные для обработки
    img2video_data = []
    for image_index_str, prompt, model_index_str in matches:
        image_index = int(image_index_str)
        model_index = int(model_index_str)
        img2video_data.append({
            'image_index': image_index,
            'prompt': prompt.strip(),
            'model_index': model_index,
        })

    await state.update_data(img2video_data=img2video_data)

    # Сразу запускаем обработку видео
    await process_img2video_with_data(message, state)


# Обработка видео с готовыми данными
async def process_img2video_with_data(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    img2video_data = state_data.get("img2video_data", [])
    temp_paths_for_video_generation = state_data.get("temp_paths_for_video_generation", [])

    if not img2video_data:
        await safe_send_message(
            "❌ Ошибка: данные для обработки видео не найдены",
            message,
        )
        return

    await state.set_state(None)

    # Обрабатываем все изображения в видео
    # Задачи запускаются параллельно, но старт каждой с задержкой 0.5 секунды
    tasks = []
    for data in img2video_data:
        task = asyncio.create_task(
            process_video(
                message=message,
                prompt=data['prompt'],
                image_index=data['image_index'],
                model_index=data['model_index'],
                temp_paths_for_video_generation=temp_paths_for_video_generation,  # Передаем полный список путей
            )
        )
        tasks.append(task)
        await asyncio.sleep(0.5)

    # После завершения задачи — обновляем state
    for coro in asyncio.as_completed(tasks):
        model_name, video_path = await coro

        if not video_path:
            await safe_send_message(
                f"Ошибка: не удалось найти путь к видео для сохранения для модели {model_name}",
                message,
            )
            continue

        data_for_update = {f"{model_name}": video_path}
        await appendDataToStateArray(
            state,
            "generated_video_paths",
            data_for_update,
            unique_keys=("model_name",),
        )


# Обработка ввода одного промпта для img2video (старый функционал)
async def handle_single_prompt_for_img2video(
    message: types.Message,
    state: FSMContext,
):
    logger.info("Обрабатываем один промпт в handle_single_prompt_for_img2video")
    
    # Получаем промпт
    prompt = message.text

    await state.update_data(prompt_for_img2video=prompt)

    state_data = await state.get_data()
    temp_paths_for_video_generation = state_data.get(
        "temp_paths_for_video_generation", []
    )

    message_text = text.ASK_FOR_MODEL_NAME_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT \
        if len(temp_paths_for_video_generation) == 1 \
        else text.GET_MODEL_INDEXES_FOR_ALL_IMAGES_TEXT.format(len(temp_paths_for_video_generation))

    logger.info(f"Отправляем текст для запроса модели: {message_text}")

    await safe_send_message(
        message_text,
        message,
    )

    await state.set_state(
        StartGenerationState.ask_for_model_index_for_img2video,
    )


# Хендлер для обработки ввода имени модели для сохранения видео
async def handle_model_index_for_video_generation_from_image(
    message: types.Message,
    state: FSMContext,
):
    # Получаем данные из стейта
    state_data = await state.get_data()

    temp_paths_for_video_generation = state_data.get(
        "temp_paths_for_video_generation",
    )

    prompt = state_data.get(
        "prompt_for_img2video",
    )

    model_indexes = []

    if len(temp_paths_for_video_generation) == 1:
        # Получаем данные по имени модели
        try:
            model_index = int(message.text)

            # Проверяем существование модели
            if not check_model_index_is_exist(model_index):
                await safe_send_message(
                    text.MODEL_NOT_FOUND_TEXT.format(model_index, all_model_indexes),
                    message,
                )
                return

            model_indexes.append((1, model_index))
        except ValueError:
            logger.error(f"Произошла ошибка при получении индекса модели: {message.text}")
            await safe_send_message(
                text.WRONG_MODEL_INDEX_TEXT.format(message.text),
                message,
            )
            return
        except Exception as e:
            logger.error(f"Произошла ошибка при получении индекса модели: {e}")
            await safe_send_message(
                text.WRONG_MODEL_INDEX_TEXT.format(message.text),
                message,
            )
            return
    else:
        # Получаем текст сообщения
        lines = message.text.strip().split('\n')
        model_indexes = []

        for line in lines:
            # Пропускаем пустые строки
            if not line.strip():
                continue

            # Разделяем по дефису
            parts = line.split('-')

            if len(parts) != 2:
                await safe_send_message(
                    text.WRONG_FORMAT_FOR_MODEL_INDEXES_FOR_ALL_IMAGES_TEXT.format(line),
                    message,
                )
                return

            try:
                image_index = int(parts[0].strip())
                model_index = int(parts[1].strip())
                
                # Проверяем индекс изображения
                if image_index < 1 or image_index > len(temp_paths_for_video_generation):
                    await safe_send_message(
                        f"❌ Неверный индекс изображения: {image_index}. Допустимые значения: 1-{len(temp_paths_for_video_generation)}",
                        message,
                    )
                    return
                
                # Проверяем существование модели
                if not check_model_index_is_exist(model_index):
                    await safe_send_message(
                        text.MODEL_NOT_FOUND_TEXT.format(model_index, all_model_indexes),
                        message,
                    )
                    return
                
                model_indexes.append((image_index, model_index))
            except ValueError:
                await safe_send_message(
                    f"❌ Неверный формат в строке: {line}. Ожидается: номер изображения - номер модели",
                    message,
                )
                return

        # Проверяем, что количество введённых индексов равно количеству изображений
        if len(model_indexes) != len(temp_paths_for_video_generation):
            await safe_send_message(
                text.WRONG_AMOUNT_OF_MODEL_INDEXES_FOR_ALL_IMAGES_TEXT,
                message,
            )
            return

    # Обновляем стейт
    img2video_temp_paths_for_with_model_names = {}
    for image_index, model_index in model_indexes:
        img2video_temp_paths_for_with_model_names[get_model_name_by_index(model_index)] = \
            temp_paths_for_video_generation[image_index - 1]

    await state.update_data(img2video_temp_paths_for_with_model_names=img2video_temp_paths_for_with_model_names)
    
    # Если индекс какой-то модели больше числа моделей или меньше 1, то просим ввести другой индекс
    for image_index, model_index in model_indexes:
        if not check_model_index_is_exist(model_index):
            await safe_send_message(
                text.MODEL_NOT_FOUND_TEXT.format(model_index, all_model_indexes),
                message,
            )
            return

    await state.set_state(None)

    # Обрабатываем все изображения в видео
    # Задачи запускаются параллельно, но старт каждой с задержкой 0.5 секунды
    tasks = []
    for image_index, model_index in model_indexes:
        task = asyncio.create_task(
            process_video(
                message=message,
                prompt=prompt,
                image_index=image_index,
                model_index=model_index,
                temp_paths_for_video_generation=temp_paths_for_video_generation,
            )
        )
        tasks.append(task)
        await asyncio.sleep(0.5)

    # После завершения задачи — обновляем state
    for coro in asyncio.as_completed(tasks):
        try:
            result = await coro
            # process_video из img2video возвращает кортеж (model_name, video_path)
            if isinstance(result, tuple) and len(result) == 2:
                model_name, video_path = result
                
                if not video_path:
                    await safe_send_message(
                        f"Ошибка: не удалось найти путь к видео для сохранения для модели {model_name}",
                        message,
                    )
                    continue

                data_for_update = {f"{model_name}": video_path}
                await appendDataToStateArray(
                    state,
                    "generated_video_paths",
                    data_for_update,
                    unique_keys=("model_name",),
                )
        except Exception as e:
            logger.error(f"Ошибка при обработке видео: {e}")
            await safe_send_message(
                f"Ошибка при генерации видео: {str(e)}",
                message,
            )
            continue


# Добавление обработчиков
def hand_add():
    img2video_router.callback_query.register(
        start_generateVideoFromImage,
        lambda call: call.data == "generateVideoFromImage",
    )
    img2video_router.message.register(
        get_images_for_img2video,
        StateFilter(StartGenerationState.send_image_for_video_generation),
    )
    img2video_router.callback_query.register(
        done_send_images_for_img2video,
        lambda call: call.data == "img2video|done_send_images",
    )
    img2video_router.message.register(
        handle_single_prompt_for_img2video,
        StateFilter(
            StartGenerationState.write_single_prompt_for_img2video,
        ),
    )
    img2video_router.message.register(
        handle_model_index_for_video_generation_from_image,
        StateFilter(
            StartGenerationState.ask_for_model_index_for_img2video,
        ),
    )
    # Новые обработчики для уникальных промптов
    img2video_router.callback_query.register(
        choose_prompt_type_for_img2video,
        lambda call: call.data.startswith("img2video|prompt_type"),
    )
    img2video_router.message.register(
        handle_chunk_input_for_img2video,
        StateFilter(
            StartGenerationState.collecting_prompt_parts_for_img2video,
        ),
    )
    img2video_router.callback_query.register(
        finish_prompt_input_for_img2video,
        lambda call: call.data == "img2video|finish_prompt",
    )
