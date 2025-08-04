
import asyncio

import httpx
from aiogram.fsm.context import FSMContext
from iloveapi import ILoveApi

from bot.logger import logger
from bot.services.iloveapi.client.api_client import ILoveAPI as CustomILoveAPI
from bot.settings import settings
from bot.utils.handlers import appendDataToStateArray
from bot.utils.retryOperation import retryOperation


async def _process_upscale_task(temp_image_path: str, client: ILoveApi):
    """
    Внутренняя функция для обработки задачи upscale с повторными попытками
    """
    logger.info("Создаю задачу upscaleimage")
    task = client.create_task("upscaleimage")
    
    logger.info(f"Обрабатываю файл: {temp_image_path} с множителем 4")
    task.process_files(temp_image_path, multiplier=4)
    
    logger.info("Загружаю обработанный файл")
    task.download(temp_image_path)
    
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
        
        # Создаем клиент с увеличенными таймаутами
        client = ILoveApi(
            public_key=settings.PUBLIC_ILOVEAPI_API_KEY,
            secret_key=settings.SECRET_ILOVEAPI_API_KEY,
        )
        
        # Устанавливаем увеличенные таймауты для HTTP клиента
        if hasattr(client, 'client') and hasattr(client.client, 'timeout'):
            client.client.timeout = httpx.Timeout(
                connect=60.0,  # таймаут подключения
                read=600.0,    # таймаут чтения (10 минут)
                write=60.0,    # таймаут записи
                pool=60.0      # таймаут пула соединений
            )
        
        # Используем функцию повторных попыток с увеличенными таймаутами
        await retryOperation(
            _process_upscale_task,
            3,  # max_attempts
            10.0,  # delay (увеличиваем задержку между попытками)
            temp_image_path,
            client
        )
        
        logger.info(f"Второй upscale успешно завершен для: {temp_image_path}")
        
    except httpx.ReadTimeout as e:
        error_text = f"Таймаут при увеличении качества изображения: {e}"
        logger.error(error_text)
        logger.error(f"Детали ошибки - путь: {temp_image_path}, модель: {model_name}, индекс: {image_index}, пользователь: {user_id}")
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
            "error_type": "timeout"
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
            "error_type": "connect_timeout"
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
            "error_type": "general"
        }
        await appendDataToStateArray(
            state,
            "second_upscale_errors",
            data_for_update,
        )
        raise e
