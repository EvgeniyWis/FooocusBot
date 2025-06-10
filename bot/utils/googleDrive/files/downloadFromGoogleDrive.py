import os

import httpx
from logger import logger

RESULTS_FOLDER_PATH = "facefusion-docker/.assets/images/results"


# Скачивание файла из Google Drive
async def downloadFromGoogleDrive(url: str, file_id: str) -> str | None:
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        logger.info(f"Попытка скачать файл с URL: {url}")

        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0), follow_redirects=True) as client:
            response = await client.get(url)
            logger.info(f"Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                os.makedirs(RESULTS_FOLDER_PATH, exist_ok=True)
                file_path = os.path.join(RESULTS_FOLDER_PATH, f"{file_id}.jpg")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                logger.info(f"Файл успешно сохранен по пути: {file_path}")
                return file_path
            
            logger.error(f"Неудачный статус ответа: {response.status_code}")
            return None
    except Exception as e:
        raise Exception(f"Произошла ошибка при скачивании файла из Google Drive: {e}")
