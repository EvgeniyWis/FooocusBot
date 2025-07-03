import asyncio

import httpx

from bot.logger import logger


# Функция-обёртка для отправки POST-запросов с настройками таймаутов
async def httpx_post(
    url: str,
    headers: dict,
    json: dict = None,
    data: dict = None,
    files: dict = None,
    timeout: int = 60,
    with_response_text_logging: bool = True,
):
    response = None
    response_json = None

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
        ) as client:
            response = await client.post(
                url,
                headers=headers,
                data=data,
                json=json,
                files=files,
                timeout=httpx.Timeout(
                    connect=30,  # таймаут на подключение
                    read=120,  # таймаут на чтение
                    write=30,  # таймаут на запись
                    pool=30,  # таймаут на получение соединения из пула
                ),
            )

            if with_response_text_logging:
                logger.info(f"Тело ответа: {response.text}")

            if response.status_code != 200:
                if response.status_code == 404:
                    logger.info(
                        f"Найдена завершенная/удаленная генерация. Статус код: {response.status_code}",
                    )
                raise Exception(
                    f"Сервер вернул ошибку: {response.status_code}",
                )

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
        logger.error(f"Ошибка при выполнении запроса: {str(e)} Ответ: {response.text}")
        await asyncio.sleep(10)
        raise

    return response_json
