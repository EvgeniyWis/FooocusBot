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
    REDIS_HOST: str
    REDIS_PORT: str = "6379"
    REDIS_DB: str = "0"

    # Адрес Runpod
    RUNPOD_HOST: str

    # Идентификаторы эндпоинтов Runpod
    SETTING_1_ENDPOINT_ID: str
    SETTING_2_ENDPOINT_ID: str
    SETTING_3_ENDPOINT_ID: str
    SETTING_4_ENDPOINT_ID: str

    # Общий негатив-промпт
    COMMON_NEGATIVE_PROMPT = (
        # Качество и технические проблемы
        "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, pony, negativeXL_D, "
        "low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, "
        "blurry, jpeg artifacts, overexposed, underexposed, low-quality shading, low res, "
        
        # Проблемы с лицом и анатомией
        "ugly face, bad anatomy, unrealistic anatomy, deformed eyes, unnatural face, distorted face, "
        "barbie face, uncanny valley, big head, disproportionately large head, disproportionately long torso, "
        "extra limbs, distorted proportions, exaggerated curves, "
        
        # Проблемы с руками
        "mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, bad hands, "
        "tiny hands, low quality hands, six fingers, long neck, "
        
        # Проблемы с глазами и другими частями тела
        "blurry face, blurry eyes, tiny feet, multiple women, "
        
        # Нежелательные элементы
        "text, signature, signature artist, multiple female, multiple male, "
        "hat, multicolored hair, pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, "
        "steering wheel, man, "
        
        # Стили и эффекты
        "cartoon, anime, 3d, cgi, illustration, doll-like, overly muscular, chubby, plastic skin, waxy texture, "
        
        # Усиленная защита от обнаженности
        "naked nipples, naked breasts, topless, bare breasts, exposed breasts, uncovered breasts, "
        "nipples showing, nipples visible, breast exposure, chest exposure, "
        "(((naked nipples))), (((naked breasts))), (((topless))), (((bare breasts))), (((exposed breasts))), "
        "(((nipples showing))), (((nipples visible))), (((breast exposure))), (((chest exposure))), "
        "nude, nudity, naked, topless, bare chest, exposed chest, "
        "(((nude))), (((nudity))), (((naked))), (((topless))), (((bare chest))), (((exposed chest))), "
        
        # Защита от несовершеннолетних
        "child, children, kid, toddler, baby, minor, teenager, young girl, young boy, childlike, underage, "
        "preteen, infant, low quality child, "
        
        # Проблемы с ногами
        "spread legs, open legs, legs apart, legs wide open, legs spread, "
        "(((spread legs))), (((open legs))), (((legs apart))), (((legs wide open))), (((legs spread))), "
        "no spread legs, no open legs, no legs apart, no legs wide open, no legs spread, "
        
        # Дополнительные негативные элементы
        "unnatural smile, ugly, "
        
        # Усиленные негативные промпты для максимальной защиты
        "((((naked)))), ((((topless)))), ((((bare breasts)))), ((((exposed breasts)))), "
        "((((nipples)))), ((((nude)))), ((((nudity)))), ((((chest exposure)))), "
        "((((breast exposure)))), ((((nipples showing)))), ((((nipples visible)))), "
        "((((naked nipples)))), ((((naked breasts)))), ((((bare chest)))), ((((exposed chest))))"
    )

    # Промпт для upscale
    COMMON_UPSCALE_PROMPT = "high-resolution, ultra-detailed, photorealistic female model, perfect hand anatomy, anatomically correct fingers and nails, natural finger positioning, symmetrical hands, sharp skin texture, realistic skin pores, high-definition lighting, smooth shading, 8k skin detail, flawless complexion, crisp fabric edges, clean outlines, realistic lighting gradients, upscale to ultra quality, fine finger joints, soft shadows, cinematic render"

    # Мок-ссылки
    MOCK_LINK_FOR_SAVE_IMAGE: str
    MOCK_LINK_FOR_SAVE_VIDEO: str

    # Параметры Facefusion
    FACEFUSION_CONTAINER_NAME: str


settings = Settings()  # type: ignore
