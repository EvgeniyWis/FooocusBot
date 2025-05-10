from .generateLoras import setting3_generateLoras
from ..generateData import generateData

# Функция для генерации данных для запроса настройки 3
def setting3_generateData(model_name: str, prompt: str, lorasWeights: list[int]):
    loras = setting3_generateLoras(lorasWeights)
    advanced_params = {"guidance_scale": 4, "sampler_name": "euler", "overwrite_step": 35}
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generateData(model_name, prompt, loras, advanced_params, base_config_model_name)
    return data