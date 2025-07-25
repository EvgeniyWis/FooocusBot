import httpx

from bot.services.iloveapi.facade.task_facade import TaskFacade
from bot.services.iloveapi.types.upscale_image import (
    ToolDataUpscaleImage,
    UpscaleMultiplier,
)


class UpscaleImageService:
    def __init__(self, task_facade: TaskFacade):
        self.task_facade = task_facade

    def _make_tool_data(self, multiplier: UpscaleMultiplier) -> ToolDataUpscaleImage:
        return {"multiplier": multiplier}

    async def upscale_image_file(self, file: str, multiplier: UpscaleMultiplier) -> httpx.Response:
        tool_data = self._make_tool_data(multiplier)
        return await self.task_facade.run_image_task(
            tool="upscaleimage",
            filename=file,
            tool_data=tool_data,
            uploader_method=self.task_facade.uploader.upload_file,
        )

    async def upscale_image_cloud_file(self, cloud_file: str, multiplier: UpscaleMultiplier) -> httpx.Response:
        tool_data = self._make_tool_data(multiplier)
        return await self.task_facade.run_image_task(
            tool="upscaleimage",
            filename=cloud_file,
            tool_data=tool_data,
            uploader_method=self.task_facade.uploader.upload_cloud_file,
        ) 