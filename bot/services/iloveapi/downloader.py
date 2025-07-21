from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI


class ILoveAPIDownloader:
    """
    Сервис для загрузки файлов из ILoveAPI.
    """
    def __init__(self, api: ILoveAPI) -> None:
        """
        Args:
            api (ILoveAPI): Экземпляр клиента ILoveAPI.
        """
        self.api = api
        logger.info("Инициализирован выгрузчик ILoveAPI")

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
        response = await self.api.iloveapi_get(url, with_base_url=False)
        return response

