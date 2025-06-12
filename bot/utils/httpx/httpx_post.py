import httpx
from logger import logger
import asyncio


# Функция-обёртка для отправки POST-запросов с настройками таймаутов
async def httpx_post(url: str, headers: dict, json: dict = None, timeout: int = 60):
    response_json = None
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout), follow_redirects=True) as client:
        try:
            response = await client.post(
                url,
                headers=headers,
                json=json,
                timeout=httpx.Timeout(
                    connect=30,  # таймаут на подключение
                    read=120,    # таймаут на чтение
                    write=30,    # таймаут на запись
                    pool=30,     # таймаут на получение соединения из пула
                ), 
            )
            logger.info(f"Статус код ответа: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")

            if response.status_code != 200:
                raise Exception(f"Сервер вернул ошибку: {response.status_code}")

            try:
                response_json = response.json()
                logger.info(f"Ответ от сервера по отмене работы: {response_json}")
            except ValueError as e: 
                logger.error(
                    f"Ошибка при парсинге JSON ответа: {e}, тело ответа: {response.text}",
                )
                raise Exception("Сервер вернул невалидный JSON")
                
        except httpx.ReadTimeout:
            logger.error(f"Превышено время ожидания ответа от сервера!")
            await asyncio.sleep(10)
        except httpx.ConnectTimeout:
            logger.error(f"Превышено время ожидания подключения к серверу!")
            await asyncio.sleep(10)
        except httpx.RequestError as e:
            logger.error(f"Ошибка при выполнении запроса: {str(e)} \nТело ответа: {response.text if response else 'нет ответа'}")
            await asyncio.sleep(10)

    return response_json



