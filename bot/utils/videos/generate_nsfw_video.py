from domain.entities.video_generation import (
    ErrorStatus,
    NSFWVideoStatus,
    ProcessingStatus,
    QueuedStatus,
    StartGenerationStatus,
    TimeoutStatus,
)

from bot.factory.comfyui_video_service import get_video_service
from bot.logger import logger


async def generate_nsfw_video(
    prompt: str,
    temp_path: str,
    seconds: int,
) -> NSFWVideoStatus:
    video_service = get_video_service()

    try:
        result = await video_service.generate(
            prompt,
            temp_path,
            seconds=seconds,
        )
    except Exception as e:
        logger.error(f"Ошибка при генерации: {e}")
        return ErrorStatus(status="error")

    queue = result["queue"]
    prompt_id = result["prompt_id"]
    approx_wait = result["approx_wait"]
    wait_min = approx_wait // 60 if approx_wait else 0
    status = queue.get("status")

    if status == "queued" and queue.get("position"):
        return QueuedStatus(
            status="queued",
            position=queue["position"],
            queue_length=queue["queue_length"],
            wait_min=wait_min,
            prompt_id=prompt_id,
        )

    elif status == "processing":
        return ProcessingStatus(
            status="processing",
            wait_min=wait_min,
            prompt_id=prompt_id,
        )

    elif status == "queued":
        try:
            await video_service.wait_until_generation_starts(prompt_id)
            return StartGenerationStatus(
                status="start_generation",
                wait_min=wait_min,
                prompt_id=prompt_id,
            )
        except TimeoutError:
            return TimeoutStatus(status="timeout")

    return ErrorStatus(status="error")
