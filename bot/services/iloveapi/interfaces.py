from typing import Any, Dict, List, Protocol

from .types import FileFormat, ToolType


class UploaderProtocol(Protocol):
    async def upload(self, server: str, task_id: str, cloud_file: str) -> str:
        ...

class DownloaderProtocol(Protocol):
    async def download(self, server: str, task_id: str) -> str:
        ...

class ProcesserProtocol(Protocol):
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
    async def start_task(self, tool: ToolType) -> Dict[str, Any]:
        ...
