from typing import Any, Dict

from bot.services.base_api_client import BaseAPIClient
from bot.services.iloveapi.auth import ILoveAPIAuth
from bot.utils.httpx import httpx_post


class ILoveAPI(BaseAPIClient):
    """
    Клиент для работы с ILoveAPI. Управляет аутентификацией и отправкой запросов.
    """
    def __init__(self, base_url: str, public_key: str) -> None:
        """
        Args:
            base_url (str): Базовый URL API.
            public_key (str): Публичный ключ для аутентификации.
        """
        super().__init__(base_url)
        self.auth_service: ILoveAPIAuth = ILoveAPIAuth(base_url, public_key)

    async def post(self, path: str, json: Dict[str, Any] = None, files: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Выполняет POST-запрос к ILoveAPI с автоматическим добавлением токена.

        Args:
            path (str): Путь запроса.
            json (dict, optional): JSON-данные для отправки.
            files (dict, optional): Файлы для отправки.

        Returns:
            dict: Ответ от сервера.
        """
        token = await self.auth_service.get_token()
        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await httpx_post(url, json=json, files=files, headers=headers)
        json_resp = resp.json()
        return json_resp