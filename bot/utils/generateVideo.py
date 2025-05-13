import requests
import os
import logging
import pathlib

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Настройка вывода в файл
file_handler = logging.FileHandler('Logs.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Настройка вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
import asyncio
import base64


async def generateVideo(prompt: str, image: str) -> None:
    try:
        # Формируем тело запроса
        input = {
            "prompt": prompt,
            "model": "pro",
            "duration": "5",
            "aspect_ratio": "9:16",
            "negative_prompt": "mismatched elements.",
            "cfg_scale": 0.7,
            "version": "kling-v1-6",
            "image_file": image,
            "translate_input": False
        }

        headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f"Bearer {os.getenv('KLING_API_KEY')}"
            }

        # Отправляем запрос на генерацию видео
        url_endpoint = "https://api.gen-api.ru/api/v1/networks/kling"
        response = requests.post(url_endpoint, json=input, headers=headers)
        json = response.json()

        if json.get('error'):
            logger.error(f"Ошибка валидации: {json.get('errors_validation')}")
            return None

        logger.info(f"Запрос на генерацию видео отправлен. Ответ: {json}")

        # Проверяем статус задания в цикле
        request_id = json.get('request_id')
        if not request_id:
            logger.error("Не получен request_id в ответе API")
            return None

        url_status_endpoint = f"https://api.gen-api.ru/api/v1/request/get/{request_id}"

        while True:
            response = requests.get(url_status_endpoint, headers=headers)
            json = response.json()

            logger.info(f"Статус задания с id {request_id}: {json['status']}")

            if json['status'] == 'error':
                logger.error(f"Ошибка при генерации видео: {json}")
                return None

            if json['status'] == 'success': # Если статус задания успешный, то выходим из цикла
                break

            await asyncio.sleep(10)

        # Получаем ссылку на выходное видео
        result_url = json['full_response']['url']
        logger.info(f"Ссылка на выходное видео: {result_url}")
        return result_url

    except Exception as e:
        logger.error(f"Ошибка при отправке запроса на генерацию видео: {e}")
        return None


if __name__ == "__main__":  
    image_path = pathlib.Path(__file__).parent.parent.parent / "bot/images/faceswap/evanoir.xo.jpg"
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    asyncio.run(generateVideo(
        "Из лица появляется пиявка, которая начинает проникать в глаз",
        encoded_image))