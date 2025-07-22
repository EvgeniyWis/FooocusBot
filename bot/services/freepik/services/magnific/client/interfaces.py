from typing import Protocol

from bot.services.freepik.services.magnific.client.types import (
    MagnificStatusResponse,
    MagnificTaskResponse,
)


class StatusServiceProtocol(Protocol):
    """
    Протокол для обработки статуса задачи с помощью Magnific.
    Пример:
        class MyStatusService:
            async def get_status(self, task_id: str) -> dict:
                ...
    """
    async def get_status(self, task_id: str) -> MagnificStatusResponse:
        ...

class UpscalerProtocol(Protocol):
    """
    Протокол upscale изображения с помощью Magnific.
    """
    async def upscale(
        self,
        image: str,
        optimized_for: str = ...,
        creativity: int = ...,
        hdr: int = ...,
        resemblance: int = ...,
        fractality: int = ...,
        engine: str = ...,
    ) -> MagnificTaskResponse:
        ...

class MagnificTaskFacadeProtocol(Protocol):
    async def upscale_image(self, image: str) -> str:
        ...
