from config import COMMON_NEGATIVE_PROMPT
from logger import logger

from ..jobs.checkJobStatus import checkJobStatus
from ..jobs.getJobID import getJobID
from aiogram.fsm.context import FSMContext


# Функция для upscale сгенерированного изображения
async def upscaleImage(input_image: str, base_config_model_name: str, setting_number: int, state: FSMContext) -> str:
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
    job_id = await getJobID(dataJSON, setting_number, state)

    # Проверяем статус работы
    response_json = await checkJobStatus(job_id, setting_number, state, timeout=1000)

    if not response_json:
        raise Exception("Не удалось сделать upscale для изображения")

    # Получаем изображение
    image_data = response_json["output"][0]["base64"]

    return image_data
