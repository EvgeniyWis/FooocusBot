import asyncio
import os
import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext
from InstanceBot import bot
from keyboards.videoGeneration import keyboards as video_generation_keyboards
from logger import logger

from utils import text
from utils.retryOperation import retryOperation
from utils.videos.generateVideo import generateVideo


# Функция для генерации видео из изображения
async def generateVideoFromImage(
    file_id_index: int,
    prompt: str,
    message: types.Message,
    state: FSMContext,
):
    try:
        # Получаем данные из стейта и file id изображения
        stateData = await state.get_data()
        image_file_ids = stateData.get("image_file_ids_for_videoGenerationFromImage", [])
        image_file_id = image_file_ids[file_id_index]

        # Скачиваем изображение (file_id) и получаем путь к файлу с таймаутом
        try:
            file = await asyncio.wait_for(
                bot.get_file(image_file_id),
                timeout=30,
            )
        except TimeoutError:
            raise TimeoutError(
                "Время ожидания получения файла Telegram истекло",
            )
        file_path = file.file_path
        temp_path = f"FocuuusBot/temp/images/{image_file_id}.jpg"
        try:
            await asyncio.wait_for(
                bot.download_file(file_path, temp_path),
                timeout=60,
            )
        except TimeoutError:
            raise Exception(
                "⏰ Время ожидания скачивания файла Telegram истекло. Попробуйте позже.",
            )

        # Генерируем видео
        video_path = await retryOperation(
            generateVideo,
            10,
            1.5,
            prompt,
            None,
            temp_path,
        )

        # Сохраняем путь к видео в стейт
        if "video_paths" not in stateData:
            await state.update_data(video_paths=[video_path])
        else:
            video_paths = stateData.get("video_paths", [])
            video_paths.append(video_path)
            await state.update_data(video_paths=video_paths)

        video = types.FSInputFile(video_path)
        await message.answer_video(
            video=video,
            caption=text.SUCCESS_VIDEO_GENERATION_FROM_IMAGE_TEXT,
            reply_markup=video_generation_keyboards.generatedVideoKeyboard(
                file_id_index,
            ),
        )

        # Спрашиваем, в папку какой модели сохранить видео и нужно ли перегенерировать видео
        await state.set_state(None)

        # Удаляем временное изображение
        if os.path.exists(temp_path):   
            os.remove(temp_path)
    except Exception as e:
        traceback.print_exc()
        await message.answer(
            text.GENERATE_VIDEO_FROM_IMAGE_ERROR_TEXT.format(e),
        )
        raise Exception(f"Произошла ошибка при генерации видео из изображения: {e}")
