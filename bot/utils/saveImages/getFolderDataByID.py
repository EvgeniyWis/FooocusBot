from .auth import service
from logger import logger

# Функция для получения данных папки по её id
def getFolderDataByID(folder_id: str):
    try:
        folder = service.files().get(
            fileId=folder_id,
            fields='webViewLink, parents'
        ).execute()
        return folder
    except Exception as e:
        logger.error(f"Ошибка при получении данных папки: {e}")
        return None