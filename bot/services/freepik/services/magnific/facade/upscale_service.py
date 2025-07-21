

import asyncio

from bot.services.freepik.services.magnific.client.base_service import (
    MagnificBaseService,
)
from bot.services.freepik.services.magnific.services.status_service import (
    MagnificStatusService,
)
from bot.services.freepik.services.magnific.services.upscaler import (
    MagnificUpscaler,
)


class MagnificUpscaleService(MagnificBaseService):
    """
    Фасадный сервис для работы с upscale Magnific.
    """
    def __init__(
        self,
        upscaler: MagnificUpscaler,
        status_service: MagnificStatusService,
    ) -> None:
        """
        Args:
            upscaler (MagnificUpscaler): Сервис upscale.
            status_service (MagnificGetStatus): Сервис получения статуса.
        """
        self.upscaler = upscaler
        self.status_service = status_service

    async def upscale(self, image: str) -> str:
        """
        Upscale изображение с помощью Magnific.

        Args:
            image (str): Base64-encoded изображение.

        Returns:
            str: URL upscale изображения.
        """
        task_id = await self.upscaler.upscale(image)

        while True:
            response = await self.status_service.get_status(task_id)

            if response["status"] == "COMPLETED":
                return response["generated"][0]

            if response["status"] == "FAILED":
                raise RuntimeError("Не получилось реализовать Magnific Upscale изображения!")

            await asyncio.sleep(10)
