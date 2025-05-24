import requests
from utils.googleDrive.files.downloadFromGoogleDrive import downloadFromGoogleDrive
from logger import logger
from utils.googleDrive.files.getGoogleDriveFileID import getGoogleDriveFileID
import os
import asyncio
from utils.videos.downloadVideo import downloadVideo


# Генерация видео с помощью kling
async def generateVideo(prompt: str, image_url: str) -> None:
    try:
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
            "model": "standart",
            "duration": "5",
            "aspect_ratio": "9:16",
            "negative_prompt": "cartoon, anime, 3D render, low resolution, blurry, out of focus, pixelated, overexposed, underexposed, oversaturated, flat lighting, unrealistic proportions, unnatural colors, poorly detailed textures, poorly rendered hair, low-quality shadows, distorted features, artificial-looking expressions, plastic skin, unnatural movement, stiff pose, low-quality assets, low frame rate, poorly lit environments, amateur composition, unbalanced colors, noise, grainy image, lack of depth, unnatural anatomy, clipping issues, over-sharpening, artificial glow, mismatched elements.",
            "cfg_scale": 0.7,
            "version": "kling-v1-6",
        }

        # Открываем файл для отправки
        files = {
            'image': ('image.jpg', open(image_path, 'rb'), 'image/jpeg')
        }

        headers = {
            'Accept': 'application/json',
            'Authorization': f"Bearer {os.getenv('KLING_API_KEY')}"
        }

        # Отправляем запрос на генерацию видео
        url_endpoint = "https://api.gen-api.ru/api/v1/networks/kling"
        response = requests.post(url_endpoint, data=data, files=files, headers=headers)
        json = response.json()

        logger.info(f"Ответ на запрос на генерацию видео: {json}")

        if json.get('error'):
            logger.error(f"Ошибка валидации: {json.get('errors_validation')}")
            return None

        logger.info(f"Запрос на генерацию видео отправлен. Ответ: {json}")

        # Проверяем статус задания в цикле
        request_id = json['request_id']
        if not request_id:
            logger.error("Не получен request_id в ответе API")
            return None

        url_status_endpoint = f"https://api.gen-api.ru/api/v1/request/get/{request_id}"

        while True:
            try:
                response = requests.get(url_status_endpoint, headers=headers)
                json = response.json()

                logger.info(f"Статус задания на генерацию видео с id {request_id}: {json['status']}")

                if json['status'] == 'error':
                    raise Exception(json['result'][0])

                elif json['status'] == 'success': # Если статус задания успешный, то возвращаем ответ
                    # Получаем ссылку на выходное видео
                    logger.info(f"Выходные данные запроса по id {request_id}: {json}")
                    result_url = json['full_response'][0]['url']
                    logger.info(f"Ссылка на выходное видео: {result_url}")
                    
                    # Скачиваем видео локально
                    video_path = await downloadVideo(result_url)
                    if not video_path:
                        logger.error(f"Не удалось скачать видео: {result_url}")
                        raise Exception("Не удалось скачать видео")
                        
                    return video_path
                
            except Exception as e:
                logger.error(f"Ошибка при получении статуса задания: {e}")
                raise e

            await asyncio.sleep(10)

    except Exception as e:
        logger.error(f"Ошибка при отправке запроса на генерацию видео: {e}")
        raise e