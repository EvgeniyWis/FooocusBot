import aiofiles

from bot.helpers import text
from bot.InstanceBot import bot
from bot.logger import logger
from bot.settings import settings
from bot.utils.get_api_headers import get_kling_headers
from bot.utils.googleDrive.files import (
    downloadFromGoogleDrive,
    getGoogleDriveFileID,
)
from bot.utils.httpx import httpx_post
from bot.utils.videos.errors_texts import NOT_ENOUGH_MONEY_ERROR_TEXT


async def start_generate_video(
    prompt: str,
    image_url: str = None,
    image_path: str = None,
) -> dict | None:
    """
    Функция для скачивания изображения по ссылке или по пути к файлу и
    отправки запроса на генерацию видео с помощью API kling

    Args:
        prompt (str): Промпт для генерации видео
        image_url (str): Ссылка на изображение
        image_path (str): Путь к изображению

    Returns:
        dict: JSON ответ от API kling
        None: Если произошла ошибка
    """

    if not image_path and not image_url:
        raise Exception("Не удалось найти изображение для генерации видео!")

    logger.info(
        f"Генерация видео с помощью kling: \nПромпт: {prompt}\nСсылка на изображение: {image_url}\nПуть к изображению: {image_path}",
    )

    if image_url:
        # Получаем id изображения
        image_id = getGoogleDriveFileID(image_url)
        if not image_id:
            logger.error("Не удалось получить id изображения")
            return None

        # Скачиваем изображение
        image_path = await downloadFromGoogleDrive(image_id)
        if not image_path:
            logger.error("Не удалось скачать изображение")
            return None

    # Формируем данные запроса
    data = {
        "prompt": prompt,
        "model": "standard",
        "duration": "5",
        "aspect_ratio": "9:16",
        "negative_prompt": "cartoon, anime, 3D render, low resolution, blurry, out of focus, pixelated, overexposed, underexposed, oversaturated, flat lighting, unrealistic proportions, unnatural colors, poorly detailed textures, poorly rendered hair, low-quality shadows, distorted features, artificial-looking expressions, plastic skin, unnatural movement, stiff pose, low-quality assets, low frame rate, poorly lit environments, amateur composition, unbalanced colors, noise, grainy image, lack of depth, unnatural anatomy, clipping issues, over-sharpening, artificial glow, mismatched elements.",
        "cfg_scale": 0.7,
    }

    # Асинхронное открытие файла для отправки
    async with aiofiles.open(image_path, "rb") as image_file:
        files = {
            "image_url": (
                "image.jpg",
                await image_file.read(),
                "image/jpeg",
            ),
        }

    # Отправляем запрос на генерацию видео
    url_endpoint = "https://api.gen-api.ru/api/v1/networks/kling-v2-1"
    json = await httpx_post(
        url_endpoint,
        get_kling_headers(),
        data=data,
        files=files,
    )

    logger.info(f"Ответ на запрос на генерацию видео: {json}")

    if json.get("error"):
        # Обрабатываем ошибки валидации
        errors_validation = json.get("errors_validation")

        if errors_validation:
            logger.error(
                f"Ошибка валидации: {errors_validation}",
            )

        # Обрабатываем ошибку недостаточного баланса
        if json["error"] == NOT_ENOUGH_MONEY_ERROR_TEXT:
            try:
                await bot.send_message(
                    settings.ADMIN_ID,
                    text.KLING_INSUFFICIENT_BALANCE_TEXT,
                )
            finally:
                raise SystemError(text.KLING_INSUFFICIENT_BALANCE_TEXT)

        raise Exception(json["error"])

    logger.info(
        f"Запрос на генерацию видео отправлен. Ответ: {json}",
    )

    return json
