
from aiogram.fsm.context import FSMContext
from iloveapi import ILoveApi

from bot.logger import logger
from bot.settings import settings
from bot.utils.handlers import appendDataToStateArray


async def second_upscale_image(
    temp_image_path: str,
    model_name: str,
    image_index: int,
    user_id: int,
    state: FSMContext,
):
    """
    Функция для второго upscale изображения с помощью ILoveAPI

    Args:
        temp_image_path (str): путь к временному изображению
        model_name (str): название модели
        image_index (int): индекс изображения
        user_id (int): айди пользователя
        state (FSMContext): контекст состояния

    Returns:
        str: путь к изображению
    """
    logger.info(f"Начинаю второй upscale изображения: {temp_image_path}, модель: {model_name}, индекс: {image_index}, пользователь: {user_id}")

    # Запускаем задачу
    try:
        logger.info("Создаю клиент ILoveApi")
        client = ILoveApi(
            public_key=settings.PUBLIC_ILOVEAPI_API_KEY,
            secret_key=settings.SECRET_ILOVEAPI_API_KEY,
        )

        logger.info("Создаю задачу upscaleimage")
        task = client.create_task("upscaleimage")
        
        logger.info(f"Обрабатываю файл: {temp_image_path} с множителем 2")
        task.process_files(temp_image_path, multiplier=2)
        
        logger.info("Загружаю обработанный файл")
        task.download(temp_image_path)
        
        logger.info(f"Второй upscale успешно завершен для: {temp_image_path}")
    except Exception as e:
        error_text = f"Ошибка при увеличении качества изображения: {e}"
        logger.error(error_text)
        logger.error(f"Детали ошибки - путь: {temp_image_path}, модель: {model_name}, индекс: {image_index}, пользователь: {user_id}")
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
        }
        await appendDataToStateArray(
            state,
            "second_upscale_errors",
            data_for_update,
        )
        raise e
