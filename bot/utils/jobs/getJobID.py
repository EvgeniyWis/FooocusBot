from logger import logger
from .. import retryOperation
from .sendRunRequest import sendRunRequest


# Функция для отправки запроса на Runpod с обработкой сетевых ошибок и получения id работы
async def getJobID(dataJSON: dict):
    # Делаем запрос на генерацию
    logger.info(f"Отправка запроса на генерацию...")

    # Получаем id работы
    response_json = await retryOperation(sendRunRequest, 10, 2, dataJSON)

    logger.info(f"Ответ на запрос: {response_json}")
    
    job_id = response_json['id']

    logger.info(f"Получен id работы: {job_id}")

    return job_id
