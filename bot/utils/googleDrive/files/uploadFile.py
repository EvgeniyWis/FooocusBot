from googleapiclient.http import MediaFileUpload
from logger import logger

from bot.utils.googleDrive.auth import service


# Функция для загрузки файла на Google Drive
async def uploadFile(
    file_path: str, file_metadata: dict, name: str, folder_name: str
):
    media = MediaFileUpload(file_path, resumable=True)
    try:
        file = (
            service.files()
            .create(
                body=file_metadata, media_body=media, fields="id, webViewLink"
            )
            .execute()
        )

        # Добавление разрешения на публичный доступ
        permission = {
            "type": "anyone",
            "role": "reader",
        }
        
        try:
            service.permissions().create(
                fileId=file["id"],
                body=permission,
            ).execute()
        except Exception as e:
            logger.error(f"Ошибка при установке публичного доступа: {e}")

        logger.info(
            f"Файл {name} успешно загружен {f'в папку {folder_name}' if folder_name else '!'}: {file['webViewLink']}"
        )
        return file
    finally:
        media.stream().close()