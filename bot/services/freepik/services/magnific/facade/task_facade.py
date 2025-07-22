import asyncio

from bot.logger import logger
from bot.services.freepik.services.magnific.client.base_service import (
    MagnificBaseService,
)
from bot.services.freepik.services.magnific.services.status_service import (
    MagnificStatusService,
)
from bot.services.freepik.services.magnific.services.upscaler import (
    MagnificUpscaler,
)
from bot.services.freepik.services.magnific.utils.logger import (
    log_magnific_step,
)


class MagnificTaskFacade(MagnificBaseService):
    """
    Универсальный фасад для работы с задачами Magnific (upscale).
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

    @log_magnific_step("upscale_image")
    async def upscale_image(self, image: str) -> str:
        """
        Upscale изображение с помощью Magnific.
        Args:
            image (str): Base64-encoded изображение.
        Returns:
            str: URL upscale изображения.
        """
        task = await self.upscaler.upscale(image)
        task_id = task.get('task_id')
        if not task_id:
            raise RuntimeError(f"Не получен task_id от Magnific: {task}")
        return await self._wait_for_completion(task_id)

    async def _wait_for_completion(self, task_id: str, poll_interval: int = 10) -> str:
        """
        Ожидание завершения задачи по task_id.
        Returns:
            str: URL результата.
        """
        while True:
            response = await self.status_service.get_status(task_id)
            logger.info(f"[Magnific] Статус задачи {task_id}: {response}")
            if response.get("status") == "COMPLETED":
                generated = response.get("generated")
                if not generated:
                    raise RuntimeError(f"Magnific: нет результата в ответе: {response}")
                return generated[0]
            if response.get("status") == "FAILED":
                raise RuntimeError(f"Magnific: задача завершилась с ошибкой: {response}")
            await asyncio.sleep(poll_interval)
