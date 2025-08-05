import random
import time

import httpx
from iloveapi import ILoveApi

from bot.logger import logger
from bot.settings import settings


def create_client_with_retry(max_retries=10):
    """Создает клиент с механизмом повторных попыток"""
    for attempt in range(max_retries):
        try:
            # Создаем клиент с увеличенными таймаутами
            client = ILoveApi(
                public_key=settings.PUBLIC_ILOVEAPI_API_KEY,
                secret_key=settings.SECRET_ILOVEAPI_API_KEY,
                timeout=httpx.Timeout(
                    connect=120.0,
                    read=1800.0,
                    write=120.0,
                    pool=120.0,
                ),
            )
            return client
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logger.warning(f"Попытка {attempt + 1} создания клиента не удалась: {e}")
            time.sleep(2 ** attempt + random.uniform(0, 1)) 