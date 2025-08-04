from bot.settings import settings


# Глобальная функция для генерации данных для запроса
def generate_data(
    model_name: str,
    model_index: int,
    setting_number: int | str,
    picture_folder_id: str,
    video_folder_id: str,
    nsfw_video_folder_id: str,
    prompt: str,
    loras: list[dict],
    base_config_model_name: str,
    image_number: int = 4,
    negative_prompt: str = settings.COMMON_NEGATIVE_PROMPT,
    embeddings: list[str] | None = None,
    guidance_scale: float = 3.5,
) -> dict:
    """
    Генерирует данные для запроса

    Args:
        model_name: str - название модели
        model_index: int - индекс модели
        setting_number: int | str - номер настройки
        picture_folder_id: str - id папки с изображениями
        video_folder_id: str - id папки с видео
        nsfw_video_folder_id: str - id папки с NSFW видео
        prompt: str - промпт
        loras: list[dict] - лоры
        base_config_model_name: str - название базовой модели
        image_number: int - количество изображений
        negative_prompt: str - отрицательный промпт
        embeddings: list[str] | None - эмбеддинги
        guidance_scale: float - параметр guidance scale

    Returns:
        dict - данные для запроса
    """
    if embeddings is None:
        embeddings = []
    data = {
        "json": {
            "input": {
                "api_name": "txt2img",
                "require_base64": True,
                "prompt": f"{', '.join(embeddings)} {prompt}",
                "loras": loras,
                "image_number": image_number,
                "advanced_params": {
                    "sampler_name": "euler_ancestral",
                    "overwrite_step": 60,
                },
                "negative_prompt": negative_prompt,
                "base_model_name": base_config_model_name,
                "style_selections": [],
                "guidance_scale": guidance_scale,
                "aspect_ratios_selection": "720*1280",
            },
        },
        "model_name": model_name,
        "model_index": model_index,
        "picture_folder_id": picture_folder_id,
        "video_folder_id": video_folder_id,
        "nsfw_video_folder_id": nsfw_video_folder_id,
        "setting_number": setting_number,
    }
    return data
