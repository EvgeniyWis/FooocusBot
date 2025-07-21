from typing import Any, Dict

from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.types import ToolType
from bot.utils.httpx import httpx_get


class ILoveAPIStarter:
    """
    Сервис для старта задач в ILoveAPI.
    """
    def __init__(self, api: ILoveAPI) -> None:
        """
        Args:
            api (ILoveAPI): Экземпляр клиента ILoveAPI.
        """
        self.api = api
        logger.info("Инициализирован стартер ILoveAPI")

    async def start_task(self, tool: ToolType) -> Dict[str, Any]:
        """
        Стартер задач в ILoveAPI.

        Args:
            tool (ToolType): Тип инструмента.

        Returns:
            dict: JSON ответ.

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
