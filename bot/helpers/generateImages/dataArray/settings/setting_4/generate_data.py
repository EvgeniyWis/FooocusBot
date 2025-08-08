from bot.helpers.generateImages.dataArray.generate_data import generate_data
from bot.helpers.generateImages.dataArray.settings.setting_4.generate_loras import (
    setting4_generate_loras,
)
from bot.app.config.settings import settings


# Функция для генерации данных для запроса группы 4
def setting4_generate_data(
    model_name: str,
    model_index: int,
    picture_folder_id: str,
    video_folder_id: str,
    nsfw_video_folder_id: str,
    prompt: str,
    loras_weights: list[int],
    image_number: int = 4,
    negative_prompt: str = settings.COMMON_NEGATIVE_PROMPT,
):
    loras = setting4_generate_loras(loras_weights)
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generate_data(
        model_name=model_name,
        model_index=model_index,
        setting_number=4,
        picture_folder_id=picture_folder_id,
        video_folder_id=video_folder_id,
        nsfw_video_folder_id=nsfw_video_folder_id,
        prompt=prompt,
        loras=loras,
        base_config_model_name=base_config_model_name,
        image_number=image_number,
        negative_prompt=negative_prompt,
    )
    return data
