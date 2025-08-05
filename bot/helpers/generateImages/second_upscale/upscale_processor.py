import os

import httpx
from aiogram.fsm.context import FSMContext

from bot.logger import logger
from bot.utils.handlers import appendDataToStateArray
from bot.utils.retryOperation import retryOperation

from .client_factory import create_client_with_retry
from .downloader import download_with_retry
from .task_processor import process_task_with_retry


async def _process_upscale_task(temp_image_path: str):
    """
    Внутренняя функция для обработки задачи upscale с повторными попытками
    """

    # Проверяем существование файла
    if not os.path.exists(temp_image_path):
        raise FileNotFoundError(f"Файл для upscale не найден: {temp_image_path}")
    
    # Проверяем размер файла
    file_size = os.path.getsize(temp_image_path)
    if file_size == 0:
        raise ValueError(f"Файл пустой: {temp_image_path}")
    
    logger.info(f"Создаю задачу upscaleimage для файла размером {file_size} байт")
    
    try:
        # Создаем клиент с повторными попытками
        client = create_client_with_retry()
        
        # Обрабатываем задачу с повторными попытками
        task = process_task_with_retry(client, temp_image_path, multiplier=4)
        
        # Скачиваем результат с повторными попытками
        if download_with_retry(task, temp_image_path):
            logger.info("Задача успешно выполнена!")
        else:
            raise Exception("Не удалось скачать файл ни одним способом")
        
    except Exception as e:
        logger.error(f"Критическая ошибка при обработке upscale: {e}")
        raise
    
    # Проверяем, что файл был обновлен
    if not os.path.exists(temp_image_path):
        raise FileNotFoundError(f"Обработанный файл не найден после загрузки: {temp_image_path}")
    
    new_file_size = os.path.getsize(temp_image_path)
    logger.info(f"Файл успешно обработан. Новый размер: {new_file_size} байт")
    
    return task


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
        logger.info("Создаю клиент ILoveApi с увеличенными таймаутами")

        # Используем функцию повторных попыток с увеличенными таймаутами
        await retryOperation(
            _process_upscale_task,
            3,  # max_attempts (увеличиваем количество попыток)
            30.0,  # delay (увеличиваем задержку между попытками до 30 секунд)
            temp_image_path,
        )

        logger.info(f"Второй upscale успешно завершен для: {temp_image_path}")

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
            "second_upscale_errors",
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
            "second_upscale_errors",
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
            "second_upscale_errors",
            data_for_update,
        )
        raise e 