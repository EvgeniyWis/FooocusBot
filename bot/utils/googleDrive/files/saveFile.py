import http.client
import os
import shutil
import socket

from bot import constants
from bot.logger import logger
from bot.utils.googleDrive.auth import service
from bot.utils.googleDrive.files.uploadFile import uploadFile
from bot.utils.googleDrive.folders.createFolder import createFolder
from bot.utils.retryOperation import retryOperation


# Сохранение одного файла
async def saveFile(
    file_path: str,
    user_id: int,
    folder_name: str,
    initial_folder_id: int,
    current_date: str,
    image_index: int | None = None,
):
    try:
        if not initial_folder_id:
            logger.error(
                f"Некорректный initial_folder_id: {initial_folder_id}",
            )
            raise ValueError("Некорректный initial_folder_id")

        # Проверяем есть ли папка с сегодняшней датой
        try:
            results = (
                service.files()
                .list(
                    q=f"'{str(initial_folder_id)}' in parents and name = '{current_date}'",
                    fields="files(id, name)",
                    pageSize=1000,
                )
                .execute()
            )
        except (
            socket.gaierror,
            http.client.RemoteDisconnected,
            http.client.HTTPException,
            ConnectionError,
            OSError,
        ) as e:
            logger.error(f"Сетевая ошибка при проверке папки с датой: {e}")
            raise ValueError(f"Ошибка подключения к Google Drive: {e}")

        # Если папка с сегодняшней датой есть, то получаем её id
        if results.get("files", []):
            date_folder_id = results.get("files", [])[0].get("id")
        else:  # Если папки с сегодняшней датой нет, то создаём её
            date_folder_id, date_folder_link = await createFolder(
                current_date,
                None,
                initial_folder_id,
            )
            logger.info(
                f"Полученный folder_id для папки с датой: {date_folder_id} и ссылка на папку: {date_folder_link}",
            )

        # Получаем кол-во файлов в папке
        try:
            results = (
                service.files()
                .list(
                    q=f"'{str(date_folder_id)}' in parents",
                    fields="files(id, name)",
                    pageSize=1000,
                )
                .execute()
            )
        except (
            socket.gaierror,
            http.client.RemoteDisconnected,
            http.client.HTTPException,
            ConnectionError,
            OSError,
        ) as e:
            logger.error(f"Сетевая ошибка при получении списка файлов: {e}")
            raise Exception(f"Ошибка подключения к Google Drive: {e}")

        files_count = len(results.get("files", []))

        # Создаем имя для файла
        name = f"{files_count + 1}.{file_path.split('.')[-1]}"

        # Создаем метаданные для файла
        file_metadata = {
            "name": name,
            "parents": [date_folder_id],
        }

        # Загружаем файл
        file = await retryOperation(
            uploadFile,
            10,
            2,
            file_path,
            file_metadata,
            name,
            folder_name,
        )

        if image_index is not None:
            # Удаляем файл изображения
            temp_path = os.path.join(
                constants.TEMP_FOLDER_PATH,
                f"{folder_name}_{user_id}",
                f"{image_index}.jpg",
            )
            if os.path.exists(temp_path):
                os.remove(temp_path)

        else:
            # Удаляем папку с изображениями
            temp_path = os.path.join(
                constants.TEMP_FOLDER_PATH,
                f"{folder_name}_{user_id}",
            )
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)

        return file["webViewLink"]

    except Exception as e:
        logger.error(f"Произошла ошибка при сохранении файла: {e}")
        raise RuntimeError(f"Произошла ошибка при сохранении файла: {e}")
