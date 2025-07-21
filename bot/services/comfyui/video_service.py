import asyncio
import os
import time

from bot.logger import logger
from bot.services.comfyui.api_client import ComfyUIAPI
from bot.services.comfyui.metrics import ComfyUIMetricsService
from bot.services.comfyui.prompt_executor import ComfyUIPromptExecutor
from bot.services.comfyui.queue_inspector import ComfyUIQueueInspector
from bot.services.comfyui.uploader import ComfyUIUploader
from bot.services.comfyui.workflow_preparer import ComfyUIWorkflowPreparer


class ComfyUIVideoService:
    def __init__(self, api_url: str, workflow_path: str, avg_times_path: str):
        self.api = ComfyUIAPI(api_url)
        self.uploader = ComfyUIUploader(self.api)
        self.executor = ComfyUIPromptExecutor(self.api)
        self.preparer = ComfyUIWorkflowPreparer(workflow_path)
        self.inspector = ComfyUIQueueInspector(self.api)
        self.metrics = ComfyUIMetricsService(avg_times_path)

    async def generate(
        self,
        prompt: str,
        image_path: str,
        seconds: int,
    ) -> dict:
        image_name = await self.uploader.upload_image(image_path)
        workflow = self.preparer.prepare(prompt, image_name, seconds)
        prompt_id = await self.executor.submit_prompt(workflow)
        queue = await self.inspector.get_queue_position(prompt_id)
        avg = await self.metrics.get_avg()

        approx_wait = None
        if queue["status"] == "queued" and queue["position"]:
            approx_wait = int(avg * queue["position"])
        else:
            approx_wait = avg

        return {
            "prompt_id": prompt_id,
            "queue": queue,
            "approx_wait": approx_wait,
        }

    async def wait_until_generation_starts(
        self,
        prompt_id: str,
        timeout: int = 10000,
    ):
        start = time.time()

        while time.time() - start < timeout:
            queue_info = await self.inspector.get_queue_position(prompt_id)
            if queue_info["status"] == "processing":
                return
            await asyncio.sleep(160)
        logger.error(
            f"Timeout ожидания начала генерации ComfyUI для промпта {prompt_id}",
        )
        raise TimeoutError(
            "Задача не начала обрабатываться в течение допустимого времени.",
        )

    async def wait_for_result(
        self,
        prompt_id: str,
        timeout: int = 10000,
    ) -> dict:
        start = time.time()
        for _ in range(timeout // 60):
            await asyncio.sleep(160)
            status = await self.executor.get_status(prompt_id)
            video_paths = self._extract_outputs(status)
            if video_paths:
                duration = time.time() - start
                await self.metrics.save(duration)
                video_urls = self.get_video_urls(status)
                self.cleanup_local_output()

                return {"video_urls": video_urls, "duration": duration}
        logger.error(
            f"Timeout получения результата генерации ComfyUI для промпта {prompt_id}",
        )
        return {"error": "Timeout"}

    def _extract_outputs(self, status_json: dict) -> list[str]:
        if not status_json:
            return []

        # Промпт ID всегда один
        prompt_id, prompt_data = next(iter(status_json.items()))
        outputs = prompt_data.get("outputs", {})

        urls = []

        for node_output in outputs.values():
            if isinstance(node_output, dict):
                for output in node_output.get("gifs", []):
                    path = output.get("fullpath")
                    if path:
                        urls.append(path)

        return urls

    def _build_url(self, endpoint: str, file_info: dict) -> str:
        filename = file_info["filename"]
        subfolder = file_info.get("subfolder")

        if filename.endswith(".mp4"):
            filename_for_url = filename.replace(".mp4", ".mov")
            format_param = "video/quicktime"
        else:
            filename_for_url = filename
            format_param = "video/h264-mp4"

        base = (
            f"{self.api.base_url}/{endpoint}"
            f"?filename={filename_for_url}"
            f"&type=output"
            f"&format={format_param}"
        )
        if subfolder:
            base += f"&subfolder={subfolder}"
        return base

    def get_video_urls(self, status_json: dict) -> list[str]:
        if not status_json:
            return []

        prompt_id, prompt_data = next(iter(status_json.items()))
        outputs = prompt_data.get("outputs", {})

        urls = []
        for node_output in outputs.values():
            if isinstance(node_output, dict):
                for gif in node_output.get("gifs", []):
                    fullpath = gif.get("fullpath")
                    if fullpath:
                        parts = fullpath.split("/ComfyUI/output/")[-1].split(
                            "/",
                        )
                        if len(parts) >= 2:
                            subfolder = "/".join(parts[:-1])
                            filename = parts[-1]
                            file_info = {
                                "filename": filename,
                                "subfolder": subfolder,
                            }
                            url = self._build_url("view", file_info)
                            urls.append(url)
        return urls

    def cleanup_local_output(self, folder="./ComfyUI/output"):
        for root, _, files in os.walk(folder):
            for f in files:
                if f.endswith((".mp4", ".jpg", ".png")):
                    try:
                        os.remove(os.path.join(root, f))
                        logger.info(
                            f"Очищена папка ComfyUI/output: {root}/{f}",
                        )
                    except Exception as e:
                        logger.warning(f"Ошибка при удалении {f}: {e}")
