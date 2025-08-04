import asyncio

from bot.logger import logger
from bot.services.freepik.services.magnific.client.api_client import (
    MagnificAPI,
)
from bot.services.freepik.services.magnific.client.base_service import (
    BaseService,
)
from bot.services.freepik.services.magnific.client.exceptions import (
    MagnificAPIError,
)
from bot.services.freepik.services.magnific.interfaces.protocols import (
    MagnificTaskFacadeProtocol,
)
from bot.services.freepik.services.magnific.services.status_service import (
    StatusService,
)
from bot.services.freepik.services.magnific.services.upscaler import (
    UpscalerService,
)
from bot.services.freepik.services.magnific.types.responses import (
    MagnificStatusResponse,
    MagnificTaskResponse,
)
from bot.services.freepik.services.magnific.utils.logger import (
    log_magnific_step,
)


class TaskFacade(BaseService, MagnificTaskFacadeProtocol):
    """
    Универсальный фасад для работы с задачами Magnific (upscale).
    """
    def __init__(
        self,
        api: MagnificAPI,
        upscaler: UpscalerService,
        status_service: StatusService,
    ) -> None:
        """
        Args:
            api (MagnificAPI): API клиент.
            upscaler (UpscalerService): Сервис upscale.
            status_service (StatusService): Сервис получения статуса.
        """
        super().__init__(api)
        self.upscaler = upscaler
        self.status_service = status_service

    @log_magnific_step("upscale_image")
    async def upscale_image(
        self,
        image: str,
        optimized_for: str,
        creativity: int,
        hdr: int,
        resemblance: int,
        fractality: int,
        engine: str,
        scale_factor: str,
    ) -> str:
        """
        Upscale изображение с помощью Magnific.
        Args:
            image (str): Base64-encoded изображение.
            группы апскейла:
            optimized_for (str): Оптимизация для.
            creativity (int): Креативность.
            hdr (int): HDR.
            resemblance (int): Сходство.
            fractality (int): Фрактальность.
            engine (str): Движок.
            scale_factor (str): Масштаб.
        Returns:
            str: URL upscale изображения.
        """
        task: MagnificTaskResponse = await self.upscaler.upscale(
            image,
            optimized_for=optimized_for,
            creativity=creativity,
            hdr=hdr,
            resemblance=resemblance,
            fractality=fractality,
            engine=engine,
            scale_factor=scale_factor,
        )
        task_id = task.get("task_id")
        if not task_id:
            raise MagnificAPIError(f"Не получен task_id от Magnific: {task}")
        return await self._wait_for_completion(task_id)

    async def _wait_for_completion(self, task_id: str, poll_interval: int = 10) -> str:
        """
        Ожидание завершения задачи по task_id.
        Returns:
            str: URL результата.
        """
        while True:
            response: MagnificStatusResponse = await self.status_service.get_status(task_id)
            logger.info(f"[Magnific] Статус задачи {task_id}: {response}")
            if response["status"] == "COMPLETED":
                generated = response["generated"]
                if not generated:
                    raise MagnificAPIError(f"Magnific: нет результата в ответе: {response}")
                return generated[0]
            if response["status"] == "FAILED":
                raise MagnificAPIError(f"Magnific: задача завершилась с ошибкой: {response}")
            await asyncio.sleep(poll_interval)
