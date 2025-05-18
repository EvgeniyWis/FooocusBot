from .generateLoras import setting4_generateLoras
from ..generateData import generateData

# Функция для генерации данных для запроса настройки 4
def setting4_generateData(model_name: str, picture_folder_id: str, video_folder_id: str, prompt: str, lorasWeights: list[int]):
    loras = setting4_generateLoras(lorasWeights)
    advanced_params = {"guidance_scale": 4, "sampler_name": "euler_ancestral", "overwrite_step": 60}
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generateData(model_name, picture_folder_id, video_folder_id, prompt, loras, advanced_params, base_config_model_name)
    return data