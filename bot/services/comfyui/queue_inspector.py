from bot.app.core.logging import logger
from bot.services.comfyui.api_client import ComfyUIAPI


class ComfyUIQueueInspector:
    def __init__(self, api: ComfyUIAPI):
        self.api = api
        logger.info("Инициализирован инспектор очереди ComfyUI")

    async def get_queue_position(self, prompt_id: str) -> dict:
        logger.info(f"Проверка позиции в очереди для промпта: {prompt_id}")
        try:
            data = await self.api.get("/queue")
            pending = data.get("queue_pending", [])

            for idx, item in enumerate(pending):
                if prompt_id in str(item):
                    status = {
                        "position": idx + 1,
                        "status": "queued",
                        "queue_length": len(pending),
                    }
                    logger.info(
                        f"Промпт {prompt_id} находится в очереди на позиции {idx + 1}/{len(pending)}",
                    )
                    return status

            running = data.get("queue_running", [])
            for item in running:
                if prompt_id in str(item):
                    status = {
                        "position": 0,
                        "status": "processing",
                        "queue_length": 0,
                    }
                    logger.info(f"Промпт {prompt_id} сейчас обрабатывается")
                    return status

            logger.info(
                f"Промпт {prompt_id} не найден в очереди. Длина очереди: {len(pending)}",
            )
            return {
                "position": None,
                "status": None,
                "queue_length": len(pending),
            }
        except Exception as e:
            logger.error(
                f"Ошибка при проверке позиции в очереди для промпта {prompt_id}: {str(e)}",
            )
            raise
