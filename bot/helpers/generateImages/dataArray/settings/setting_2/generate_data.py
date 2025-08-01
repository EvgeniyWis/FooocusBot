from bot.helpers.generateImages.dataArray.generate_data import generate_data
from bot.helpers.generateImages.dataArray.settings.setting_2.generate_loras import (
    setting2_generate_loras,
)


# Функция для генерации данных для запроса группы 2
def setting2_generate_data(
    model_name: str,
    model_index: int,
    picture_folder_id: str,
    video_folder_id: str,
    nsfw_video_folder_id: str,
    prompt: str,
    loras_weights: list[int],
    image_number: int = 4,
):
    loras = setting2_generate_loras(loras_weights)
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generate_data(
        model_name,
        model_index,
        picture_folder_id,
        video_folder_id,
        nsfw_video_folder_id,
        prompt,
        loras,
        base_config_model_name,
        image_number,
    )
    return data
