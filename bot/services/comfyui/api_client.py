import httpx

from bot.logger import logger


class ComfyUIAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        logger.info(
            f"Инициализирован API клиент ComfyUI с базовым URL: {base_url}",
        )

    async def post(
        self,
        path: str,
        json: dict = None,
        files: dict = None,
    ) -> dict:
        url = f"{self.base_url}{path}"
        logger.info(f"Отправка POST запроса на {url}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=json, files=files)
            try:
                resp.raise_for_status()
                logger.info(f"Успешный POST запрос к {path}")
                return resp.json()
            except httpx.HTTPError as e:
                logger.error(
                    f"Ошибка HTTP при POST запросе к {path}: {str(e)}",
                )
                raise

    async def get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"
        logger.info(f"Отправка GET запроса на {url}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            try:
                resp.raise_for_status()
                logger.info(f"Успешный GET запрос к {path}")
                return resp.json()
            except httpx.HTTPError as e:
                logger.error(f"Ошибка HTTP при GET запросе к {path}: {str(e)}")
                raise
