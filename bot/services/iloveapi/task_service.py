from typing import Any, Dict

from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.types import ToolType

from .interfaces import (
    DownloaderProtocol,
    ProcesserProtocol,
    StarterProtocol,
    UploaderProtocol,
)


class ILoveAPITaskService:
    """
    Фасадный сервис для работы с задачами ILoveAPI (запуск, загрузка, обработка).
    """
    def __init__(
        self,
        api: ILoveAPI,
        starter: StarterProtocol,
        uploader: UploaderProtocol,
        processer: ProcesserProtocol,
        downloader: DownloaderProtocol,
    ) -> None:
        """
        Args:
            api (ILoveAPI): Экземпляр клиента ILoveAPI.
            starter (StarterProtocol): Сервис старта задач.
            uploader (UploaderProtocol): Сервис загрузки файлов.
            processer (ProcesserProtocol): Сервис обработки файлов.
            downloader (DownloaderProtocol): Сервис загрузки файлов.
        """
        self.api = api
        self.starter = starter
        self.uploader = uploader
        self.processer = processer
        self.downloader = downloader

    async def run_image_task(
        self,
        tool: ToolType,
        file: str,
        tool_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Запускает задачу обработки изображения в ILoveAPI.

        Args:
            tool (ToolType): Тип инструмента.
            file (str): Путь к файлу.
            tool_data (dict): Дополнительные параметры инструмента.

        Returns:
            dict: Результат обработки.
        """
        task_json = await self.starter.start_task(tool)
        logger.info(f"Задача запущена: {task_json}")
        server = task_json["server"]
        task_id = task_json["task"]
        logger.info(f"Сервер: {server}, ID задачи: {task_id}")

        server_filename = await self.uploader.upload(server, task_id, file)
        logger.info(f"Файл загружен: {server_filename}")

        files = [{"server_filename": server_filename, "filename": file}]
        logger.info(f"Файлы для обработки: {files} и {tool_data}")
        await self.processer.process(server, task_id, tool, files, tool_data)
        logger.info("Обработка завершена успешно!")

        result = await self.downloader.download(server, task_id)
        logger.info(f"Файл выгружен: {result}")
        return result

    async def resize_image(
        self,
        file: str,
        width: int,
        height: int,
    ) -> Dict[str, Any]:
        """
        Обёртка для задачи изменения размера изображения.

        Args:
            file (str): Путь к файлу.
            width (int): Новая ширина.
            height (int): Новая высота.

        Returns:
            dict: Результат обработки.
        """
        tool_data = {
            "pixels_width": width,
            "pixels_height": height,
            "maintain_ratio": True,
        }
        return await self.run_image_task(
            "resizeimage",
            file,
            tool_data
        )