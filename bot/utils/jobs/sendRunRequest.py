import httpx
from config import RUNPOD_HEADERS, RUNPOD_HOST
from logger import logger


# Функция для отправки запроса на генерацию
async def sendRunRequest(dataJSON: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{RUNPOD_HOST}/run",
            headers=RUNPOD_HEADERS,
            json=dataJSON,
            timeout=httpx.Timeout(
                10,
                read=30,
            ),  # (connect timeout, read timeout)
        )
        logger.info(f"Статус код ответа: {response.status_code}")
        logger.info(f"Тело ответа: {response.text}")

        if response.status_code != 200:
            raise Exception(f"Сервер вернул ошибку: {response.status_code}")

        try:
            response_json = response.json()
            return response_json
        except (
            ValueError
        ) as e:  # response.json() выкидывает ValueError, если JSON невалидный
            logger.error(
                f"Ошибка при парсинге JSON ответа: {e}, тело ответа: {response.text}",
            )
            raise Exception("Сервер вернул невалидный JSON")
