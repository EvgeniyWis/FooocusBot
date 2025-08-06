
import httpx
from aiogram.fsm.context import FSMContext

from bot.logger import logger
from bot.services.iloveapi import ILoveApiUpscaler
from bot.utils.handlers import appendDataToStateArray
from bot.utils.retryOperation import retryOperation


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

    # Создаем экземпляр сервиса апскейла
    upscaler = ILoveApiUpscaler()
    
    # Выполняем апскейл
    logger.info(f"Начинаю апскейл изображения: {temp_image_path}, модель: {model_name}, индекс: {image_index}, пользователь: {user_id}")

    # Запускаем задачу
    try:
        logger.info("Создаю клиент ILoveApi с увеличенными таймаутами")

        # Используем функцию повторных попыток с увеличенными таймаутами
        await retryOperation(
            upscaler.process_upscale_task,
            3,  # max_attempts (увеличиваем количество попыток)
            30.0,  # delay (увеличиваем задержку между попытками до 30 секунд)
            temp_image_path,
            4,
        )

        logger.info(f"Апскейл успешно завершен для: {temp_image_path}")

    except httpx.ReadTimeout as e:
        error_text = f"Таймаут при увеличении качества изображения: {e}"
        logger.error(error_text)
        logger.error(f"Детали ошибки - путь: {temp_image_path}, модель: {model_name}, индекс: {image_index}, пользователь: {user_id}")
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
            "error_type": "timeout",
        }
        await appendDataToStateArray(
            state,
            "upscale_errors",
            data_for_update,
        )
        raise e
    except httpx.ConnectTimeout as e:
        error_text = f"Таймаут подключения при увеличении качества изображения: {e}"
        logger.error(error_text)
        logger.error(f"Детали ошибки - путь: {temp_image_path}, модель: {model_name}, индекс: {image_index}, пользователь: {user_id}")
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
            "error_type": "connect_timeout",
        }
        await appendDataToStateArray(
            state,
            "upscale_errors",
            data_for_update,
        )
        raise e
    except Exception as e:
        error_text = f"Ошибка при увеличении качества изображения: {e}"
        logger.error(error_text)
        logger.error(f"Детали ошибки - путь: {temp_image_path}, модель: {model_name}, индекс: {image_index}, пользователь: {user_id}")
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
            "error_type": "general",
        }
        await appendDataToStateArray(
            state,
            "upscale_errors",
            data_for_update,
        )
        raise e

    return temp_image_path
