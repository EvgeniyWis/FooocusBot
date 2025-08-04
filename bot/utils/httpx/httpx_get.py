import asyncio
import httpx

from bot.logger import logger


# Функция для отправки GET-запросов с настройками таймаутов
async def httpx_get(
    url: str, 
    headers: dict = None, 
    timeout: int = 60, 
    stream: bool = False,
    is_long_operation: bool = False,
) -> dict:
    # Увеличиваем таймауты для длительных операций
    if is_long_operation:
        timeout_config = httpx.Timeout(
            connect=60,   # таймаут на подключение
            read=600,     # таймаут на чтение (10 минут)
            write=60,     # таймаут на запись
            pool=60,      # таймаут на получение соединения из пула
        )
    else:
        timeout_config = httpx.Timeout(
            connect=30,   # таймаут на подключение
            read=120,     # таймаут на чтение
            write=30,     # таймаут на запись
            pool=30,      # таймаут на получение соединения из пула
        )

    try:
        async with httpx.AsyncClient(
            timeout=timeout_config, 
            follow_redirects=True,
        ) as client:
            response = await client.get(url, headers=headers, timeout=timeout_config)

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

            response_json = response.json()
            logger.error(f"Ошибка при выполнении запроса: {response.status_code} Ответ: {response_json}")
            return None
            
    except httpx.ReadTimeout:
        logger.error("Превышено время ожидания ответа от сервера!")
        await asyncio.sleep(10)
        raise
    except httpx.ConnectTimeout:
        logger.error("Превышено время ожидания подключения к серверу!")
        await asyncio.sleep(10)
        raise
    except httpx.RequestError as e:
        logger.error(f"Ошибка при выполнении запроса: {str(e)}")
        await asyncio.sleep(10)
        raise
