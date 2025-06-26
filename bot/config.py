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

from dotenv import load_dotenv
from logger import logger

# ID эндпоинтов для генерации изображений (для каждой настройки своя)
SETTING_1_ENDPOINT_ID = "idxmpy4kkpl9d1"
SETTING_2_ENDPOINT_ID = "vmoqasbdvt7wl6"
SETTING_3_ENDPOINT_ID = "e2u67i0khvang0"
SETTING_4_ENDPOINT_ID = "if2vaadpx2bo1u"

# Константы для путей к директориям
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "FocuuusBot", ".env")
logger.info(f"Путь к .env файлу: {env_path}")
logger.info(f"Файл .env существует: {os.path.exists(env_path)}")

# Очищаем переменные окружения, которые могут конфликтовать с .env файлом
variables_to_clear = ["BOT_API_TOKEN", "RUNPOD_API_KEY", "KLING_API_KEY"]
for var in variables_to_clear:
    if var in os.environ:
        logger.info(f"Удаляем переменную окружения: {var}")
        del os.environ[var]

# Загружаем .env файл с принудительным переопределением
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)
    logger.info("✅ .env файл загружен с переопределением")

    # Проверяем, что переменные загрузились
    bot_token = os.getenv("BOT_API_TOKEN")
    runpod_key = os.getenv("RUNPOD_API_KEY")
    kling_key = os.getenv("KLING_API_KEY")

    logger.info(f"BOT_API_TOKEN загружен: {'Да' if bot_token else 'Нет'}")
    logger.info(f"RUNPOD_API_KEY загружен: {'Да' if runpod_key else 'Нет'}")
    logger.info(f"KLING_API_KEY загружен: {'Да' if kling_key else 'Нет'}")

    if bot_token:
        logger.info(f"Токен бота: {bot_token[:10]}...{bot_token[-10:] if len(bot_token) > 20 else '***'}")
else:
    logger.warning(f"⚠️ .env файл не найден по пути: {env_path}")

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


def get_current_tokens():
    """Получить текущие токены с отладочной информацией."""
    bot_token = os.getenv("BOT_API_TOKEN")
    runpod_key = os.getenv("RUNPOD_API_KEY")
    kling_key = os.getenv("KLING_API_KEY")

    logger.info("🔍 Текущие токены:")
    logger.info(f"BOT_API_TOKEN: {bot_token[:10]}...{bot_token[-10:] if bot_token and len(bot_token) > 20 else 'Не найден'}")
    logger.info(f"RUNPOD_API_KEY: {runpod_key[:10]}...{runpod_key[-10:] if runpod_key and len(runpod_key) > 20 else 'Не найден'}")
    logger.info(f"KLING_API_KEY: {kling_key[:10]}...{kling_key[-10:] if kling_key and len(kling_key) > 20 else 'Не найден'}")

    return {
        "BOT_API_TOKEN": bot_token,
        "RUNPOD_API_KEY": runpod_key,
        "KLING_API_KEY": kling_key,
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
    418325928,
]

# Администратор бота
ADMIN_ID = 5046166133

# Инициализируем общий негатив промпт
COMMON_NEGATIVE_PROMPT = (
    "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, pony, negativeXL_D, "
    "low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, "
    "mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, "
    "signature, signature artist, multiple female, multiple male, bad anatomy, low res, blurry face, blurry eyes, "
    "tiny hands, tiny feet, multiple women, disproportionately large head, disproportionately long torso, six fingers, "
    "low quality hands, hat, multicolored hair, pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, "
    "steering wheel, man, naked nipples, naked breasts, cartoon, anime, 3d, cgi, illustration, doll-like, overly muscular, "
    "chubby, plastic skin, waxy texture, blurry, jpeg artifacts, extra limbs, distorted proportions, unnatural face, "
    "unrealistic anatomy, deformed eyes, exaggerated curves, barbie face, uncanny valley, big head, overexposed, "
    "underexposed, low-quality shading, unnatural smile, bad anatomy, ugly, distorted face, extra limbs, blurry, "
    "low quality child, children, kid, toddler, baby, minor, teenager, young girl, young boy, childlike, underage, "
    "preteen, infant, (((spread legs))), spread legs, open legs, legs apart, legs wide open, legs spread, "
    "no spread legs, no open legs, no legs apart, no legs wide open, no legs spread"
)
