from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import os
from logger import logger
import shutil


# Авторизация и инициализация клиента google drive
SCOPES = ['https://www.googleapis.com/auth/drive']
current_dir = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(current_dir, "..", "config", "googleDrive.json")
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)


async def save_image(image: str, index: int, folder_name: str = None, folder_id: int = None):
    name = f'{f"{folder_name}_{index}" if folder_name else "test"}.png'
    file_path = image

    if folder_id:
        file_metadata = {
                        'name': name,
                        'parents': [folder_id]
                    }
        
    else:
        file_metadata = {
                        'name': name,
                    }
        
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    
    # Добавление разрешения на публичный доступ
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(
        fileId=file['id'],
        body=permission
    ).execute()
    
    logger.info(f"Изображение {name} успешно загружено {f'в папку {folder_name}' if folder_name else '!'}")
    media.stream().close()
    
    if not folder_name or not folder_id:
        return file['webViewLink']



async def save_images(images: list[str], folder_name: str = None) -> str:
    if folder_name:
        # Создание метаданных для новой папки
        folder_metadata = {
            'name': folder_name,  # Имя вашей папки
            'mimeType': 'application/vnd.google-apps.folder',
        }

        # Создание папки
        folder = service.files().create(body=folder_metadata, fields='id,webViewLink').execute()
        
        # Добавление разрешения на публичный доступ
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=folder.get('id'),
            body=permission
        ).execute()
        
        logger.info(f"Папка {folder_name} создана с ID: {folder['id']}")
        logger.info(f"Ссылка на папку: {folder['webViewLink']}")

        # Загрузка изображений в папку
        for index, image in enumerate(images):
            await save_image(image, index, folder_name, folder["id"])

        result = folder.get('webViewLink')
    else:
        result = await save_image(images[0], 0)

    # Удаляем папку temp
    shutil.rmtree("temp")

    logger.info(f"Временная папка temp успешно удалена!")

    return result