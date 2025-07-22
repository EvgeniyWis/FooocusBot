from bot.logger import logger
from bot.services.freepik.services.magnific.client.base_service import (
    MagnificBaseService,
)
from bot.services.freepik.services.magnific.client.exceptions import (
    MagnificAPIError,
)
from bot.services.freepik.services.magnific.client.interfaces import (
    StatusServiceProtocol,
)
from bot.services.freepik.services.magnific.client.types import (
    MagnificStatusResponse,
)
from bot.services.freepik.services.magnific.utils.validation import (
    validate_task_id,
)


class MagnificStatusService(MagnificBaseService, StatusServiceProtocol):
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
        validate_task_id(task_id)
        try:
            logger.info(f"[MagnificStatusService] Получение статуса для task_id={task_id}")
            response = await self.api.get(
                f"{self.api.base_url}/{task_id}",
            )
            logger.info(f"[MagnificStatusService] Ответ: {response}")
            return response
        except Exception as e:
            logger.error(f"[MagnificStatusService] Ошибка получения статуса: {e}")
            raise MagnificAPIError(str(e))
