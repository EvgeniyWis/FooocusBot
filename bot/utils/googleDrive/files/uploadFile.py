
import tempfile

import aiohttp
from aiogoogle import Aiogoogle
from logger import logger

from bot.utils.googleDrive.auth import client_creds, user_creds


# Функция для загрузки файла на Google Drive
async def uploadFile(
    file_metadata: dict, name: str, folder_name: str,
    file_path: str = None, file_url: str = None,
):
    if file_url:
        # Скачиваем файл по URL во временный файл чанками
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status != 200:
                    raise Exception(f"Ошибка скачивания файла: {resp.status}")
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    async for chunk in resp.content.iter_chunked(1024 * 1024):
                        tmp_file.write(chunk)
                file_path = tmp_file.name

    async with Aiogoogle(client_creds=client_creds, user_creds=user_creds) as aiogoogle:
        drive_v3 = await aiogoogle.discover('drive', 'v3')

        # Загружаем файл
        file = await aiogoogle.as_user(
            drive_v3.files.create(
                upload_file=file_path,
                fields="id, webViewLink",
                json=file_metadata,
            )
        )

        # Делаем файл публичным
        permission = {
            "type": "anyone",
            "role": "reader",
        }
        try:
            await aiogoogle.as_user(
                drive_v3.permissions.create(
                    fileId=file["id"],
                    json=permission,
                )
            )
        except Exception as e:
            logger.error(f"Ошибка при установке публичного доступа: {e}")

        logger.info(
            f"Файл {name} успешно загружен {f'в папку {folder_name}' if folder_name else '!'}: {file['webViewLink']}"
        )
        return file