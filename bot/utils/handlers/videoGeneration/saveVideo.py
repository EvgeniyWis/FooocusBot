from utils.saveImages.getFolderDataByID import getFolderDataByID
from utils.files.saveFile import saveFile
from utils import text
from logger import logger
from utils.generateImages.dataArray.getModelNameIndex import getModelNameIndex
from aiogram import types
from datetime import datetime
from utils.generateImages.dataArray.getDataByModelName import getDataByModelName


# Функция для сохранения видео в папку модели
async def saveVideo(video_path: str, model_name: str, message: types.Message):
    # Получаем текущую дату
    now = datetime.now().strftime("%Y-%m-%d")

    # Получаем id пользователя
    user_id = message.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале сохранения видео
    await message.answer(text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))

    # Получаем данные о модели по имени
    model_data = getDataByModelName(model_name)

    # Сохраняем видео
    link = await saveFile(video_path, user_id, model_name, model_data['video_folder_id'], now, False)

    if not link:
        await message.answer(text.SAVE_FILE_ERROR_TEXT)
        return
    
    # Получаем данные родительской папки
    folder = getFolderDataByID(model_data['video_folder_id'])
    parent_folder_id = folder['parents'][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(f"Данные папки по id {model_data['video_folder_id']}: {folder}")

    # Отправляем сообщение о сохранении видео
    await message.answer(text.SAVE_VIDEO_SUCCESS_TEXT
    .format(link, model_name, parent_folder['webViewLink'], model_name_index))