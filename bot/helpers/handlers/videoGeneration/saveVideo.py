import os
from datetime import datetime

import pytz
from aiogram import types
from logger import logger

from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
)
from bot.settings import settings
from bot.utils.googleDrive.files import saveFile
from bot.utils.googleDrive.folders import getFolderDataByID
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Функция для сохранения видео в папку модели
async def saveVideo(video_path: str, model_name: str, message: types.Message):
    # Получаем текущую дату
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz).strftime("%Y-%m-%d")

    # Получаем id пользователя
    user_id = message.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале сохранения видео
    message_for_delete = await safe_send_message(
        text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index),
        message,
    )

    # Получаем данные о модели по имени
    model_data = await getDataByModelName(model_name)

    logger.info(f"Данные модели: {model_data}")

    # Сохраняем видео
    link = await saveFile(
        file_path=video_path,
        user_id=user_id,
        folder_name=model_name,
        initial_folder_id=model_data["video_folder_id"],
        current_date=now,
        extension="mp4",
    )

    if not link:
        await safe_send_message(
            text.SAVE_FILE_ERROR_TEXT.format(model_name, model_name_index),
            message,
        )
        return

    # Получаем данные родительской папки
    folder = await getFolderDataByID(model_data["video_folder_id"])
    parent_folder_id = folder["parents"][0]
    parent_folder = await getFolderDataByID(parent_folder_id)

    logger.info(
        f"Данные папки по id {model_data['video_folder_id']}: {folder}",
    )

    # Удаляем сообщение о начале сохранения видео
    try:
        await message_for_delete.delete()
    except Exception as e:
        logger.error(
            f"Ошибка при удалении сообщения о начале сохранения видео: {e}",
        )

    # Отправляем сообщение о сохранении видео
    video = types.FSInputFile(video_path)
    await message.answer_video(
        video=video,
        caption=text.SAVE_VIDEO_SUCCESS_TEXT.format(
            link,
            model_name,
            parent_folder["webViewLink"],
            model_name_index,
        ),
    )

    # Удаляем видео из папки temp
    if not settings.MOCK_VIDEO_MODE:
        try:
            os.remove(video_path)
        except Exception as e:
            logger.error(f"Ошибка при удалении видео из папки temp: {e}")
