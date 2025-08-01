from aiogram.fsm.context import FSMContext
from logger import logger
from utils.handlers.appendDataToStateArray import appendDataToStateArray

from bot.constants import MULTI_IMAGE_NUMBER
from bot.helpers.jobs.send_run_request import send_run_request
from bot.utils.retryOperation import retryOperation


# Функция для отправки запроса на Runpod с обработкой сетевых ошибок и получения id работы
async def get_job_ID(
    dataJSON: dict,
    group_number: int | str,
    state: FSMContext,
    user_id: int,
    job_type: str,
):
    # Делаем запрос на генерацию
    logger.info("Отправка запроса на генерацию...")

    # Обновляем данные о числе изображений, в зависимости от того, есть ли мультигенерация
    state_data = await state.get_data()
    if state_data.get("multi_select_mode", False) and job_type == "image_generation":
        dataJSON["input"]["image_number"] = MULTI_IMAGE_NUMBER

    # Получаем id работы
    response_json = await retryOperation(
        send_run_request,
        10,
        2,
        dataJSON,
        group_number,
    )

    logger.info(f"Ответ на запрос: {response_json}")

    job_id = response_json["id"]

    logger.info(f"Получен id работы: {job_id}")

    # Сохраняем его в стейт
    data_for_update = {
        "job_id": job_id,
        "group_number": group_number,
        "user_id": user_id,
        "job_type": job_type,
    }
    logger.info(f"Сохраняем id работы в стейт: {job_id}")
    await appendDataToStateArray(
        state,
        "image_generation_jobs",
        data_for_update,
        unique_keys=("job_id",),
    )

    return job_id
