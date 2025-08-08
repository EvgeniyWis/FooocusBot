import random
import time
from typing import Optional

import httpx

from bot.app.core.logging import logger
from bot.app.config.settings import settings
from iloveapi import ILoveApi


class ILoveApiClient:
    """Клиент для работы с ILoveAPI"""
    
    def __init__(self, max_retries: int = 10):
        self.max_retries = max_retries
        self._client: Optional[ILoveApi] = None
    
    def create_client_with_retry(self) -> ILoveApi:
        """Создает клиент с механизмом повторных попыток"""
        for attempt in range(self.max_retries):
            try:
                # Проверяем наличие API ключей
                if not settings.PUBLIC_ILOVEAPI_API_KEY or not settings.SECRET_ILOVEAPI_API_KEY:
                    raise ValueError("Отсутствуют API ключи для ILoveAPI")
                
                logger.info("Создаем клиент ILoveAPI...")
                
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
                self._client = client
                logger.info("Клиент ILoveAPI успешно создан")
                return client
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                logger.warning(f"Попытка {attempt + 1} создания клиента не удалась: {e}")
                time.sleep(2 ** attempt + random.uniform(0, 1))
    
    @property
    def client(self) -> ILoveApi:
        """Получает клиент, создавая его при необходимости"""
        if self._client is None:
            self._client = self.create_client_with_retry()
        return self._client
    
    def reset_client(self):
        """Сбрасывает клиент для пересоздания"""
        self._client = None 