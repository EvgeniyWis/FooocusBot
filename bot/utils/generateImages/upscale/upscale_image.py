from config import COMMON_NEGATIVE_PROMPT
from logger import logger

from utils.jobs.getJobID import getJobID
from aiogram.fsm.context import FSMContext

from utils.generateImages.upscale.check_upscale_status import check_upscale_status


async def upscale_image(input_image: str, base_config_model_name: str, setting_number: int, 
    state: FSMContext, user_id: int, model_name: str, image_index: int) -> str:
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
            "negative_prompt": COMMON_NEGATIVE_PROMPT,
            "base_model_name": base_config_model_name,
        },
    }

    # Делаем запрос на генерацию и получаем id работы
    job_id = await getJobID(dataJSON, setting_number, state, user_id, "upscale")

    # Проверяем статус работы
    result = await check_upscale_status(job_id, setting_number, state, model_name, image_index, user_id)

    return result
