from .generateLoras import setting3_generateLoras
from ..generateData import generateData

# Функция для генерации данных для запроса настройки 3
def setting3_generateData(model_name: str, picture_folder_id: str, video_folder_id: str, prompt: str,
    lorasWeights: list[int], image_number: int = 4, negative_prompt: str = ""):
    loras = setting3_generateLoras(lorasWeights)
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generateData(model_name, picture_folder_id, video_folder_id, prompt, loras, base_config_model_name, image_number, negative_prompt)
    return data