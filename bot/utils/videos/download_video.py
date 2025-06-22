import os

from bot.config import VIDEOS_TEMP_DIR
from bot.utils.httpx import httpx_get


async def download_video(url: str) -> str:
    """
    Скачивание видео по ссылке и сохранении его в папку temp

    Args:
        url (str): Ссылка на видео

    Returns:
        str: Путь к сгенерированному видео
    """
    try:
        # Создаем временную директорию, если её нет
        os.makedirs(VIDEOS_TEMP_DIR, exist_ok=True)

        # Генерируем уникальное имя файла
        video_path = f"{VIDEOS_TEMP_DIR}/{os.urandom(8).hex()}.mp4"

        # Скачиваем видео
        response = await httpx_get(url, timeout=180, stream=True)

        if response and response.status_code == 200:
            with open(video_path, "wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
            return video_path
        else:
            raise Exception(
                f"Не удалось скачать видео, статус код: {response.status_code if response else 'нет ответа'}",
            )
    except Exception as e:
        raise Exception(f"Произошла ошибка при скачивании видео: {e}")
