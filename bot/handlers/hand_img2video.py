import asyncio

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import bot.constants as constants
from bot.helpers import text
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.helpers.generateImages.dataArray.getModelNameByIndex import (
    getModelNameByIndex,
)
from bot.helpers.handlers.img2video import process_video
from bot.InstanceBot import bot, router
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
        photo = message.photo[-1]
        image_file_id = photo.file_id
        img2video_images_file_ids.append(image_file_id)
    else:
        for message in album:
            photo = message.photo[-1]
            image_file_id = photo.file_id
            img2video_images_file_ids.append(image_file_id)

    # Сохраняем путь в стейт
    await state.update_data(img2video_images_file_ids=img2video_images_file_ids)

    await safe_send_message(
        text.SUCCESS_GET_IMAGES_FOR_VIDEO_GENERATION_TEXT.format(len(img2video_images_file_ids))
        if len(img2video_images_file_ids) > 1 else text.SUCCESS_GET_IMAGE_FOR_VIDEO_GENERATION_TEXT,
        message,
    )


# Обработка нажатия на кнопку "✅ Готово" для прекращения сбора изображений для генерации видео
async def done_send_images_for_img2video(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    img2video_images_file_ids = state_data.get("img2video_images_file_ids", [])

    if len(img2video_images_file_ids) == 0:
        await safe_send_message(
            text.NO_IMAGES_FOR_VIDEO_GENERATION_ERROR_TEXT,
            message,
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
                message,
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
                message,
            )
            raise TimeoutError(
                "Время ожидания скачивания файла Telegram истекло.",
            )

    # Сохраняем путь в стейт
    await state.update_data(temp_paths_for_video_generation=temp_paths_for_video_generation)

    # Просим пользователя ввести промпт для генерации видео
    await state.set_state(None)

    message_text = text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT \
        if len(temp_paths_for_video_generation) ==  1 \
        else text.WRITE_PROMPT_FOR_MULTI_VIDEO_GENERATION_FROM_IMAGE_TEXT.format(len(temp_paths_for_video_generation))

    await safe_send_message(
        message_text,
        message,
    )

    await state.set_state(
        StartGenerationState.write_prompt_for_img2video,
    )


# Хендлер для обработки промпта для генерации видео из изображения
async def handle_prompt_for_img2video(
    message: types.Message,
    state: FSMContext,
):
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
            model_indexes.append((1, model_index))
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

            image_index = int(parts[0].strip())
            model_index = int(parts[1].strip())
            model_indexes.append((image_index, model_index))

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
        img2video_temp_paths_for_with_model_names[getModelNameByIndex(model_index)] = \
            temp_paths_for_video_generation[image_index - 1]

    await state.update_data(img2video_temp_paths_for_with_model_names=img2video_temp_paths_for_with_model_names)

    # Получаем данные всех моделей
    all_data_arrays = getAllDataArrays()
    all_data_arrays_length = sum(len(arr) for arr in all_data_arrays)

    # Если индекс какой-то модели больше числа моделей или меньше 1, то просим ввести другой индекс
    for image_index, model_index in model_indexes:
        if model_index > all_data_arrays_length or model_index < 1:
            await safe_send_message(
                text.MODEL_NOT_FOUND_TEXT.format(model_index, image_index),
            message,
            )
            return

    await state.set_state(None)

    # Обрабатываем все изображения в видео
    tasks = [
        process_video(
            message=message,
            prompt=prompt,
            image_index=image_index,
            model_index=model_index,
            temp_paths_for_video_generation=temp_paths_for_video_generation,
        )
        for image_index, model_index in model_indexes
    ]

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


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        start_generateVideoFromImage,
        lambda call: call.data == "generateVideoFromImage",
    )

    router.message.register(
        get_images_for_img2video,
        StateFilter(StartGenerationState.send_image_for_video_generation),
    )

    router.callback_query.register(
        done_send_images_for_img2video,
        lambda call: call.data == "img2video|done_send_images",
    )

    router.message.register(
        handle_prompt_for_img2video,
        StateFilter(
            StartGenerationState.write_prompt_for_img2video,
        ),
    )

    router.message.register(
        handle_model_index_for_video_generation_from_image,
        StateFilter(
            StartGenerationState.ask_for_model_index_for_img2video,
        ),
    )
