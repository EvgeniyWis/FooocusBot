# Функция для генерации массива лор
def generateLoras(weights: list[int]):
    loras = [{"model_name": "Pony_Realism_Slider.safetensors", "enabled": True},
                      {"model_name": "Breast_Size_Slider.safetensors", "enabled": True},
                      {"model_name": "Nipple_Size_Slider_alpha1.0_rank4_noxattn_last.safetensors", "enabled": True},
                      {"model_name": "body_weight_slider_v1.safetensors", "enabled": True},
                      {"model_name": "StS-Breast-Enlarger-Slider-PonyXL-v0.8.safetensors", "enabled": True},
                      {"model_name": "igbaddie-PN.safetensors", "enabled": True},
                      {"model_name": "natural_breasts_v1.safetensors", "enabled": True},
                      {"model_name": "Hour_Glass_Body_By_Stable_Yogi_PONY0_V1.safetensors", "enabled": True}]
    for index, weight in enumerate(weights):
        loras[index]["weight"] = weight
    return loras