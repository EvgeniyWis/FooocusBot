from config import RUNPOD_HOST, RUNPOD_HEADERS
from utils.jobs.getEndpointID import getEndpointID
from logger import logger
import httpx


# Функция для отмены всех работ
async def cancelJobs(jobs_ids: list[dict]):
    # Если нет работ, то ничего не делаем
    if len(jobs_ids) == 0:
        return False
    
    # Отменяем все работы
    for job_dict in jobs_ids:
        # Получаем id работы и номер настройки
        setting_number = job_dict["setting_number"]
        job_id = job_dict["job_id"]
        
        # Получаем ID эндпоинта для генерации изображений
        ENDPOINT_ID = await getEndpointID(setting_number)

        # Формируем URL для отправки запроса
        url = f"{RUNPOD_HOST}/{ENDPOINT_ID}/cancel/{job_id}"

        # Отправляем запрос на генерацию
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=RUNPOD_HEADERS,
                timeout=httpx.Timeout(
                    10,
                    read=60,
                ), 
            )
            logger.info(f"Статус код ответа: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")

            if response.status_code != 200:
                raise Exception(f"Сервер вернул ошибку: {response.status_code}")
            
            logger.info(f"Работа по id {job_id} отменена!")

            try:
                response_json = response.json()
                logger.info(f"Ответ от сервера по отмене работы: {response_json}")
            except (
                ValueError
            ) as e: 
                logger.error(
                    f"Ошибка при парсинге JSON ответа: {e}, тело ответа: {response.text}",
                )
                raise Exception("Сервер вернул невалидный JSON")

    return True