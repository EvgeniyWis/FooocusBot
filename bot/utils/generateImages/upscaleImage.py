from ..jobs.getJobID import getJobID
from ..jobs.checkJobStatus import checkJobStatus
from logger import logger

# Функция для upscale сгенерированного изображения
async def upscaleImage(input_image: str) -> str:
    # Логирование
    logger.info(f"Делаем upscale для изображения...")

    # Формируем json для отправки
    dataJSON = {
        "input": {
            "api_name": "upscale-vary2",
            "require_base64": True,
            "uov_method": "Upscale (1.5x)",
            "input_image": input_image,
            "advanced_params": {"guidance_scale": 3.5, "sampler_name": "euler_ancestral", "overwrite_step": 30},
        }
    }

    # Делаем запрос на генерацию и получаем id работы
    job_id = await getJobID(dataJSON)

    # Проверяем статус работы
    response_json = await checkJobStatus(job_id)

    # Получаем изображение
    image_data = response_json["output"][0]["base64"]

    return image_data

