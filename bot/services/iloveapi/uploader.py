from bot.logger import logger
from bot.services.iloveapi.base_service import ILoveAPIBaseService
from bot.services.iloveapi.types import UploadResponse

from .interfaces import UploaderProtocol


class ILoveAPIUploader(ILoveAPIBaseService, UploaderProtocol):
    """
    Сервис для загрузки файлов в ILoveAPI.
    """
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
        response: UploadResponse = await self.api.post(
            url,
            data=data,
            with_base_url=False,
        )
        server_filename: str = response["server_filename"]
        return server_filename

