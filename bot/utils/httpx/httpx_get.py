import asyncio

import httpx

from bot.app.core.logging import logger


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
            connect=120,   # таймаут на подключение (2 минуты)
            read=1800,     # таймаут на чтение (30 минут)
            write=120,     # таймаут на запись (2 минуты)
            pool=120,      # таймаут на получение соединения из пула (2 минуты)
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
                # Проверяем Content-Type для определения типа ответа
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type or 'text/' in content_type:
                    try:
                        response_json = response.json()
                        logger.info(f"Ответ от сервера: {response_json}")
                        return response_json
                    except ValueError as e:
                        logger.error(f"Ошибка при парсинге ответа от сервера: {e}")
                        return response
                else:
                    # Для бинарных данных (изображения, файлы) возвращаем response
                    return response

            try:
                response_json = response.json()
                logger.error(f"Ошибка при выполнении запроса: {response.status_code} Ответ: {response_json}")
                
                # Извлекаем сообщение об ошибке из ответа
                if (
                    "error" in response_json
                    and "message" in response_json["error"]
                ):
                    error_message = response_json["error"]["message"]
                elif "message" in response_json:
                    error_message = response_json["message"]
                elif "result" in response_json:
                    error_message = response_json["result"]
                elif "error" in response_json:
                    error_message = str(response_json["error"])
                else:
                    error_message = f"HTTP {response.status_code}: {response.text[:200]}"
                    
                raise Exception(error_message)
            except ValueError:
                # Если ответ не является JSON
                error_message = f"HTTP {response.status_code}: {response.text[:200]}"
                logger.error(f"Невалидный JSON ответ. Статус: {response.status_code}, Тело: {response.text}")
                raise Exception(error_message)
            
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
    except Exception as e:
        logger.error(f"Неожиданная ошибка при выполнении GET запроса: {str(e)}")
        await asyncio.sleep(10)
        raise
