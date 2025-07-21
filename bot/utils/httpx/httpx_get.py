import httpx

from bot.logger import logger


# Функция для отправки GET-запросов с настройками таймаутов
async def httpx_get(
    url: str, headers: dict = None, timeout: int = 60, stream: bool = False,
) -> dict:
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(timeout), follow_redirects=True,
    ) as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            if stream:
                return response
            try:
                response_json = response.json()
                logger.info(f"Ответ от сервера: {response_json}")
                return response_json
            except ValueError as e:
                logger.error(f"Ошибка при парсинге ответа от сервера: {e}")
                return response

        logger.error(f"Ошибка при выполнении запроса: {response.status_code} Ответ: {response}")
        return None
