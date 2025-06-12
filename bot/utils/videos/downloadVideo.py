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
        response_json = await httpx_get(url, 180)

        if response_json:
            with open(video_path, "wb") as f:
                f.write(response_json.content)
            return video_path
        else:
            raise Exception(f"Не удалось скачать видео, ответ: {response_json.text}")
    except Exception as e:
        raise Exception(f"Произошла ошибка при скачивании видео: {e}")
