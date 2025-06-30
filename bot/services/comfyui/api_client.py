import httpx


class ComfyUIAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def post(
        self, path: str, json: dict = None, files: dict = None
    ) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}{path}", json=json, files=files
            )
            resp.raise_for_status()
            return resp.json()

    async def get(self, path: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}{path}")
            resp.raise_for_status()
            return resp.json()
