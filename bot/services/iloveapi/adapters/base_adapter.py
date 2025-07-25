from bot.logger import logger
from bot.services.iloveapi.client.api_client import ILoveAPI


class ILoveAPIBaseService:
    def __init__(self, api: ILoveAPI) -> None:
        self.api = api
        logger.info(f"Инициализирован сервис {self.__class__.__name__}")
