from googleapiclient.http import MediaFileUpload
from config import TEMP_FOLDER_PATH
from logger import logger
from ..saveImages.auth import service
import shutil
import asyncio
from ..saveImages.deleteParentFolder import deleteParentFolder
from ..saveImages.createFolder import createFolder


# Сохранение одного файла
async def saveFile(file_path: str, user_id: int, folder_name: str, initial_folder_id: int, current_date: str, with_deleting_temp_folder: bool = True):
    try:
        if not initial_folder_id:
            logger.error(f"Некорректный initial_folder_id: {initial_folder_id}")
            raise ValueError("Некорректный initial_folder_id")

        # Проверяем есть ли папка с сегодняшней датой
        results = service.files().list(
            q=f"'{str(initial_folder_id)}' in parents and name = '{current_date}'",
            fields="files(id, name)",
            pageSize=1000
        ).execute()

        # Если папка с сегодняшней датой есть, то получаем её id
        if results.get('files', []):
            date_folder_id = results.get('files', [])[0].get('id')
        else: # Если папки с сегодняшней датой нет, то создаём её
            date_folder_id, date_folder_link = createFolder(current_date, initial_folder_id)
            logger.info(f"Полученный folder_id для папки с датой: {date_folder_id} и ссылка на папку: {date_folder_link}")

        # Получаем кол-во файлов в папке
        results = service.files().list(
            q=f"'{str(date_folder_id)}' in parents",
            fields="files(id, name)",
            pageSize=1000
        ).execute()
        files_count = len(results.get('files', []))

        # Создаем имя для файла
        name = f'{files_count + 1}.{file_path.split(".")[-1]}'

        # Создаем метаданные для файла
        file_metadata = {
                        'name': name,
                        'parents': [date_folder_id]
                    }
            
        # Загружаем файл
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
        
        logger.info(f"Файл {name} успешно загружен {f'в папку {folder_name}' if folder_name else '!'}: {file['webViewLink']}")
        media.stream().close()

        if with_deleting_temp_folder:
            # Удаляем папку с файлами
            shutil.rmtree(f"{TEMP_FOLDER_PATH}/{f'{folder_name}_{user_id}' if folder_name else ""}")

            # Через 1 час удаляем и папку в более верхнем уровне
            asyncio.create_task(deleteParentFolder(folder_name, user_id))
            
        return file['webViewLink']

    except Exception as e:
        logger.error(f"Ошибка при сохранении файла: {str(e)}")
        return False