"""
Файл для хранения конфигурационных данных бота, таких как:
- ID Runpod эндпоинтов - используются для обращения к Runpod, на котором хостится нейросеть для генерации изображений.
Каждый эндпоинт относится к конкретной настройке.

- Константы для путей директорий

- Хедеры и урлы запросов

- ID пользователей

- Общий негативный промпт
"""

import os

# ID эндпоинтов для генерации изображений (для каждой настройки своя)
SETTING_1_ENDPOINT_ID = "idxmpy4kkpl9d1"
SETTING_2_ENDPOINT_ID = "vmoqasbdvt7wl6"
SETTING_3_ENDPOINT_ID = "e2u67i0khvang0"
SETTING_4_ENDPOINT_ID = "if2vaadpx2bo1u"

# Константы для путей к директориям
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, ".env")

TEMP_IMAGE_FILES_DIR = os.path.join(BASE_DIR, "bot", "temp", "images")

FACEFUSION_DIR = os.path.join(os.path.dirname(BASE_DIR), "facefusion-docker")

TEMP_FOLDER_PATH = os.path.join(FACEFUSION_DIR, ".assets", "images", "temp")

VIDEOS_TEMP_DIR = os.path.join(BASE_DIR, "bot", "temp", "videos")

PROCESS_IMAGE_TASK = "process_image"
PROCESS_VIDEO_TASK = "process_video"
PROCESS_IMAGE_BLOCK_TASK = "process_image_block"

FACEFUSION_RESULTS_DIR = os.path.join(
    FACEFUSION_DIR,
    ".assets",
    "images",
    "results",
)

TEMP_DIR = os.path.join(BASE_DIR, "temp")


def get_runpod_headers() -> dict:
    """Get headers for Runpod API requests with validation."""
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        raise ValueError("RUNPOD_API_KEY environment variable is not set")
    return {
        "Content-Type": "application/json",
        "Authorization": api_key,
    }


def get_kling_headers() -> dict:
    """Get headers for kling API requests with validation."""
    api_key = os.getenv("KLING_API_KEY")
    if not api_key:
        raise ValueError("KLING_API_KEY environment variable is not set")
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


# URL для запросов на Runpod
RUNPOD_HOST = "https://api.runpod.ai/v2"

# ID чата разработчика
DEV_CHAT_IDS = [1979922062, 5046166133]

# Пользователи, которые могут использовать бота
ALLOWED_USERS = [
    6455916237,
    885831766,
    835641645,
    196507796,
    930038985,
    722063648,
    5948408400,
    1979922062,
    5046166133,
    866512502,
    7313424156,
    7687069152,
    7787997166,
    7515433330,
]

# Администратор бота
ADMIN_ID = 5046166133

# Инициализируем общий негатив промпт
COMMON_NEGATIVE_PROMPT = "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, low res, blurry face, blurry eyes, tiny hands, tiny feet, multiple women, disproportionately large head, disproportionately long torso, six fingers, low quality hands, hat, multicolored hair, pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, naked breasts, cartoon, anime, 3d, cgi, illustration, doll-like, overly muscular, chubby, plastic skin, waxy texture, blurry, jpeg artifacts, extra limbs, distorted proportions, unnatural face, unrealistic anatomy, deformed eyes, exaggerated curves, barbie face, uncanny valley, big head, overexposed, underexposed, low-quality shading, unnatural smile, bad anatomy, ugly, distorted face, extra limbs, blurry, low quality child, children, kid, toddler, baby, minor, teenager, young girl, young boy, childlike, underage, preteen, infant"
