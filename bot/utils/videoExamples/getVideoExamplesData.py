import os

# Функция для получения примеров шаблонов для генерации видео с помощью kling
async def getVideoExamplesData() -> dict:
    # Путь к папке с видео
    folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "videos", "templates_examples")
    
    # Расширения видеофайлов, которые хотим найти
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}

    # Получаем список всех файлов в папке с нужными расширениями
    video_files = [f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) and
                os.path.splitext(f)[1].lower() in video_extensions]

    # Формируем массив из промптов
    prompts = ["hips dance", "hips dance 2"]

    # Если длина массива промптов и длина массива видео не равны, то выводим ошибку
    if len(prompts) != len(video_files):
        raise ValueError("Длина массива промптов и длина массива видео не равны")

    # Формируем объект с промптами и видео
    result = {}
    for index, file in enumerate(video_files):
        result[index] = {"file_path": os.path.join(folder_path, file), "prompt": prompts[index]}

    return result