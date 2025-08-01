from bot.helpers.generateImages.dataArray.generate_data import generate_data
from bot.helpers.generateImages.dataArray.settings.setting_3.generate_loras import (
    setting3_generate_loras,
)
from bot.settings import settings


# Функция для генерации данных для запроса группы 3
def setting3_generate_data(
    model_name: str,
    picture_folder_id: str,
    video_folder_id: str,
    nsfw_video_folder_id: str,
    prompt: str,
    loras_weights: list[int],
    image_number: int = 4,
    negative_prompt: str = settings.COMMON_NEGATIVE_PROMPT,
):
    loras = setting3_generate_loras(loras_weights)
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generate_data(
        model_name,
        picture_folder_id,
        video_folder_id,
        nsfw_video_folder_id,
        prompt,
        loras,
        base_config_model_name,
        image_number,
        negative_prompt,
    )
    return data
