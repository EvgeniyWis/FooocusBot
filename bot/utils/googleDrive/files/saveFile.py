import http.client
import os
import shutil
import socket

from aiogoogle import Aiogoogle

from bot.app.config import constants
from bot.app.core.logging import logger
from bot.utils.googleDrive.auth import client_creds, user_creds
from bot.utils.googleDrive.files.uploadFile import uploadFile
from bot.utils.googleDrive.folders.createFolder import createFolder
from bot.utils.retryOperation import retryOperation


# Сохранение одного файла
async def saveFile(
    user_id: int,
    folder_name: str,
    initial_folder_id: int,
    current_date: str,
    image_index: int | None = None,
    file_path: str = None,
    file_url: str = None,
    name_postfix: str = None,
    extension: str = "jpg",
):
    try:
        if not initial_folder_id:
            logger.error(
                f"Некорректный initial_folder_id: {initial_folder_id}",
            )
            raise ValueError("Некорректный initial_folder_id")

        async with Aiogoogle(client_creds=client_creds, user_creds=user_creds) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", 'v3')

            # Проверяем есть ли папка с сегодняшней датой
            try:
                results = await aiogoogle.as_user(
                    drive_v3.files.list(
                        q=f"'{str(initial_folder_id)}' in parents and name = '{current_date}'",
                        fields="files(id, name)",
                        pageSize=1000,
                    )
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
            else:
                # Создаём папку с сегодняшней датой
                folder_metadata = {
                    "name": current_date,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [initial_folder_id],
                }
                folder = await aiogoogle.as_user(
                    drive_v3.files.create(
                        json=folder_metadata,
                        fields="id,webViewLink"
                    )
                )
                date_folder_id = folder["id"]
                date_folder_link = folder["webViewLink"]
                # Делаем папку публичной
                permission = {
                    "type": "anyone",
                    "role": "reader",
                    "allowFileDiscovery": True,
                }
                try:
                    await aiogoogle.as_user(
                        drive_v3.permissions.create(
                            fileId=date_folder_id,
                            json=permission,
                            fields="id"
                        )
                    )
                except Exception as e:
                    logger.error(f"Ошибка при установке публичного доступа к папке: {e}")
                logger.info(
                    f"Полученный folder_id для папки с датой: {date_folder_id} и ссылка на папку: {date_folder_link}",
                )

            # Получаем кол-во файлов в папке
            try:
                results = await aiogoogle.as_user(
                    drive_v3.files.list(
                        q=f"'{str(date_folder_id)}' in parents",
                        fields="files(id, name)",
                        pageSize=1000,
                    )
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
            name = f"{files_count + 1}_{name_postfix}.{extension}" if name_postfix else f"{files_count + 1}.{extension}"

            # Создаем метаданные для файла
            file_metadata = {
                "name": name,
                "parents": [date_folder_id],
            }

            # Загружаем файл
            file = await retryOperation(
                uploadFile,
                3,
                2,
                file_metadata,
                name,
                folder_name,
                file_path,
                file_url,
            )

            if not file_url:
                if image_index is not None:
                    # Удаляем файл изображения
                    temp_path = os.path.join(
                        constants.FACEFUSION_TEMP_IMAGES_FOLDER_PATH,
                        f"{folder_name}_{user_id}",
                        f"{image_index}.jpg",
                    )
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                else:
                    # Удаляем папку с изображениями
                    temp_path = os.path.join(
                        constants.FACEFUSION_TEMP_IMAGES_FOLDER_PATH,
                        f"{folder_name}_{user_id}",
                    )
                    if os.path.exists(temp_path):
                        shutil.rmtree(temp_path)

            return file["webViewLink"]

    except Exception as e:
        logger.error(f"Произошла ошибка при сохранении файла: {e}")
        raise RuntimeError(f"Произошла ошибка при сохранении файла: {e}")
