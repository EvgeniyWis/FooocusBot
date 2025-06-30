import os

import aiofiles

from bot.services.comfyui.api_client import ComfyUIAPI


class ComfyUIUploader:
    def __init__(self, api: ComfyUIAPI):
        self.api = api

    async def upload_image(self, image_path: str) -> str:
        filename = os.path.basename(image_path)
        async with aiofiles.open(image_path, "rb") as f:
            content = await f.read()
        result = await self.api.post(
            "/upload/image", files={"image": (filename, content, "image/jpeg")}
        )
        return result["name"]
