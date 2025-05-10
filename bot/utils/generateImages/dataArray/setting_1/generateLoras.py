from ..generateLoras import generateLoras

# Функция для генерации массива лор для настройки 1
def setting1_generateLoras(weights: list[int]):
    loras = ["Pony_Realism_Slider.safetensors", "Breast_Size_Slider.safetensors", 
    "Nipple_Size_Slider_alpha1.0_rank4_noxattn_last.safetensors",
    "body_weight_slider_v1.safetensors",
    "StS-Breast-Enlarger-Slider-PonyXL-v0.8.safetensors",
    "igbaddie-PN.safetensors",
    "natural_breasts_v1.safetensors",
    "Hour_Glass_Body_By_Stable_Yogi_PONY0_V1.safetensors",
    "lightingSlider.safetensors"]
    
    return generateLoras(weights, loras)