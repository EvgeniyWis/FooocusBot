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


async def save_images(images: list[str], folder_name: str) -> str:
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
    
    logger.info(f"Папка {folder_name} создана с ID: {folder.get('id')}")
    logger.info(f"Ссылка на папку: {folder.get('webViewLink')}")

    # Загрузка изображений в папку
    for image in images:
        name = f'{folder_name}_{images.index(image)}.png'
        file_path = image
        file_metadata = {
                        'name': name,
                        'parents': [folder["id"]]
                    }
        media = MediaFileUpload(file_path, resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logger.info(f"Изображение {name} успешно загружено в папку {folder_name}")
        # Закрываем файл после загрузки
        media.stream().close()

    # Удаляем папку temp
    shutil.rmtree("temp")

    logger.info(f"Временная папка temp успешно удалена!")

    return folder.get('webViewLink')