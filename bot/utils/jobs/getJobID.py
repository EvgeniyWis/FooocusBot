import requests
from logger import logger
from config import RUNPOD_HEADERS, RUNPOD_HOST
import asyncio

# Функция для отправки запроса на Runpod с обработкой сетевых ошибок и получения id работы
async def getJobID(dataJSON: dict):
    # Делаем запрос на генерацию
    logger.info(f"Отправка запроса на генерацию...")

    # Получаем id работы
    max_attempts = 10
    attempt = 0
    while True:
        attempt += 1
        try:
            response = requests.post(
                f'{RUNPOD_HOST}/run', 
                headers=RUNPOD_HEADERS, 
                json=dataJSON,
                timeout=(10, 30)  # (connect timeout, read timeout)
            )
            logger.info(f"Статус код ответа: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")
            
            if response.status_code != 200:
                raise Exception(f"Сервер вернул ошибку: {response.status_code}")
                
            try:
                response_json = response.json()
                break
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"Ошибка при парсинге JSON ответа: {e}, тело ответа: {response.text}")
                raise Exception("Сервер вернул невалидный JSON")
                
        except Exception as e:
            logger.error(f"Ошибка при получении статуса работы (сетевая ошибка): {e}, попытка {attempt}/{max_attempts}")
            if attempt >= max_attempts:
                raise Exception(f"Не удалось подключиться к серверу после {max_attempts} попыток")
            # Экспоненциальное увеличение задержки между попытками
            await asyncio.sleep(min(30, 2 ** attempt))

    logger.info(f"Ответ на запрос: {response_json}")
    
    job_id = response_json['id']

    logger.info(f"Получен id работы: {job_id}")

    return job_id
