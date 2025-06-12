import os

import httpx
from logger import logger
from utils.httpx import httpx_get
from config import FACEFUSION_RESULTS_DIR


# Скачивание файла из Google Drive
async def downloadFromGoogleDrive(url: str, file_id: str) -> str | None:
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        logger.info(f"Попытка скачать файл с URL: {url}")

        response = await httpx_get(url)

        if response:
            os.makedirs(FACEFUSION_RESULTS_DIR, exist_ok=True)
            file_path = os.path.join(FACEFUSION_RESULTS_DIR, f"{file_id}.jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Файл успешно сохранен по пути: {file_path}")
            return file_path

        return None
    except Exception as e:
        raise Exception(f"Произошла ошибка при скачивании файла из Google Drive: {e}")
