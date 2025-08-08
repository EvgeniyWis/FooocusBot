from utils import retryOperation

import bot.app.config.constants as contants
from bot.app.core.logging import logger
from bot.services.comfyui.video_service import ComfyUIVideoService


async def heating_comfyui_models(video_service: ComfyUIVideoService):
    logger.info("Прогрев моделей ComfyUI")
    data = {
        "prompt": "A naked girl strokes her bare breasts with her hands,"
        " sensual movement, static camera, cinematic lighting,"
        " natural body physics, 4K detail, eye contact",
        "temp_path": contants.COMFYUI_HEATING_IMAGES_PATH
        / "heating_image.jpg",
        "seconds": 1,
    }
    status = await video_service.generate(
        data["prompt"],
        data["temp_path"],
        data["seconds"],
    )
    try:
        await video_service.wait_for_result(
            status["prompt_id"],
        )
        logger.info("Модели ComfyUI успешно прогреты и готовы к работе")
    except Exception:
        try:
            await retryOperation(
                video_service.wait_for_result,
                5,
                5,
                status["prompt_id"],
            )
        except Exception as e:
            logger.error(f"Не удалось прогреть модели ComfyUI: {e}")
            return
