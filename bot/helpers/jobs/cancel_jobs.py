from config import RUNPOD_HEADERS, RUNPOD_HOST

from bot.logger import logger
from bot.utils import httpx_post
from bot.helpers.jobs.get_endpoint_ID import get_endpoint_ID

# from utils.check_unfinished_tasks import check_unfinished_tasks


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

            # await check_unfinished_tasks.delete_task(job_id)
        except Exception as e:
            logger.error(
                f"Неожиданная ошибка при отмене работы {job_id}: {str(e)}"
            )
            continue

    return True
