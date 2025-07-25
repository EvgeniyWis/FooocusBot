from bot.services.iloveapi.adapters.base_adapter import ILoveAPIBaseService
from bot.services.iloveapi.client.interfaces import DownloaderProtocol


class Downloader(ILoveAPIBaseService, DownloaderProtocol):
    """
    Сервис для загрузки файлов из ILoveAPI.
    """

    async def download(self, server: str, task_id: str) -> str:
        """
        Выгружает файл из ILoveAPI.

        Args:
            server (str): Сервер (получается из ответа стартера).
            task_id (str): ID задачи (получается из ответа стартера).

        Returns:
            ArrayBuffer: Содержимое файла.
        """
        url = f"https://{server}/v1/download/{task_id}"
        response = await self.api.get(url, with_base_url=False)
        return response

