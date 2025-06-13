from logger import logger

from .. import retryOperation
from .sendRunRequest import sendRunRequest
from utils.handlers.appendDataToStateArray import appendDataToStateArray
from aiogram.fsm.context import FSMContext
from utils.check_unfinished_tasks import check_unfinished_tasks


# Функция для отправки запроса на Runpod с обработкой сетевых ошибок и получения id работы
async def getJobID(dataJSON: dict, setting_number: int, state: FSMContext, user_id: int, job_type: str):
    # Делаем запрос на генерацию
    logger.info("Отправка запроса на генерацию...")

    # Получаем id работы
    response_json = await retryOperation(sendRunRequest, 10, 2, dataJSON, setting_number)

    logger.info(f"Ответ на запрос: {response_json}")

    job_id = response_json["id"]

    logger.info(f"Получен id работы: {job_id}")

    # Сохраняем его в стейт
    dataForUpdate = {"job_id": job_id, "setting_number": setting_number, "user_id": user_id, "job_type": job_type}
    await appendDataToStateArray(state, "image_generation_jobs", dataForUpdate)
    await check_unfinished_tasks.append_new_task(dataForUpdate)

    return job_id
