import os

import httpx
from logger import logger


# Скачивание видео по ссылке и сохранении его в папку temp
async def downloadVideo(url: str) -> str:
    try:
        temp_folder_path = "FocuuusBot/temp/videos"
        # Создаем временную директорию, если её нет
        os.makedirs(temp_folder_path, exist_ok=True)

        # Генерируем уникальное имя файла
        video_path = f"{temp_folder_path}/{os.urandom(8).hex()}.mp4"

        # Скачиваем видео
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.get(url)
        if response.status_code == 200:
            with open(video_path, "wb") as f:
                f.write(response.content)
            return video_path
        else:
            logger.error(
                "Не удалось скачать видео, "
                f"статус код: {response.status_code}",
            )
            raise Exception(f"Не удалось скачать видео, статус код: {response.status_code}")
    except Exception as e:
        raise Exception(f"Произошла ошибка при скачивании видео: {e}")
