import random
import time

import httpx

from bot.logger import logger

from .client_factory import create_client_with_retry
from .task_processor import process_task_with_retry


def download_with_retry(task, output_path, max_retries=10):
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
                    return download_alternative(task, output_path)
                logger.warning(f"Ошибка 401 при скачивании на попытке {attempt + 1}. Повторная попытка через {2 ** attempt} секунд...")
                time.sleep(2 ** attempt + random.uniform(0, 1))
                # Пересоздаем клиент и получаем новую задачу
                client = create_client_with_retry()
                # Повторно создаем задачу
                task = process_task_with_retry(client, output_path, multiplier=4)
            else:
                raise e
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Критическая ошибка при скачивании: {e}")
                return download_alternative(task, output_path)
            logger.warning(f"Ошибка при скачивании на попытке {attempt + 1}: {e}")
            time.sleep(2 ** attempt + random.uniform(0, 1))


def download_alternative(task, output_path):
    """Альтернативный способ скачивания через прямые HTTP запросы"""
    try:
        logger.info("Пробуем альтернативный способ скачивания...")
        
        # Получаем URL для скачивания
        download_url = f"https://{task._server}.iloveimg.com/v1/download/{task._task}"
        
        # Создаем новый клиент с новыми ключами
        client = create_client_with_retry()
        
        # Формируем заголовки с аутентификацией
        headers = {
            'Authorization': f'Bearer {client._auth.access_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Выполняем запрос на скачивание
        with httpx.Client(timeout=httpx.Timeout(300.0)) as http_client:
            response = http_client.get(download_url, headers=headers)
            response.raise_for_status()
            
            # Сохраняем файл
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logger.info("Файл успешно скачан альтернативным способом!")
            return True
            
    except Exception as e:
        logger.error(f"Альтернативный способ скачивания также не удался: {e}")
        return False 