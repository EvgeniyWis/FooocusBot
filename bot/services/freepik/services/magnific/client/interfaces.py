from typing import Protocol


class StatusServiceProtocol(Protocol):
    """
    Протокол для обработки статуса задачи с помощью Magnific.
    Пример:
        class MyStatusService:
            async def get_status(self, task_id: str) -> dict:
                ...
    """
    async def get_status(self, task_id: str) -> dict:
        ...

class UpscalerProtocol(Protocol):
    """
    Протокол upscale изображения с помощью Magnific.
    Пример:
        class MyUpscaler:
            async def upscale(self, image: str) -> dict:
                ...
    """
    async def upscale(self, image: str) -> dict:
        ...
