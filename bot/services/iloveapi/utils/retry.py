import random
import time
from typing import Any

import httpx

from bot.logger import logger

from ..client.api_client import ILoveApiClient
from ..services.task_service import ILoveApiTaskService


def download_with_retry(
    task: Any, 
    output_path: str, 
    client: ILoveApiClient,
    task_service: ILoveApiTaskService,
    max_retries: int = 10
) -> bool:
    """Скачивает файл с повторными попытками при ошибках 401"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Попытка скачивания {attempt + 1}...")
            task.download(output_path)
            logger.info("Файл успешно скачан!")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                if attempt == max_retries - 1:
                    logger.warning("Все попытки скачивания исчерпаны. Пробуем альтернативный способ...")
                    raise e
                logger.warning(f"Ошибка 401 при скачивании на попытке {attempt + 1}. Повторная попытка через {2 ** attempt} секунд...")
                time.sleep(2 ** attempt + random.uniform(0, 1))
                # Пересоздаем клиент и получаем новую задачу
                client.reset_client()
                # Повторно создаем задачу
                task = task_service.process_task_with_retry(output_path, multiplier=4)
            else:
                raise e
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Критическая ошибка при скачивании: {e}")
                raise e
            logger.warning(f"Ошибка при скачивании на попытке {attempt + 1}: {e}")
            time.sleep(2 ** attempt + random.uniform(0, 1))