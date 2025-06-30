import asyncio
import time

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

    async def generate(self, prompt: str, image_path: str) -> dict:
        image_name = await self.uploader.upload_image(image_path)
        workflow = self.preparer.prepare(prompt, image_name)
        prompt_id = await self.executor.submit_prompt(workflow)
        queue = await self.inspector.get_queue_position(prompt_id)
        avg = await self.metrics.get_avg()
        return {
            "prompt_id": prompt_id,
            "queue": queue,
            "approx_wait": int(
                avg * queue["position"] if queue["position"] else 0,
            ),
        }

    async def wait_for_result(
        self,
        prompt_id: str,
        timeout: int = 3600,
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
        return {"error": "Timeout"}

    def _extract_outputs(self, status_json: dict) -> list:
        results = []
        for node in status_json.get("outputs", {}).values():
            for gif in node.get("gifs", []):
                results.append(
                    f"{self.api.base_url}/api/viewvideo?filename={gif['filename']}&type=output&subfolder={gif.get('subfolder', '')}&format=video/h264-mp4",
                )
            for img in node.get("images", []):
                results.append(
                    f"{self.api.base_url}/view?filename={img['filename']}&type=output&subfolder={img.get('subfolder', '')}",
                )
        return results
