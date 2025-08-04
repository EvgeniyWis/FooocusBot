import httpx

from bot.logger import logger
from bot.utils.httpx import httpx_get, httpx_post


class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        logger.info(f"Инициализирован API клиент с базовым URL: {base_url}")

    async def post(
        self,
        path: str,
        json: dict = None,
        data: dict = None,
        files: dict = None,
        headers: dict = None,
        with_base_url: bool = True,
        is_long_operation: bool = False,
    ) -> dict:
        url = f"{self.base_url}{path}" if with_base_url else path
        logger.info(f"Отправка POST запроса на {url}")
        resp = await httpx_post(
            url, 
            json=json, 
            data=data,
            files=files, 
            headers=headers,
            is_long_operation=is_long_operation
        )
        return resp

    async def get(
        self, 
        path: str, 
        headers: dict = None, 
        with_base_url: bool = True,
        is_long_operation: bool = False,
    ) -> dict:
        url = f"{self.base_url}{path}" if with_base_url else path
        logger.info(f"Отправка GET запроса на {url}")
        resp = await httpx_get(
            url, 
            headers=headers,
            is_long_operation=is_long_operation
        )
        return resp
