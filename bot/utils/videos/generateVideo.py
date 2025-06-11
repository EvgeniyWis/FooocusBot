import asyncio
import os

import aiofiles
import httpx
from config import ADMIN_ID
from InstanceBot import bot
from logger import logger

from utils import text

from ..googleDrive.files import downloadFromGoogleDrive, getGoogleDriveFileID
from ..videos import downloadVideo


# Генерация видео с помощью kling
async def generateVideo(
    prompt: str,
    image_url: str = None,
    image_path: str = None,
) -> str |None:
    logger.info(f"Генерация видео с помощью kling: \nПромпт: {prompt}\nСсылка на изображение: {image_url}\nПуть к изображению: {image_path}")
    try:
        if image_url:
            # Получаем id изображения
            image_id = getGoogleDriveFileID(image_url)
            if not image_id:
                logger.error("Не удалось получить id изображения")
                return None

            # Скачиваем изображение
            image_path = await downloadFromGoogleDrive(image_url, image_id)
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
        async with httpx.AsyncClient(timeout=60) as client:
            async with aiofiles.open(image_path, "rb") as image_file:
                files = {
                    "image_url": (
                        "image.jpg",
                        await image_file.read(),
                        "image/jpeg",
                    ),
                }
                headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {os.getenv('KLING_API_KEY')}",
                }

                # Отправляем запрос на генерацию видео
                url_endpoint = "https://api.gen-api.ru/api/v1/networks/kling-v2-1"
                response = await client.post(
                    url_endpoint,
                    data=data,
                    files=files,
                    headers=headers,
                )
                json = response.json()

                logger.info(f"Ответ на запрос на генерацию видео: {json}")

                if json.get("error"):
                    logger.error(
                        f"Ошибка валидации: {json.get('errors_validation')}",
                    )

                    if (
                        json["error"]
                        == "У Вас недостаточно средств на балансе. Подтвердите свой номер телефона и мы начислим Вам стартовый баланс."
                    ):
                        try:
                            await bot.send_message(
                                ADMIN_ID,
                                text.KLING_INSUFFICIENT_BALANCE_TEXT,
                            )
                        finally:
                            raise Exception(text.KLING_INSUFFICIENT_BALANCE_TEXT)

                    return None

                logger.info(
                    f"Запрос на генерацию видео отправлен. Ответ: {json}",
                )

                # Проверяем статус задания в цикле
                request_id = json["request_id"]
                if not request_id:
                    logger.error("Не получен request_id в ответе API")
                    return None

                url_status_endpoint = (
                    f"https://api.gen-api.ru/api/v1/request/get/{request_id}"
                )

                while True:
                    try:
                        response = await client.get(
                            url_status_endpoint,
                            headers=headers,
                        )
                        json = response.json()

                        logger.info(
                            f"Статус задания на генерацию видео с id {request_id}: "
                            f"{json['status']}",
                        )

                        if json["status"] == "error":
                            logger.error(f"Ошибка при генерации видео: {json}")
                            raise Exception(json["result"][0])

                        elif json["status"] == "success":
                            # Получаем ссылку на выходное видео
                            logger.info(
                                f"Выходные данные запроса по id {request_id}: {json}",
                            )
                            result_url = json["full_response"][0]["url"]
                            logger.info(
                                f"Ссылка на выходное видео: {result_url}",
                            )

                            # Скачиваем видео локально
                            video_path = await downloadVideo(result_url)
                            if not video_path:
                                logger.error(
                                    f"Не удалось скачать видео: {result_url}",
                                )
                                raise Exception("Не удалось скачать видео")

                            # Проверяем, что файл существует и имеет размер больше 0
                            if (
                                not os.path.exists(video_path)
                                or os.path.getsize(video_path) == 0
                            ):
                                logger.error(
                                    "Видео файл не существует или "
                                    f"имеет нулевой размер: {video_path}",
                                )

                                # Сохраняем по-новой
                                video_path = await downloadVideo(result_url)
                                if not video_path:
                                    logger.error(
                                        f"Не удалось скачать видео: {result_url}",
                                    )
                                    raise Exception("Не удалось скачать видео")

                            return video_path

                    except Exception as e:
                        logger.error(
                            f"Ошибка при получении статуса задания: {e}",
                        )
                        raise e

                    await asyncio.sleep(10)

    except Exception as e:
        raise e
