import os

from dotenv import find_dotenv, load_dotenv
from logger import logger

import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'FocuuusBot', '.env')
logger.info(f"Путь к .env файлу: {env_path}")
logger.info(f"Файл .env существует: {os.path.exists(env_path)}")

if 'BOT_API_TOKEN' in os.environ:
    del os.environ['BOT_API_TOKEN']

load_dotenv(env_path, override=True)

logger.info(f"BOT_API_TOKEN: {os.getenv('BOT_API_TOKEN')}")



# ID эндпоинтов для генерации изображений (для каждой настройки своя)
SETTING_1_ENDPOINT_ID = "idxmpy4kkpl9d1"
SETTING_2_ENDPOINT_ID = "vmoqasbdvt7wl6"
SETTING_3_ENDPOINT_ID = "e2u67i0khvang0"
SETTING_4_ENDPOINT_ID = "if2vaadpx2bo1u"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger.info(f"BASE_DIR: {BASE_DIR}")

TEMP_IMAGE_FILES_DIR = os.path.join(BASE_DIR, "bot", "temp", "images")
logger.info(f"TEMP_IMAGE_FILES_DIR: {TEMP_IMAGE_FILES_DIR}")

FACEFUSION_DIR = os.path.join(os.path.dirname(BASE_DIR), "facefusion-docker")
logger.info(f"FACEFUSION_DIR: {FACEFUSION_DIR}")

TEMP_FOLDER_PATH = os.path.join(FACEFUSION_DIR, ".assets", "images", "temp")
logger.info(f"TEMP_FOLDER_PATH: {TEMP_FOLDER_PATH}")

FACEFUSION_RESULTS_DIR = os.path.join(FACEFUSION_DIR, ".assets", "images", "results")
logger.info(f"FACEFUSION_RESULTS_DIR: {FACEFUSION_RESULTS_DIR}")

TEMP_DIR = os.path.join(BASE_DIR, "temp")

# Заголовки для запросов на Runpod
RUNPOD_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("RUNPOD_API_KEY"),
}

# URL для запросов на Runpod
RUNPOD_HOST = f"https://api.runpod.ai/v2"

# ID чата разработчика
DEV_CHAT_ID = 1979922062

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

# Устанавливаем режим разработки
DEVELOPMENT_MODE = False

# Устанавливаем режим с моками
MOCK_MODE = False

# Устанавливаем режим с Upscale
UPSCALE_MODE = True

# Устанавливаем режим с facefusion
FACEFUSION_MODE = True

# Инициализируем общий негатив промпт
COMMON_NEGATIVE_PROMPT = "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, low res, blurry face, blurry eyes, tiny hands, tiny feet, multiple women, disproportionately large head, disproportionately long torso, six fingers, low quality hands, hat, multicolored hair, pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, naked breasts, cartoon, anime, 3d, cgi, illustration, doll-like, overly muscular, chubby, plastic skin, waxy texture, blurry, jpeg artifacts, extra limbs, distorted proportions, unnatural face, unrealistic anatomy, deformed eyes, exaggerated curves, barbie face, uncanny valley, big head, overexposed, underexposed, low-quality shading, unnatural smile, bad anatomy, ugly, distorted face, extra limbs, blurry, low quality child, children, kid, toddler, baby, minor, teenager, young girl, young boy, childlike, underage, preteen, infant"
