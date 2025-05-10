from ..generateLoras import generateLoras

# Функция для генерации массива лор для настройки 3
def setting3_generateLoras(weights: list[int]):
    loras = ["Nipple_Size_Slider.safetensors", "Crazy_Girlfriend_Mix.safetensors",
    "Real_Beauty.safetensors", "Breast_Enlargement_Slider.safetensors", "Big_Natural_Breasts.safetensors",
    "Body_Weight_Slider.safetensors"]
    
    return generateLoras(weights, loras)