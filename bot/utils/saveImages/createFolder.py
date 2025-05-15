from .auth import service
from logger import logger

# Создание папки
def createFolder(folder_name: str, parent_folder_id: str = None, with_nested_folder: bool = False) -> tuple[str, str]:
    # Создание метаданных для новой папки
    folder_metadata = {
        'name': folder_name,  # Имя вашей папки
        'mimeType': 'application/vnd.google-apps.folder',
    }

    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]

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

    if with_nested_folder:
        # Создание вложенной папки
        nested_folder_name = "videos"
        nested_folder_metadata = {
            'name': nested_folder_name, 
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder['id']]
        }
        nested_folder = service.files().create(body=nested_folder_metadata, fields='id,webViewLink').execute()
        
        logger.info(f"Папка {folder_name} создана с ID: {folder['id']}")
        logger.info(f"Ссылка на папку: {folder['webViewLink']}")

        return folder['id'], nested_folder['webViewLink']
    else:
        return folder['id'], folder['webViewLink']
    