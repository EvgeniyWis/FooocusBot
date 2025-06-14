from bot.helpers.generateImages.dataArray.generateData import generateData
from bot.helpers.generateImages.dataArray.setting_2.generateLoras import (
    setting2_generateLoras,
)


# Функция для генерации данных для запроса настройки 2
def setting2_generateData(
    model_name: str,
    picture_folder_id: str,
    video_folder_id: str,
    prompt: str,
    lorasWeights: list[int],
    image_number: int = 4,
):
    loras = setting2_generateLoras(lorasWeights)
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generateData(
        model_name,
        picture_folder_id,
        video_folder_id,
        prompt,
        loras,
        base_config_model_name,
        image_number,
    )
    return data
