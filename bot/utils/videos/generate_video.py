from bot.utils.videos.check_video_generation_status import (
    check_video_generation_status,
)
from bot.utils.videos.start_generate_video import start_generate_video


async def generate_video(
    prompt: str,
    image_url: str = None,
    image_path: str = None,
) -> str | None:
    """
    Генерация видео с помощью kling

    Args:
        prompt (str): Промпт для генерации видео
        image_url (str): Ссылка на изображение
        image_path (str): Путь к изображению

    Returns:
        str: Путь к сгенерированному видео
        None: Если произошла ошибка
    """

    try:
        json = await start_generate_video(prompt, image_url, image_path)

        video_path = await check_video_generation_status(json)

        return video_path

    except Exception as e:
        raise e
