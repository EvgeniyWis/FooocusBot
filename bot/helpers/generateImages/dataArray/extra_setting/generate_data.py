from bot.helpers.generateImages.dataArray.generate_data import generate_data
from bot.helpers.generateImages.dataArray.setting_1.generate_loras import (
    setting1_generate_loras,
)
from bot.settings import settings


# Функция для генерации данных для запроса по экстра-настройке
def extra_setting_generate_data(
    model_name: str,
    picture_folder_id: str,
    video_folder_id: str,
    prompt: str,
    loras_weights: list[int],
    image_number: int = 4,
    negative_prompt: str = settings.COMMON_NEGATIVE_PROMPT,
):
    loras = setting1_generate_loras(loras_weights)
    base_config_model_name = "CyberRealistic_Pony.safetensors"
    data = generate_data(
        model_name,
        picture_folder_id,
        video_folder_id,
        prompt,
        loras,
        base_config_model_name,
        image_number,
        negative_prompt,
        guidance_scale=3,
    )
    return data
