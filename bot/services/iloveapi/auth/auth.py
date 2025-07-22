from typing import Optional

from bot.logger import logger
from bot.utils.httpx import httpx_post


class ILoveAPIAuth:
    """
    Сервис аутентификации и менеджер токена для ILoveAPI.
    """
    def __init__(self, base_url: str, public_key: str) -> None:
        """
        Args:
            base_url (str): Базовый URL API.
            public_key (str): Публичный ключ для аутентификации.
        """
        self.base_url = base_url
        self.public_key = public_key
        self._token: Optional[str] = None
        logger.info("Инициализирован аутентификатор ILoveAPI")

    async def get_token(self) -> str:
        """
        Возвращает актуальный токен. Если токена нет — выполняет аутентификацию.

        Returns:
            str: JWT токен.
        """
        if not self._token:
            self._token = await self._auth()

            if not self._token:
                raise RuntimeError("Не удалось получить токен от ILoveAPI (пустой токен)")

        return self._token

    async def _auth(self) -> str:
        """
        Выполняет аутентификацию в ILoveAPI и возвращает токен.

        Returns:
            str: JWT токен.
        """
        url = f"{self.base_url}/auth"
        data = {"public_key": self.public_key}
        try:
            response = await httpx_post(url, data=data)
            jwt_token = response.get("token")
            if not jwt_token:
                logger.error(f"Ответ от ILoveAPI не содержит токен: {response}")
                return None
            return jwt_token
        except Exception as e:
            logger.error(f"Ошибка при аутентификации в ILoveAPI: {e}")
            return None
