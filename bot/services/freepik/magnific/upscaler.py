from bot.logger import logger
from bot.services.freepik.magnific.api_client import MagnificAPI


class MagnificUpscaler:
    """
    Сервис для upscale изображений с помощью Magnific.
    """
    def __init__(self, api: MagnificAPI) -> None:
        """
        Args:
            api (MagnificAPI): Экземпляр клиента Magnific.
        """
        self.api = api
        logger.info("Инициализирован Magnific Upscaler")

    async def upscale(self, image: str) -> dict:
        """
        Upscale изображение с помощью Magnific.

        Args:
            image (str): Base64-encoded изображение.

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
        json = {
            "image": image,
            "optimized_for": "standard",
            "creativity": -8,
            "hdr": 8,
            "resemblance": -10,
            "fractality": 6,
            "engine": "magnific_sharpy",
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = await self.api.post(
            self.api.base_url,
            json=json,
            headers=headers,
        )
        return response

