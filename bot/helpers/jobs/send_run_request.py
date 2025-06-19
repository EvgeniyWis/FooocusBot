from bot.helpers.jobs.get_endpoint_ID import get_endpoint_ID
from bot.settings import settings
from bot.utils import httpx_post
from bot.utils.get_api_headers import get_runpod_headers


# Функция для отправки запроса на генерацию
async def send_run_request(dataJSON: dict, setting_number: int):
    # Получаем ID эндпоинта для генерации изображений
    ENDPOINT_ID = await get_endpoint_ID(setting_number)

    # Формируем URL для отправки запроса
    url = f"{settings.RUNPOD_HOST}/{ENDPOINT_ID}/run"

    # Отправляем запрос на генерацию
    response_json = await httpx_post(
        url,
        get_runpod_headers(),
        json=dataJSON,
        with_response_text_logging=False,
    )

    return response_json
