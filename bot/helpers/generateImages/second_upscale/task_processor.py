import random
import time

import httpx

from bot.logger import logger

from .client_factory import create_client_with_retry


def process_task_with_retry(client, file_path, multiplier=4, max_retries=3):
    """Обрабатывает задачу с повторными попытками при ошибках 401"""
    for attempt in range(max_retries):
        try:
            task = client.create_task("upscaleimage")
            task.process_files(file_path, multiplier=multiplier)
            return task
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                if attempt == max_retries - 1:
                    raise e
                logger.warning(f"Ошибка 401 на попытке {attempt + 1}. Повторная попытка через {2 ** attempt} секунд...")
                time.sleep(2 ** attempt + random.uniform(0, 1))
                # Пересоздаем клиент для новой попытки
                client = create_client_with_retry()
            else:
                raise e
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logger.warning(f"Ошибка на попытке {attempt + 1}: {e}")
            time.sleep(2 ** attempt + random.uniform(0, 1)) 