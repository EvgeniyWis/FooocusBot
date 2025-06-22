import asyncio
import os

from bot.logger import logger
from bot.utils.get_api_headers import get_kling_headers
from bot.utils.httpx import httpx_get
from bot.utils.videos import download_video


async def check_video_generation_status(request_id: str) -> str | None:
    """
    Функция для проверки статуса задания на генерацию видео с помощью API kling

    Args:
        request_id (str): ID задания на генерацию видео

    Returns:
        str: Путь к сгенерированному видео
    """
    url_status_endpoint = (
        f"https://api.gen-api.ru/api/v1/request/get/{request_id}"
    )

    while True:
        try:
            json = await httpx_get(
                url_status_endpoint,
                headers=get_kling_headers(),
            )

            logger.info(
                f"Статус задания на генерацию видео с id {request_id}: "
                f"{json['status']}",
            )

            if json["status"] == "error":
                # Обрабатываем ошибку промпта, непройденного модераций
                PROMPT_NOT_PASSED_MODERATION_ERROR_TEXT = "Параметры сформированы некорректно. Пожалуйста, убедитесь в правильности введенных данных и отсутствии неприемлемого контента в подсказках."

                if (
                    json["result"][0]
                    == PROMPT_NOT_PASSED_MODERATION_ERROR_TEXT
                ):
                    return {"error": PROMPT_NOT_PASSED_MODERATION_ERROR_TEXT}

                logger.error(f"Ошибка при генерации видео: {json}")
                raise Exception(json["result"][0])

            elif json["status"] == "success":
                # Получаем ссылку на выходное видео
                logger.info(
                    f"Выходные данные запроса по id {request_id}: {json}",
                )
                result_url = json["full_response"][0]["url"]
                logger.info(
                    f"Ссылка на выходное видео: {result_url}",
                )

                # Скачиваем видео локально
                video_path = await download_video(result_url)
                logger.info(f"Путь к скачанному видео: {video_path}")
                if not video_path:
                    logger.error(
                        f"Не удалось скачать видео: {result_url}",
                    )
                    raise Exception("Не удалось скачать видео")

                # Проверяем, что файл существует и имеет размер больше 0
                if (
                    not os.path.exists(video_path)
                    or os.path.getsize(video_path) == 0
                ):
                    logger.error(
                        "Видео файл не существует или "
                        f"имеет нулевой размер: {video_path}",
                    )

                    # Сохраняем по-новой
                    video_path = await download_video(result_url)
                    logger.info(f"Путь к скачанному видео: {video_path}")
                    if not video_path:
                        logger.error(
                            f"Не удалось скачать видео: {result_url}",
                        )
                        raise Exception("Не удалось скачать видео")

                return video_path

        except Exception as e:
            logger.error(
                f"Ошибка при получении статуса задания: {e}",
            )
            raise e

        await asyncio.sleep(10)
