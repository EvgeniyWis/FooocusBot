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
from bot.services.freepik.services.magnific.utils.validation import (
    ValidationMixin,
)


class UpscalerService(BaseService, UpscalerProtocol, ValidationMixin):
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
        scale_factor: str = "2x",
    ) -> MagnificTaskResponse:
        """
        Upscale изображение с помощью Magnific.

        Args:
            image (str): Base64-encoded изображение.
            группы upscale:
            optimized_for (str): Оптимизация для.
            creativity (int): Креативность.
            hdr (int): HDR.
            resemblance (int): Сходство.
            fractality (int): Фрактальность.
            engine (str): Движок.
            scale_factor (str): Масштаб.

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
            "scale_factor": scale_factor,
        }
        headers = {
            "Content-Type": "application/json",
        }
        try:
            logger.info("[MagnificUpscaler] Отправка изображения на upscale")
            response = await self.api.post(
                json=json,
                headers=headers,
            )
            data = response["data"]
            logger.info(f"[MagnificUpscaler] Ответ: {data}")
            if not isinstance(data, dict) or "task_id" not in data:
                raise MagnificAPIError(f"Некорректный ответ от Magnific: {data}")
            return data
        except MagnificAPIError:
            raise
        except Exception as e:
            logger.error(f"[MagnificUpscaler] Ошибка upscale: {e}")
            raise MagnificAPIError(str(e))

