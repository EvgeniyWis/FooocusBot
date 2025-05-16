import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# ID эндпоинта для генерации изображений
ENDPOINT_ID="ectawq7nebpa5w"

# Путь к папке для сохранения временных файлов
TEMP_FOLDER_PATH = "facefusion-docker/.assets/images/temp"

# Заголовки для запросов на Runpod
RUNPOD_HEADERS = {
    "Content-Type": "application/json",
    'Authorization': os.getenv("RUNPOD_API_KEY")
}

# URL для запросов на Runpod
RUNPOD_HOST = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"