from bot.services.base_api_client import BaseAPIClient
from bot.services.iloveapi.auth.auth import ILoveAPIAuth


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

    async def post(
        self,
        url: str,
        json: dict = None,
        data: dict = None,
        files: dict = None,
        with_base_url: bool = True,
        is_long_operation: bool = False,
    ) -> dict:
        """
        Выполняет POST-запрос к ILoveAPI с автоматическим добавлением токена.

        Args:
            url (str): URL запроса.
            json (dict, optional): JSON-данные для отправки.
            files (dict, optional): Файлы для отправки.
            is_long_operation (bool): Флаг для длительных операций (например, upscale).

        Returns:
            dict: Ответ от сервера.
        """
        token = await self.auth_service.get_token()
        if not token:
            raise RuntimeError("Не удалось получить токен для ILoveAPI")

        headers = {"Authorization": f"Bearer {token}"}
        resp = await super().post(
            url, 
            json=json, 
            data=data, 
            files=files, 
            headers=headers, 
            with_base_url=with_base_url,
            is_long_operation=is_long_operation
        )
        return resp

    async def get(
        self,
        url: str,
        with_base_url: bool = True,
        extra_headers: dict = None,
        is_long_operation: bool = False,
    ) -> dict:
        token = await self.auth_service.get_token()
        if not token:
            raise RuntimeError("Не удалось получить токен для ILoveAPI")

        headers = {"Authorization": f"Bearer {token}"}

        if extra_headers:
            headers.update(extra_headers)

        resp = await super().get(
            url, 
            headers=headers, 
            with_base_url=with_base_url,
            is_long_operation=is_long_operation
        )
        return resp
