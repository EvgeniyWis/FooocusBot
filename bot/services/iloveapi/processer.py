from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.types import FileFormat, ToolType
from bot.utils.httpx import httpx_post


class ILoveAPIProcesser:
    def __init__(self, api: ILoveAPI):
        self.api = api
        logger.info("Инициализирован обработчик ILoveAPI")

    async def process(self, server: str, task_id: str, tool: ToolType, files: list[FileFormat]) -> str:
        """
        Обработка файлов в ILoveAPI

        Args:
            server (str): Сервер (получается из ответа стартера)
            task_id (str): ID задачи (получается из ответа стартера)
            tool (ToolType): Тип инструмента
            files (list[FileFormat]): Список файлов

        Returns:
            str: Имя файла на сервере
        """
        url = f"https://{server}/v1/process"

        data = {
            "task": task_id,
            "tool": tool,
            "files": files,
        }

        response = await httpx_post(url, data=data)
        json = response.json()

        return json

