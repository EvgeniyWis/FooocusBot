from typing import Any, Dict

from bot.services.base_api_client import BaseAPIClient
from bot.services.iloveapi.auth import ILoveAPIAuth


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

    async def iloveapi_post(
        self,
        url: str,
        json: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
        files: Dict[str, Any] = None,
        with_base_url: bool = True,
    ) -> Dict[str, Any]:
        """
        Выполняет POST-запрос к ILoveAPI с автоматическим добавлением токена.

        Args:
            url (str): URL запроса.
            json (dict, optional): JSON-данные для отправки.
            files (dict, optional): Файлы для отправки.

        Returns:
            dict: Ответ от сервера.
        """
        token = await self.auth_service.get_token()
        if not token:
            raise RuntimeError("Не удалось получить токен для ILoveAPI")

        headers = {"Authorization": f"Bearer {token}"}
        resp = await self.post(url, json=json, data=data, files=files, headers=headers, with_base_url=with_base_url)
        return resp

    async def iloveapi_get(
        self,
        url: str,
        with_base_url: bool = True,
        extra_headers: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        token = await self.auth_service.get_token()
        if not token:
            raise RuntimeError("Не удалось получить токен для ILoveAPI")

        headers = {"Authorization": f"Bearer {token}"}

        if extra_headers:
            headers.update(extra_headers)

        resp = await self.get(url, headers=headers, with_base_url=with_base_url)
        return resp
