from bot.logger import logger
from bot.services.iloveapi.api_client import ILoveAPI
from bot.utils.httpx import httpx_post


class ILoveAPIAuth:
    """
    Сервис аутентификации для ILoveAPI.
    """
    def __init__(self, api: ILoveAPI) -> None:
        """
        Args:
            api (ILoveAPI): Экземпляр клиента ILoveAPI.
        """
        self.api = api
        logger.info("Инициализирован аутентификатор ILoveAPI")

    async def auth(self, public_key: str) -> str:
        """
        Аутентификация в ILoveAPI.

        Args:
            public_key (str): Публичный ключ.

        Returns:
            str: JWT токен.
        """
        url = f"{self.api.base_url}/auth"
        data = {"public_key": public_key}
        response = await httpx_post(url, data=data)
        json = response.json()
        jwt_token: str = json["token"]
        return jwt_token
