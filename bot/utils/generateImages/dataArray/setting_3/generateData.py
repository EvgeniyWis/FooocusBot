from .generateLoras import setting3_generateLoras
from ..generateData import generateData

# Функция для генерации данных для запроса настройки 3
def setting3_generateData(model_name: str, picture_folder_id: str, video_folder_id: str, prompt: str, lorasWeights: list[int]):
    loras = setting3_generateLoras(lorasWeights)
    advanced_params = {"guidance_scale": 4, "sampler_name": "euler_ancestral", "overwrite_step": 35}
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generateData(model_name, picture_folder_id, video_folder_id, prompt, loras, advanced_params, base_config_model_name)
    return data