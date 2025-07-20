from bot.services.base_api_client import BaseAPIClient
from bot.services.iloveapi.auth import ILoveAPIAuth
from bot.utils.httpx import httpx_post


class ILoveAPI(BaseAPIClient):
    def __init__(self, base_url: str, public_key: str):
        super().__init__(base_url)
        self.public_key = public_key
        self.token = None
        self.auth_service = ILoveAPIAuth(self)

    async def ensure_token(self):
        if not self.token:
            self.token = await self.auth_service.auth(self.public_key)

    async def post(self, path: str, json: dict = None, files: dict = None) -> dict:
        await self.ensure_token()
        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = await httpx_post(url, json=json, files=files, headers=headers)
        return resp.json()