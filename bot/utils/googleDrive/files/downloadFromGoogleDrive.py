import os

import httpx
from logger import logger

RESULTS_FOLDER_PATH = "facefusion-docker/.assets/images/results"


# Скачивание файла из Google Drive
async def downloadFromGoogleDrive(url: str, file_id: str) -> str | None:
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"

        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.get(url)
            if response.status_code == 200:
                os.makedirs(RESULTS_FOLDER_PATH, exist_ok=True)
                file_path = os.path.join(RESULTS_FOLDER_PATH, f"{file_id}.jpg")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return file_path
            return None
    except Exception as e:
        logger.error(f"Ошибка при скачивании изображения: {e}")
        return None
