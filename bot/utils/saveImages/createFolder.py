from .auth import service
from logger import logger

# Создание папки
def createFolder(folder_name: str):
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

    return folder