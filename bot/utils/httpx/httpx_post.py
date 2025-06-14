import asyncio

import httpx

from bot.logger import logger
from bot.storage import get_redis_storage



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
    response_json = None

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(timeout), follow_redirects=True
    ) as client:
        try:
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
                    # Получаем job_id из url
                    job_id = url.split("/")[-1]
                    logger.info(f"Удаляем задачу из Redis, как недействительную: {job_id}")
                    
                    # Удаляем задачу из Redis, как недействительную
                    redis_storage = get_redis_storage()
                    await redis_storage.delete_task(job_id)
                else:
                    raise Exception(
                        f"Сервер вернул ошибку: {response.status_code}"
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
        except httpx.ConnectTimeout:
            logger.error("Превышено время ожидания подключения к серверу!")
            await asyncio.sleep(10)
        except httpx.RequestError as e:
            logger.error(
                f"Ошибка при выполнении запроса: {str(e)} \nТело ответа: {response.text if response else 'нет ответа'}"
            )
            await asyncio.sleep(10)

    return response_json
