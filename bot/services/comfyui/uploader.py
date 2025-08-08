import os

import aiofiles

from bot.app.core.logging import logger
from bot.services.comfyui.api_client import ComfyUIAPI


class ComfyUIUploader:
    def __init__(self, api: ComfyUIAPI):
        self.api = api
        logger.info("Инициализирован загрузчик ComfyUI")

    async def upload_image(self, image_path: str) -> str:
        filename = os.path.basename(image_path)
        logger.info(f"Начало загрузки изображения: {filename}")

        try:
            async with aiofiles.open(image_path, "rb") as f:
                content = await f.read()

            logger.info(f"Прочитано {len(content)} байт из файла {filename}")
            result = await self.api.post(
                "/upload/image",
                files={"image": (filename, content, "image/jpeg")},
            )

            logger.info(
                f"Изображение {filename} успешно загружено, присвоено имя: {result['name']}",
            )
            return result["name"]

        except Exception as e:
            logger.error(
                f"Ошибка при загрузке изображения {filename}: {str(e)}",
            )
            raise
