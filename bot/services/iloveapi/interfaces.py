from typing import Any, Dict, List, Protocol

import httpx

from .types import (
    FileFormat,
    StartTaskResponse,
    ToolType,
)


class UploaderProtocol(Protocol):
    """
    Протокол загрузчика файлов для ILoveAPI.
    Пример:
        class MyUploader:
            async def upload(self, server: str, task_id: str, cloud_file: str) -> str:
                ...
    """
    async def upload(self, server: str, task_id: str, cloud_file: str) -> str:
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

class ProcesserProtocol(Protocol):
    """
    Протокол процессора задач для ILoveAPI.
    Пример:
        class MyProcesser:
            async def process(self, server: str, task_id: str, tool: ToolType, files: List[FileFormat], tool_data: Dict[str, Any]) -> Dict[str, Any]:
                ...
    """
    async def process(
        self,
        server: str,
        task_id: str,
        tool: ToolType,
        files: List[FileFormat],
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
