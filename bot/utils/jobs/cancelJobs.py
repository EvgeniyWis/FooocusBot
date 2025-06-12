from config import RUNPOD_HOST, RUNPOD_HEADERS

from logger import logger

from utils import httpx_post
from utils.jobs.getEndpointID import getEndpointID

# Функция для отмены всех работ
async def cancelJobs(jobs_ids: list[dict]):
    # Если нет работ, то ничего не делаем
    if len(jobs_ids) == 0:
        return False
    
    # Отменяем все работы
    for job_dict in jobs_ids:
        try:
            # Получаем id работы и номер настройки
            setting_number = job_dict["setting_number"]
            job_id = job_dict["job_id"]
            
            # Получаем ID эндпоинта для генерации изображений
            ENDPOINT_ID = await getEndpointID(setting_number)

            # Формируем URL для отправки запроса
            url = f"{RUNPOD_HOST}/{ENDPOINT_ID}/cancel/{job_id}"

            # Отправляем запрос на отмену работы
            await httpx_post(url, RUNPOD_HEADERS)
        except Exception as e:
            logger.error(f"Неожиданная ошибка при отмене работы {job_id}: {str(e)}")
            continue

    return True