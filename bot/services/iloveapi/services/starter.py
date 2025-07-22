from bot.services.iloveapi.client.base_service import ILoveAPIBaseService
from bot.services.iloveapi.client.types import StartTaskResponse, ToolType

from ..client.interfaces import StarterProtocol


class ILoveAPIStarter(ILoveAPIBaseService, StarterProtocol):
    """
    Сервис для старта задач в ILoveAPI.
    """
    async def start_task(self, tool: ToolType) -> StartTaskResponse:
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
        url = f"/start/{tool}"
        response: StartTaskResponse = await self.api.get(url)
        return response
