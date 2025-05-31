import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# ID эндпоинта для генерации изображений
ENDPOINT_ID = "h76ebzwzulgkmu"

# Путь к папке для сохранения временных файлов
TEMP_FOLDER_PATH = "facefusion-docker/.assets/images/temp"

# Заголовки для запросов на Runpod
RUNPOD_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("RUNPOD_API_KEY"),
}

# URL для запросов на Runpod
RUNPOD_HOST = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"

# ID чата разработчика
DEV_CHAT_ID = 5046166133

# Пользователи, которые могут использовать бота
ALLOWED_USERS = [
    DEV_CHAT_ID,
    6455916237,
    885831766,
    835641645,
    196507796,
    930038985,
    722063648,
    5948408400,
]

# Администратор бота
ADMIN_ID = 5046166133

# Устанавливаем режим разработки
DEVELOPMENT_MODE = False

# Устанавливаем режим с моками
MOCK_MODE = False

# Инициализируем общий негатив промпт
COMMON_NEGATIVE_PROMPT = "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, low res, blurry face, blurry eyes, tiny hands, tiny feet, multiple women, disproportionately large head, disproportionately long torso, six fingers, low quality hands, hat, multicolored hair, pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, naked breasts, cartoon, anime, 3d, cgi, illustration, doll-like, overly muscular, chubby, plastic skin, waxy texture, blurry, jpeg artifacts, extra limbs, distorted proportions, unnatural face, unrealistic anatomy, deformed eyes, exaggerated curves, barbie face, uncanny valley, big head, overexposed, underexposed, low-quality shading, unnatural smile"
