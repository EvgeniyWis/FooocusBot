import os
from datetime import datetime

import pytz
from aiogram import types

from bot.app.config.settings import settings
from bot.app.core.logging import logger
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_model_index_by_model_name,
    getDataByModelName,
)
from bot.utils.googleDrive.files import saveFile
from bot.utils.googleDrive.folders import getFolderDataByID
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)
from bot.utils.videos.download_nsfw_video import download_nsfw_videos


# Функция для сохранения видео в папку модели
async def saveVideo(
    model_name: str,
    message: types.Message,
    video_path: str | None = None,
    video_url: str | None = None,
    is_nsfw_generation: bool = False,
    extension: str = "mp4",
):
    # Получаем текущую дату
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz).strftime("%Y-%m-%d")

    # Получаем id пользователя
    user_id = message.from_user.id

    # Получаем индекс модели
    model_name_index = get_model_index_by_model_name(model_name)

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
        file_url=video_url,
        user_id=user_id,
        folder_name=model_name,
        initial_folder_id=model_data["video_folder_id"]
        if not is_nsfw_generation
        else model_data["nsfw_video_folder_id"],
        current_date=now,
        extension=extension,
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
    caption = text.SAVE_VIDEO_SUCCESS_TEXT.format(
        link,
        model_name,
        parent_folder["webViewLink"],
        model_name_index,
    )

    if video_url:
        video_paths = [v async for v in download_nsfw_videos([video_url])]
        video_path = video_paths[0][0].path

    video = types.FSInputFile(video_path)
    await message.answer_video(
        video=video,
        caption=caption,
    )

    # Удаляем видео из папки temp
    if not settings.MOCK_VIDEO_MODE and video_path:
        try:
            os.remove(video_path)
        except Exception as e:
            logger.error(f"Ошибка при удалении видео из папки temp: {e}")
