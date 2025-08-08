import random
import time
from typing import Any

import httpx

from bot.app.core.logging import logger
from bot.services.iloveapi.client.api_client import ILoveApiClient


class ILoveApiTaskService:
    """Сервис для работы с задачами ILoveAPI"""
    
    def __init__(self, client: ILoveApiClient):
        self.client = client
    
    def process_task_with_retry(
        self,
        file_path: str,
        task_type: str, 
        max_retries: int = 3,
        **kwargs: Any,
    ) -> Any:
        """Обрабатывает задачу с повторными попытками при ошибках 401"""
        for attempt in range(max_retries):
            try:
                client_instance = self.client.client
                task = client_instance.create_task(task_type)
                task.process_files(file_path, **kwargs)
                return task
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Ошибка 401 на попытке {attempt + 1}. Повторная попытка через {2 ** attempt} секунд...")
                    time.sleep(2 ** attempt + random.uniform(0, 1))
                    # Пересоздаем клиент для новой попытки
                    self.client.reset_client()
                else:
                    raise e
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logger.warning(f"Ошибка на попытке {attempt + 1}: {e}")
                time.sleep(2 ** attempt + random.uniform(0, 1)) 