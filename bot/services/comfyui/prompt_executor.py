from bot.logger import logger
from bot.services.comfyui.api_client import ComfyUIAPI


class ComfyUIPromptExecutor:
    def __init__(self, api: ComfyUIAPI):
        self.api = api
        logger.info("Инициализирован исполнитель промптов ComfyUI")

    async def submit_prompt(self, workflow: dict) -> str:
        logger.info("Отправка нового промпта в ComfyUI")
        try:
            result = await self.api.post(
                "/api/prompt",
                json={"prompt": workflow},
            )
            prompt_id = result.get("prompt_id")
            if not prompt_id:
                logger.error(
                    f"Ошибка отправки промпта - не получен prompt_id в ответе: {result}",
                )
                raise RuntimeError(f"Не возвращен ID промпта: {result}")

            logger.info(
                f"Промпт успешно отправлен, получен ID: {prompt_id}",
            )
            return prompt_id
        except Exception as e:
            logger.error(f"Ошибка при отправке промпта: {str(e)}")
            raise

    async def get_status(self, prompt_id: str) -> dict:
        logger.info(f"Проверка статуса промпта: {prompt_id}")
        try:
            status = await self.api.get(f"/api/history/{prompt_id}")
            logger.info(f"Статус промпта {prompt_id}: {status}")
            return status
        except Exception as e:
            logger.error(
                f"Ошибка при получении статуса промпта {prompt_id}: {str(e)}",
            )
            raise
