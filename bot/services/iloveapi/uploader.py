from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI

from .interfaces import UploaderProtocol


class ILoveAPIUploader(UploaderProtocol):
    """
    Сервис для загрузки файлов в ILoveAPI.
    """
    def __init__(self, api: ILoveAPI) -> None:
        """
        Args:
            api (ILoveAPI): Экземпляр клиента ILoveAPI.
        """
        self.api = api
        logger.info("Инициализирован загрузчик ILoveAPI")

    async def upload(self, server: str, task_id: str, cloud_file: str) -> str:
        """
        Загружает файл в ILoveAPI.

        Args:
            server (str): Сервер (получается из ответа стартера).
            task_id (str): ID задачи (получается из ответа стартера).
            cloud_file (str): Путь к файлу.

        Returns:
            str: Имя файла на сервере.
        """
        url = f"https://{server}/v1/upload"
        data = {"task": task_id, "cloud_file": cloud_file}
        logger.info(f"Загружаем файл {cloud_file} в ILoveAPI")
        response = await self.api.iloveapi_post(
            url,
            data=data,
            with_base_url=False,
        )
        server_filename: str = response["server_filename"]
        return server_filename

