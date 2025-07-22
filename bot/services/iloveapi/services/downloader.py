from bot.services.iloveapi.client.base_service import ILoveAPIBaseService

from ..client.interfaces import DownloaderProtocol


class ILoveAPIDownloader(ILoveAPIBaseService, DownloaderProtocol):
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

