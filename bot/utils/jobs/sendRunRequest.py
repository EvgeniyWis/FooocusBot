from config import RUNPOD_HOST, RUNPOD_HEADERS
from logger import logger
import requests


# Функция для отправки запроса на генерацию
async def sendRunRequest(dataJSON: dict):
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
        return response_json
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Ошибка при парсинге JSON ответа: {e}, тело ответа: {response.text}")
        raise Exception("Сервер вернул невалидный JSON")
