from ... import retryOperation
from config import TEMP_FOLDER_PATH
from logger import logger
import shutil
import asyncio
from ..folders.deleteParentFolder import deleteParentFolder
from ..folders.createFolder import createFolder
from ..auth import service
from .uploadFile import uploadFile

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
            date_folder_id, date_folder_link = await createFolder(current_date, None, initial_folder_id)
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
        file = await retryOperation(uploadFile, 3, 2, file_path, file_metadata, name, folder_name)

        if with_deleting_temp_folder:
            # Удаляем папку с файлами
            shutil.rmtree(f"{TEMP_FOLDER_PATH}/{f'{folder_name}_{user_id}' if folder_name else ""}")

            # Через 1 час удаляем и папку в более верхнем уровне
            asyncio.create_task(deleteParentFolder(folder_name, user_id))
            
        return file['webViewLink']

    except Exception as e:
        logger.error(f"Ошибка при сохранении файла: {str(e)}")
        return False