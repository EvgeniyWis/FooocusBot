from bot.logger import logger
from bot.services.freepik.services.magnific.client.base_service import (
    BaseService,
)
from bot.services.freepik.services.magnific.client.exceptions import (
    MagnificAPIError,
)
from bot.services.freepik.services.magnific.interfaces.protocols import (
    UpscalerProtocol,
)
from bot.services.freepik.services.magnific.types.responses import (
    MagnificTaskResponse,
)


class UpscalerService(BaseService, UpscalerProtocol):
    """
    Сервис для upscale изображений с помощью Magnific.
    """
    async def upscale(
        self,
        image: str,
        optimized_for: str = "standard",
        creativity: int = -8,
        hdr: int = 8,
        resemblance: int = -10,
        fractality: int = 6,
        engine: str = "magnific_sharpy",
    ) -> MagnificTaskResponse:
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
        self.validate_base64_image(image)
        json = {
            "image": image,
            "optimized_for": optimized_for,
            "creativity": creativity,
            "hdr": hdr,
            "resemblance": resemblance,
            "fractality": fractality,
            "engine": engine,
        }
        headers = {
            "Content-Type": "application/json",
        }
        try:
            logger.info("[MagnificUpscaler] Отправка изображения на upscale")
            response = await self.api.post(
                self.api.base_url,
                json=json,
                headers=headers,
            )
            logger.info(f"[MagnificUpscaler] Ответ: {response}")
            if not isinstance(response, dict) or "task_id" not in response:
                raise MagnificAPIError(f"Некорректный ответ от Magnific: {response}")
            return response
        except MagnificAPIError:
            raise
        except Exception as e:
            logger.error(f"[MagnificUpscaler] Ошибка upscale: {e}")
            raise MagnificAPIError(str(e))

