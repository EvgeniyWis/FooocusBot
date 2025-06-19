from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(override=True)


class Settings(BaseSettings):
    RUNPOD_API_KEY: str
    KLING_API_KEY: str
    BOT_API_TOKEN: str

    # user_id пользователей / администраторов
    ADMIN_ID: int
    DEV_CHAT_IDS: List[int]
    ALLOWED_USERS: List[int]

    # Режимы и флаги
    DEVELOPMENT_MODE: bool = False
    MOCK_MODE: bool = False
    UPSCALE_MODE: bool = True
    FACEFUSION_MODE: bool = True

    # Ключи Redis для восстановления задач
    PROCESS_IMAGE_TASK: str = "process_image"
    PROCESS_VIDEO_TASK: str = "process_video"
    PROCESS_IMAGE_BLOCK_TASK: str = "process_image_block"

    # Redis
    REDIS_PASSWORD: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_DB: str = "0"

    # Адрес Runpod
    RUNPOD_HOST: str

    # Идентификаторы эндпоинтов Runpod
    SETTING_1_ENDPOINT_ID: str
    SETTING_2_ENDPOINT_ID: str
    SETTING_3_ENDPOINT_ID: str
    SETTING_4_ENDPOINT_ID: str

    # Общий промпт
    COMMON_NEGATIVE_PROMPT: str = (
        "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, "
        "pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, "
        "normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, "
        "long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, low res, "
        "blurry face, blurry eyes, tiny hands, tiny feet, multiple women, disproportionately large head, "
        "disproportionately long torso, six fingers, low quality hands, hat, multicolored hair, pubic hair, asian, tan lines, "
        "makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, naked breasts, cartoon, anime, 3d, "
        "cgi, illustration, doll-like, overly muscular, chubby, plastic skin, waxy texture, blurry, jpeg artifacts, extra limbs, "
        "distorted proportions, unnatural face, unrealistic anatomy, deformed eyes, exaggerated curves, barbie face, uncanny valley, "
        "big head, overexposed, underexposed, low-quality shading, unnatural smile, bad anatomy, ugly, distorted face, extra limbs, "
        "blurry, low quality child, children, kid, toddler, baby, minor, teenager, young girl, young boy, childlike, underage, "
        "preteen, infant"
    )

    # Мок-ссылки
    MOCK_LINK_FOR_SAVE_IMAGE: str
    MOCK_LINK_FOR_SAVE_VIDEO: str

    # Параметры Facefusion
    FACEFUSION_CONTAINER_NAME: str


settings = Settings()
