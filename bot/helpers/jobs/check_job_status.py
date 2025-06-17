import asyncio

import httpx
from aiogram.fsm.context import FSMContext

from bot.config import RUNPOD_HEADERS, RUNPOD_HOST
from bot.helpers.jobs.delete_job import delete_job
from bot.helpers.jobs.edit_job_message import edit_job_message
from bot.helpers.jobs.get_endpoint_ID import get_endpoint_ID
from bot.logger import logger
from bot.utils import httpx_post

CANCELLED_JOB_TEXT = "Работа была отменена"


async def check_job_status(
    job_id: str,
    setting_number: int,
    user_id: int,
    message_id: int,
    state: FSMContext = None,
    is_test_generation: bool = False,
    checkOtherJobs: bool = True,
    timeout: int = 600 * 100,
):
    """
    Функция для проверки статуса работы по id и возврата соответствующего результата

    Args:
        job_id (str): ID работы
        setting_number (int): Номер настройки
        user_id (int): ID пользователя
        message_id (int): ID сообщения
        state (FSMContext): Контекст состояния
        is_test_generation (bool): Флаг тестовой генерации
        checkOtherJobs (bool): Флаг проверки других работ, должны ли они проверяться
    """

    response_json = None

    try:
        start_time = asyncio.get_event_loop().time()

        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(
                    "Превышено время ожидания статуса работы",
                )

            try:
                # Получаем ID эндпоинта для генерации изображений
                ENDPOINT_ID = await get_endpoint_ID(setting_number)

                # Формируем URL для отправки запроса
                url = f"{RUNPOD_HOST}/{ENDPOINT_ID}/status/{job_id}"
                response_json = await httpx_post(
                    url,
                    RUNPOD_HEADERS,
                    with_response_text_logging=False,
                )

            except (
                httpx.ConnectError,
                httpx.ConnectTimeout,
                httpx.ReadTimeout,
            ) as e:
                logger.error(
                    f"Ошибка соединения при получении статуса работы: {e}",
                )
                await asyncio.sleep(10)
                continue

            if state and not is_test_generation and checkOtherJobs:
                await edit_job_message(
                    job_id,
                    message_id,
                    state,
                    response_json,
                    user_id,
                )

            if response_json["status"] == "COMPLETED":
                break

            elif response_json["status"] in ["FAILED", "CANCELLED"]:
                if response_json["status"] == "FAILED":
                    response_json = response_json["error"]

                elif response_json["status"] == "CANCELLED":
                    response_json = CANCELLED_JOB_TEXT

                break

            await asyncio.sleep(10)

    except Exception as e:
        await delete_job(job_id, state)
        logger.error(
            f"Критическая ошибка при проверке статуса работы {job_id}: {str(e)}",
        )
        raise e

    # Когда работа завершена, получаем изображение
    logger.info(f"Работа по id {job_id} завершена!")

    # Удаляем задачу из стейта и Redis
    await delete_job(job_id, state)

    # Если работа не завершена, то возвращаем False
    if not response_json or response_json == CANCELLED_JOB_TEXT:
        return False

    # Проверяем наличие выходных данных
    images_output = response_json.get("output", [])

    if images_output == []: # Если их нет, то кидаем ошибку
        raise Exception("Не удалось сгенерировать изображения")

    return response_json
