from .generateLoras import setting2_generateLoras
from ..generateData import generateData

# Функция для генерации данных для запроса настройки 2
def setting2_generateData(model_name: str, picture_folder_id: str, video_folder_id: str, prompt: str, lorasWeights: list[int]):
    loras = setting2_generateLoras(lorasWeights)
    advanced_params = {"guidance_scale": 4, "sampler_name": "euler", "overwrite_step": 35}
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generateData(model_name, picture_folder_id, video_folder_id, prompt, loras, advanced_params, base_config_model_name)
    return data