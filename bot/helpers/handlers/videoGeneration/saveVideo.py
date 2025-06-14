import os
from datetime import datetime

from aiogram import types
from logger import logger

from bot.config import MOCK_MODE
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
)
from bot.utils.googleDrive.files import saveFile
from bot.utils.googleDrive.folders import getFolderDataByID


# Функция для сохранения видео в папку модели
async def saveVideo(video_path: str, model_name: str, message: types.Message):
    # Получаем текущую дату
    now = datetime.now().strftime("%Y-%m-%d")

    # Получаем id пользователя
    user_id = message.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале сохранения видео
    message_for_delete = await message.answer(
        text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index)
    )

    # Получаем данные о модели по имени
    model_data = await getDataByModelName(model_name)

    logger.info(f"Данные модели: {model_data}")

    # Сохраняем видео
    link = await saveFile(
        video_path,
        user_id,
        model_name,
        model_data["video_folder_id"],
        now,
        False,
    )

    if not link:
        await message.answer(
            text.SAVE_FILE_ERROR_TEXT.format(model_name, model_name_index)
        )
        return

    # Получаем данные родительской папки
    folder = getFolderDataByID(model_data["video_folder_id"])
    parent_folder_id = folder["parents"][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(
        f"Данные папки по id {model_data['video_folder_id']}: {folder}"
    )

    # Удаляем сообщение о начале сохранения видео
    try:
        await message_for_delete.delete()
    except Exception as e:
        logger.error(
            f"Ошибка при удалении сообщения о начале сохранения видео: {e}"
        )

    # Отправляем сообщение о сохранении видео
    video = types.FSInputFile(video_path)
    await message.answer_video(
        video=video,
        caption=text.SAVE_VIDEO_SUCCESS_TEXT.format(
            link, model_name, parent_folder["webViewLink"], model_name_index
        ),
    )

    # Удаляем видео из папки temp
    if not MOCK_MODE:
        try:
            os.remove(video_path)
        except Exception as e:
            logger.error(f"Ошибка при удалении видео из папки temp: {e}")
