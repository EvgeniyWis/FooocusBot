from googleapiclient.http import MediaFileUpload
from logger import logger
from .auth import service
import shutil
import asyncio
from .deleteParentFolder import deleteParentFolder


# Сохранение одного изображения
async def saveImage(image: str, user_id: int, folder_name: str, folder_id: int):
    try:
        if not folder_id:
            logger.error(f"Некорректный folder_id: {folder_id}")
            raise ValueError("Некорректный folder_id")

        # Получаем кол-во изображений в папке
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name)",
            pageSize=1000
        ).execute()
        files_count = len(results.get('files', []))

        # Создаем имя для файла
        name = f'{files_count + 1}.png'
        file_path = image

        # Создаем метаданные для файла
        file_metadata = {
                        'name': name,
                        'parents': [folder_id]
                    }
            
        # Загружаем изображение
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

        # Удаляем папку с изображениями
        shutil.rmtree(f"temp/{f'{folder_name}_{user_id}' if folder_name else ""}")

        # Через 1 час удаляем и папку в более верхнем уровне
        asyncio.create_task(deleteParentFolder(folder_name, user_id))
        
        return file['webViewLink']

    except Exception as e:
        logger.error(f"Ошибка при сохранении изображения: {str(e)}")
        return False