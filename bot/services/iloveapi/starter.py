from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.types import ImagesToolType
from bot.utils.httpx import httpx_get


class ILoveAPIStarter:
    def __init__(self, api: ILoveAPI):
        self.api = api
        logger.info("Инициализирован стартер ILoveAPI")

    async def start_task(self, tool: ImagesToolType) -> dict:
        """
        Стартер задач в ILoveAPI

        Args:
            tool (ImagesToolType): Тип инструмента

        Returns:
            dict: JSON ответ

            Пример ответа:
            {
                "server": "api11.ilovepdf.com",
                "task": "g27d4mrsg3ztmnzAgm5d..."
                "remaining_credits": 1234
            }
        """
        url = f"{self.api.base_url}/start/{tool}"

        response = await httpx_get(url)
        json = response.json()

        return json
