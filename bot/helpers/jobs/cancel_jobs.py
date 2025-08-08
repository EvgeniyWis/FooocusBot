from bot.helpers.jobs.get_endpoint_ID import get_endpoint_ID
from bot.app.core.logging import logger
from bot.app.config.settings import settings
from bot.utils import httpx_post
from bot.utils.get_api_headers import get_runpod_headers


# Функция для отмены всех работ
async def cancel_jobs(jobs_ids: list[dict]):
    # Если нет работ, то ничего не делаем
    if len(jobs_ids) == 0:
        return False

    # Отменяем все работы
    for job_dict in jobs_ids:
        logger.info(f"Отменяем работу по id: {job_dict["job_id"]}")

        try:
            # Получаем id работы и номер группы
            setting_number = job_dict["setting_number"]
            job_id = job_dict["job_id"]

            # Получаем ID эндпоинта для генерации изображений
            ENDPOINT_ID = await get_endpoint_ID(setting_number)

            # Формируем URL для отправки запроса
            url = f"{settings.RUNPOD_HOST}/{ENDPOINT_ID}/cancel/{job_id}"

            # Отправляем запрос на отмену работы
            await httpx_post(url, get_runpod_headers())

        except Exception as e:
            logger.error(
                f"Неожиданная ошибка при отмене работы {job_id}: {str(e)}",
            )
            continue

    return True
