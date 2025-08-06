import os

import aiofiles

import bot.constants as constants
from bot.logger import logger
from bot.utils.httpx import httpx_get


# Скачивание файла из Google Drive
async def downloadFromGoogleDrive(file_id: str) -> str | None:
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        logger.info(f"Попытка скачать файл с URL: {url}")

        response = await httpx_get(url)

        if response and hasattr(response, 'content'):
            os.makedirs(constants.FACEFUSION_RESULTS_DIR, exist_ok=True)
            file_path = os.path.join(
                constants.FACEFUSION_RESULTS_DIR, f"{file_id}.jpg"
            )
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(response.content)
            logger.info(f"Файл успешно сохранен по пути: {file_path}")
            return file_path

        return None
    except Exception as e:
        raise Exception(
            f"Произошла ошибка при скачивании файла из Google Drive: {e}",
        )
