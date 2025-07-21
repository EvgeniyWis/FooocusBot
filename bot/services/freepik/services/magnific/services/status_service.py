from bot.services.freepik.services.magnific.client.base_service import (
    MagnificBaseService,
)


class MagnificStatusService(MagnificBaseService):
    """
    Сервис для обработки статуса задачи с помощью Magnific.
    """

    async def get_status(self, task_id: str) -> dict:
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

        response = await self.api.get(
            f"{self.api.base_url}/{task_id}",
        )

        return response
