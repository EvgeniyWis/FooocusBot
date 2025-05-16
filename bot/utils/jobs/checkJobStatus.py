from typing import Callable
import requests
from logger import logger
from config import RUNPOD_HEADERS, RUNPOD_HOST
import asyncio


# Функция для получения статуса работы
async def checkJobStatus(job_id: str, inner_callback: Callable[[], None] = None):
    while True:
        try:
            response = requests.post(f'{RUNPOD_HOST}/status/{job_id}', headers=RUNPOD_HEADERS)
            response_json = response.json()
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка при получении статуса работы (сетевая ошибка): {e}")
            await asyncio.sleep(10)
            continue

        logger.info(f"Получен статус работы c id {job_id}: {response_json['status']}")

        if inner_callback:
            inner_callback()

        if response_json['status'] == 'COMPLETED':
            break

        elif response_json['status'] in ['FAILED', 'CANCELLED']:
            if response_json['status'] == 'FAILED':
                raise Exception(response_json['error'])
            else:
                raise Exception("Работа была отменена")

        await asyncio.sleep(10)

    # Когда работа завершена, получаем изображение
    logger.info(f"Работа по id {job_id} завершена!")

    return response_json