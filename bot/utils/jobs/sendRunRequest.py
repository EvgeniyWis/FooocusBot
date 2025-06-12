from config import RUNPOD_HEADERS, RUNPOD_HOST

from utils.jobs.getEndpointID import getEndpointID
from utils import httpx_post


# Функция для отправки запроса на генерацию
async def sendRunRequest(dataJSON: dict, setting_number: int):
    # Получаем ID эндпоинта для генерации изображений
    ENDPOINT_ID = await getEndpointID(setting_number)

    # Формируем URL для отправки запроса
    url = f"{RUNPOD_HOST}/{ENDPOINT_ID}/run"

    # Отправляем запрос на генерацию
    response_json = await httpx_post(url, RUNPOD_HEADERS, dataJSON, with_response_text_logging=False)

    return response_json