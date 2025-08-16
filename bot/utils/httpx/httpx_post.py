import asyncio

import httpx

from bot.app.core.logging import logger
from bot.utils.httpx.error_texts import PAYMENT_RUNPOD_ERROR_TEXT


# Функция-обёртка для отправки POST-запросов с настройками таймаутов
async def httpx_post(
    url: str,
    headers: dict = None,
    json: dict = None,
    data: dict = None,
    files: dict = None,
    timeout: int = 60,
    with_response_text_logging: bool = True,
    is_long_operation: bool = False,
) -> dict:
    response = None
    response_json = None

    try:
        # Увеличиваем таймауты для длительных операций (например, upscale)
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

        async with httpx.AsyncClient(
            timeout=timeout_config,
            follow_redirects=True,
        ) as client:
            response = await client.post(
                url,
                headers=headers,
                data=data,
                json=json,
                files=files,
                timeout=timeout_config,
            )

            if with_response_text_logging:
                logger.info(f"Тело ответа: {response.text}")

            if response.status_code != 200:
                if response.status_code == 404:
                    logger.error(
                        f"Несуществующий URL: {url}. Статус: {response.status_code}, Ответ: {response.text[:200]}",
                    )
                    raise Exception(f"Сервер не найден (404): {url}")

                if response.status_code == 402 and "runpod" in url.lower():
                    raise Exception(PAYMENT_RUNPOD_ERROR_TEXT)

                # Логируем детали ошибки
                logger.error(f"HTTP ошибка {response.status_code} для URL: {url}")
                logger.error(f"Заголовки ответа: {dict(response.headers)}")
                logger.error(f"Тело ответа: {response.text[:500]}")

                try:
                    response_json = response.json()
                    logger.error(f"Ошибка API. Статус: {response.status_code}, Ответ: {response_json}")
                    
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
                except ValueError:
                    # Если ответ не является JSON
                    error_message = f"HTTP {response.status_code}: {response.text[:200]}"
                    logger.error(f"Невалидный JSON ответ. Статус: {response.status_code}, Тело: {response.text}")

                # Проверяем, не содержит ли ошибка подозрительные сообщения
                if "failed to get" in error_message.lower():
                    logger.error(f"Сервер вернул подозрительное сообщение об ошибке: {error_message}")
                    error_message = f"Ошибка сервера {response.status_code}: {response.text[:100]}"

                raise Exception(error_message)

            try:
                response_json = response.json()

                if with_response_text_logging:
                    logger.info(f"Ответ от сервера: {response_json}")
            except ValueError as e:
                logger.error(
                    f"Ошибка при парсинге JSON ответа: {e}, тело ответа: {response.text}",
                )
                raise Exception("Сервер вернул невалидный JSON")

    except httpx.ReadTimeout:
        logger.error("Превышено время ожидания ответа от сервера!")
        await asyncio.sleep(10)
        raise
    except httpx.ConnectTimeout:
        logger.error("Превышено время ожидания подключения к серверу!")
        await asyncio.sleep(10)
        raise
    except httpx.RequestError as e:
        logger.error(
            f"Ошибка при выполнении запроса: {str(e)} Ответ: {response}",
        )
        await asyncio.sleep(10)
        raise

    return response_json
