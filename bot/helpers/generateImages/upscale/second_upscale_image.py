
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
    import os
    
    # Проверяем существование файла
    if not os.path.exists(temp_image_path):
        raise FileNotFoundError(f"Файл для upscale не найден: {temp_image_path}")
    
    # Проверяем размер файла
    file_size = os.path.getsize(temp_image_path)
    if file_size == 0:
        raise ValueError(f"Файл пустой: {temp_image_path}")
    
    logger.info(f"Создаю задачу upscaleimage для файла размером {file_size} байт")
    task = client.create_task("upscaleimage")
    
    logger.info(f"Обрабатываю файл: {temp_image_path} с множителем 4")
    try:
        task.process_files(temp_image_path, multiplier=4)
        logger.info("Файл успешно отправлен на обработку")
    except Exception as e:
        logger.error(f"Ошибка при отправке файла на обработку: {e}")
        raise
    
    logger.info("Загружаю обработанный файл")
    try:
        task.download(temp_image_path)
        logger.info("Файл успешно загружен")
    except Exception as e:
        logger.error(f"Ошибка при загрузке обработанного файла: {e}")
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
        
        # Создаем клиент с увеличенными таймаутами
        client = ILoveApi(
            public_key=settings.PUBLIC_ILOVEAPI_API_KEY,
            secret_key=settings.SECRET_ILOVEAPI_API_KEY,
        )
        
        # Правильно устанавливаем таймауты для HTTP клиента
        # ILoveApi использует httpx клиент внутри
        if hasattr(client, 'client') and hasattr(client.client, '_client'):
            # Устанавливаем таймауты для внутреннего httpx клиента
            client.client._client.timeout = httpx.Timeout(
                connect=120.0,  # таймаут подключения (2 минуты)
                read=1800.0,    # таймаут чтения (30 минут для upscale)
                write=120.0,    # таймаут записи (2 минуты)
                pool=120.0      # таймаут пула соединений (2 минуты)
            )
        elif hasattr(client, 'client'):
            # Альтернативный способ установки таймаутов
            client.client.timeout = httpx.Timeout(
                connect=120.0,
                read=1800.0,
                write=120.0,
                pool=120.0
            )
        
        # Используем функцию повторных попыток с увеличенными таймаутами
        await retryOperation(
            _process_upscale_task,
            5,  # max_attempts (увеличиваем количество попыток)
            30.0,  # delay (увеличиваем задержку между попытками до 30 секунд)
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
