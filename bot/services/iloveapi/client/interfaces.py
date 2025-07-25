from typing import Any, Dict, List, Protocol

import httpx

from bot.services.iloveapi.types.start_task_response import StartTaskResponse
from bot.services.iloveapi.types.task_file_format import TaskFileFormat
from bot.services.iloveapi.types.tool_type import ToolType


class UploaderProtocol(Protocol):
    """
    Протокол загрузчика файлов для ILoveAPI.
    Пример:
        class MyUploader:
            async def upload_file(self, server: str, task_id: str, file: str) -> str:
                ...

            async def upload_cloud_file(self, server: str, task_id: str, cloud_file: str) -> str:
                ...
    """
    async def upload_file(self, server: str, task_id: str, file: str) -> str:
        ...

    async def upload_cloud_file(self, server: str, task_id: str, cloud_file: str) -> str:
        ...

class DownloaderProtocol(Protocol):
    """
    Протокол скачивателя файлов для ILoveAPI.
    Пример:
        class MyDownloader:
            async def download(self, server: str, task_id: str) -> str:
                ...
    """
    async def download(self, server: str, task_id: str) -> httpx.Response:
        ...

class ProcessorProtocol(Protocol):
    """
    Протокол процессора задач для ILoveAPI.
    Пример:
        class MyProcessor:
            async def process(self, server: str, task_id: str, tool: ToolType, files: List[TaskFileFormat], tool_data: Dict[str, Any]) -> Dict[str, Any]:
                ...
    """
    async def process(
        self,
        server: str,
        task_id: str,
        tool: ToolType,
        files: List[TaskFileFormat],
        tool_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        ...

class StarterProtocol(Protocol):
    """
    Протокол стартера задач для ILoveAPI.
    Пример:
        class MyStarter:
            async def start_task(self, tool: ToolType) -> Dict[str, Any]:
                ...
    """
    async def start_task(self, tool: ToolType) -> StartTaskResponse:
        ...


class ResizerProtocol(Protocol):
    """
    Протокол ресайзера изображений для ILoveAPI.
    Пример:
        class MyResizer:
            async def resize_image(self, file: str, width: int, height: int | str) -> httpx.Response:
                ...
    """
    async def resize_image_file(self, file: str, width: int, height: int | str) -> httpx.Response:
        ...

    async def resize_image_cloud_file(self, cloud_file: str, width: int, height: int | str) -> httpx.Response:
        ...

class UpscalerProtocol(Protocol):
    """
    Протокол ускользателя изображений для ILoveAPI.
    Пример:
        class MyUpscaler:
            async def upscale_image(self, file: str, multiplier: int) -> httpx.Response:
                ...
    """
    async def upscale_image_file(self, file: str, multiplier: int) -> httpx.Response:
        ...

    async def upscale_image_cloud_file(self, cloud_file: str, multiplier: int) -> httpx.Response:
        ...