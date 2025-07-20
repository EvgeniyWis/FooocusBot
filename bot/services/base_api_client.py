import httpx

from bot.logger import logger
from bot.utils.httpx import httpx_get, httpx_post


class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        logger.info(f"Инициализирован API клиент с базовым URL: {base_url}")

    async def post(self, path: str, json: dict = None, files: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        logger.info(f"Отправка POST запроса на {url}")
        resp = await httpx_post(url, json=json, files=files)
        try:
            resp.raise_for_status()
            logger.info(f"Успешный POST запрос к {path}")
            return resp.json()
        except httpx.HTTPError as e:
            logger.error(f"Ошибка HTTP при POST запросе к {path}: {str(e)}")
            raise

    async def get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"
        logger.info(f"Отправка GET запроса на {url}")
        resp = await httpx_get(url)
        try:
            resp.raise_for_status()
            logger.info(f"Успешный GET запрос к {path}")
            return resp.json()
        except httpx.HTTPError as e:
            logger.error(f"Ошибка HTTP при GET запросе к {path}: {str(e)}")
            raise