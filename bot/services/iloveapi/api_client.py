from typing import Any, Dict, Optional

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
        self.public_key: str = public_key
        self.token: Optional[str] = None
        self.auth_service: ILoveAPIAuth = ILoveAPIAuth(self)

    async def ensure_token(self) -> None:
        """
        Проверяет наличие токена, если его нет — выполняет аутентификацию.
        """
        if not self.token:
            self.token = await self.auth_service.auth(self.public_key)

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполняет POST-запрос к ILoveAPI с автоматическим добавлением токена.

        Args:
            path (str): Путь запроса.
            json (dict, optional): JSON-данные для отправки.
            files (dict, optional): Файлы для отправки.

        Returns:
            dict: Ответ от сервера.
        """
        await self.ensure_token()
        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = await httpx_post(url, json=json, files=files, headers=headers)
        json = resp.json()
        return json