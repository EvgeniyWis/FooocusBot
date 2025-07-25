import httpx

from bot.services.iloveapi.client.interfaces import ResizerProtocol
from bot.services.iloveapi.facade.task_facade import TaskFacade
from bot.services.iloveapi.types.resize_image import ToolDataResizeImage


class ResizeImageService(ResizerProtocol):
    def __init__(self, task_facade: TaskFacade):
        self.task_facade = task_facade

    def _make_tool_data(self, width: int, height: int | str) -> ToolDataResizeImage:
        return {
            "pixels_width": width,
            "pixels_height": height,
            "maintain_ratio": True,
        }

    async def resize_image_file(self, file: str, width: int, height: int | str) -> httpx.Response:
        tool_data = self._make_tool_data(width, height)
        return await self.task_facade.run_image_task(
            tool="resizeimage",
            filename=file,
            tool_data=tool_data,
            uploader_method=self.task_facade.uploader.upload_file,
        )

    async def resize_image_cloud_file(self, cloud_file: str, width: int, height: int | str) -> httpx.Response:
        tool_data = self._make_tool_data(width, height)
        return await self.task_facade.run_image_task(
            tool="resizeimage",
            filename=cloud_file,
            tool_data=tool_data,
            uploader_method=self.task_facade.uploader.upload_cloud_file,
        ) 