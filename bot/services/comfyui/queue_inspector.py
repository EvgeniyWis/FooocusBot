from bot.services.comfyui.api_client import ComfyUIAPI


class ComfyUIQueueInspector:
    def __init__(self, api: ComfyUIAPI):
        self.api = api

    async def get_queue_position(self, prompt_id: str) -> dict:
        data = await self.api.get("/queue")
        pending = data.get("queue_pending", [])
        for idx, item in enumerate(pending):
            if prompt_id in str(item):
                return {"position": idx + 1, "queue_length": len(pending)}

        running = data.get("queue_running", [])
        for item in running:
            if prompt_id in str(item):
                return {"position": 1, "queue_length": len(pending) + 1}

        return {"position": None, "queue_length": len(pending)}
