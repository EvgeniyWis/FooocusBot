from typing import Any, Dict, List

from bot.logger import logger
from bot.services.iloveapi.client.base_service import ILoveAPIBaseService
from bot.services.iloveapi.client.interfaces import ProcessorProtocol
from bot.services.iloveapi.types.task_file_format import TaskFileFormat
from bot.services.iloveapi.types.tool_type import ToolType


class ILoveAPIProcessor(ILoveAPIBaseService, ProcessorProtocol):
    """
    Сервис для запуска обработки файлов в ILoveAPI.
    """
    async def process(
        self,
        server: str,
        task_id: str,
        tool: ToolType,
        files: List[TaskFileFormat],
        tool_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Обработка файлов в ILoveAPI.

        Args:
            server (str): Сервер (получается из ответа стартера).
            task_id (str): ID задачи (получается из ответа стартера).
            tool (ToolType): Тип инструмента.
            files (list[TaskFileFormat]): Список файлов.
            tool_data (dict): Дополнительные параметры инструмента.

        Returns:
            dict: JSON ответ.
        """
        url = f"https://{server}/v1/process"
        json = {"task": task_id, "tool": tool, "files": files, **tool_data}
        logger.info(f"Отправляем данные для обработки: {json}")
        response = await self.api.post(url, json=json, with_base_url=False)
        return response

