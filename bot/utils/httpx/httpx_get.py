import httpx
from logger import logger


# Функция для отправки GET-запросов с настройками таймаутов
async def httpx_get(url: str, timeout: int = 60):
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout), follow_redirects=True) as client:
        response = await client.get(url)
        logger.info(f"Статус ответа: {response.status_code}")

        if response.status_code == 200:
            return response

        logger.error(f"Неудачный статус ответа: {response.status_code}")
        return None





