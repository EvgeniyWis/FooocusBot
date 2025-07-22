from bot.logger import logger
from bot.services.freepik.services.magnific.client.api_client import (
    MagnificAPI,
)


class BaseService:
    def __init__(self, api: MagnificAPI) -> None:
        self.api = api
        logger.info(f"Инициализирован сервис {self.__class__.__name__}")
