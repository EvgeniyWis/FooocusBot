import asyncio
from typing import Optional

import runpod
from domain.entities.comfyui_pod import PodStatus
from requests import ReadTimeout
from runpod.error import RunPodError
from services.comfyui.video_service import ComfyUIVideoService
from utils import retryOperation

import bot.constants as constants
from bot.logger import logger
from bot.settings import settings


class UnknownRunPodException(Exception):
    """Неизвестная ошибка при запуске RunPod."""

    pass


class PodManager:
    def __init__(self, api_key: str, video_service: ComfyUIVideoService):
        runpod.api_key = api_key
        self.video_service = video_service

    async def get_pod_by_name(self, name: str) -> Optional[dict]:
        pods = runpod.get_pods()
        return next((pod for pod in pods if pod.get("name") == name), None)

    async def is_pod_running(self, pod_id: str) -> bool:
        pod = runpod.get_pod(pod_id)
        return pod.get("desiredStatus") == "RUNNING"

    async def request_start_pod(self, pod_id: str) -> PodStatus:
        try:
            runpod.resume_pod(pod_id, gpu_count=4)
            logger.info(f"Запрос на запуск пода {pod_id} успешно отправлен.")
            return PodStatus.START_REQUESTED
        except RunPodError as e:
            logger.exception(f"RunPodError при запуске пода {pod_id}")
            if "There are not enough free GPUs" in e.message:
                return PodStatus.NOT_ENOUGH_FREE_GPU
            return PodStatus.ERROR
        except ReadTimeout as e:
            logger.exception(f"ReadTimeout при запуске пода {pod_id}")
            raise ReadTimeout(f"ReadTimeout при запуске пода {pod_id}: {e}")
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при запуске пода {pod_id}")
            raise UnknownRunPodException(
                f"Ошибка при запуске пода {pod_id}: {e}",
            )

    async def poll_until_running(
        self,
        pod_id: str,
        timeout_seconds: int = 1000,
        interval: int = 10,
    ) -> bool:
        elapsed = 0
        while elapsed < timeout_seconds:
            if await self.is_pod_running(pod_id):
                logger.info(
                    f"Под {pod_id} был запущен спустя {elapsed} секунд.",
                )
                return True
            await asyncio.sleep(interval)
            elapsed += interval
        logger.warning(
            f"Под {pod_id} не запустился за {timeout_seconds} секунд.",
        )
        return False

    async def start_pod(self) -> PodStatus:
        pod = await self.get_pod_by_name(settings.COMFYUI_POD_NAME)
        if not pod:
            logger.warning(f"Под {settings.COMFYUI_POD_NAME} не найден.")
            return PodStatus.NOT_FOUND

        pod_id = pod.get("id")

        if await self.is_pod_running(pod_id):
            logger.info(f"Под {pod_id} уже запущен.")
            return PodStatus.ALREADY_RUNNING

        status = await self.request_start_pod(pod_id)

        if status != PodStatus.START_REQUESTED:
            return status

        if not await self.poll_until_running(pod_id):
            return PodStatus.TIMEOUT

        await self._try_heat_models()

        return PodStatus.RUNNING

    async def _try_heat_models(self):
        if not settings.HEATING_COMFYUI_MODELS:
            return

        await self._wait_after_start_heating_models(80)

        try:
            await self.heating_comfyui_models()
        except Exception:
            logger.exception("Ошибка при прогреве моделей.")

    async def _wait_after_start_heating_models(self, seconds: int):
        logger.info(f"Ожидание {seconds} секунд перед прогревом моделей.")
        await asyncio.sleep(seconds)

    async def heating_comfyui_models(self):
        logger.info("Прогрев моделей ComfyUI.")
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
            logger.info("Прогрев моделей завершен успешно.")
        except Exception:
            try:
                logger.warning(
                    "Первая попытка не удалась, повторная генерация.",
                )
                generation_result = await self.video_service.generate(
                    prompt,
                    output_path,
                    duration,
                )
                prompt_id = generation_result["prompt_id"]
                await retryOperation(
                    self.video_service.wait_for_result,
                    5,
                    5,
                    prompt_id,
                )
                logger.info("Прогрев завершен после повтора.")
            except Exception:
                logger.exception(
                    "Не удалось прогреть модели даже после повторной попытки.",
                )
