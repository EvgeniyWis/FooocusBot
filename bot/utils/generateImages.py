import requests
import base64
import os
import asyncio
from PIL import Image
import io
from logger import logger
from aiogram import types
from utils.text import GET_JOB_ID_SUCCESS_TEXT

# Функция для преобразования изображения из base64 в PIL Image
async def base64_to_image(image_data: str) -> Image.Image:
    if not image_data:
        raise ValueError("Нет данных изображения для декодирования")
    
    # Удаляем префикс Data URL если он присутствует
    if image_data.startswith("data:image/"):
        image_data = image_data.split(",", 1)[1]

    # Декодируем base64 строку в бинарные данные
    try:
        padding = len(image_data) % 4
        if padding:
            image_data += '=' * (4 - padding)
        image_bytes = base64.b64decode(image_data)
        
        # Проверяем, что данные действительно являются изображением
        if not image_bytes.startswith(b'\x89PNG\r\n\x1a\n') and not image_bytes.startswith(b'\xff\xd8'):
            raise ValueError("Полученные данные не являются изображением PNG или JPEG")
        
        # Создаем изображение из бинарных данных
        image = Image.open(io.BytesIO(image_bytes))
        
        # Проверяем, что изображение было успешно загружено
        image.verify()
        image = Image.open(io.BytesIO(image_bytes))  # Открываем заново после verify

        logger.info(f"Изображение успешно загружено: {image}")
        
        # Возвращаем изображение
        return image
        
    except Exception as e:
        print(f"Ошибка при обработке изображения: {str(e)}")
        print(f"Длина полученных данных: {len(image_data)}")
        print(f"Первые 20 символов данных: {image_data[:20]}")


# Функция для генерации изображений с помощью API
async def generateImages(prompt: str, message: types.Message):
    # Делаем запрос на генерацию
    headers = {
        "Content-Type": "application/json",
        'Authorization': os.getenv("RUNPOD_API_KEY")
    }

    host = "https://api.runpod.ai/v2/s5t9qxbuze8zpp"

    # Получаем абсолютный путь к файлу
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(current_dir, "..", "static", "images", "source.png")
    source = open(source_path, "rb").read()

    data = {
        "input": {
            "api_name": "img2img2",
            "require_base64": True,
            "prompt": prompt,
            "image_prompts": [
                {
                    "cn_img": base64.b64encode(source).decode('utf-8'),
                    "cn_stop": 0.5,
                    "cn_weight": 1,
                    "cn_type": "FaceSwap"
                },
            ],
        }
    }

    logger.info(f"Отправка запроса на генерацию...")

    # Получаем id работы
    response = requests.post(f'{host}/run', headers=headers, json=data)
    response_json = response.json()
    
    job_id = response_json['id']

    await message.edit_text(GET_JOB_ID_SUCCESS_TEXT)

    logger.info(f"Получен id работы: {job_id}")

    # Проверяем статус работы, пока она не будет завершена
    while True:
        response = requests.post(f'{host}/status/{job_id}', headers=headers)
        response_json = response.json()

        logger.info(f"Получен статус работы c id {job_id}: {response_json['status']}")

        if response_json['status'] == 'COMPLETED':
            break

        elif response_json['status'] == 'FAILED':
            raise Exception(response_json['error'])

        await asyncio.sleep(10)

    # Когда работа завершена, получаем изображение
    logger.info(f"Работа по id {job_id} завершена!")
    try:
        image_data = response_json["output"][0]["base64"]
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
    
    return await base64_to_image(image_data)


