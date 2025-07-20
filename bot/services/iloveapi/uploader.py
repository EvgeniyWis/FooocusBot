from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI
from bot.utils.httpx import httpx_post


class ILoveAPIUploader:
    def __init__(self, api: ILoveAPI):
        self.api = api
        logger.info("Инициализирован загрузчик ILoveAPI")

    async def upload(self, server: str, task_id: str, file: str) -> str:
        """
        Загрузка файла в ILoveAPI

        Args:
            server (str): Сервер (получается из ответа стартера)
            task_id (str): ID задачи (получается из ответа стартера)
            file (str): Путь к файлу

        Returns:
            str: Имя файла на сервере
        """
        url = f"https://{server}/v1/upload"

        data = {
            "task": task_id,
            "file": file,
        }

        response = await httpx_post(url, data=data)
        json = response.json()
        server_filename = json["server_filename"]

        return server_filename

