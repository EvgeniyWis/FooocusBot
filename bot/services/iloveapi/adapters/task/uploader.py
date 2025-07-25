from typing import Dict

from bot.logger import logger
from bot.services.iloveapi.adapters.base_adapter import ILoveAPIBaseService
from bot.services.iloveapi.client.interfaces import UploaderProtocol
from bot.services.iloveapi.types.upload_response import UploadResponse


class Uploader(ILoveAPIBaseService, UploaderProtocol):
    """
    Сервис для загрузки файлов в ILoveAPI.
    """
    async def _upload(self, server: str, task_id: str, file: str | None = None, 
    cloud_file: str | None = None) -> str:
        """
        Внутренний метод для загрузки файла в ILoveAPI.
        """
        url = f"https://{server}/v1/upload"

        files = None
        if file:
            data = {"task": task_id}
            files = {'file': open(file, 'rb')}
        elif cloud_file:
            data = {"task": task_id, "cloud_file": cloud_file}
            logger.info(f"Загружаем файл {cloud_file} в ILoveAPI: {data}")

        response: UploadResponse = await self.api.post(
            url,
            data=data,
            with_base_url=False,
            files=files,
        )
        server_filename: str = response["server_filename"]
        return server_filename

    async def upload_file(self, server: str, task_id: str, file: str) -> str:
        """
        Загружает локальный файл в ILoveAPI.

        Args:
            server (str): Сервер (получается из ответа стартера).
            task_id (str): ID задачи (получается из ответа стартера).
            file (str): Путь к локальному файлу.

        Returns:
            str: Имя файла на сервере.
        """
        logger.info(f"Загружаем локальный файл {file} в ILoveAPI")
        return await self._upload(server, task_id, file=file)

    async def upload_cloud_file(self, server: str, task_id: str, cloud_file: str) -> str:
        """
        Загружает файл из облака в ILoveAPI.

        Args:
            server (str): Сервер (получается из ответа стартера).
            task_id (str): ID задачи (получается из ответа стартера).
            cloud_file (str): Путь к файлу в облаке.

        Returns:
            str: Имя файла на сервере.
        """
        logger.info(f"Загружаем файл из облака {cloud_file} в ILoveAPI")
        return await self._upload(server, task_id, cloud_file=cloud_file)

