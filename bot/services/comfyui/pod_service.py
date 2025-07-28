import asyncio

import runpod
from requests import ReadTimeout
from runpod.error import RunPodError
from services.comfyui.video_service import ComfyUIVideoService
from utils import retryOperation

import bot.constants as constants
from bot.logger import logger
from bot.settings import settings


class UnknowRunPodException(Exception):
    """Вызывается при любых неизвестных ошибках на RunPod"""

    pass


class PodManager:
    def __init__(self, api_key: str, video_service: ComfyUIVideoService):
        runpod.api_key = api_key
        self.video_service = video_service

    def get_pod_by_name(self, name: str) -> dict | None:
        pods = runpod.get_pods()
        return next((pod for pod in pods if pod.get("name") == name), None)

    async def start_pod_if_not_running(self) -> bool:
        pod = self.get_pod_by_name(settings.COMFYUI_POD_NAME)

        if not pod:
            logger.warning(
                f"Под с именем {settings.COMFYUI_POD_NAME} не найден.",
            )
            return False

        pod_id = pod.get("id")
        pod_status = pod.get(
            "desiredStatus",
        )

        if pod_status == "RUNNING":
            logger.info(
                f"Под {settings.COMFYUI_POD_NAME}({pod_id}) уже запущен.",
            )
            return False

        try:
            runpod.resume_pod(pod_id, gpu_count=1)
            logger.info(
                f"Запрос на запуск пода {settings.COMFYUI_POD_NAME}({pod_id}) успешно отправлен.",
            )
        except RunPodError as e:
            logger.exception(
                f"Ошибка при запуске пода {settings.COMFYUI_POD_NAME}({pod_id})",
            )
            raise RunPodError(
                f"Ошибка при запуске пода {settings.COMFYUI_POD_NAME}({pod_id}): {e}",
            )
        except ReadTimeout as e:
            logger.exception(
                f"ReadTimeout при запуске пода {settings.COMFYUI_POD_NAME}({pod_id})",
            )
            raise ReadTimeout(
                f"ReadTimeout при запуске пода {settings.COMFYUI_POD_NAME}({pod_id}) - {e}",
            )
        except Exception as e:
            logger.exception(
                f"Неизвестная ошибка при запуске пода {settings.COMFYUI_POD_NAME}({pod_id})",
            )
            raise UnknowRunPodException(
                f"Неизвестная ошибка при запуске пода {settings.COMFYUI_POD_NAME}({pod_id}): {e}",
            )

        if settings.HEATING_COMFYUI_MODELS:
            sleep_sec = 80
            logger.info(
                f"Ожидаем {sleep_sec} секунд перед прогревом моделей ComfyUI",
            )
            await asyncio.sleep(sleep_sec)
            await self.heating_comfyui_models()

        return True

    async def heating_comfyui_models(self):
        logger.info("Прогрев моделей ComfyUI")

        prompt = settings.COMFYUI_HEATING_PROMPT
        output_path = (
            constants.COMFYUI_HEATING_IMAGES_PATH / "heating_image.jpg"
        )
        duration = 1

        try:
            generation_result = await self.video_service.generate(
                prompt,
                output_path,
                duration,
            )
            prompt_id = generation_result["prompt_id"]

            await self.video_service.wait_for_result(prompt_id)
            logger.info("Модели ComfyUI успешно прогреты и готовы к работе")
        except Exception:
            try:
                logger.warning(
                    "Первая попытка прогрева не удалась. Повтор через retryOperation.",
                )
                await retryOperation(
                    self.video_service.wait_for_result,
                    5,
                    5,
                    prompt_id,
                )
                logger.info("Прогрев моделей завершён после повторной попытки")
            except Exception:
                logger.exception(
                    "Не удалось прогреть модели ComfyUI даже после повторной попытки",
                )
