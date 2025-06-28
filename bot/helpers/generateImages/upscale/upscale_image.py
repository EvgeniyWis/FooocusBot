from aiogram.fsm.context import FSMContext

from bot.helpers.generateImages.upscale.check_upscale_status import (
    check_upscale_status,
)
from bot.helpers.jobs.get_job_ID import get_job_ID
from bot.logger import logger
from bot.settings import settings
from bot.utils.handlers import appendDataToStateArray


async def upscale_image(
    input_image: str,
    base_config_model_name: str,
    setting_number: int,
    state: FSMContext,
    user_id: int,
    model_name: str,
    image_index: int,
    message_id: int,
) -> str:
    """
    Функция для посылания запроса на upscale сгенерированного изображения и проверки его статуса работы

    Attributes:
        input_image (str): сгенерированное входное изображение
        base_config_model_name (str): базовая модель нейросети, на которой будет сделан upscale
        setting_number (int): номер настройки
        state (FSMContext): контекст состояния
        user_id (int): id пользователя
        model_name (str): название модели
        image_index (int): индекс изображения
    """

    # Логирование
    logger.info("Делаем upscale для изображения...")

    # Формируем json для отправки
    dataJSON = {
        "input": {
            "api_name": "upscale-vary2",
            "require_base64": True,
            "uov_method": "Upscale (1.5x)",
            "input_image": input_image,
            "advanced_params": {
                "sampler_name": "euler_ancestral",
                "overwrite_step": 60,
            },
            "style_selections": [],
            "guidance_scale": 3.5,
            "negative_prompt": settings.COMMON_NEGATIVE_PROMPT,
            "base_model_name": base_config_model_name,
            "prompt": settings.COMMON_UPSCALE_PROMPT,
        },
    }

    # Делаем запрос на генерацию и получаем id работы
    job_id = await get_job_ID(
        dataJSON,
        setting_number,
        state,
        user_id,
        "upscale",
    )

    # Сохраняем имя модели и индекс изображения в стейт
    data_for_update = {
        "model_name": model_name,
        "image_index": image_index,
        "job_id": job_id,
    }
    await appendDataToStateArray(
        state,
        "upscale_data",
        data_for_update,
        unique_keys=("model_name", "image_index"),
    )

    # Проверяем статус работы
    result = await check_upscale_status(
        job_id,
        setting_number,
        state,
        model_name,
        image_index,
        user_id,
        message_id,
    )

    return result
