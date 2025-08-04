from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(override=True)


class Settings(BaseSettings):
    RUNPOD_API_KEY: str
    KLING_API_KEY: str
    BOT_API_TOKEN: str
    PUBLIC_ILOVEAPI_API_KEY: str
    SECRET_ILOVEAPI_API_KEY: str
    FREEPIK_API_KEY: str

    # user_id пользователей / администраторов
    ADMIN_ID: int
    DEV_CHAT_IDS: list[int]
    ALLOWED_USERS: list[int]

    # Режимы и флаги
    MOCK_IMAGES_MODE: bool = False
    MOCK_VIDEO_MODE: bool = False
    UPSCALE_MODE: bool = True
    SECOND_UPSCALE_MODE: bool = True
    FACEFUSION_MODE: bool = True
    RECOVERING_TASKS: bool = True
    HEATING_COMFYUI_MODELS: bool = True

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
    EXTRA_SETTING_ENDPOINT_ID: str

    # Общий негатив-промпт
    COMMON_NEGATIVE_PROMPT: ClassVar[str] = """
        low quality, worst quality, bad anatomy, disfigured, mutated, deformed, extra limbs, missing limbs, (incorrect hands: 1.2), (wrong number of fingers: 1.3), (more than 5 fingers: 1.4), (less than 5 fingers: 1.4), fused fingers, malformed hands, distorted hands, asymmetric hands, poorly drawn hands, unnatural hands, long neck, disproportionate body, oversized head, tiny feet, blurry face, blurry eyes, oversaturated, underexposed, overexposed, bad proportions, unnatural smile, exaggerated curves, plastic skin, waxy texture, jpeg artifacts, low res, text, signature, watermark, cartoon, anime, 3d, cgi, illustration, doll-like, uncanny valley, barbie face, overly muscular, chubby, (multiple subjects: 1.2), multiple arms, multiple legs, pubic hair, makeup, lipstick, tattoo, colored tattoo, standing with back to camera, (((buttocks))), (((showing ass))), religious symbols, priest's cross, ugly, mutated facial features, distorted perspective, unnatural lighting, oversmoothed, (asian: 0.8), (black skin: 0.8), (man: 0.8), (woman: 0.8), nudity, naked nipples, poorly detailed clothing, hat, steering wheel, playing cards, multicolored hair, tan lines, six fingers  
    """

    # Промпт для upscale
    COMMON_UPSCALE_PROMPT: ClassVar[str] = (
        "high-resolution, ultra-detailed, photorealistic female model, perfect hand anatomy, anatomically correct fingers and nails, natural finger positioning, symmetrical hands, sharp skin texture, realistic skin pores, high-definition lighting, smooth shading, 8k skin detail, flawless complexion, crisp fabric edges, clean outlines, realistic lighting gradients, upscale to ultra quality, fine finger joints, soft shadows, cinematic render"
    )

    # Мок-ссылки
    MOCK_LINK_FOR_SAVE_IMAGE: str
    MOCK_LINK_FOR_SAVE_VIDEO: str

    # Параметры Facefusion
    FACEFUSION_CONTAINER_NAME: str

    # Параметры ComfyUI
    COMFYUI_API_URL: str
    COMFYUI_API_KEY: str
    COMFYUI_POD_NAME: str = "comfyui-video_gen"
    COMFYUI_HEATING_PROMPT: str = (
        "A naked girl strokes her bare breasts with her hands, "
        "sensual movement, static camera, cinematic lighting, "
        "natural body physics, 4K detail, eye contact"
    )

    # Параметры ILoveAPI
    ILOVEAPI_API_URL: str

    # Параметры Freepik API
    FREEPIK_API_URL: str


settings = Settings()  # type: ignore
