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

# todo: добавить очистку файлов с комфика
# не качается видос


class ComfyUIVideoService:
    def __init__(self, api_url: str, workflow_path: str, avg_times_path: str):
        self.api = ComfyUIAPI(api_url)
        self.uploader = ComfyUIUploader(self.api)
        self.executor = ComfyUIPromptExecutor(self.api)
        self.preparer = ComfyUIWorkflowPreparer(workflow_path)
        self.inspector = ComfyUIQueueInspector(self.api)
        self.metrics = ComfyUIMetricsService(avg_times_path)

    async def generate(self, prompt: str, image_path: str) -> dict:
        image_name = await self.uploader.upload_image(image_path)
        workflow = self.preparer.prepare(prompt, image_name)
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
            await asyncio.sleep(30)
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
            await asyncio.sleep(60)
            status = await self.executor.get_status(prompt_id)
            urls = self._extract_outputs(status)
            if urls:
                duration = time.time() - start
                await self.metrics.save(duration)
                return {"video_urls": urls, "duration": duration}
        logger.error(
            f"Timeout получения результата генерации ComfyUI для промпта {prompt_id}",
        )
        return {"error": "Timeout"}

    def _extract_outputs(self, status_json: dict) -> list:
        results = []
        for node in status_json.get("outputs", {}).values():
            for gif in node.get("gifs", []):
                results.append(
                    f"{self.api.base_url}/api/viewvideo?filename={
                    gif['filename']}&type=output&subfolder={
                    gif.get('subfolder', '')}&format=video/h264-mp4",
                )
            for img in node.get("images", []):
                results.append(
                    f"{self.api.base_url}/view?filename={
                    img['filename']}&type=output&subfolder={
                    img.get('subfolder', '')}",
                )
        logger.info(
            f"Найдены результаты генерации: {results}",
        ) if results else logger.info(
            f"Результаты генерации не найдены для status_json: {status_json}",
        )
        return results

    def cleanup_local_output(self, folder="./ComfyUI/output"):
        for root, _, files in os.walk(folder):
            for f in files:
                if f.endswith((".mp4", ".jpg", ".png")):
                    try:
                        os.remove(os.path.join(root, f))
                    except Exception:
                        pass
