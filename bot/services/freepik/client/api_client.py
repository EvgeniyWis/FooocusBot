from bot.services.base_api_client import BaseAPIClient


class FreepikAPI(BaseAPIClient):
    def __init__(self, base_url: str, api_key: str) -> None:
        super().__init__(base_url)
        self.api_key = api_key

    def _add_auth_header(self, headers=None):
        auth_header = {
            "x-freepik-api-key": self.api_key,
        }
        if headers:
            return {**headers, **auth_header}
        return auth_header

    async def post(self, url="", data=None, headers=None, files=None, json=None):
        headers = self._add_auth_header(headers)
        return await super().post(url, data=data, headers=headers, files=files, json=json)

    async def get(self, url="", headers=None):
        headers = self._add_auth_header(headers)
        return await super().get(url, headers=headers)