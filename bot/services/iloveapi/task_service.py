from typing import Any, Dict

from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.processer import ILoveAPIProcesser
from bot.services.iloveapi.starter import ILoveAPIStarter
from bot.services.iloveapi.types import ToolType
from bot.services.iloveapi.uploader import ILoveAPIUploader


class ILoveAPITaskService:
    """
    Фасадный сервис для работы с задачами ILoveAPI (запуск, загрузка, обработка).
    """
    def __init__(
        self,
        api: ILoveAPI,
        starter: ILoveAPIStarter,
        uploader: ILoveAPIUploader,
        processer: ILoveAPIProcesser,
    ) -> None:
        """
        Args:
            api (ILoveAPI): Экземпляр клиента ILoveAPI.
            starter (ILoveAPIStarter): Сервис старта задач.
            uploader (ILoveAPIUploader): Сервис загрузки файлов.
            processer (ILoveAPIProcesser): Сервис обработки файлов.
        """
        self.api = api
        self.starter = starter
        self.uploader = uploader
        self.processer = processer

    async def run_image_task(
        self,
        tool: ToolType,
        file_path: str,
        tool_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Запускает задачу обработки изображения в ILoveAPI.

        Args:
            tool (ToolType): Тип инструмента.
            file_path (str): Путь к файлу.
            tool_data (dict): Дополнительные параметры инструмента.

        Returns:
            dict: Результат обработки.
        """
        task_json = await self.starter.start_task(tool)
        server = task_json["server"]
        task_id = task_json["task"]
        server_filename = await self.uploader.upload(server, task_id, file_path)
        files = [{"server_filename": server_filename, "filename": file_path}]
        result = await self.processer.process(server, task_id, tool, files, tool_data)
        return result

    async def resize_image(
        self,
        file_path: str,
        width: int,
        height: int,
    ) -> Dict[str, Any]:
        """
        Обёртка для задачи изменения размера изображения.

        Args:
            file_path (str): Путь к файлу.
            width (int): Новая ширина.
            height (int): Новая высота.

        Returns:
            dict: Результат обработки.
        """
        return await self.run_image_task(
            ToolType.RESIZE_IMAGE,
            file_path,
            {"pixels_width": width, "pixels_height": height}
        )