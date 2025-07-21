from bot.logger import logger
from bot.services.freepik.magnific.api_client import MagnificAPI


class MagnificGetStatus:
    """
    Сервис для получения статуса задачи с помощью Magnific.
    """
    def __init__(self, api: MagnificAPI) -> None:
        """
        Args:
            api (MagnificAPI): Экземпляр клиента Magnific.
        """
        self.api = api
        logger.info("Инициализирован получатель статуса Magnific")

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
                    "https://openapi-generator.tech",
                    "https://openapi-generator.tech"
                ],
                "task_id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
                "status": "IN_PROGRESS"
            }
        """

        response = await self.api.get(
            f"{self.api.base_url}/{task_id}",
        )
        return response

