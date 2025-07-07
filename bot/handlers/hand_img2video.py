import asyncio
import os
import traceback

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
from bot.helpers.handlers.videoGeneration import (
    check_video_path,
    saveVideo,
)
from bot.InstanceBot import bot, router
from bot.logger import logger
from bot.states import StartGenerationState
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Обработка нажатия на кнопку "📹 Сгенерировать видео из изображения'"
async def start_generateVideoFromImage(
    call: types.CallbackQuery,
    state: FSMContext,
):
    await call.message.edit_text(text.SEND_IMAGE_FOR_VIDEO_GENERATION)
    await state.set_state(StartGenerationState.send_image_for_video_generation)


# Обработка присылания изображения для генерации видео и запроса на присылания промпта
async def write_prompt_for_videoGenerationFromImage(
    message: types.Message,
    state: FSMContext,
):
    # Проверяем, есть ли изображение в сообщении
    if not message.photo:
        await safe_send_message(
            text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT,
            message,
        )
        return

    # Получаем file_id самого большого изображения
    photo = message.photo[-1]
    await state.update_data(
        image_file_id_for_videoGenerationFromImage=photo.file_id,
    )

    # Просим пользователя ввести промпт для генерации видео
    await state.set_state(None)
    await safe_send_message(
        text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FOR_IMAGE_TEXT,
        message,
    )
    await state.set_state(
        StartGenerationState.write_prompt_for_videoGenerationFromImage,
    )


# Хендлер для обработки промпта для генерации видео из изображения
async def handle_prompt_for_videoGenerationFromImage(
    message: types.Message,
    state: FSMContext,
):
    # Получаем промпт
    prompt = message.text

    await state.update_data(prompt_for_videoGenerationFromImage=prompt)
    state_data = await state.get_data()
    image_file_id = state_data.get(
        "image_file_id_for_videoGenerationFromImage",
    )

    if not image_file_id:
        await safe_send_message(
            text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT,
            message,
        )
        return

    # Отправляем сообщение о прогрессе
    generate_video_from_image_progress_message = await safe_send_message(
        text.GENERATE_VIDEO_FROM_IMAGE_PROGRESS_TEXT,
        message,
    )

    try:
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

        # Генерируем видео
        video_path = await check_video_path(
            prompt,
            message,
            image_index=None,
            image_url=None,
            temp_path=temp_path,
            model_name=None,
        )

        await generate_video_from_image_progress_message.delete()

        if not video_path:
            return

        await state.update_data(
            video_path_for_img2video=video_path,
        )

        video = types.FSInputFile(video_path)
        await message.answer_video(
            video=video,
            caption=text.GENERATE_VIDEO_FROM_IMAGE_SUCCESS_TEXT,
        )

        # Спрашиваем, в папку какой модели сохранить видео
        await state.set_state(None)
        await safe_send_message(
            text.ASK_FOR_MODEL_NAME_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT,
            message,
        )
        await state.set_state(
            StartGenerationState.ask_for_model_name_for_video_generation_from_image,
        )

        # Удаляем временное изображение
        os.remove(temp_path)
    except Exception as e:
        traceback.print_exc()
        raise e


# Хендлер для обработки ввода имени модели для сохранения видео
async def handle_model_name_for_video_generation_from_image(
    message: types.Message,
    state: FSMContext,
):
    # Получаем данные
    state_data = await state.get_data()

    # Получаем данные по имени модели
    try:
        model_index = int(message.text)
    except Exception as e:
        logger.error(f"Произошла ошибка при получении индекса модели: {e}")
        await safe_send_message(
            text.WRONG_MODEL_INDEX_TEXT.format(message.text),
            message,
        )
        return

    # Получаем данные всех моделей
    all_data_arrays = getAllDataArrays()
    all_data_arrays_length = sum(len(arr) for arr in all_data_arrays)

    # Если индекс больше числа моделей или меньше 1, то просим ввести другой индекс
    if model_index > all_data_arrays_length or model_index < 1:
        await safe_send_message(
            text.MODEL_NOT_FOUND_TEXT.format(model_index),
            message,
        )
        return

    # Получаем путь к видео
    video_path = state_data.get("video_path_for_img2video", "")

    # Получаем название модели по индексу
    model_name = getModelNameByIndex(model_index)

    # Сохраняем видео
    await state.set_state(None)
    await saveVideo(video_path, model_name, message)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        start_generateVideoFromImage,
        lambda call: call.data == "generateVideoFromImage",
    )

    router.message.register(
        write_prompt_for_videoGenerationFromImage,
        StateFilter(StartGenerationState.send_image_for_video_generation),
    )

    router.message.register(
        handle_prompt_for_videoGenerationFromImage,
        StateFilter(
            StartGenerationState.write_prompt_for_videoGenerationFromImage,
        ),
    )

    router.message.register(
        handle_model_name_for_video_generation_from_image,
        StateFilter(
            StartGenerationState.ask_for_model_name_for_video_generation_from_image,
        ),
    )