from bot.services.iloveapi.adapters.base_adapter import ILoveAPIBaseService
from bot.services.iloveapi.client.interfaces import StarterProtocol
from bot.services.iloveapi.types.start_task_response import StartTaskResponse
from bot.services.iloveapi.types.tool_type import ToolType


class Starter(ILoveAPIBaseService, StarterProtocol):
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
