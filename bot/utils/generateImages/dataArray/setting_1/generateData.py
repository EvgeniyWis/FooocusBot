from .generateLoras import setting1_generateLoras
from ..generateData import generateData

# TODO: изменить на 4
# Функция для генерации данных для запроса настройки 1
def setting1_generateData(model_name: str, picture_folder_id: str, video_folder_id: str,
    prompt: str, lorasWeights: list[int], image_number: int = 1):
    loras = setting1_generateLoras(lorasWeights)
    base_config_model_name = "CyberRealistic_Pony.safetensors"
    data = generateData(model_name, picture_folder_id, video_folder_id, prompt, loras, base_config_model_name, image_number=image_number)
    return data