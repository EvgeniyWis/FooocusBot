from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.types import ImagesToolType
from bot.utils.httpx import httpx_get


class ILoveAPIImagesStarter:
    def __init__(self, api: ILoveAPI):
        self.api = api
        logger.info("Инициализирован стартер для изображений ILoveAPI")

    async def start_task(self, tool: ImagesToolType) -> str:
        url = f"{self.api.base_url}/start/{tool}"

        response = await httpx_get(url)

        
