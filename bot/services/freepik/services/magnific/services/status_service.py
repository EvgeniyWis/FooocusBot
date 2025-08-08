from bot.app.core.logging import logger
from bot.services.freepik.services.magnific.client.base_service import (
    BaseService,
)
from bot.services.freepik.services.magnific.client.exceptions import (
    MagnificAPIError,
)
from bot.services.freepik.services.magnific.interfaces.protocols import (
    StatusServiceProtocol,
)
from bot.services.freepik.services.magnific.types.responses import (
    MagnificStatusResponse,
)
from bot.services.freepik.services.magnific.utils.validation import (
    ValidationMixin,
)


class StatusService(BaseService, StatusServiceProtocol, ValidationMixin):
    """
    Сервис для обработки статуса задачи с помощью Magnific.
    """

    async def get_status(self, task_id: str) -> MagnificStatusResponse:
        """
        Получает статус задачи с помощью Magnific.

        Args:
            task_id (str): ID задачи.

        Returns:
            dict: Ответ сервера.

            Пример ответа:
            {
                "generated": [
                "https://ai-statics.freepik.com/completed_task_image.jpg"
                ],
                "task_id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
                "status": "COMPLETED"
            }
        """
        self.validate_task_id(task_id)
        try:
            logger.info(f"[MagnificStatusService] Получение статуса для task_id={task_id}")
            url = f"/{task_id}"
            response = await self.api.get(
                url,
            )
            data = response["data"]
            logger.info(f"[MagnificStatusService] Ответ: {data}")
            if not isinstance(data, dict) or "status" not in data:
                raise MagnificAPIError(f"Некорректный ответ от Magnific: {data}")
            return data
        except MagnificAPIError:
            raise
        except Exception as e:
            logger.error(f"[MagnificStatusService] Ошибка получения статуса: {e}")
            raise MagnificAPIError(str(e))
