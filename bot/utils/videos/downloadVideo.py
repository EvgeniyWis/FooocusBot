import os

from utils.httpx import httpx_get


# Скачивание видео по ссылке и сохранении его в папку temp
async def downloadVideo(url: str) -> str:
    try:
        temp_folder_path = "FocuuusBot/temp/videos"
        # Создаем временную директорию, если её нет
        os.makedirs(temp_folder_path, exist_ok=True)

        # Генерируем уникальное имя файла
        video_path = f"{temp_folder_path}/{os.urandom(8).hex()}.mp4"

        # Скачиваем видео
        response = await httpx_get(url, timeout=180, stream=True)

        if response and response.status_code == 200:
            with open(video_path, "wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
            return video_path
        else:
            raise Exception(f"Не удалось скачать видео, статус код: {response.status_code if response else 'нет ответа'}")
    except Exception as e:
        raise Exception(f"Произошла ошибка при скачивании видео: {e}")
