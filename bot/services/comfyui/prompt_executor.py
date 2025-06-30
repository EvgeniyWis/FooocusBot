from bot.services.comfyui.api_client import ComfyUIAPI


class ComfyUIPromptExecutor:
    def __init__(self, api: ComfyUIAPI):
        self.api = api

    async def submit_prompt(self, workflow: dict) -> str:
        result = await self.api.post("/api/prompt", json={"prompt": workflow})
        prompt_id = result.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"Prompt ID not returned: {result}")
        return prompt_id

    async def get_status(self, prompt_id: str) -> dict:
        return await self.api.get(f"/api/history/{prompt_id}")
