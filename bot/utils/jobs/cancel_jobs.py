from config import RUNPOD_HEADERS, RUNPOD_HOST

from bot.logger import logger
from bot.torage import get_task_service
from bot.utils import httpx_post
from bot.utils.jobs.get_endpoint_ID import get_endpoint_ID


# Функция для отмены всех работ
async def cancel_jobs(jobs_ids: list[dict]):
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
            ENDPOINT_ID = await get_endpoint_ID(setting_number)

            # Формируем URL для отправки запроса
            url = f"{RUNPOD_HOST}/{ENDPOINT_ID}/cancel/{job_id}"

            # Отправляем запрос на отмену работы
            await httpx_post(url, RUNPOD_HEADERS)

            # Удаляем задачу из Redis
            task_service = get_task_service()
            await task_service.delete_task(job_id)
        except Exception as e:
            logger.error(
                f"Неожиданная ошибка при отмене работы {job_id}: {str(e)}",
            )
            continue

    return True
