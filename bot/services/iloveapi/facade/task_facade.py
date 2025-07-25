import httpx

from bot.logger import logger
from bot.services.iloveapi.adapters.base_adapter import ILoveAPIBaseService
from bot.services.iloveapi.client.api_client import ILoveAPI
from bot.services.iloveapi.client.interfaces import (
    DownloaderProtocol,
    ProcessorProtocol,
    StarterProtocol,
    UploaderProtocol,
)
from bot.services.iloveapi.types.start_task_response import StartTaskResponse
from bot.services.iloveapi.types.tool_type import ToolType
from bot.services.iloveapi.utils.validation import (
    validate_file_format,
)


class TaskFacade(ILoveAPIBaseService):
    """
    Базовый фасад для работы с тасками ILoveAPI (создание, загрузка, обработка, скачивание результата).
    """
    def __init__(
        self,
        api: ILoveAPI,
        starter: StarterProtocol,
        uploader: UploaderProtocol,
        processor: ProcessorProtocol,
        downloader: DownloaderProtocol,
    ) -> None:
        super().__init__(api)
        self.starter = starter
        self.uploader = uploader
        self.processor = processor
        self.downloader = downloader

    async def run_image_task(
        self,
        tool: ToolType,
        filename: str,
        tool_data,
        uploader_method,
    ) -> httpx.Response:
        """
        Универсальный метод для запуска задачи обработки изображения в ILoveAPI.
        """
        task_json: StartTaskResponse = await self.starter.start_task(tool)
        logger.info(f"Задача запущена: {task_json}")
        server = task_json["server"]
        task_id = task_json["task"]
        logger.info(f"Сервер: {server}, ID задачи: {task_id}")

        server_filename: str = await uploader_method(server, task_id, filename)
        logger.info(f"Файл загружен: {server_filename}")

        files = [{"server_filename": server_filename, "filename": filename}]
        for f in files:
            validate_file_format(f)
        logger.info(f"Файлы для обработки: {files} и {tool_data}")
        await self.processor.process(server, task_id, tool, files, tool_data)
        logger.info("Обработка завершена успешно!")

        result = await self.downloader.download(server, task_id)
        logger.info(f"Файл выгружен: {result}")
        return result
