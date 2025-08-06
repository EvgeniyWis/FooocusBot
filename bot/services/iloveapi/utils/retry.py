import os
import random
import time
from typing import Any

import httpx

from bot.logger import logger


def download_with_retry(
    task: Any, 
    output_path: str, 
    max_retries: int = 10
) -> bool:
    """Скачивает файл с повторными попытками при ошибках 401"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Попытка скачивания {attempt + 1}...")
            
            # Проверяем размер файла до скачивания
            if os.path.exists(output_path):
                original_size = os.path.getsize(output_path)
                logger.info(f"Размер файла до скачивания: {original_size} байт")
            
            task.download(output_path)
            
            # Проверяем размер файла после скачивания
            if os.path.exists(output_path):
                new_size = os.path.getsize(output_path)
                logger.info(f"Размер файла после скачивания: {new_size} байт")
                
                if new_size == 0:
                    logger.error("Скачанный файл пустой!")
                    return False
                elif new_size < 100:  # Подозрительно маленький файл
                    logger.warning(f"Скачанный файл подозрительно маленький: {new_size} байт")
            
            logger.info("Файл успешно скачан!")
            return True
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                if attempt == max_retries - 1:
                    logger.warning("Все попытки скачивания исчерпаны. Пробуем альтернативный способ...")
                    raise e
                logger.warning(f"Ошибка 401 при скачивании на попытке {attempt + 1}. Повторная попытка через {2 ** attempt} секунд...")
                time.sleep(2 ** attempt + random.uniform(0, 1))
            else:
                logger.error(f"HTTP ошибка при скачивании: {e.response.status_code} - {e}")
                raise e
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Критическая ошибка при скачивании: {e}")
                raise e
            logger.warning(f"Ошибка при скачивании на попытке {attempt + 1}: {e}")
            time.sleep(2 ** attempt + random.uniform(0, 1))
    
    return False