import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# ID эндпоинта для генерации изображений
ENDPOINT_ID="h76ebzwzulgkmu"

# Путь к папке для сохранения временных файлов
TEMP_FOLDER_PATH = "facefusion-docker/.assets/images/temp"

# Заголовки для запросов на Runpod
RUNPOD_HEADERS = {
    "Content-Type": "application/json",
    'Authorization': os.getenv("RUNPOD_API_KEY")
}

# URL для запросов на Runpod
RUNPOD_HOST = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"

# ID чата разработчика
DEV_CHAT_ID = 1979922062

# Пользователи, которые могут использовать бота
ALLOWED_USERS = [
    DEV_CHAT_ID,
    6455916237,
    885831766,
    835641645,
    196507796,
    930038985
]

# Администратор бота
ADMIN_ID = 6455916237
