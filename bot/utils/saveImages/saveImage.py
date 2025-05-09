from googleapiclient.http import MediaFileUpload
from logger import logger
from .auth import service
import shutil
import asyncio
from .deleteParentFolder import deleteParentFolder

# Сохранение одного изображения
async def saveImage(image: str, index: int, user_id: int, job_id: int, folder_name: str, folder_id: int):
    name = f'{folder_name}_{job_id}_{index}.png'
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

    # Удаляем папку с изображениями
    shutil.rmtree(f"temp/{f'{folder_name}_{user_id}' if folder_name else ""}/{job_id}")

    # Через 3 часа удаляем и папку в более верхнем уровне
    asyncio.create_task(deleteParentFolder(folder_name, user_id))
    
    return file['webViewLink']

