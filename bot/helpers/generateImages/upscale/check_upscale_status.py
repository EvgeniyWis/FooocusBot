from aiogram.fsm.context import FSMContext
from storage import get_redis_storage

from bot.helpers.generateImages.dataArray import (
    get_group_number_by_model_name,
    get_setting_number_by_model_name,
)
from bot.helpers.jobs.check_job_status import check_job_status
from bot.logger import logger
from bot.utils.images.base64_to_image import base64_to_image


async def check_upscale_status(
    job_id: str,
    state: FSMContext,
    model_name: str,
    image_index: int,
    user_id: int,
    message_id: int,
) -> str:
    """
    Функция для проверки статуса работы upscale и отсылания улучшенного изображения

    Attributes:
        job_id (str): id работы
        state (FSMContext): контекст состояния
        model_name (str): название модели
        image_index (int): индекс изображения
        user_id (int): id пользователя
    """

    # Получаем номер настройки по имени модели
    setting_number = get_setting_number_by_model_name(model_name)

    # Получаем номер группы по имени модели
    group_number = get_group_number_by_model_name(model_name)

    # Проверяем статус работы
    response_json = await check_job_status(
        job_id,
        setting_number,
        group_number,
        user_id,
        message_id,
        state,
        timeout=1000,
        checkOtherJobs=False,
    )

    if not response_json:
        logger.error(f"Не удалось сделать upscale для изображения с ответом от сервера: {response_json}")
        raise Exception("Не удалось сделать upscale для изображения")


    # Проверяем структуру ответа
    if isinstance(response_json, str):
        if response_json == "Работа была отменена":
            redis_storage = get_redis_storage()
            await redis_storage.delete_task_process_image(
                user_id,
                model_name,
                image_index,
            )
            return None
        raise Exception(f"Ошибка при апскейле изображения: {response_json}")

    if (
        "output" not in response_json
        or not isinstance(response_json["output"], list)
        or not response_json["output"]
    ):
        raise Exception(f"Некорректный формат ответа: {response_json}")

    # Получаем изображение из ответа
    output = response_json["output"][0]
    if isinstance(output, dict) and "base64" in output:
        image_data = output["base64"]
    elif isinstance(output, str):
        # Если пришел сразу base64 строкой
        image_data = output
    else:
        raise Exception(f"Неподдерживаемый формат выходных данных: {output}")

    # Сохраняем изображения по этому же пути
    return await base64_to_image(
        image_data,
        model_name,
        image_index,
        user_id,
    )
