from bot.settings import settings


# Глобальная функция для генерации данных для запроса
def generateData(
    model_name: str,
    picture_folder_id: str,
    video_folder_id: str,
    prompt: str,
    loras: list[dict],
    base_config_model_name: str,
    image_number: int,
    negative_prompt: str = settings.COMMON_NEGATIVE_PROMPT,
    embeddings: list[str] | None = None,
):
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
                "guidance_scale": 3.5,
                "aspect_ratios_selection": "720*1280",
            },
        },
        "model_name": model_name,
        "picture_folder_id": picture_folder_id,
        "video_folder_id": video_folder_id,
    }
    return data
